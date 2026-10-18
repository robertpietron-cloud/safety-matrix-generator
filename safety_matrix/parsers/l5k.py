# =============================================================================
# Project : Safety Matrix Generator (GuardLogix SafetyTask -> Cause & Effect)
# File    : safety_matrix/parsers/l5k.py
# Author  : Robert Pietroń
# Revision: 1.0.0 (2026-10-18)
# Changes :
#   1.0.0 (2026-10-18) - First universal release: L5K (ASCII export) parser for
#                        controller, SafetyTagMap, modules + CIP Safety
#                        connections, tags (comments, aliases, initial values),
#                        programs, routines (rungs + rung comments), tasks and
#                        Add-On Instructions.  Tolerates exports pasted into
#                        Word (blank lines between lines).
# =============================================================================
"""Parser for Studio 5000 / RSLogix 5000 ``.L5K`` exports."""
from __future__ import annotations

import re
from typing import Dict, List, Optional, Tuple

from ..model import (AOIDefinition, AOIParameter, Connection, Module, Program, Project,
                     Routine, Rung, Tag, Task)

_ESC = {'N': '\n', 'L': '\n', 'R': '\r', 'T': '\t', 'P': '\f', "'": "'", '"': '"', '$': '$'}


def unescape(s: str) -> str:
    """Decode L5K string escapes ($N, $', $$, $hh ...)."""
    out, i = [], 0
    while i < len(s):
        c = s[i]
        if c == '$' and i + 1 < len(s):
            n = s[i + 1]
            if n.upper() in _ESC:
                out.append(_ESC[n.upper()] if n.upper() in 'NLRTP' else _ESC[n])
                i += 2
                continue
            if re.match(r'[0-9A-Fa-f]{2}', s[i + 1:i + 3]):
                out.append(chr(int(s[i + 1:i + 3], 16)))
                i += 3
                continue
        out.append(c)
        i += 1
    return ''.join(out)


def strip_block_comments(text: str) -> str:
    """Remove (* ... *) comments outside of string literals."""
    out, i, n, q = [], 0, len(text), None
    while i < n:
        c = text[i]
        if q:
            out.append(c)
            if c == '$' and i + 1 < n:
                out.append(text[i + 1])
                i += 2
                continue
            if c == q:
                q = None
            i += 1
            continue
        if c in '"\'':
            q = c
            out.append(c)
            i += 1
            continue
        if text.startswith('(*', i):
            j = text.find('*)', i + 2)
            i = n if j < 0 else j + 2
            continue
        out.append(c)
        i += 1
    return ''.join(out)


def _balance(s: str, depth=0, q=None):
    """Return (paren/bracket depth, open quote) after scanning s."""
    i = 0
    while i < len(s):
        c = s[i]
        if q:
            if c == '$':
                i += 2
                continue
            if c == q:
                q = None
        elif c in '"\'':
            q = c
        elif c in '([':
            depth += 1
        elif c in ')]':
            depth -= 1
        i += 1
    return depth, q


def split_top(s: str, sep=',') -> List[str]:
    """Split on `sep` at nesting depth 0, outside string literals."""
    parts, cur, depth, q, i = [], [], 0, None, 0
    while i < len(s):
        c = s[i]
        if q:
            cur.append(c)
            if c == '$' and i + 1 < len(s):
                cur.append(s[i + 1])
                i += 2
                continue
            if c == q:
                q = None
        elif c in '"\'':
            q = c
            cur.append(c)
        elif c in '([':
            depth += 1
            cur.append(c)
        elif c in ')]':
            depth -= 1
            cur.append(c)
        elif c == sep and depth == 0:
            parts.append(''.join(cur).strip())
            cur = []
        else:
            cur.append(c)
        i += 1
    if ''.join(cur).strip():
        parts.append(''.join(cur).strip())
    return parts


def parse_string(v: str) -> str:
    """Concatenate adjacent "..." literals and unescape."""
    parts = re.findall(r'"((?:[^"$]|\$.)*)"', v, re.S)
    if not parts:
        return v.strip()
    return unescape(''.join(parts))


