# =============================================================================
# Project : Safety Matrix Generator (GuardLogix SafetyTask -> Cause & Effect)
# File    : safety_matrix/pipeline.py
# Author  : Robert Pietroń
# Revision: 1.0.0 (2026-10-18)
# Changes :
#   1.0.0 (2026-10-18) - First universal release: end-to-end pipeline
#                        (load -> analyse -> audit -> workbook / JSON).
# =============================================================================
"""End-to-end pipeline used by the CLI and the Python API."""
from __future__ import annotations

import json
from typing import List, Optional

from .analysis import Analysis
from .audit import run_audit
from .config import Layout, load_config
from .excel import MatrixWorkbook
from .i18n import Tr
from .parsers import load_project
from .report_json import to_dict


def run(input_path: str, output_path: Optional[str], config_path: Optional[str] = None,
        languages: Optional[List[str]] = None, default_language: Optional[str] = None,
        json_path: Optional[str] = None, author: Optional[str] = None, revision: Optional[str] = None) -> dict:
    cfg = load_config(config_path)
    if languages:
        cfg.languages = [l.lower() for l in languages]
        if not default_language and cfg.default_language not in cfg.languages:
            cfg.default_language = cfg.languages[0]
    if default_language:
        cfg.default_language = default_language.lower()
    # the default language is always listed first (dictionary column order and fallback)
    cfg.languages = [cfg.default_language] + [l for l in cfg.languages if l != cfg.default_language]
    if author:
        cfg.author = author
    if revision:
        cfg.revision = revision
    project = load_project(input_path)
    if project.safety_task is None and not project.safety_programs():
        raise SystemExit('No safety task / safety program found in the export.')
    A = Analysis(project, cfg.options())
    findings = run_audit(A, cfg.crtl_priority_ms)
    tr = Tr(cfg.languages)
    layout = Layout(A, cfg, tr)
    summary = {
        'controller': project.controller, 'devices': len(A.devices), 'effects': len(A.matrix_effects()),
        'cells': {c: sum(1 for x in A.cells.values() if x.code == c) for c in sorted({x.code for x in A.cells.values()})},
        'alarm': sum(1 for f in findings if f.severity == 'ALARM'), 'dead': sum(1 for f in findings if f.severity == 'DEAD'),
        'verify': sum(1 for f in findings if f.severity == 'VERIFY'),
    }
    if output_path:
        MatrixWorkbook(A, findings, layout, cfg, tr).build(output_path)
    if json_path:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(to_dict(A, findings, layout), f, ensure_ascii=False, indent=1)
    return summary
