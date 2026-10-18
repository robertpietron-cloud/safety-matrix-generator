# =============================================================================
# Project : Safety Matrix Generator (GuardLogix SafetyTask -> Cause & Effect)
# File    : safety_matrix/instructions.py
# Author  : Robert Pietroń
# Revision: 1.0.0 (2026-10-18)
# Changes :
#   1.0.0 (2026-10-18) - First universal release: registry of GuardLogix safety
#                        application instructions (operand roles in neutral
#                        text), standard ladder instruction classes, device type
#                        classification and ID abbreviations.
# =============================================================================
"""Instruction registry.

Operand lists give the neutral-text operand order (operand 0 = backing tag).
``verified=True`` means the order was confirmed on real exports; for the other
instructions the order follows the Rockwell operand tables (configuration
operands first, then inputs).  When the operand count of a call does not match
the registry, roles are inferred heuristically and the device is flagged
[TO BE VERIFIED] in the report.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from .model import io_parts


@dataclass(frozen=True)
class InstrSpec:
    name: str
    role: str                       # 'device', 'output', 'muting', 'mode'
    operands: Tuple[str, ...]
    device_type: str = ''           # fixed device type ('' = classify by name)
    verified: bool = False
    channels: Tuple[str, str] = ('ChannelA', 'ChannelB')
    reset: str = 'CircuitReset'
    reset_type: str = 'ResetType'
    extra: Dict[str, str] = field(default_factory=dict)


_LEGACY = ('ResetType', 'ChannelA', 'ChannelB', 'CircuitReset', 'FaultReset')
_DCS = ('SafetyFunction', 'InputType', 'DiscrepancyTime', 'RestartType', 'ColdStartType')

SAFETY_INSTRUCTIONS: Dict[str, InstrSpec] = {s.name: s for s in [
    # ---- input (cause) instructions
    InstrSpec('ESTOP', 'device', ('EStop',) + _LEGACY, 'EMERGENCY STOP', verified=True),
    InstrSpec('RIN', 'device', ('RIN',) + _LEGACY, verified=True),
    InstrSpec('LC', 'device', ('LC', 'ResetType', 'ChannelA', 'ChannelB', 'InputFilterTime', 'MuteLightCurtain',
                               'CircuitReset', 'FaultReset'), 'LIGHT CURTAIN', verified=True),
    InstrSpec('DIN', 'device', ('DIN',) + _LEGACY),
    InstrSpec('ENPEN', 'device', ('ENPEN',) + _LEGACY, 'ENABLING DEVICE'),
    InstrSpec('THRS', 'device', ('THRS', 'ActiveLow', 'ChannelValueTime', 'RightButtonNormallyOpen',
                                 'RightButtonNormallyClosed', 'LeftButtonNormallyOpen', 'LeftButtonNormallyClosed',
                                 'FaultReset'), 'TWO-HAND CONTROL', channels=('RightButtonNormallyOpen', 'LeftButtonNormallyOpen'),
              reset='FaultReset', reset_type=''),
    InstrSpec('THRSE', 'device', ('THRSe',), 'TWO-HAND CONTROL'),
    InstrSpec('DCS', 'device', ('DCS',) + _DCS + ('ChannelA', 'ChannelB', 'InputStatus', 'Reset'),
              reset='Reset', reset_type='RestartType'),
    InstrSpec('DCST', 'device', ('DCST',) + _DCS + ('ChannelA', 'ChannelB', 'TestRequest', 'InputStatus', 'Reset'),
              reset='Reset', reset_type='RestartType'),
    InstrSpec('DCSTM', 'device', ('DCSTM',), reset='Reset', reset_type='RestartType'),
    InstrSpec('DCSTL', 'device', ('DCSTL',), reset='Reset', reset_type='RestartType'),
    InstrSpec('DCSRT', 'device', ('DCSRT',), 'ENABLING DEVICE', reset='', reset_type=''),
    InstrSpec('DCM', 'device', ('DCM',), reset='', reset_type=''),
    InstrSpec('DCA', 'device', ('DCA',), 'ANALOG SAFETY INPUT', reset='Reset', reset_type=''),
    InstrSpec('DCAF', 'device', ('DCAF',), 'ANALOG SAFETY INPUT', reset='Reset', reset_type=''),
    InstrSpec('SMAT', 'device', ('SMAT', 'RestartType', 'ShortCircuitDetectDelayTime', 'ChannelA', 'ChannelB',
                                 'InputStatus', 'Reset'), 'SAFETY MAT', reset='Reset', reset_type='RestartType'),
    # ---- output instructions (EDM)
    InstrSpec('ROUT', 'output', ('ROUT', 'FeedbackType', 'Enable', 'Feedback1', 'Feedback2', 'FaultReset'),
              verified=True, channels=('Feedback1', 'Feedback2'), reset='FaultReset', reset_type='',
              extra={'enable': 'Enable'}),
    InstrSpec('CROUT', 'output', ('CROUT', 'FeedbackType', 'FeedbackReactionTime', 'Actuate', 'Feedback1', 'Feedback2',
                                  'InputStatus', 'OutputStatus', 'Reset'),
              channels=('Feedback1', 'Feedback2'), reset='Reset', reset_type='', extra={'enable': 'Actuate'}),
    # ---- muting / mode selection
    InstrSpec('TSAM', 'muting', ('TSAM',), reset='', reset_type=''),
    InstrSpec('TSSM', 'muting', ('TSSM',), reset='', reset_type=''),
    InstrSpec('FSBM', 'muting', ('FSBM',), reset='', reset_type=''),
    InstrSpec('FPMS', 'mode', ('FPMS',), reset='', reset_type=''),
    InstrSpec('EPMS', 'mode', ('EPMS',), reset='', reset_type=''),
]}

# Standard ladder instructions -------------------------------------------------
CONDITIONS = {'XIC', 'XIO'}
COMPARISONS = {'EQU', 'NEQ', 'LES', 'LEQ', 'GRT', 'GEQ', 'LIM', 'MEQ', 'CMP'}
EDGE_OUTPUTS = {'OSR', 'OSF'}
TIMERS = {'TON', 'TOF', 'RTO', 'TONR', 'TOFR', 'RTOR', 'TONS', 'TOFS'}
OFF_DELAY_TIMERS = {'TOF', 'TOFR', 'TOFS'}
COUNTERS = {'CTU', 'CTD', 'CTUD'}
NO_EFFECT = {'NOP', 'LBL', 'TND', 'RET', 'SBR', 'UID', 'UIE', 'EOT', 'SFP', 'SFR'}
FLOW_CONTROL = {'JMP', 'MCR', 'FOR', 'BRK', 'EVENT', 'AFI'}
# data instructions: index of the destination operand (None = no destination)
DATA_DEST = {
    'MOV': 1, 'MVM': 2, 'COP': 1, 'CPS': 1, 'FLL': 1, 'CLR': 0, 'CPT': 0, 'ADD': 2, 'SUB': 2, 'MUL': 2,
    'DIV': 2, 'MOD': 2, 'SQR': 1, 'NEG': 1, 'ABS': 1, 'AND': 2, 'OR': 2, 'XOR': 2, 'NOT': 1, 'BAND': 2,
    'BOR': 2, 'BXOR': 2, 'BNOT': 1, 'BTD': 2, 'SWPB': 2, 'TOD': 1, 'FRD': 1, 'DEG': 1, 'RAD': 1, 'TRN': 1,
    'RES': 0, 'GSV': 3, 'SSV': None, 'BSL': 0, 'BSR': 0, 'FFL': 1, 'FFU': 1, 'LFL': 1, 'LFU': 1, 'SIZE': 2,
    'CONCAT': 2, 'MID': 3, 'DTOS': 1, 'STOD': 1, 'RTOS': 1, 'STOR': 1, 'UPPER': 1, 'LOWER': 1,
    'MSG': None, 'ONS': None,
}

# Device types ------------------------------------------------------------------
DEVICE_TYPES = ['EMERGENCY STOP', 'SAFETY DOOR', 'SAFETY GATE', 'SAFETY SWITCH', 'LIGHT CURTAIN', 'SAFETY SCANNER',
                'SAFETY MAT', 'TWO-HAND CONTROL', 'ENABLING DEVICE', 'ANALOG SAFETY INPUT', 'SAFETY INPUT',
                'DIRECT SAFETY INPUT', 'EXTERNAL SAFETY SIGNAL']
TYPE_ABBR = {'EMERGENCY STOP': 'ES', 'SAFETY DOOR': 'DS', 'SAFETY GATE': 'SG', 'SAFETY SWITCH': 'SS',
             'LIGHT CURTAIN': 'LC', 'SAFETY SCANNER': 'SC', 'SAFETY MAT': 'SM', 'TWO-HAND CONTROL': 'TH',
             'ENABLING DEVICE': 'ED', 'ANALOG SAFETY INPUT': 'AI', 'SAFETY INPUT': 'SI',
             'DIRECT SAFETY INPUT': 'DI', 'EXTERNAL SAFETY SIGNAL': 'XS'}

_NAME_RULES = [
    (r'scan|skan', 'SAFETY SCANNER'),
    (r'light|curtain|(^|_)lc(_|\d|$)|kurtyn|lysgard|barri', 'LIGHT CURTAIN'),
    (r'e_?stop|estop|emg|emerg|n[øo]d_?stop|awaryj|arret|aru', 'EMERGENCY STOP'),
    (r'switch|wylacz|interrupteur|afbryder', 'SAFETY SWITCH'),
    (r'gate|bramk|furtk|l[åa]ge|portillon', 'SAFETY GATE'),
    (r'door|drzw|d[øo]r(_|\d|$)|porte|guard|oslon', 'SAFETY DOOR'),
    (r'(^|_)mat(_|\d|$)|mata', 'SAFETY MAT'),
    (r'two.?hand|2.?hand|thrs|dwur', 'TWO-HAND CONTROL'),
    (r'enabl|pendant|zezwol', 'ENABLING DEVICE'),
]


def classify_device(instr: str, tag: str, operands: Dict[str, str]) -> str:
    """Device type from the instruction, its SafetyFunction operand or the tag name (labelling only)."""
    spec = SAFETY_INSTRUCTIONS.get(instr.upper())
    if instr.upper() == 'LC':
        return 'SAFETY SCANNER' if re.search(r'scan|skan', tag, re.I) else 'LIGHT CURTAIN'
    if spec and spec.device_type:
        return spec.device_type
    hint = operands.get('SafetyFunction', '') + ' ' + tag
    for rx, typ in _NAME_RULES:
        if re.search(rx, hint, re.I):
            return typ
    return 'SAFETY INPUT'


def looks_literal(op: str) -> bool:
    return bool(re.fullmatch(r'[+-]?\d+(\.\d+)?([eE][+-]?\d+)?|\d+#[0-9A-Fa-f_]+|\?|', op.strip()))


def map_operands(spec: InstrSpec, args: List[str]) -> Tuple[Dict[str, str], bool]:
    """Map call operands to roles. Returns (roles, heuristic)."""
    if len(spec.operands) > 1 and len(args) == len(spec.operands):
        return dict(zip(spec.operands, args)), False
    roles = {spec.operands[0] if spec.operands else 'Tag': args[0] if args else ''}
    tags = [a for a in args[1:] if not looks_literal(a) and not re.fullmatch(r'[A-Z_]+', a)]
    io = [a for a in tags if (io_parts(a) or ('', '', ''))[1] in ('I', 'SI')]
    chans = (io or [a for a in tags if not a.endswith('.O1')])[:2]
    if chans:
        roles[spec.channels[0]] = chans[0]
        roles[spec.channels[1]] = chans[1] if len(chans) > 1 else chans[0]
    if spec.reset and tags:
        resets = [a for a in tags if re.search(r'reset|rst|quit|ack', a, re.I)]
        roles[spec.reset] = (resets or [tags[-1]])[-1]
    kw = [a for a in args[1:] if re.fullmatch(r'[A-Z_]+', a)]
    if spec.reset_type and kw:
        man = [a for a in kw if a in ('MANUAL', 'AUTOMATIC')]
        if man:
            roles[spec.reset_type] = man[0]
    lc = [a for a in args[1:] if a.endswith('.O1')]
    if lc:
        roles['LightCurtain'] = lc[0]
    return roles, True


def reset_is_manual(spec: Optional[InstrSpec], roles: Dict[str, str]) -> Optional[bool]:
    """True = manual reset, False = automatic, None = unknown."""
    if not spec or not spec.reset_type:
        return None
    v = roles.get(spec.reset_type, '').upper()
    if v in ('MANUAL', '0'):
        return True
    if v in ('AUTOMATIC', 'AUTO', '1'):
        return False
    return None
