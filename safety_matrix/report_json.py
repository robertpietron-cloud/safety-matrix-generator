# =============================================================================
# Project : Safety Matrix Generator (GuardLogix SafetyTask -> Cause & Effect)
# File    : safety_matrix/report_json.py
# Author  : Robert Pietroń
# Revision: 1.0.0 (2026-10-18)
# Changes :
#   1.0.0 (2026-10-18) - First universal release: machine-readable JSON export
#                        of devices, effects, matrix cells (with rung paths) and
#                        audit findings.
# =============================================================================
"""JSON export of the analysis (for diffing revisions, CI checks or other tools)."""
from __future__ import annotations

from typing import List

from . import __version__
from .analysis import Analysis
from .audit import Finding


def _loc(A: Analysis, l):
    return None if l is None else {'program': l.program, 'routine': l.routine, 'rung': l.rung, 'aoi': l.aoi or None,
                                   'label': A.loc_label(l)}


def to_dict(A: Analysis, findings: List[Finding], layout=None) -> dict:
    p = A.p
    return {
        'generator': {'name': 'safety-matrix-generator', 'version': __version__, 'author': 'Robert Pietroń'},
        'source': {'file': p.source_name, 'format': p.source_format, 'controller': p.controller, 'processor': p.processor,
                   'software': p.software_version, 'safety_level': p.safety_level,
                   'safety_task': {'name': A.task.name, 'period_ms': A.task.rate_ms, 'watchdog_ms': A.task.watchdog_ms} if A.task else None,
                   'safety_tag_map': p.safety_tag_map},
        'scan_order': [f'{pg}/{r}' for pg, r in A.lm.executed],
        'devices': [{'tag': d.tag, 'id': d.id or None, 'zone': d.zone or None, 'type': d.type, 'instruction': d.instr, 'kind': d.kind,
                     'channel_a': d.ch_a, 'channel_b': d.ch_b, 'reset': d.reset,
                     'reset_type': {True: 'MANUAL', False: 'AUTOMATIC'}.get(d.reset_manual),
                     'filter_ms': d.filter_ms, 'mute': d.mute or None, 'location': _loc(A, d.loc), 'outputs_tripped': d.n_eff,
                     'flags': [k for k, v in (('constant_channels', d.const_channels), ('equal_channels', d.equal_channels),
                                              ('standard_channels', d.std_channels), ('heuristic_operands', d.heuristic)) if v]}
                    for d in A.devices.values()],
        'effects': [{'key': e.key, 'kind': e.kind, 'outputs': e.outputs, 'instruction': e.instr or None, 'info': e.info,
                     'in_matrix': e.in_matrix, 'reason': e.reason or None, 'location': _loc(A, A.effect_rung(e)),
                     'baseline_true': sorted(e.baseline)} for e in A.effects],
        'cells': [{'device': d, 'effect': k, 'code': c.code, 'raw_code': c.raw,
                   'path': [{'tag': t, 'at': A.loc_label(l)} for t, l in c.path],
                   'bypass': c.bypass, 'conditions': c.conditions, 'partners': c.partners, 'delay_ms': c.delay_ms}
                  for (d, k), c in A.cells.items()],
        'findings': [{'severity': f.severity, 'rule': f.key, 'routine': f.routine, 'rungs': f.rungs, 'element': f.element,
                      'priority': f.priority, 'params': {k: str(v) for k, v in f.params.items()}} for f in findings],
    }
