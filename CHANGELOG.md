<!--
=============================================================================
Project : Safety Matrix Generator (GuardLogix SafetyTask -> Cause & Effect)
File    : CHANGELOG.md
Author  : Robert Pietroń
Revision: 1.1.0 (2026-10-18)
Changes :
  1.0.0 (2026-10-18) - Change log of the project (with the lineage of the
                       PortalSaw matrix revisions 1.0-1.4).
  1.1.0 (2026-10-18) - Entry for the manual GitHub Actions workflows.
=============================================================================
-->

# Changelog

All notable changes are listed here. Every source file also keeps its own revision and change list in its header.

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