def parse_attrs(s: str) -> Dict[str, str]:
    """'A := 1, B := "x", COMMENT.PT00DATA := "y"' -> dict (string values unescaped)."""
    out = {}
    for part in split_top(s):
        if ':=' not in part:
            continue
        k, v = part.split(':=', 1)
        k, v = k.strip(), v.strip()
        out[k] = parse_string(v) if v.startswith('"') else v
    return out


def parse_value(v: str):
    """Parse an initial value: int, float, or (nested) list; None if not numeric."""
    v = v.strip()
    if not v:
        return None
    if v.startswith('['):
        inner = v[1:-1] if v.endswith(']') else v[1:]
        return [parse_value(x) for x in split_top(inner)]
    m = re.fullmatch(r'([+-]?)(\d+)#([0-9A-Fa-f_]+)', v)
    if m:
        val = int(m.group(3).replace('_', ''), int(m.group(2)))
        return -val if m.group(1) == '-' else val
    try:
        return int(v)
    except ValueError:
        pass
    try:
        return float(v)
    except ValueError:
        return None


def _num(v: Optional[str]) -> Optional[float]:
    if v is None:
        return None
    try:
        return float(str(v).strip().strip('"'))
    except ValueError:
        return None


class _Lines:
    def __init__(self, lines: List[str]):
        self.lines = lines
        self.i = 0

    def eof(self):
        return self.i >= len(self.lines)

    def peek(self) -> str:
        return self.lines[self.i]

    def next(self) -> str:
        s = self.lines[self.i]
        self.i += 1
        return s

    def header(self) -> str:
        """Read a 'KEYWORD name (attrs ...)' header that may span several lines."""
        s = self.next()
        depth, q = _balance(s)
        while (depth > 0 or q) and not self.eof():
            nxt = self.next()
            s += '\n' + nxt
            depth, q = _balance(nxt, depth, q)
        return s

    def statement(self) -> str:
        """Read up to the terminating ';' (outside strings and brackets)."""
        s = self.next()
        depth, q = _balance(s)
        while not (depth <= 0 and not q and s.rstrip().endswith(';')) and not self.eof():
            nxt = self.next()
            s += '\n' + nxt
            depth, q = _balance(nxt, depth, q)
        return s.rstrip().rstrip(';').strip()

    def skip_to(self, end_kw: str):
        while not self.eof():
            if self.next().startswith(end_kw):
                return


def _head(s: str) -> Tuple[str, str, Dict[str, str]]:
    """'MODULE Name (attrs)' -> ('MODULE', 'Name', attrs)."""
    m = re.match(r'^(\w+)\s+([^\s(]+)?\s*(\((.*)\))?\s*$', s.strip(), re.S)
    if not m:
        return s.split()[0], '', {}
    return m.group(1), m.group(2) or '', parse_attrs(m.group(4) or '')


def _find_paren_block(s: str, start: int) -> int:
    """Index just after the ')' matching the '(' at s[start]."""
    depth, q, i = 0, None, start
    while i < len(s):
        c = s[i]
        if q:
            if c == '$':
                i += 2
                continue
            if c == q:
                q = None
        elif c in '"\'':
            q = c
        elif c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return len(s)


def parse_tag_statement(st: str, scope: str) -> Optional[Tag]:
    """'Name : TYPE[10] (attrs) := value' or 'Name OF Base (attrs)'."""
    st = st.strip()
    m = re.match(r'^([A-Za-z_]\w*)\s+OF\s+(\S+?)\s*(\(|$)', st)
    if m:
        tag = Tag(name=m.group(1), alias_for=m.group(2), scope=scope)
        p = st.find('(', m.end(2))
        if p >= 0:
            attrs = parse_attrs(st[p + 1:_find_paren_block(st, p) - 1])
            _apply_tag_attrs(tag, attrs)
        return tag
    m = re.match(r'^([A-Za-z_]\w*)\s*:\s*([A-Za-z_][\w:]*)\s*(\[[\d,\s]*\])?\s*', st)
    if not m:
        return None
    tag = Tag(name=m.group(1), data_type=m.group(2) + (m.group(3) or ''), scope=scope)
    rest = st[m.end():]
    if rest.startswith('('):
        end = _find_paren_block(rest, 0)
        _apply_tag_attrs(tag, parse_attrs(rest[1:end - 1]))
        rest = rest[end:].strip()
    if rest.startswith(':='):
        tag.value = parse_value(rest[2:])
    return tag


