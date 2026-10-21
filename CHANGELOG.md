<!--
=============================================================================
Project : Safety Matrix Generator (GuardLogix SafetyTask -> Cause & Effect)
File    : CHANGELOG.md
Author  : Robert Pietroń
Revision: 1.2.0 (2026-10-21)
Changes :
  1.0.0 (2026-10-18) - Change log of the project (with the lineage of the
                       PortalSaw matrix revisions 1.0-1.4).
  1.1.0 (2026-10-18) - Entry for the manual GitHub Actions workflows.
  1.2.0 (2026-10-21) - Entry for generator 1.1.0.
=============================================================================
-->

# Changelog

All notable changes are listed here. Every source file also keeps its own revision and change list in its header.

## 1.1.0 – 2026-10-21 – second real-program check (Robert Pietroń)

Found while checking a second real GuardLogix project (the export itself is not part of the repository):

* **Fixed – false critical alarms:** "standard bit alone energises a safety output" is now evaluated with every device
  of the output tripped; a standard permissive in series (`XIC(std) XIC(Area_OK)`) is no longer reported.
* **Fixed – constant bridge not seen:** program-scope operands (`Program\Tag.0`) are split correctly, so bits of
  program tags get their initial value; a device bridged by a constant contact (initial value 1, never written) gets
  code `N` and a critical alarm naming the device (also when a series contact is distributed into the branch).
* **Fixed – timer presets `?`:** L5K neutral text shows `TON(T,?,?)`; the preset is read from the TIMER tag value,
  array element or AOI local tag (stop category 1 delay, test record).
* **Fixed – std writes not found:** the search for writes of SafetyTagMap sources covers AOI Output/InOut parameters,
  data instructions, timers/counters, JSR return / SBR parameters, unknown instructions (conservatively), aliases,
  program-scope shadowing, consumed tags, ST assignments and calls, FBD output references and SFC action code.
* **Fixed – drive peripheral sub-modules** (`$NoName`, `…PERIPHERAL-MODULE`) are not reported as hardwired drives.
* **New – copied channels:** channels that are plain copies of inputs are followed to the physical channel (module,
  CRTL, comments, equal-channel / standard / constant checks); copies executed after the instruction add one scan.
* **New – scan-order lag:** links of a cause→effect path read before they are written in the scan; shown per cell,
  in the reaction time and as findings.
* **New – ROUT/CROUT through copies** are grouped as one effect; findings for equal feedback channels and for outputs
  switched by logic that bypasses the instruction enable (EDM mismatch).
* **New findings:** SafetyTagMap destination written by the safety logic (and read before the write), outputs always
  on / energised only on a trip, AFI on a rung without outputs, off-delay timers outside device paths, computed
  channels; stop category 1 only for timers that lie in a device→output path.
* JSON: channel sources, copy rungs, scan lag per device and cell. Tests: synthetic `tests/data/ScanCell.L5K`.

## Repository – 2026-10-18 (package unchanged, 1.0.0)

* New manual workflow **Generate Safety Matrix** (`.github/workflows/generate.yml`, *Run workflow*): export and
  configuration from the repository, languages, author, revision, optional failure on critical alarms; summary with the
  critical alarms on the run page, workbook + JSON as an artifact; inputs passed via environment variables.
* Workflow **tests** can be started manually (choice of Python versions) and keeps the demo workbook as an artifact.

## 1.0.0 – 2026-10-18 – first universal release (Robert Pietroń)

* Parsers: L5K (also pasted into Word `.docx`), L5X; modules, CIP Safety connections (RPI, TM, NDM, CRTL), I/O comments,
  tags with comments / aliases / initial values, SafetyTagMap, programs, routines with rung comments, tasks, Add-On Instructions.
* Ladder engine: scan order via the JSR call tree, AOI inlining, alias and program-scope resolution, registry of
  GuardLogix safety instructions (ESTOP, RIN, LC, DIN, ENPEN, THRS, DCS, DCST, SMAT, ROUT, CROUT, muting and mode
  instructions), timers (off-delay → stop category 1), edges, comparisons, data instructions.
* Analysis: automatic causes (safety input instructions, direct safety inputs, consumed safety tags) and effects
  (ROUT/CROUT pairs, safety outputs, CIP Safety STO/SS1/SBC/SLS, configured information bits); codes X, X1, XB, XC, XM, N
  and S, SB, SC, SM; rung paths; reset sources traced into the standard code; restart and stop-category metadata;
  reaction-time data.
* Automatic validation report (critical alarms, dead elements, items to verify) with routine and rung.
* Excel workbook (Start, Group Interlocks, MOTOR, VALVE, Legend, Safety functions, Test record, Devices, Outputs,
  C&E paths, Validation report, Dictionary) in PL / EN / FR / DA with an in-workbook language switch; cached formula
  values so every viewer shows the default language; JSON export.
* YAML configuration, `init-config` skeleton generator, CLI (`analyze`, `init-config`, `dump`, `--fail-on-alarm`).
* Tests (synthetic DemoCell in L5K and L5X), header checker, CI workflow.
* Regression: on the PortalSaw line the generator reproduces the validated matrix rev 1.4 cell by cell
  (33 devices, 31 outputs, 289 intersections).

## Lineage – PortalSaw matrix (manual / semi-automatic, 2026-10-18)

| Rev. | Change |
|---|---|
| 1.0 | First matrix from PortalSaw20261007.L5K (Group Interlocks, MOTOR, VALVE, metadata, paths, report) |
| 1.1 | Legends of designations on the matrix sheets and the Legend sheet; document author |
| 1.2 | Validation test record; safety functions with reaction times (CRTL) and PL fields; code drop-downs with colouring |
| 1.3 | PL / EN language switch (Start sheet + dictionary) |
| 1.4 | French and Danish added to the language switch |
