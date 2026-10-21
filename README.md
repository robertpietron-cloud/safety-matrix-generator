<!--
=============================================================================
Project : Safety Matrix Generator (GuardLogix SafetyTask -> Cause & Effect)
File    : README.md
Author  : Robert Pietroń
Revision: 1.2.0 (2026-10-21)
Changes :
  1.0.0 (2026-10-18) - First universal release: description, installation,
                       usage, configuration, method, rules, limitations (EN/PL).
  1.1.0 (2026-10-18) - Manual GitHub Actions runs (Generate Safety Matrix,
                       tests); status badge.
  1.2.0 (2026-10-21) - Generator 1.1.0: copied channels, scan-order lag,
                       constant bypass, new audit rules, ST/FBD/SFC writers.
=============================================================================
-->

# Safety Matrix Generator

[![tests](https://github.com/robertpietron-cloud/safety-matrix-generator/actions/workflows/tests.yml/badge.svg)](https://github.com/robertpietron-cloud/safety-matrix-generator/actions/workflows/tests.yml)

**Cause & Effect (Safety Matrix) generator for Rockwell Automation GuardLogix / Compact GuardLogix safety programs.**
It reads a Studio 5000 Logix Designer export (`.L5K` or `.L5X`), analyses the ladder logic of the **SafetyTask**
deterministically, and writes an Excel workbook with the safety matrix, a validation report, a safety-function sheet
with reaction times and a validation test record – in **Polish, English, French and Danish** with a language switch
inside the workbook.

Author: **Robert Pietroń** · License: MIT · Python ≥ 3.9

> ⚠️ The generator supports the engineer – it does not replace the risk assessment, SISTEMA calculation or the
> validation of the safety functions according to ISO 13849-2 / IEC 62061. Every result must be reviewed by a competent person.

---

## What you get

| Sheet | Contents |
|---|---|
| **Start** | cover page, language switch (PL / EN / FR / DA), list of sheets, summary |
| **Group Interlocks** | matrix: rows = safety outputs, columns = input devices grouped by zone; Enable Group; reset / stop category rows |
| **MOTOR** / **VALVE** | matrix: rows = devices, columns = outputs (valves on VALVE); every coloured cell carries a comment with the rung path; output metadata (EDM, reset, restart, stop category) |
| **Legend** | codes, IDs, zones, output types, instructions, abbreviations, method, revision history, sources |
| **Safety functions** | one row per device: outputs, input structure, worst-case reaction time from the CIP Safety connection data (CRTL, LC filter, task period + watchdog), PLr / Cat. / PL fields |
| **Test record** | generated ISO 13849-2 test protocol: function test, channel discrepancy, OR combinations, standard bypasses, EDM, loss of communication |
| **Devices** / **Outputs** | channels, instruction, rung, reset type and source (traced into the standard code), muting, address/IP, EDM, CRTL |
| **C&E paths** | every intersection with its full path `tag [routine R rung]` and bypass bit / OR partner |
| **Validation report** | **critical alarms**, **dead** inputs/outputs/tags and **items to verify** – each with routine and rung |
| **Dictionary** | all texts in all languages (corrections here change the workbook) |

Optionally a machine-readable **JSON** with devices, outputs, cells (paths) and findings.

### Matrix codes

| Code | Meaning |
|---|---|
| `X` | tripping the device switches the output off directly |
| `X1` | as X, but effectively single-channel (both channels on one input, or a direct input) – **alarm** |
| `XB` | trips, but a **standard-control bit** (SafetyTagMap) can bypass / mute it – **alarm** |
| `XC` | trips only together with another device (parallel OR branch) |
| `XM` | trips unless an internal condition holds (muting instruction, comparison, mode, data) |
| `N` | in the logic but non-functional (constant channel inputs) – **alarm** |
| `S` `SB` `SC` `SM` | the same for information signals to standard control (not safety outputs) |

## Installation

```bash
git clone https://github.com/robertpietron-cloud/safety-matrix-generator.git
cd safety-matrix-generator
pip install .            # or: pip install -r requirements.txt
```

## Quick start (demo project included)

```bash
# 1. analyse the synthetic demo cell (deliberately contains typical defects)
safety-matrix analyze examples/demo/DemoCell.L5K -c examples/demo/config.yaml -o DemoCell_matrix.xlsx --json DemoCell.json

# 2. your own program: start without a configuration ...
safety-matrix analyze MyLine.L5K -o MyLine_matrix.xlsx

# 3. ... then create a configuration skeleton, edit zone names / descriptions and run again
safety-matrix init-config MyLine.L5K -o myline.yaml --lang pl,en
safety-matrix analyze MyLine.L5K -c myline.yaml -o MyLine_matrix.xlsx

# check what the parser read
safety-matrix dump MyLine.L5K --routine MainRoutine
```

`python -m safety_matrix …` works as well. Useful options of `analyze`:

| Option | |
|---|---|
| `--lang pl,en,fr,da` | languages written to the workbook (one language = plain workbook without the switch) |
| `--default-lang pl` | language shown when the workbook is opened |
| `--json FILE` | also write the analysis as JSON |
| `--author`, `--revision` | document data (override the configuration) |
| `--fail-on-alarm` | exit code 2 when critical alarms are found (for CI pipelines) |

Accepted inputs: `.L5K`, `.L5X`, and an L5K pasted into a Word document (`.docx`) or a text file.

Python API:

```python
from safety_matrix import generate
summary = generate('MyLine.L5K', 'MyLine_matrix.xlsx', config_path='myline.yaml', languages=['pl', 'en'])
```

## Running on GitHub (manual workflow)

**Actions → Generate Safety Matrix → Run workflow** analyses an export stored in the repository and needs no local
installation. Inputs: export path (default: the demo), configuration path (empty = automatic layout), languages,
default language, author, revision, *fail on critical alarms* and how many days to keep the files. The run page shows a
summary with the critical alarms; the workbook and the JSON are in the **Artifacts** section of the run.

> ⚠️ Artifacts of a **public** repository can be downloaded by other GitHub users. Analyse customer exports only in a
> **private copy** of the repository (Use this template / private fork) or locally with the CLI.

The **tests** workflow can also be started manually (**Actions → tests → Run workflow**, optional list of Python
versions); it keeps the demo workbook as an artifact.

## Configuration (YAML, everything optional)

```yaml
document:
  title: SAFETY MATRIX – My line (SafetyTask)
  author: Robert Pietroń
  revision: '1.0'
  date: '2026-10-18'
  revisions:                          # revision history shown on the Legend sheet
  - {rev: '1.0', date: '2026-10-18', author: Robert Pietroń, text: {pl: Pierwsze wydanie, en: First issue}}
languages: [pl, en, fr, da]
default_language: pl
analysis:
  info_effects: ['Safety_ToStd[0].0']  # safety bits read by standard control -> S codes
  include_effects: []                  # force an output into the matrix
  exclude_effects: []                  # hide an output
  crtl_priority_ms: 1000               # input CRTL >= this value -> PRIORITY item in the report
  direct_inputs: true                  # raw safety inputs used directly in the logic become causes
zones:                                 # default: one zone per routine (scan order)
- name: {pl: 'STREFA 1 : PRASA', en: 'ZONE 1 : PRESS'}
  devices: [EStop_Panel, Door_Press]   # explicit order, and/or
  routines: [Press]                    # all devices whose instruction is in these routines
effect_groups:                         # default: one group per routine of the output rung
- name: {pl: PRASA, en: PRESS}
  effects: [K1K2_Main, 'Press_Drive:SO.SafeTorqueOff']
devices:
  Door_Press: {type: SAFETY DOOR, id: DS 1.1, description: {pl: Drzwi prasy -B50, en: Press door -B50}}
effects:
  Valve_Press: {valve: true, description: {pl: Zawór prasy, en: Press valve}}
```

A complete real-life example (four languages, 33 devices, 31 outputs) is in
[`examples/portalsaw/config.yaml`](examples/portalsaw/config.yaml). The PLC export of that line is **not** part of the repository.

## Method

1. **Parsing** – controller, `SafetyTagMap`, modules and CIP Safety connections (RPI, Timeout/Network Delay Multiplier,
   Connection Reaction Time Limit, I/O comments), tags (descriptions, member comments, aliases, initial values),
   programs, routines, rungs and rung comments, tasks, Add-On Instructions.
2. **Scan order** – the safety programs are walked from their main routine through the `JSR` call tree, exactly as the
   controller scans them; uncalled routines are reported as dead; safety AOIs are inlined (parameters, local tags).
3. **Boolean model** – every rung becomes an expression (`·` AND, `∥` OR, NOT, edges `OSR/OSF/ONS`, timers,
   comparisons). A safety input instruction (`ESTOP`, `RIN`, `LC`, `DCS`, `DCST`, `SMAT`, …) is a **cause**; its `.O1`
   is the device state (LC mute input and TSAM/TSSM/FSBM muting included). Outputs (**effects**) are the safety outputs
   written in the SafetyTask (`ROUT`/`CROUT` pairs as one column), CIP Safety drive outputs (`:SO.SafeTorqueOff`,
   SS1/SBC/SLS requests) and configured information bits. Instruction channels that are plain copies of inputs
   (`XIC(input) OTE(copy)`) are followed back to the physical channel (module, CRTL, I/O comment, equal-channel check);
   outputs driven by a `ROUT`/`CROUT` through such copies are grouped under the instruction.
4. **Healthy state** – all devices healthy, standard-mapped bits and other free conditions at 0 (or at the smallest set
   needed to energise the output); never-written tags take their initial value; seal-in contacts are assumed on.
5. **Cells** – for every device in the logic cone of an output: trip the device → output off? (`X`); restored by a
   standard bit (`XB`) or by an internal condition (`XM`); off only together with another device (`XC`); then
   `N` / `X1` for constant / single-channel devices – `N` also when the device is bridged by a constant contact (a tag
   with initial value 1 that the logic never writes, e.g. a forgotten commissioning bit). The full rung path of every
   cell is stored, including the **scan-order lag** (a tag read before it is written in the scan = +1 task period).
   **No link is ever derived from tag-name similarity.**
6. **Metadata** – reset type and reset sources (traced one level into the standard code through the SafetyTagMap),
   EDM feedback, restart behaviour (seal-in analysis), stop category (off-delay timers in the path → category 1 with
   the preset; `?` presets of L5K exports are read from the TIMER tag value), reaction-time data per device (incl.
   scan-order lag).
7. **Audit** – rules below; each finding carries routine and rung numbers.

### Audit rules

| Severity | Rule |
|---|---|
| **ALARM** | constant channel inputs · channels from standard tags · standard bit bypassing a device (XB) · muting driven from standard control · standard bit alone energising a safety output (with all devices tripped) · E-stop with automatic reset · both channels on the same input · AFI (also on a rung without outputs) · constant contact / branch bridging a device · reset generated automatically (latched in a standard sequence / written by the SafetyTask) |
| **DEAD** | devices without effect on safety outputs · unused muting blocks · constant (never written) tags · unused safety tags · unused safety I/O channels · uncalled routines · safety modules / drives not used · drives without CIP Safety |
| **VERIFY** | input / output / drive CRTL (PRIORITY above the threshold, scan-order lag included) · channels copied from inputs (late copies = +1 scan) or computed by logic · tags read before they are written in the scan · SafetyTagMap destination also written by the safety logic · ROUT/CROUT with both feedbacks on one input · ROUT/CROUT outputs switched by logic outside the instruction enable · OSF/OSR + OTE on one tag · multiple OTE · ROUT reset conditioned by another `.FP` · OR-connected devices · automatic restart via seal-in · automatic reset of guards · resets from standard control · standard bits never written (writes searched in ladder incl. AOI Output/InOut parameters and data instructions, ST, FBD and SFC actions) · outputs always on / energised only on a trip / without a device · missing I/O comments · data / comparison / latch conditions · direct safety inputs · heuristic operand mapping · protected / non-ladder routines, AOIs, JMP/MCR, unknown instructions, conditional JSR · ROUT channel mismatch · loads of outputs · stop category, off-delay timers outside device paths · forces · completeness |

### Supported instructions

| Instruction | Operand order |
|---|---|
| `ESTOP`, `RIN`, `LC`, `ROUT` | verified on real exports |
| `DCS`, `DCST`, `SMAT`, `CROUT`, `DIN`, `ENPEN`, `THRS` | Rockwell operand tables (configuration operands, then inputs) |
| `DCSTM`, `DCSTL`, `DCSRT`, `DCM`, `DCA/DCAF`, `THRSe`, `TSAM`, `TSSM`, `FSBM`, `FPMS`, `EPMS` | roles inferred from the operands – flagged *to verify* |
| `XIC XIO OTE OTL OTU OSR OSF ONS JSR AFI NOP`, timers `TON TOF RTO TONR TOFR TONS TOFS`, counters, comparisons, data instructions | standard ladder semantics |

The cause/effect link never depends on the operand order (it follows `.O1` through the logic); only the channel / reset
metadata does – which is why inferred mappings are reported.

## Limitations

* Only **ladder (RLL)** routines of the safety task are analysed; ST/FBD/SFC and source-protected routines/AOIs are
  reported, not analysed. In the standard programs ST/FBD/SFC code is searched only for writes of SafetyTagMap sources.
* Steady-state analysis: one-shot pulses are 0, timers are evaluated at their final state, seal-ins are on.
  Sequencing, discrepancy timing and reset edges are covered by the generated test record, not by the matrix.
* Several OTE coils on one tag: the last one in the scan wins (reported).
* L5X support is tested on synthetic files; please report exports that do not parse.
* Physical wiring (what a ROUT output supplies, hardwired STO) is not in the code and is always listed *to verify*.

## Data protection

PLC exports contain customer know-how and password hashes. `.gitignore` excludes `*.L5K`, `*.L5X`, `*.ACD` and
generated workbooks – only the synthetic demo files are tracked. Keep project exports outside the repository.

## Development

```bash
pip install -e . pytest
python -m pytest            # or: python -m unittest discover
python tools/check_headers.py
```

Every file starts with a header – project, file, author, revision with date and the list of changes, e.g.:

```python
# =============================================================================
# Project : Safety Matrix Generator (GuardLogix SafetyTask -> Cause & Effect)
# File    : safety_matrix/analysis.py
# Author  : Robert Pietroń
# Revision: 1.0.0 (2026-10-18)
# Changes :
#   1.0.0 (2026-10-18) - First universal release ...
# =============================================================================
```

When a file changes, raise its revision and add a line to its *Changes* list (and to `CHANGELOG.md`).
Texts live in `safety_matrix/locales/{pl,en,fr,da}.py` – all four catalogues must have the same keys (checked by the tests).

---

## Opis po polsku

**Generator macierzy bezpieczeństwa (Safety Matrix / Cause & Effect) dla programów GuardLogix.** Program czyta eksport
Studio 5000 (`.L5K`, `.L5X` lub L5K wklejony do `.docx`), deterministycznie analizuje logikę drabinkową **SafetyTask**
i tworzy skoroszyt Excel: macierz wg wzorca (Group Interlocks, MOTOR, VALVE), legendę, funkcje bezpieczeństwa z czasami
reakcji (CRTL z konfiguracji CIP Safety), protokół testów walidacyjnych (ISO 13849-2), arkusze urządzeń, wyjść
i ścieżek oraz **raport walidacyjny** (alarmy krytyczne, martwe elementy, pozycje do weryfikacji – zawsze z rutyną
i numerem rungu). Teksty w czterech językach (PL, EN, FR, DA) z przełącznikiem na arkuszu *Start*.

Zasady analizy: każde skrzyżowanie wynika ze ścieżki logicznej w kodzie (symulacja boolowska rungów w kolejności
skanowania, z rozwinięciem JSR i bloków AOI) – nigdy z podobieństwa nazw tagów. Kanały będące kopiami wejść
(`XIC(wejście) OTE(kopia)`) są śledzone do wejścia fizycznego, a odczyt tagu przed jego zapisem w cyklu jest liczony
jako dodatkowy okres zadania w czasie reakcji. Styk o stałej wartości 1 (np. pozostawiony bit uruchomieniowy)
mostkujący urządzenie daje w macierzy kod `N` i alarm krytyczny. EDM i przyciski resetu są metadanymi,
nie przyczynami. Bity z `SafetyTagMap` traktowane są jako sterowanie standardowe: jeśli mogą obejść funkcję
bezpieczeństwa, komórka dostaje kod `XB`, a raport – alarm krytyczny.

Na GitHubie: **Actions → Generate Safety Matrix → Run workflow** – podajesz ścieżkę eksportu w repozytorium, konfigurację
i języki; skoroszyt i JSON są w sekcji *Artifacts* przebiegu, a podsumowanie z alarmami krytycznymi na stronie przebiegu.
Programy klientów analizuj wyłącznie w **prywatnej kopii** repozytorium albo lokalnie – artefakty publicznego
repozytorium mogą pobrać inni użytkownicy GitHuba.

Szybki start:

```bash
pip install .
safety-matrix analyze examples/demo/DemoCell.L5K -c examples/demo/config.yaml -o DemoCell_macierz.xlsx
safety-matrix init-config MojaLinia.L5K -o mojalinia.yaml --lang pl,en     # szkielet konfiguracji do uzupełnienia
safety-matrix analyze MojaLinia.L5K -c mojalinia.yaml -o MojaLinia_macierz.xlsx
```

Wynik wspiera inżyniera, ale **nie zastępuje** oceny ryzyka ani walidacji funkcji bezpieczeństwa – każdą pozycję
raportu musi ocenić kompetentna osoba. Eksportów sterowników klientów nie należy umieszczać w repozytorium.