def _apply_tag_attrs(tag: Tag, attrs: Dict[str, str]):
    for k, v in attrs.items():
        if k == 'Description':
            tag.description = v
        elif k.startswith('COMMENT'):
            member = k[len('COMMENT'):]
            tag.comments[member] = v
        elif k == 'Class':
            tag.tag_class = v
        elif k == 'Producer':
            tag.usage, tag.producer = 'Consumed', v
        elif k == 'RemoteTag':
            tag.remote_tag = v
        elif k == 'Usage' and v in ('Produced', 'Consumed'):
            tag.usage = v
        elif k == 'ProduceCount' and not tag.usage:
            tag.usage = 'Produced'


def _parse_tags(L: _Lines, scope: str, end_kw='END_TAG') -> Dict[str, Tag]:
    tags = {}
    while not L.eof():
        s = L.peek()
        if s.startswith(end_kw):
            L.next()
            break
        st = L.statement()
        t = parse_tag_statement(st, scope)
        if t:
            tags[t.name] = t
    return tags


def _parse_routine(L: _Lines, header: str) -> Routine:
    kw, name, attrs = _head(header)
    kind = {'ROUTINE': 'RLL', 'FBD_ROUTINE': 'FBD', 'ST_ROUTINE': 'ST', 'SFC_ROUTINE': 'SFC'}.get(kw, 'RLL')
    r = Routine(name=name, kind=kind, description=attrs.get('Description', ''))
    end_kw = 'END_' + kw
    if kind != 'RLL':
        L.skip_to(end_kw)
        return r
    pending_comment = ''
    n = 0
    while not L.eof():
        s = L.peek()
        if s.startswith(end_kw):
            L.next()
            break
        st = L.statement()
        m = re.match(r'^(RC|N|I|D|R|IE|RR|E)\s*:\s*(.*)$', st, re.S)
        if not m:
            continue
        typ, body = m.group(1), m.group(2)
        if typ == 'RC':
            pending_comment = parse_string(body)
            continue
        r.rungs.append(Rung(number=n, text=' '.join(body.split()), comment=pending_comment, kind=typ))
        pending_comment = ''
        n += 1
    return r


def _parse_program(L: _Lines, header: str, project: Project) -> Program:
    _, name, attrs = _head(header)
    prog = Program(name=name, program_class=attrs.get('Class', 'Standard'),
                   main_routine=attrs.get('MAIN', ''), disabled=attrs.get('DisableFlag', '0') not in ('0', 'No'))
    while not L.eof():
        s = L.peek()
        if s.startswith('END_PROGRAM'):
            L.next()
            break
        if s == 'TAG' or s.startswith('TAG '):
            L.next()
            prog.tags.update(_parse_tags(L, name))
        elif re.match(r'^(ROUTINE|FBD_ROUTINE|ST_ROUTINE|SFC_ROUTINE)\b', s):
            r = _parse_routine(L, L.header())
            prog.routines[r.name] = r
        elif s.startswith('ENCODED_DATA'):
            h = L.header()
            a = _head(h)[2]
            rname = a.get('Name', '')
            if a.get('EncodedType', '').upper() == 'ROUTINE' and rname:
                prog.routines[rname] = Routine(name=rname, protected=True)
            _skip_encoded(L)
        elif s.startswith('CHILD_PROGRAMS'):
            L.skip_to('END_CHILD_PROGRAMS')
        elif s.startswith('PARAMETERS'):
            L.next()
            prog.tags.update(_parse_tags(L, name, 'END_PARAMETERS'))
        else:
            L.next()
    return prog


