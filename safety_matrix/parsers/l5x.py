# =============================================================================
# Project : Safety Matrix Generator (GuardLogix SafetyTask -> Cause & Effect)
# File    : safety_matrix/parsers/l5x.py
# Author  : Robert Pietroń
# Revision: 1.0.0 (2026-10-18)
# Changes :
#   1.0.0 (2026-10-18) - First universal release: L5X (XML) parser producing the
#                        same model as the L5K parser (SafetyInfo/SafetyTagMap,
#                        Modules/Ports/Connections, Tags, Programs, RLL
#                        routines, Tasks, Add-On Instructions).
# =============================================================================
"""Parser for Studio 5000 ``.L5X`` (XML) exports."""
from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from typing import Optional

from ..model import (AOIDefinition, AOIParameter, Connection, Module, Program, Project,
                     Routine, Rung, Tag, Task)
from .l5k import parse_safety_tag_map, parse_value


def _a(el, *names, default=''):
    """Attribute lookup, case-insensitive, first match of several candidate names."""
    if el is None:
        return default
    low = {k.lower(): v for k, v in el.attrib.items()}
    for n in names:
        if n.lower() in low:
            return low[n.lower()]
    return default


def _num(v) -> Optional[float]:
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _text(el) -> str:
    return (el.text or '').strip() if el is not None else ''


def _bool(v) -> bool:
    return str(v).strip().lower() in ('true', '1', 'yes')


def _tag_from_el(el, scope: str) -> Tag:
    tag = Tag(name=_a(el, 'Name'), data_type=_a(el, 'DataType'), scope=scope, tag_class=_a(el, 'Class'),
              alias_for=_a(el, 'AliasFor'))
    dims = _a(el, 'Dimensions')
    if dims and tag.data_type:
        tag.data_type += '[' + dims.replace(' ', ',') + ']'
    tag.description = _text(el.find('Description'))
    for c in el.findall('./Comments/Comment'):
        tag.comments[_a(c, 'Operand')] = _text(c)
    ttype = _a(el, 'TagType')
    if ttype == 'Consumed':
        tag.usage = 'Consumed'
        ci = el.find('ConsumeInfo')
        tag.producer, tag.remote_tag = _a(ci, 'Producer'), _a(ci, 'RemoteTag')
    elif ttype == 'Produced':
        tag.usage = 'Produced'
    for d in el.findall('Data'):
        if _a(d, 'Format') == 'L5K':
            tag.value = parse_value(_text(d))
            break
    else:
        dv = el.find('./Data/DataValue')
        if dv is not None:
            tag.value = parse_value(_a(dv, 'Value'))
    return tag


def _routine_from_el(el) -> Routine:
    r = Routine(name=_a(el, 'Name'), kind=_a(el, 'Type', default='RLL') or 'RLL',
                description=_text(el.find('Description')))
    if el.find('.//EncodedData') is not None or _a(el, 'EncodedType'):
        r.protected = True
        return r
    for i, rung in enumerate(el.findall('./RLLContent/Rung')):
        num = _a(rung, 'Number')
        txt = _text(rung.find('Text')).rstrip(';').strip()
        r.rungs.append(Rung(number=int(num) if num.isdigit() else i, text=' '.join(txt.split()),
                            comment=_text(rung.find('Comment')), kind=_a(rung, 'Type', default='N') or 'N'))
    return r


