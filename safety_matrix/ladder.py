# =============================================================================
# Project : Safety Matrix Generator (GuardLogix SafetyTask -> Cause & Effect)
# File    : safety_matrix/ladder.py
# Author  : Robert Pietroń
# Revision: 1.0.0 (2026-10-18)
# Changes :
#   1.0.0 (2026-10-18) - First universal release: neutral-text tokenizer and a
#                        scan-order walker of the SafetyTask (JSR call tree,
#                        Add-On Instruction inlining, alias and program-scope
#                        resolution) producing tag definitions, safety
#                        instruction instances, timers and diagnostics.
# =============================================================================
"""Ladder (RLL) neutral text -> boolean model of the safety task."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, NamedTuple, Optional, Tuple

from . import instructions as INS
from .logic import AND, FALSE, NOT, OR, TRUE, VAR
from .model import Program, Project, split_operand


class Instr(NamedTuple):
    name: str
    args: List[str]


class Loc(NamedTuple):
    program: str
    routine: str
    rung: int
    aoi: str = ''           # 'AOIName(Instance)' when inside an inlined AOI

    def label(self, multi_program=False) -> str:
        r = f'{self.program}/{self.routine}' if multi_program else self.routine
        if self.aoi:
            r = f'{r} → {self.aoi}'
        return f'{r} R{self.rung}'


def split_args(s: str) -> List[str]:
    out, cur, depth, q = [], [], 0, None
    for c in s:
        if q:
            cur.append(c)
            if c == q:
                q = None
            continue
        if c in '"\'':
            q = c
        elif c in '([':
            depth += 1
        elif c in ')]':
            depth -= 1
        elif c == ',' and depth == 0:
            out.append(''.join(cur).strip())
            cur = []
            continue
        cur.append(c)
    if cur or out:
        out.append(''.join(cur).strip())
    return out


def tokenize(txt: str):
    toks, i, n = [], 0, len(txt)
    while i < n:
        c = txt[i]
        if c in ' \t\r\n':
            i += 1
        elif c in '[],':
            toks.append(c)
            i += 1
        else:
            m = re.match(r'([A-Za-z_][A-Za-z0-9_]*)\s*\(', txt[i:])
            if not m:
                raise ValueError(f'cannot parse rung text near: {txt[i:i + 40]!r}')
            j = i + m.end()
            depth, q = 1, None
            while j < n and depth:
                ch = txt[j]
                if q:
                    if ch == q:
                        q = None
                elif ch in '"\'':
                    q = ch
                elif ch == '(':
                    depth += 1
                elif ch == ')':
                    depth -= 1
                j += 1
            inner = txt[i + m.end():j - 1]
            toks.append(Instr(m.group(1), split_args(inner) if inner.strip() else []))
            i = j
    return toks


# ------------------------------------------------------------------ model records
@dataclass
class DeviceInstr:
    tag: str
    instr: str
    roles: Dict[str, str]
    loc: Loc
    heuristic: bool = False
    conditional: bool = False


@dataclass
class OutputInstr:
    tag: str
    instr: str
    roles: Dict[str, str]
    loc: Loc
    heuristic: bool = False


@dataclass
class MutingInstr:
    tag: str
    instr: str
    args: List[str]
    light_curtain: str
    loc: Loc


@dataclass
class TimerInfo:
    tag: str
    kind: str
    preset: Optional[float]
    preset_raw: str
    loc: Loc


@dataclass
class LadderModel:
    defs: Dict[str, list] = field(default_factory=dict)            # tag -> [(expr, loc, instr)]
    writes: Dict[str, List[Tuple[Loc, str]]] = field(default_factory=dict)
    reads: Dict[str, List[Loc]] = field(default_factory=dict)
    devices: Dict[str, DeviceInstr] = field(default_factory=dict)
    outputs: Dict[str, OutputInstr] = field(default_factory=dict)
    mutings: Dict[str, MutingInstr] = field(default_factory=dict)
    modes: Dict[str, Loc] = field(default_factory=dict)
    timers: Dict[str, TimerInfo] = field(default_factory=dict)
    flow: List[Tuple[Loc, str]] = field(default_factory=list)       # AFI, JMP, MCR ...
    unknown: List[Tuple[Loc, str]] = field(default_factory=list)    # unknown instructions
    comparisons: Dict[str, List[Loc]] = field(default_factory=dict)
    calls: List[Tuple[Loc, str, bool]] = field(default_factory=list)  # (loc, routine, conditional)
    executed: List[Tuple[str, str]] = field(default_factory=list)     # (program, routine) in scan order
    rungs: Dict[Loc, Tuple[str, str, list]] = field(default_factory=dict)  # loc -> (text, comment, tokens)
    aoi_calls: List[Tuple[Loc, str, str, bool]] = field(default_factory=list)  # (loc, aoi, instance, protected)
    aliases: Dict[str, str] = field(default_factory=dict)
    data_writes: Dict[str, List[Loc]] = field(default_factory=dict)
    multi_program: bool = False

    def first_def(self, tag):
        lst = self.defs.get(tag)
        return lst[-1] if lst else None


_KEYWORDS = {'MANUAL', 'AUTOMATIC', 'NEGATIVE', 'POSITIVE', 'ENABLE', 'DISABLE'}


class _Ctx(NamedTuple):
    program: Program
    routine: str
    rung: int
    subst: Dict[str, str]
    aoi: str
    depth: int


class LadderBuilder:
    """Walks the safety programs in scan order and builds a :class:`LadderModel`."""

    def __init__(self, project: Project, programs: Optional[List[Program]] = None):
        self.p = project
        self.programs = programs if programs is not None else project.safety_programs()
        self.m = LadderModel(multi_program=len(self.programs) > 1)
        names = {}
        for prog in self.programs:
            for t in prog.tags:
                names.setdefault(t, []).append(prog.name)
        self._ambiguous = {t for t, ps in names.items() if len(ps) > 1 or t in project.tags}

    # ----------------------------------------------------------------- name resolution
    def res(self, op: str, ctx: _Ctx) -> str:
        op = op.strip()
        if not op or INS.looks_literal(op) or op.startswith(("'", '"')):
            return op
        base, rest = split_operand(op)
        root = base.split(':')[0] if ':' in base else base
        if ctx.subst and root in ctx.subst:
            return ctx.subst[root] + base[len(root):] + rest
        for _ in range(8):                                   # alias chains
            tag = ctx.program.tags.get(base) or self.p.tags.get(base)
            if tag is None or not tag.alias_for:
                break
            self.m.aliases[base] = tag.alias_for
            b2, r2 = split_operand(tag.alias_for)
            base, rest = b2, r2 + rest
        if base in ctx.program.tags and base in self._ambiguous:
            return f'{ctx.program.name}\\{base}{rest}'
        return base + rest

    # ----------------------------------------------------------------- bookkeeping
    def _loc(self, ctx: _Ctx) -> Loc:
        return Loc(ctx.program.name, ctx.routine, ctx.rung, ctx.aoi)

    def _def(self, tag, expr, ctx, instr):
        self.m.defs.setdefault(tag, []).append((expr, self._loc(ctx), instr))
        self._write(tag, ctx, instr)

    def _write(self, tag, ctx, instr):
        self.m.writes.setdefault(tag, []).append((self._loc(ctx), instr))

    def _read(self, tag, ctx):
        if tag and not INS.looks_literal(tag) and tag not in _KEYWORDS:
            self.m.reads.setdefault(tag, []).append(self._loc(ctx))

    # ----------------------------------------------------------------- scan
    def build(self) -> LadderModel:
        for prog in self.programs:
            if prog.disabled:
                continue
            main = prog.main_routine or ('MainRoutine' if 'MainRoutine' in prog.routines else '')
            if main in prog.routines:
                self._run_routine(prog, main, [], '')
        return self.m

    def _run_routine(self, prog: Program, rname: str, stack: list, aoi_label: str):
        r = prog.routines.get(rname)
        if r is None or (prog.name, rname) in stack:
            return
        self.m.executed.append((prog.name, rname))
        if r.protected or r.kind != 'RLL':
            self.m.flow.append((Loc(prog.name, rname, -1), 'PROTECTED' if r.protected else r.kind))
            return
        stack = stack + [(prog.name, rname)]
        for rung in r.rungs:
            if rung.kind.upper() in ('I', 'IE', 'RR'):
                continue                                         # pending edits are not executed
            ctx = _Ctx(prog, rname, rung.number, {}, '', 0)
            toks = tokenize(rung.text)
            self.m.rungs[self._loc(ctx)] = (rung.text, rung.comment, self._resolved(toks, ctx))
            cond, pos = self._walk(toks, 0, TRUE, ctx, stack)
            if pos != len(toks):
                raise ValueError(f'unbalanced rung {rname} {rung.number}: {rung.text}')

    def _resolved(self, toks, ctx):
        out = []
        for t in toks:
            if isinstance(t, Instr):
                out.append(Instr(t.name, [self.res(a, ctx) for a in t.args]))
            else:
                out.append(t)
        return out

    def _walk(self, toks, pos, cond, ctx: _Ctx, stack):
        while pos < len(toks):
            t = toks[pos]
            if t == '[':
                pos += 1
                legs = []
                while True:
                    c2, pos = self._walk(toks, pos, cond, ctx, stack)
                    legs.append(c2)
                    if toks[pos] == ',':
                        pos += 1
                        continue
                    if toks[pos] == ']':
                        pos += 1
                        break
                cond = OR(*legs) if len(legs) > 1 else legs[0]
                continue
            if t in (',', ']'):
                return cond, pos
            cond = self._instr(t, cond, ctx, stack)
            pos += 1
        return cond, pos

    # ----------------------------------------------------------------- instructions
    def _instr(self, t: Instr, cond, ctx: _Ctx, stack):
        name = t.name.upper()
        R = lambda a: self.res(a, ctx)
        args = t.args
        loc = self._loc(ctx)
        if name == 'XIC':
            a = R(args[0]); self._read(a, ctx)
            return AND(cond, VAR(a))
        if name == 'XIO':
            a = R(args[0]); self._read(a, ctx)
            return AND(cond, NOT(VAR(a)))
        if name in INS.COMPARISONS:
            ra = [R(a) for a in args]
            for a in ra:
                self._read(a, ctx)
            text = f"{name}({','.join(ra)})"
            self.m.comparisons.setdefault(text, []).append(loc)
            return AND(cond, ('cmp', text))
        if name == 'ONS':
            a = R(args[0]); self._write(a, ctx, 'ONS')
            return ('edge', cond)
        if name == 'AFI':
            self.m.flow.append((loc, 'AFI'))
            return FALSE
        if name == 'OTE':
            self._def(R(args[0]), cond, ctx, 'OTE')
            return cond
        if name in ('OTL', 'OTU'):
            self._write(R(args[0]), ctx, name)
            return cond
        if name in INS.EDGE_OUTPUTS:
            self._write(R(args[0]), ctx, name)
            self._def(R(args[1]), ('edge', cond), ctx, name)
            return cond
        if name in INS.TIMERS:
            tag = R(args[0])
            pre_raw = args[1] if len(args) > 1 else ''
            try:
                pre = float(pre_raw)
            except ValueError:
                pre = None
            self.m.timers[tag] = TimerInfo(tag, name, pre, pre_raw, loc)
            self._def(tag + '.DN', ('timer', name, pre, cond, tag), ctx, name)
            self._def(tag + '.EN', cond, ctx, name)
            self._def(tag + '.TT', FALSE, ctx, name)
            return cond
        if name in INS.COUNTERS:
            tag = R(args[0])
            self.m.data_writes.setdefault(tag, []).append(loc)
            self._write(tag, ctx, name)
            return cond
        if name == 'JSR':
            target = args[0].strip() if args else ''
            self.m.calls.append((loc, target, cond != TRUE))
            self._run_routine(ctx.program, target, stack, ctx.aoi)
            return cond
        if name in INS.NO_EFFECT:
            return cond
        if name in INS.FLOW_CONTROL:
            self.m.flow.append((loc, name))
            return cond
        spec = INS.SAFETY_INSTRUCTIONS.get(name)
        if spec:
            return self._safety(spec, t, cond, ctx)
        aoi = self.p.aois.get(t.name) or next((a for n, a in self.p.aois.items() if n.upper() == name), None)
        if aoi:
            return self._aoi(aoi, t, cond, ctx, stack)
        if name in INS.DATA_DEST:
            idx = INS.DATA_DEST[name]
            for i, a in enumerate(args):
                ra = R(a)
                if idx is not None and i == idx:
                    self.m.data_writes.setdefault(ra, []).append(loc)
                    self._write(ra, ctx, name)
                else:
                    self._read(ra, ctx)
            return cond
        self.m.unknown.append((loc, t.name))
        for a in args:
            self._read(R(a), ctx)
        return cond

    def _safety(self, spec: INS.InstrSpec, t: Instr, cond, ctx: _Ctx):
        roles, heur = INS.map_operands(spec, t.args)
        config_roles = {'ResetType', 'FeedbackType', 'SafetyFunction', 'InputType', 'RestartType', 'ColdStartType',
                        'DiscrepancyTime', 'InputFilterTime', 'FeedbackReactionTime', 'ShortCircuitDetectDelayTime'}
        roles = {k: (v if k in config_roles else self.res(v, ctx)) for k, v in roles.items()}
        tag = self.res(t.args[0], ctx) if t.args else ''
        loc = self._loc(ctx)
        for k, v in roles.items():
            if k not in config_roles and v != tag:
                self._read(v, ctx)
        for a in t.args[1:]:
            ra = self.res(a, ctx)
            if ra not in roles.values():
                self._read(ra, ctx)
        if spec.role == 'device':
            self.m.devices[tag] = DeviceInstr(tag, spec.name, roles, loc, heur, cond != TRUE)
            expr = VAR('DEV:' + tag)
            mute = roles.get('MuteLightCurtain')
            if mute and mute not in ('0',):
                expr = TRUE if mute == '1' else OR(expr, VAR(mute))
            self._def(tag + '.O1', AND(cond, expr), ctx, spec.name)
            return cond
        if spec.role == 'output':
            self.m.outputs[tag] = OutputInstr(tag, spec.name, roles, loc, heur)
            enable = roles.get(spec.extra.get('enable', 'Enable'), '')
            en = VAR(enable) if enable and not INS.looks_literal(enable) else (TRUE if enable == '1' else FALSE)
            for o in ('.O1', '.O2'):
                self._def(tag + o, AND(cond, en), ctx, spec.name)
            return cond
        if spec.role == 'muting':
            ra = [self.res(a, ctx) for a in t.args]
            lc = next((a for a in ra[1:] if a.endswith('.O1')), '')
            self.m.mutings[tag] = MutingInstr(tag, spec.name, ra, lc, loc)
            expr = OR(VAR(lc), VAR('MUTE:' + tag)) if lc else VAR('MUTE:' + tag)
            self._def(tag + '.O1', AND(cond, expr), ctx, spec.name)
            return cond
        # mode selectors and others: outputs are data-dependent
        self.m.modes[tag] = loc
        self.m.data_writes.setdefault(tag, []).append(loc)
        self._write(tag, ctx, spec.name)
        return cond

    def _aoi(self, aoi, t: Instr, cond, ctx: _Ctx, stack):
        inst = self.res(t.args[0], ctx) if t.args else '?'
        loc = self._loc(ctx)
        self.m.aoi_calls.append((loc, aoi.name, inst, aoi.protected or aoi.logic is None))
        params = aoi.call_parameters()
        actual = dict(zip([p.name for p in params], [self.res(a, ctx) for a in t.args[1:]]))
        if aoi.protected or aoi.logic is None or ctx.depth > 8:
            for p in params:
                a = actual.get(p.name, '')
                if p.usage == 'Output' and a:
                    self.m.data_writes.setdefault(a, []).append(loc)
                    self._write(a, ctx, aoi.name)
                elif a:
                    self._read(a, ctx)
            return cond
        subst = {}
        for p in aoi.parameters:
            subst[p.name] = actual[p.name] if (p.usage == 'InOut' and p.name in actual) else f'{inst}.{p.name}'
        for lt in aoi.local_tags:
            subst[lt.name] = f'{inst}.{lt.name}'
        label = f'{aoi.name}({inst})'
        for p in params:
            a = actual.get(p.name, '')
            if p.usage == 'Input' and a:
                self._read(a, ctx)
                val = TRUE if a == '1' else FALSE if a == '0' else VAR(a)
                self._def(f'{inst}.{p.name}', val, ctx, aoi.name)
        self._def(f'{inst}.EnableIn', cond, ctx, aoi.name)
        for rung in aoi.logic.rungs:
            c2 = _Ctx(ctx.program, ctx.routine, ctx.rung, subst, (ctx.aoi + ' → ' if ctx.aoi else '') + f'{label} R{rung.number}',
                      ctx.depth + 1)
            toks = tokenize(rung.text)
            self._walk(toks, 0, TRUE, c2, stack)
        for p in params:
            a = actual.get(p.name, '')
            if p.usage == 'Output' and a and not INS.looks_literal(a):
                self._def(a, VAR(f'{inst}.{p.name}'), ctx, aoi.name)
        if cond != TRUE:
            self.m.flow.append((loc, f'AOI-COND:{aoi.name}'))
        return cond


def build_ladder(project: Project) -> LadderModel:
    return LadderBuilder(project).build()


# ------------------------------------------------------------------ condition formatting
def format_condition(tokens, self_tag: str, is_reset_like, is_status) -> str:
    """Human-readable permissive part of a rung: AND = ' · ', OR = '( a ∥ b )'.

    Branches containing the seal-in contact or a reset/edge signal are dropped (restart logic),
    as are diagnostic status bits."""
    items, _ = _fmt_seq(tokens, 0, self_tag, is_reset_like, is_status)
    return ' · '.join(i for i in items if i not in ('SELF', 'EDGE'))


def _fmt_seq(toks, pos, self_tag, is_reset_like, is_status):
    items = []
    while pos < len(toks):
        t = toks[pos]
        if t == '[':
            pos += 1
            legs = []
            while True:
                it, pos = _fmt_seq(toks, pos, self_tag, is_reset_like, is_status)
                legs.append(it)
                if toks[pos] == ',':
                    pos += 1
                    continue
                pos += 1
                break
            if any(x in ('SELF', 'EDGE') for leg in legs for x in leg):
                continue
            legs = [' · '.join(leg) for leg in legs if leg]
            if legs:
                items.append('(' + ' ∥ '.join(legs) + ')' if len(legs) > 1 else legs[0])
            continue
        if t in (',', ']'):
            return items, pos
        name, args = t
        if name.upper() in ('XIC', 'XIO') and args:
            v = args[0]
            if v == self_tag:
                items.append('SELF')
            elif is_reset_like(v):
                items.append('EDGE')
            elif is_status(v):
                pass
            else:
                items.append(('NOT ' if name.upper() == 'XIO' else '') + v)
        elif name.upper() in INS.COMPARISONS:
            items.append(f"{name}({','.join(args)})")
        pos += 1
    return items, pos


def seal_in_legs(tokens, self_tag: str) -> Optional[List[List[str]]]:
    """Legs of the OR branch that contains the seal-in contact XIC(self_tag); each leg = list of contact operands."""
    groups, stack = [], []
    for t in tokens:
        if t == '[':
            stack.append([[]])
        elif t == ',' and stack:
            stack[-1].append([])
        elif t == ']' and stack:
            g = stack.pop()
            groups.append(g)
            if stack:
                for leg in g:
                    stack[-1][-1].extend(leg)
        elif isinstance(t, Instr) and t.name.upper() in ('XIC', 'XIO') and t.args and stack:
            stack[-1][-1].append(t.args[0])
    for g in groups:
        if any(self_tag in leg for leg in g):
            return g
    return None