def _skip_encoded(L: _Lines):
    while not L.eof():
        s = L.peek()
        if s.startswith('END_ENCODED_DATA'):
            L.next()
            return
        if re.match(r'^(ROUTINE|END_PROGRAM|END_ADD_ON|PROGRAM|TAG\b|CHILD_PROGRAMS)', s):
            return
        L.next()


def _parse_aoi(L: _Lines, header: str) -> AOIDefinition:
    _, name, attrs = _head(header)
    aoi = AOIDefinition(name=name, aoi_class=attrs.get('Class', ''), description=attrs.get('Description', ''))
    while not L.eof():
        s = L.peek()
        if s.startswith('END_ADD_ON_INSTRUCTION_DEFINITION'):
            L.next()
            break
        if s.startswith('PARAMETERS'):
            L.next()
            while not L.eof() and not L.peek().startswith('END_PARAMETERS'):
                st = L.statement()
                m = re.match(r'^([A-Za-z_]\w*)\s*:\s*([\w:]+)', st)
                if not m:
                    continue
                p = st.find('(')
                a = parse_attrs(st[p + 1:_find_paren_block(st, p) - 1]) if p >= 0 else {}
                aoi.parameters.append(AOIParameter(name=m.group(1), data_type=m.group(2),
                                                   usage=a.get('Usage', 'Input'),
                                                   required=a.get('Required', 'No') == 'Yes'))
            L.next()
        elif s.startswith('LOCAL_TAGS'):
            L.next()
            aoi.local_tags = list(_parse_tags(L, name, 'END_LOCAL_TAGS').values())
        elif re.match(r'^(ROUTINE|FBD_ROUTINE|ST_ROUTINE|SFC_ROUTINE)\b', s):
            r = _parse_routine(L, L.header())
            if r.name == 'Logic':
                aoi.logic = r
        elif s.startswith('ENCODED_DATA'):
            aoi.protected = True
            L.header()
            _skip_encoded(L)
        else:
            L.next()
    return aoi


def _parse_module(L: _Lines, header: str) -> Module:
    _, name, a = _head(header)
    slot = a.get('Slot')
    mod = Module(name=name, parent=a.get('Parent', ''), catalog=a.get('CatalogNumber', ''),
                 slot=int(slot) if slot and slot.lstrip('-').isdigit() else None,
                 address=a.get('NodeAddress', ''), port_label=a.get('PortLabel', ''),
                 description=a.get('Description', ''),
                 safety_enabled=(a['SafetyEnabled'] == '1') if 'SafetyEnabled' in a else None,
                 inhibited=a.get('Inhibited', '0') in ('1', 'Yes'))
    while not L.eof():
        s = L.peek()
        if s.startswith('END_MODULE'):
            L.next()
            break
        if s.startswith('ExtendedProp'):
            line = L.next()
            while ']]]' not in line and not L.eof():
                line = L.next()
        elif s.startswith('CONNECTION'):
            mod.connections.append(_parse_connection(L, L.header(), mod))
        else:
            L.statement()
    return mod