def parse_l5x(text: str, source_name: str = '') -> Project:
    root = ET.fromstring(text.encode('utf-8') if isinstance(text, str) else text)
    proj = Project(source_name=source_name, source_format='L5X',
                   software_version=_a(root, 'SoftwareRevision'))
    ctrl = root.find('Controller')
    if ctrl is None:
        raise ValueError('L5X without a <Controller> element')
    proj.controller = _a(ctrl, 'Name')
    proj.processor = _a(ctrl, 'ProcessorType')
    si = ctrl.find('SafetyInfo')
    if si is not None:
        proj.safety_level = _a(si, 'SafetyLevel')
        if _a(si, 'SafetyLocked'):
            proj.safety_locked = _bool(_a(si, 'SafetyLocked'))
        proj.safety_tag_map = parse_safety_tag_map(_text(si.find('SafetyTagMap')))
    if not proj.safety_level:
        proj.safety_level = _a(ctrl, 'SafetyLevel')

    # ------------------------------------------------------------ modules
    for m in ctrl.findall('./Modules/Module'):
        mod = Module(name=_a(m, 'Name'), parent=_a(m, 'ParentModule'), catalog=_a(m, 'CatalogNumber'),
                     description=_text(m.find('Description')), inhibited=_bool(_a(m, 'Inhibited')))
        if _a(m, 'SafetyEnabled'):
            mod.safety_enabled = _bool(_a(m, 'SafetyEnabled'))
        for p in m.findall('./Ports/Port'):
            if _bool(_a(p, 'Upstream')):
                addr = _a(p, 'Address')
                if _a(p, 'Type').lower() == 'ethernet' or re.match(r'\d+\.\d+\.\d+\.\d+$', addr):
                    mod.address = addr
                    mod.port_label = 'ENet'
                elif addr.lstrip('-').isdigit():
                    mod.slot = int(addr)
        for c in m.findall('.//Connections/Connection'):
            name, ctype = _a(c, 'Name'), _a(c, 'Type')
            kind = 'input' if 'input' in (ctype + name).lower() else 'output' if 'output' in (ctype + name).lower() else ''
            rpi = _num(_a(c, 'RPI'))
            con = Connection(name=name, kind=kind, rpi_ms=rpi / 1000.0 if rpi is not None else None,
                             timeout_multiplier=_num(_a(c, 'TimeoutMultiplier')),
                             network_delay_multiplier=_num(_a(c, 'NetworkDelayMultiplier')),
                             reaction_time_limit_ms=_num(_a(c, 'ReactionTimeLimit', 'ConnectionReactionTimeLimit')),
                             tag_suffix=_a(c, 'InputTagSuffix', 'OutputTagSuffix'))
            safety_hint = 'safety' in (ctype + name).lower() or con.reaction_time_limit_ms is not None
            for tagel, is_in in ((c.find('InputTag'), True), (c.find('OutputTag'), False)):
                if tagel is None:
                    continue
                if _a(tagel, 'Class') == 'Safety' or safety_hint:
                    con.safety = True
                suffix = (_a(c, 'InputTagSuffix') if is_in else _a(c, 'OutputTagSuffix')) or ('I' if is_in else 'O')
                for cm in tagel.findall('./Comments/Comment'):
                    member = _a(cm, 'Operand').lstrip('.')
                    mod.comments[f'{suffix.upper()}.{member.upper()}'] = _text(cm)
                    con.comments[member.upper()] = _text(cm)
            if safety_hint:
                con.safety = True
            if con.safety and not con.tag_suffix:
                con.tag_suffix = 'I' if kind == 'input' else 'O'
            mod.connections.append(con)
        proj.modules[mod.name] = mod

    # ------------------------------------------------------------ AOIs
    for d in ctrl.findall('./AddOnInstructionDefinitions/AddOnInstructionDefinition'):
        aoi = AOIDefinition(name=_a(d, 'Name'), aoi_class=_a(d, 'Class'), description=_text(d.find('Description')))
        for p in d.findall('./Parameters/Parameter'):
            aoi.parameters.append(AOIParameter(name=_a(p, 'Name'), data_type=_a(p, 'DataType'),
                                               usage=_a(p, 'Usage', default='Input'), required=_bool(_a(p, 'Required'))))
        aoi.local_tags = [_tag_from_el(t, aoi.name) for t in d.findall('./LocalTags/LocalTag')]
        for r in d.findall('./Routines/Routine'):
            rr = _routine_from_el(r)
            if rr.name == 'Logic':
                aoi.logic = rr
        if d.find('.//EncodedData') is not None:
            aoi.protected = True
        proj.aois[aoi.name] = aoi

    # ------------------------------------------------------------ tags, programs, tasks
    for t in ctrl.findall('./Tags/Tag'):
        tag = _tag_from_el(t, 'controller')
        proj.tags[tag.name] = tag
    for p in ctrl.findall('./Programs/Program'):
        prog = Program(name=_a(p, 'Name'), program_class=_a(p, 'Class', default='Standard') or 'Standard',
                       main_routine=_a(p, 'MainRoutineName'), disabled=_bool(_a(p, 'Disabled')))
        for t in p.findall('./Tags/Tag'):
            tag = _tag_from_el(t, prog.name)
            prog.tags[tag.name] = tag
        for r in p.findall('./Routines/Routine'):
            rr = _routine_from_el(r)
            prog.routines[rr.name] = rr
        for e in p.findall('./Routines/EncodedData'):
            name = _a(e, 'Name')
            if name:
                prog.routines[name] = Routine(name=name, protected=True)
        proj.programs[prog.name] = prog
    for t in ctrl.findall('./Tasks/Task'):
        task = Task(name=_a(t, 'Name'), task_class=_a(t, 'Class', default='Standard') or 'Standard',
                    task_type=_a(t, 'Type'), rate_ms=_num(_a(t, 'Rate')), watchdog_ms=_num(_a(t, 'Watchdog')),
                    programs=[_a(s, 'Name') for s in t.findall('./ScheduledPrograms/ScheduledProgram')])
        proj.tasks[task.name] = task
    return proj