def _parse_connection(L: _Lines, header: str, mod: Module) -> Connection:
    _, name, a = _head(header)
    kind = 'input' if ('InputTagSuffix' in a or 'input' in name.lower()) else \
        'output' if ('OutputTagSuffix' in a or 'output' in name.lower()) else ''
    rate = _num(a.get('Rate'))
    con = Connection(name=name, kind=kind, rpi_ms=rate / 1000.0 if rate is not None else None,
                     timeout_multiplier=_num(a.get('TimeoutMultiplier')),
                     network_delay_multiplier=_num(a.get('NetworkDelayMultiplier')),
                     reaction_time_limit_ms=_num(a.get('ReactionTimeLimit')),
                     tag_suffix=a.get('InputTagSuffix') or a.get('OutputTagSuffix') or '')
    while not L.eof():
        s = L.peek()
        if s.startswith('END_CONNECTION'):
            L.next()
            break
        st = L.statement()
        m = re.match(r'^(InputData|OutputData|InputTag|OutputTag)\s*(\()?', st)
        if not m:
            continue
        is_in = m.group(1).startswith('Input')
        attrs = {}
        if m.group(2):
            p = st.find('(')
            attrs = parse_attrs(st[p + 1:_find_paren_block(st, p) - 1])
        if attrs.get('Class') == 'Safety':
            con.safety = True
        suffix = (a.get('InputTagSuffix') if is_in else a.get('OutputTagSuffix')) or ('I' if is_in else 'O')
        for k, v in attrs.items():
            if k.startswith('COMMENT'):
                member = k[len('COMMENT'):].lstrip('.')
                mod.comments[f'{suffix.upper()}.{member.upper()}'] = v
                con.comments[member.upper()] = v
    if con.safety and not con.tag_suffix:
        con.tag_suffix = 'I' if kind == 'input' else 'O'
    return con


def parse_l5k(text: str, source_name: str = '') -> Project:
    """Parse the text of an L5K export into a :class:`Project`."""
    proj = Project(source_name=source_name, source_format='L5K')
    m = re.search(r'Version\s*:=\s*([^\n]+)', text[:2000])
    if m:
        proj.software_version = m.group(1).strip()
    body = strip_block_comments(text.replace('\r\n', '\n').replace('\r', '\n'))
    lines = [ln.strip() for ln in body.split('\n')]
    lines = [ln for ln in lines if ln]
    L = _Lines(lines)
    while not L.eof():
        s = L.peek()
        if s.startswith('CONTROLLER '):
            _, name, a = _head(L.header())
            proj.controller = name
            proj.processor = a.get('ProcessorType', '')
            proj.safety_level = a.get('SafetyLevel', '')
            if 'SafetyLocked' in a:
                proj.safety_locked = a['SafetyLocked'] in ('Yes', '1')
            proj.safety_tag_map = parse_safety_tag_map(a.get('SafetyTagMap', ''))
            if not proj.software_version and a.get('Major'):
                proj.software_version = f"v{a['Major']}"
        elif s.startswith('DATATYPE '):
            L.skip_to('END_DATATYPE')
        elif s.startswith('MODULE '):
            mod = _parse_module(L, L.header())
            proj.modules[mod.name] = mod
        elif s.startswith('ADD_ON_INSTRUCTION_DEFINITION '):
            aoi = _parse_aoi(L, L.header())
            proj.aois[aoi.name] = aoi
        elif s == 'TAG' or s.startswith('TAG '):
            L.next()
            proj.tags.update(_parse_tags(L, 'controller'))
        elif s.startswith('PROGRAM '):
            prog = _parse_program(L, L.header(), proj)
            proj.programs[prog.name] = prog
        elif s.startswith('TASK '):
            _, name, a = _head(L.header())
            task = Task(name=name, task_class=a.get('Class', 'Standard'), task_type=a.get('Type', ''),
                        rate_ms=_num(a.get('Rate')), watchdog_ms=_num(a.get('Watchdog')))
            while not L.eof() and not L.peek().startswith('END_TASK'):
                st = L.statement()
                if re.fullmatch(r'[A-Za-z_]\w*', st):
                    task.programs.append(st)
            L.next()
            proj.tasks[name] = task
        elif s.startswith(('TREND ', 'QUICK_WATCH', 'WATCH_LIST')):
            kw = s.split()[0]
            L.skip_to('END_' + kw)
        else:
            L.next()
    return proj


def parse_safety_tag_map(s: str) -> Dict[str, str]:
    """' Std1=Safe1, Std2=Safe2' -> {'Std1': 'Safe1', ...} (standard -> safety)."""
    out = {}
    for part in s.split(','):
        if '=' in part:
            a, b = part.split('=', 1)
            if a.strip() and b.strip():
                out[a.strip()] = b.strip()
    return out
