# =============================================================================
# Project : Safety Matrix Generator (GuardLogix SafetyTask -> Cause & Effect)
# File    : safety_matrix/analysis.py
# Author  : Robert Pietroń
# Revision: 1.1.0 (2026-10-21)
# Changes :
#   1.0.0 (2026-10-18) - First universal release (method of PortalSaw matrix
#                        rev 1.0-1.4 generalised): automatic detection of
#                        causes (safety input instructions, direct safety inputs,
#                        consumed safety signals) and effects (ROUT/CROUT
#                        outputs, plain safety outputs, CIP Safety drive
#                        STO/SS1), deterministic cell codes X/X1/XB/XC/XM/N and
#                        S/SB/SC/SM, rung paths, stop category from off-delay
#                        timers, reset sources incl. trace into standard code,
#                        CIP Safety reaction-time data.
#   1.1.0 (2026-10-21) - Channels copied from inputs followed to the physical
#                        channel (module, CRTL, checks); scan-order lag per cell;
#                        constant-contact bypass -> code N; ROUT/CROUT outputs
#                        grouped also through plain copies; search of writes in
#                        standard code extended (AOI Output/InOut, data instr.,
#                        JSR/SBR, unknown instr., aliases, ST/FBD/SFC, consumed).
# =============================================================================
"""Cause & effect analysis of a GuardLogix safety task."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from . import instructions as INS
from .ladder import Instr, LadderModel, Loc, build_ladder, format_condition, seal_in_legs, split_args, tokenize
from .logic import Evaluator, vars_in
from .model import Module, Project, Tag, io_parts, split_operand

STO_RE = re.compile(r'^(SafeTorqueOff|STO\w*|SS1\w*|SafeStop\w*|SBC\w*|SafeBrake\w*|SLS\w*Request)$', re.I)
FAULT_FALSE_RE = re.compile(r'(ConnectionFaulted|SafetyFault|\.FP|Fault\w*|Faulted|ResetRequired|TorqueDisabled|'
                            r'Muting\d*Status|\.Ready)$', re.I)
STATUS_TRUE_RE = re.compile(r'(CombinedInputStatus|CombinedOutputStatus|Pt\d+InputStatus|Pt\d+OutputStatus|'
                            r'InputStatus|OutputStatus|ConnectionStatus|SafetyOutputEnabled)$', re.I)
RESET_NAME_RE = re.compile(r'reset|rst|quit|ack|kvitt', re.I)

MATRIX_CODES = ['X', 'X1', 'XB', 'XC', 'XM', 'N', 'S', 'SB', 'SC', 'SM']
INFO_MAP = {'X': 'S', 'XB': 'SB', 'XC': 'SC', 'XM': 'SM'}


@dataclass
class Device:
    tag: str
    instr: str
    type: str
    loc: Optional[Loc]
    roles: Dict[str, str] = field(default_factory=dict)
    heuristic: bool = False
    conditional: bool = False
    kind: str = 'instr'             # 'instr' | 'direct' | 'external'
    ch_a: str = ''
    ch_b: str = ''
    reset: str = ''
    reset_manual: Optional[bool] = None
    filter_ms: Optional[float] = None
    mute: str = ''
    const_channels: bool = False
    equal_channels: bool = False
    std_channels: bool = False
    # channels behind intermediate copies (XIC(input) OTE(copy)): final source operand and the copy chain
    src_a: str = ''
    src_b: str = ''
    copies: List[Tuple[str, str, Optional[Loc]]] = field(default_factory=list)   # (channel role, copy tag, rung)
    channel_lag: int = 0            # copies executed after the instruction in the scan (previous-scan values)
    computed: List[str] = field(default_factory=list)                         # channels computed by logic
    # filled later
    zone: str = ''
    id: str = ''
    n_eff: int = 0

    @property
    def phys_a(self) -> str:
        return self.src_a or self.ch_a

    @property
    def phys_b(self) -> str:
        return self.src_b or self.ch_b


@dataclass
class Effect:
    key: str                        # unique id (ROUT/CROUT tag, output tag, CIP tag, info tag)
    kind: str                       # ROUT, CROUT, OUT, STO, SS1, SBC, SLS, INFO
    var: str                        # tag evaluated for the effect
    outputs: List[str]
    loc: Optional[Loc]
    instr: str = ''                 # ROUT/CROUT tag driving the outputs
    module: str = ''
    info: bool = False
    energized: bool = False
    baseline: Dict[str, bool] = field(default_factory=dict)
    in_matrix: bool = False
    reason: str = ''                # why not in the matrix
    group: str = ''


@dataclass
class Cell:
    code: str
    raw: str
    path: List[Tuple[str, Optional[Loc]]]
    bypass: List[str] = field(default_factory=list)
    conditions: List[str] = field(default_factory=list)
    partners: List[str] = field(default_factory=list)
    delay_ms: Optional[float] = None
    lag: int = 0                    # SafetyTask scans of delay caused by the scan order (read before write)


@dataclass
class Options:
    info_effects: List[str] = field(default_factory=list)
    include_effects: List[str] = field(default_factory=list)
    exclude_effects: List[str] = field(default_factory=list)
    device_types: Dict[str, str] = field(default_factory=dict)
    direct_inputs: bool = True


class Analysis:
    def __init__(self, project: Project, options: Optional[Options] = None):
        self.p = project
        self.o = options or Options()
        self.lm: LadderModel = build_ladder(project)
        self.task = project.safety_task
        self.std_map = project.safety_tag_map
        self.std_dests = set(self.std_map.values())
        self.std_src_of = {v: k for k, v in self.std_map.items()}
        self._tag_cache: Dict[str, Optional[Tag]] = {}
        self.promoted: Dict[str, str] = {}          # leaf name -> 'direct' / 'external'
        self.init_consts: Dict[str, bool] = {}      # leaves constant only through the tag's initial value
        self.lags: Dict[Tuple[str, Loc], Dict[str, object]] = {}   # (tag, rung writing it) -> earlier readers/effects
        self.ev = Evaluator(self.lm.defs, self._leaf)
        # same logic, but initial-value constants are free leaves (to find bypasses by constant contacts)
        self.ev_nc = Evaluator(self.lm.defs, self._leaf_nc)
        self.devices: Dict[str, Device] = {}
        self.effects: List[Effect] = []
        self.cells: Dict[Tuple[str, str], Cell] = {}
        self.std_bits: List[str] = []
        self.notes: List[str] = []
        self._std_index = None
        self._run()

    # ================================================================= tag helpers
    def find_tag(self, name: str) -> Optional[Tag]:
        """Tag object (program scope first) for an operand root."""
        if name in self._tag_cache:
            return self._tag_cache[name]
        base = split_operand(name)[0]
        prog = None
        if '\\' in base:
            prog, base = base.split('\\', 1)
        t = None
        for pg in self.p.safety_programs():
            if prog and pg.name != prog:
                continue
            if base in pg.tags:
                t = pg.tags[base]
                break
        if t is None:
            t = self.p.tags.get(base)
        self._tag_cache[name] = t
        return t

    def is_std(self, name: str) -> bool:
        base = split_operand(name)[0]
        return base in self.std_dests

    def _leaf(self, name: str):
        if name.startswith('DEV:'):
            return 'dev', name[4:]
        if name in self.promoted:
            return 'dev', name
        if name.startswith('MUTE:'):
            return 'free', 'mute'
        if re.match(r'^[A-Z]{2,4}\(', name):          # comparison text
            return 'free', 'cmp'
        if self.is_std(name):
            return 'free', 'std'
        if FAULT_FALSE_RE.search(name):
            return 'const', False
        if STATUS_TRUE_RE.search(name):
            return 'const', True
        io = io_parts(name)
        if io and io[1] in ('I', 'SI'):
            return 'free', 'input'
        if name in self.lm.data_writes or split_operand(name)[0] in self.lm.data_writes:
            return 'free', 'data'
        if name in self.lm.writes:
            kinds = {w for _, w in self.lm.writes[name]}
            return 'free', 'latch' if kinds & {'OTL', 'OTU'} else 'data'
        t = self.find_tag(name)
        if t is not None:
            if t.usage == 'Consumed':
                return 'free', 'ext'
            base, member = split_operand(name)
            base = base.split('\\')[-1]
            v = t.bit_value(member)
            if v is not None:
                self.init_consts[name] = v
                return 'const', v
        return 'free', 'unk'

    def _leaf_nc(self, name: str):
        k, v = self.ev.leaf_info(name)
        if k == 'const' and name in self.init_consts:
            return 'free', 'init'
        return k, v

    def leaf_class(self, name: str) -> str:
        k, v = self.ev.leaf_info(name)
        return v if k == 'free' else k

    # ================================================================= main
    def _run(self):
        self._collect_devices()
        self._collect_effects()
        self._baselines()
        if self.o.direct_inputs:
            self._promote_direct_inputs()
        self._cells()
        self._finish()

    def _collect_devices(self):
        for tag, d in self.lm.devices.items():
            spec = INS.SAFETY_INSTRUCTIONS.get(d.instr)
            roles = d.roles
            ch_a, ch_b = roles.get(spec.channels[0], ''), roles.get(spec.channels[1], '')
            dev = Device(tag=tag, instr=d.instr, type=self.o.device_types.get(tag) or INS.classify_device(d.instr, tag, roles),
                         loc=d.loc, roles=roles, heuristic=d.heuristic or not spec.verified and len(spec.operands) <= 1,
                         conditional=d.conditional, ch_a=ch_a, ch_b=ch_b, reset=roles.get(spec.reset, '') if spec.reset else '',
                         reset_manual=INS.reset_is_manual(spec, roles), mute=roles.get('MuteLightCurtain', ''))
            if d.instr == 'LC':
                try:
                    dev.filter_ms = float(roles.get('InputFilterTime', ''))
                except ValueError:
                    dev.filter_ms = None
            if dev.mute in ('0',):
                dev.mute = ''
            self._resolve_channels(dev)
            srcs = [c for c in (dev.phys_a, dev.phys_b) if c]
            dev.const_channels = bool(ch_a) and all(self._is_constant(c) for c in srcs)
            dev.equal_channels = bool(ch_a) and dev.phys_a == dev.phys_b and not dev.const_channels
            dev.std_channels = any(self.is_std(c) for c in srcs)
            self.devices[tag] = dev

    def copy_source(self, op: str) -> Tuple[str, List[Tuple[str, Loc]]]:
        """Follow plain copies 'XIC(a) OTE(b)' (single writer, single OTE) back to the source operand.

        Returns (source operand, [(copy tag, rung of the copy), ...]) - the operand itself if it is not a copy."""
        chain: List[Tuple[str, Loc]] = []
        cur = op
        for _ in range(8):
            if not cur or io_parts(cur) or INS.looks_literal(cur):
                break
            lst = self.lm.defs.get(cur)
            if not lst or len(lst) != 1 or len(self.lm.writes.get(cur, [])) != 1:
                break
            expr, loc, instr = lst[0]
            if instr != 'OTE' or expr[0] != 'var' or loc.aoi:
                break
            chain.append((cur, loc))
            cur = expr[1]
        return cur, chain

    def _resolve_channels(self, dev: Device):
        """Channels that are intermediate copies of inputs: source operand, copy rungs and scan-order lag."""
        for role, ch in (('A', dev.ch_a), ('B', dev.ch_b)):
            if not ch or INS.looks_literal(ch):
                continue
            src, chain = self.copy_source(ch)
            lag, reader = 0, dev.loc
            for tag, loc in chain:
                dev.copies.append((role, tag, loc))
                if self.lm.order(loc) > self.lm.order(reader):
                    lag += 1
                reader = loc
            dev.channel_lag = max(dev.channel_lag, lag)
            if chain:
                if role == 'A':
                    dev.src_a = src
                else:
                    dev.src_b = src
            if src in self.lm.defs and not io_parts(src) and src not in dev.computed:
                dev.computed.append(src)

    def _is_constant(self, op: str) -> bool:
        if INS.looks_literal(op):
            return True
        if op in self.lm.defs:
            return False
        return self.ev.leaf_info(op)[0] == 'const'

    def _collect_effects(self):
        info = set(self.o.info_effects)
        excl = set(self.o.exclude_effects)
        seen = set()
        order = []
        for tag, lst in self.lm.defs.items():
            order.append((lst[-1][1], tag))
        # scan order of definitions
        rank = {loc: i for i, loc in enumerate(self.lm.rungs)}
        order.sort(key=lambda x: (rank.get(Loc(x[0].program, x[0].routine, x[0].rung), 10 ** 9), x[1]))
        for loc, tag in order:
            if tag in excl or tag in seen:
                continue
            io = io_parts(tag)
            if tag in info or tag in self.o.include_effects:
                self.effects.append(Effect(key=tag, kind='INFO' if tag in info else 'OUT', var=tag, outputs=[tag],
                                           loc=loc, info=tag in info, module=io[0] if io else ''))
                seen.add(tag)
                continue
            if not io:
                continue
            prefix, kind, member = io
            if kind == 'O':
                expr = self.ev.expr_of(tag)
                srcs = [self.copy_source(v)[0] for v in vars_in(expr)]       # ROUT.O1 also through plain copies
                drv = [v.rsplit('.', 1)[0] for v in srcs if v.rsplit('.', 1)[0] in self.lm.outputs
                       and v.endswith(('.O1', '.O2'))]
                if drv:
                    r = drv[0]
                    ex = next((e for e in self.effects if e.key == r), None)
                    if ex:
                        ex.outputs.append(tag)
                    else:
                        oi = self.lm.outputs[r]
                        self.effects.append(Effect(key=r, kind=oi.instr, var=tag, outputs=[tag], loc=oi.loc,
                                                   instr=r, module=prefix))
                else:
                    self.effects.append(Effect(key=tag, kind='OUT', var=tag, outputs=[tag], loc=loc, module=prefix))
                seen.add(tag)
            elif kind == 'SO' and STO_RE.match(member):
                k = 'STO' if re.match(r'(SafeTorqueOff|STO)', member, re.I) else re.match(r'(SS1|SBC|SLS|SafeStop|SafeBrake)', member, re.I).group(1).upper()
                k = {'SAFESTOP': 'SS1', 'SAFEBRAKE': 'SBC'}.get(k, k)
                self.effects.append(Effect(key=tag, kind=k, var=tag, outputs=[tag], loc=loc, module=prefix))
                seen.add(tag)

    def _baseline(self, var: str) -> Tuple[bool, Dict[str, bool]]:
        _, free = self.ev.cone(var)
        if self.ev.value(var):
            return True, {}
        cur = {f: True for f in free}
        if not self.ev.value(var, free=cur):
            return False, {}
        for f in sorted(free, key=lambda x: (self.leaf_class(x) != 'std', x)):
            cur[f] = False
            if not self.ev.value(var, free=cur):
                cur[f] = True
        return True, {k: v for k, v in cur.items() if v}

    def _baselines(self):
        for e in self.effects:
            e.energized, e.baseline = self._baseline(e.var)

    def _promote_direct_inputs(self):
        """Safety inputs / consumed safety tags that must be 1 for an output to be ON become causes."""
        new = {}
        for e in self.effects:
            if not e.energized:
                continue
            for leaf, v in e.baseline.items():
                cls = self.leaf_class(leaf)
                if cls not in ('input', 'ext') or not v:
                    continue
                b2 = dict(e.baseline)
                b2[leaf] = False
                if not self.ev.value(e.var, free=b2):
                    new[leaf] = 'direct' if cls == 'input' else 'external'
        if not new:
            return
        self.promoted.update(new)
        self.ev = Evaluator(self.lm.defs, self._leaf)
        self.ev_nc = Evaluator(self.lm.defs, self._leaf_nc)
        for leaf, kind in new.items():
            self.devices[leaf] = Device(tag=leaf, instr='—', loc=self._first_read(leaf), kind=kind,
                                        type='DIRECT SAFETY INPUT' if kind == 'direct' else 'EXTERNAL SAFETY SIGNAL',
                                        ch_a=leaf, ch_b=leaf, equal_channels=kind == 'direct')
        for e in self.effects:
            e.baseline = {k: v for k, v in e.baseline.items() if k not in new}
            e.energized = self.ev.value(e.var, free=e.baseline) if e.energized else e.energized

    def _first_read(self, tag) -> Optional[Loc]:
        lst = self.lm.reads.get(tag)
        return lst[0] if lst else None

    # ================================================================= cells
    def _cells(self):
        for e in self.effects:
            if not e.energized:
                e.reason = 'not_energized'
                continue
            devs, free = self.ev.cone(e.var)
            B = e.baseline
            std_free = [f for f in free if self.leaf_class(f) == 'std']
            other_free = [f for f in free if self.leaf_class(f) != 'std']
            for D in self.devices:
                if D not in devs:
                    continue
                v0 = self.ev.value(e.var, dev_off=[D], free=B)
                cell = None
                if not v0:
                    all_std = dict(B, **{s: True for s in std_free})
                    byp = [s for s in sorted(std_free) if self.ev.value(e.var, dev_off=[D], free=dict(B, **{s: not B.get(s, False)}))]
                    if byp or (std_free and self.ev.value(e.var, dev_off=[D], free=all_std)):
                        cell = Cell('XB', 'XB', [], bypass=byp or sorted(std_free))
                    else:
                        cond = [f for f in sorted(other_free)
                                if self.ev.value(e.var, dev_off=[D], free=dict(B, **{f: not B.get(f, False)}))]
                        cell = Cell('XM', 'XM', [], conditions=cond) if cond else Cell('X', 'X', [])
                else:
                    partners = [P for P in devs if P != D and self.ev.value(e.var, dev_off=[P], free=B)
                                and not self.ev.value(e.var, dev_off=[D, P], free=B)]
                    if partners:
                        cell = Cell('XC', 'XC', [], partners=sorted(partners, key=list(self.devices).index))
                    else:
                        consts = self._const_bypass(e.var, D, B)
                        if consts:                      # bridged by a constant contact -> never trips
                            cell = Cell('N', 'N', [], bypass=consts)
                if cell:
                    tags = self.ev.find_path(e.var, D) or self.ev_nc.find_path(e.var, D) or []
                    path = [(t, self._def_loc(t)) for t in reversed(tags)]
                    dev = self.devices[D]
                    if dev.kind == 'instr':
                        path = [(D + '.O1', dev.loc)] + [x for x in path if x[0] != D + '.O1']
                    cell.path = path
                    cell.delay_ms = self._path_delay(tags)
                    cell.lag = self._path_lag(tags, e.key) + dev.channel_lag
                    cell.code = self._post_code(dev, e, cell.raw)
                    self.cells[(D, e.key)] = cell

    def _const_bypass(self, var: str, dev: str, base: Dict[str, bool]) -> List[str]:
        """Constant contacts (tag initial value 1, never written) without which `dev` would switch `var` off."""
        consts = {f: self.init_consts[f] for f in self.ev_nc.cone(var)[1] if f in self.init_consts}
        if not any(consts.values()):
            return []
        cur = dict(base, **consts)
        out = []
        for c, v in consts.items():
            if not v:
                continue
            f2 = dict(cur, **{c: False})
            if self.ev_nc.value(var, free=f2) and not self.ev_nc.value(var, dev_off=[dev], free=f2):
                out.append(c)
        return sorted(out)

    def _path_lag(self, tags: List[str], effect: str) -> int:
        """Links of a path whose producing rung executes after the consuming rung (value of the previous scan)."""
        lag = 0
        for consumer, producer in zip(tags, tags[1:]):
            lc, lp = self._def_loc(consumer), self._def_loc(producer)
            if lc is None or lp is None:
                continue
            if self.lm.order(lp) > self.lm.order(lc):
                lag += 1
                g = self.lags.setdefault((producer, Loc(lp.program, lp.routine, lp.rung)), {'readers': [], 'effects': []})
                rl = Loc(lc.program, lc.routine, lc.rung)
                if rl not in g['readers']:
                    g['readers'].append(rl)
                if effect not in g['effects']:
                    g['effects'].append(effect)
        return lag

    def _post_code(self, dev: Device, e: Effect, code: str) -> str:
        if dev.const_channels:
            code = 'N'
        elif dev.equal_channels and code == 'X':
            code = 'X1'
        if e.info:
            code = INFO_MAP.get(code, code)
        return code

    def _def_loc(self, tag) -> Optional[Loc]:
        d = self.lm.first_def(tag)
        return d[1] if d else None

    def _path_delay(self, tags) -> Optional[float]:
        total, any_ = 0.0, False
        for t in tags:
            d = self.lm.first_def(t)
            if d and d[0][0] == 'timer' and d[0][1] in INS.OFF_DELAY_TIMERS:
                any_ = True
                total += d[0][2] or 0.0
        return total if any_ else None

    def _finish(self):
        for e in self.effects:
            if e.energized and not e.reason:
                hits = [d for d in self.devices if (d, e.key) in self.cells]
                if hits or e.key in self.o.include_effects or e.info:
                    e.in_matrix = True
                else:
                    e.reason = 'no_device'
        for d in self.devices.values():
            d.n_eff = sum(1 for e in self.matrix_effects(safety_only=True)
                          if (d.tag, e.key) in self.cells and self.cells[(d.tag, e.key)].code not in ('N',))
        self.std_bits = sorted({t for t in self.lm.reads if self.is_std(t)})

    # ================================================================= queries
    def matrix_effects(self, safety_only=False) -> List[Effect]:
        return [e for e in self.effects if e.in_matrix and not (safety_only and e.info)]

    def code(self, dev: str, eff: str) -> Optional[str]:
        c = self.cells.get((dev, eff))
        return c.code if c else None

    def effect(self, key) -> Optional[Effect]:
        return next((e for e in self.effects if e.key == key), None)

    def rung(self, loc: Loc):
        return self.lm.rungs.get(Loc(loc.program, loc.routine, loc.rung))

    def loc_label(self, loc: Optional[Loc]) -> str:
        if loc is None:
            return '—'
        return loc.label(self.lm.multi_program)

    # ----------------------------------------------------------------- descriptions
    def module_of(self, operand: str) -> Optional[Module]:
        io = io_parts(operand)
        if not io:
            return None
        return self.p.module_by_prefix(io[0])

    def io_comment(self, operand: str) -> str:
        io = io_parts(operand)
        if not io:
            return ''
        m = self.p.module_by_prefix(io[0])
        if not m:
            return ''
        return m.channel_comment(io[1], io[2].split('.')[0]).strip()

    def describe(self, operand: str) -> str:
        """Best available comment for an operand (tag member comment, description, I/O comment)."""
        operand = operand.split('\\')[-1]
        c = self.io_comment(operand)
        if c:
            return c
        base, member = split_operand(operand)
        t = self.find_tag(operand) or self.p.tags.get(base)
        if t is None:
            for pg in self.p.programs.values():
                if base in pg.tags:
                    t = pg.tags[base]
                    break
        if t is None:
            return ''
        if member and member in t.comments:
            return t.comments[member].strip()
        if member.upper() in {k.upper(): k for k in t.comments}:
            return t.comments[{k.upper(): k for k in t.comments}[member.upper()]].strip()
        if t.alias_for:
            c = self.io_comment(t.alias_for)
            if c:
                return c
        return (t.description or '').strip()

    def rung_comment(self, loc: Optional[Loc]) -> str:
        if not loc:
            return ''
        r = self.rung(loc)
        return (r[1] if r else '').strip()

    # ----------------------------------------------------------------- resets
    def is_reset_like(self, tag: str) -> bool:
        """Edge pulse or reset/acknowledge signal (used to hide restart branches in permissive text)."""
        d = self.lm.first_def(tag)
        if d and d[0][0] == 'edge':
            return True
        if tag in self._reset_tags():
            return True
        return bool(RESET_NAME_RE.search(tag.split('.')[-1] if '.' in tag and not io_parts(tag) else tag))

    def _reset_tags(self):
        if not hasattr(self, '_rt'):
            self._rt = {d.reset for d in self.devices.values() if d.reset}
            self._rt |= {o.roles.get(INS.SAFETY_INSTRUCTIONS[o.instr].reset, '') for o in self.lm.outputs.values()}
        return self._rt

    def is_status(self, tag: str) -> bool:
        k, v = self.ev.leaf_info(tag)
        return (k == 'const') or bool(FAULT_FALSE_RE.search(tag) or STATUS_TRUE_RE.search(tag))

    def reset_sources(self, tag: str) -> Tuple[List[str], List[Loc]]:
        """Contacts in the rungs writing a reset tag (physical / logical sources)."""
        out, locs = [], []
        if not tag or INS.looks_literal(tag):
            return out, locs
        for loc, ins in self.lm.writes.get(tag, []):
            if loc in locs:
                continue
            locs.append(loc)
            r = self.rung(loc)
            if not r:
                continue
            for t in r[2]:
                if isinstance(t, Instr) and t.name.upper() in ('XIC', 'XIO') and t.args:
                    a = t.args[0]
                    if a not in out and a != tag:
                        out.append(a)
        return out, locs

    def source_kind(self, op: str) -> str:
        """std / input / const / edge / safety for a reset source operand."""
        if self.is_std(op):
            return 'std'
        io = io_parts(op)
        if io and io[1] in ('I', 'SI'):
            return 'input'
        k, v = self.ev.leaf_info(op)
        if k == 'const' and op not in self.lm.defs:
            return 'const1' if v else 'const0'
        if op not in self.lm.writes and op not in self.lm.defs:
            return 'never'
        return 'safety'

    # ----------------------------------------------------------------- standard-code trace
    def std_source(self, op: str) -> str:
        """Standard tag mapped onto a safety tag: 'ToSafty[0].3' -> 'ProgramToSafety[0].3'."""
        base, rest = split_operand(op)
        src = self.std_src_of.get(base)
        return src + rest if src else ''

    def std_writers(self, std_tag: str) -> List[Tuple[str, str, Optional[int], str, List[str]]]:
        """Places in the standard code that write `std_tag` (or the whole tag / structure containing it):
        (program, routine, rung or None, instruction, contacts of the rung)."""
        if self._std_index is None:
            self._std_index = self._build_std_index()
        base, rest = split_operand(std_tag.strip())
        out = []
        for wrest, entry in self._std_index.get(base, []):
            if (wrest == rest or not wrest or not rest or rest.startswith(wrest + '.') or rest.startswith(wrest + '[')) \
                    and entry not in out:
                out.append(entry)
        t = self.p.tags.get(base)
        if t is not None and t.usage == 'Consumed':
            out.append(('—', t.producer or 'producer', None, 'CONSUMED', []))
        return out

    def _build_std_index(self) -> Dict[str, list]:
        """Writes in standard programs: OTE/OTL/OTU, OSR/OSF, data instructions, timers/counters, AOI Output/InOut
        parameters, JSR return / SBR parameters, unknown instructions (conservatively), ST assignments and calls,
        FBD output references.  Aliases are resolved; program-scope tags hiding a controller tag are skipped."""
        idx: Dict[str, list] = {}
        aois = {n.upper(): a for n, a in self.p.aois.items()}
        known_read = INS.CONDITIONS | INS.COMPARISONS | INS.NO_EFFECT | INS.FLOW_CONTROL | {'JSR', 'ONS'}

        def add(prog, op, entry):
            op = (op or '').strip()
            if not op or INS.looks_literal(op) or op.startswith(("'", '"')) or op == '?':
                return
            m = re.match(r'^([A-Za-z_][\w\.\[\]:]*)', op)
            if not m:
                return
            b, rest = split_operand(m.group(1))
            if '\\' in b:
                return
            for _ in range(8):                         # aliases; program tags hide controller tags
                pt = prog.tags.get(b)
                if pt is not None:
                    if not pt.alias_for:
                        return
                    a = pt.alias_for
                else:
                    ct = self.p.tags.get(b)
                    if ct is None or not ct.alias_for:
                        break
                    a = ct.alias_for
                b2, r2 = split_operand(a)
                b, rest = b2, r2 + rest
            idx.setdefault(b, []).append((rest, entry))

        def call_writes(name, args):
            """Operands written by an instruction / AOI call with the given (unresolved) arguments."""
            up = name.upper()
            aoi = aois.get(up)
            if aoi is not None:
                outs = args[:1]                       # the instance (its members are written)
                for p, a in zip(aoi.call_parameters(), args[1:]):
                    if p.usage in ('Output', 'InOut'):
                        outs.append(a)
                return outs
            if up in ('OTE', 'OTL', 'OTU'):
                return args[:1]
            if up in INS.EDGE_OUTPUTS:
                return args[1:2]
            if up in INS.TIMERS or up in INS.COUNTERS:
                return args[:1]
            if up in INS.DATA_DEST:
                i = INS.DATA_DEST[up]
                return [args[i]] if i is not None and i < len(args) else []
            if up == 'JSR':
                try:
                    return args[2 + int(args[1]):]
                except (ValueError, IndexError):
                    return []
            if up == 'SBR':
                return list(args)
            if up in known_read or up in INS.SAFETY_INSTRUCTIONS:
                return []
            return list(args)                         # unknown instruction: may write any operand

        for prog in self.p.standard_programs():
            for r in prog.routines.values():
                for rung in r.rungs:
                    try:
                        toks = tokenize(rung.text)
                    except ValueError:
                        continue
                    contacts = [t.args[0] for t in toks if isinstance(t, Instr) and t.name.upper() in ('XIC', 'XIO') and t.args]
                    for t in toks:
                        if isinstance(t, Instr):
                            for a in call_writes(t.name, t.args):
                                add(prog, a, (prog.name, r.name, rung.number, t.name.upper(), contacts))
                lang = r.kind if r.kind in ('ST', 'FBD', 'SFC') else 'ST'
                for line in r.source:
                    if line.startswith('W:'):
                        add(prog, line[2:], (prog.name, r.name, None, lang, []))
                        continue
                    code = re.sub(r'"[^"]*"|\'[^\']*\'', '', line[3:]).split('//')[0]
                    for mm in re.finditer(r'([A-Za-z_][\w\.\[\]:]*)\s*:=', code):
                        add(prog, mm.group(1), (prog.name, r.name, None, lang, []))
                    mm = re.match(r'^\s*([A-Za-z_]\w*)\s*\((.*)\)\s*;?\s*$', code)
                    if mm and mm.group(1).upper() not in ('IF', 'ELSIF', 'WHILE', 'CASE', 'FOR', 'REPEAT', 'UNTIL'):
                        for a in call_writes(mm.group(1), split_args(mm.group(2))):
                            add(prog, a, (prog.name, r.name, None, lang, []))
        return idx

    def std_trace(self, bit: str, max_writers: int = 3) -> str:
        """'ToSafty[0].10' -> "ProgramToSafety[0].10 'comment' ← MainProgram/A42 R5 OTE: a 'c', b"."""
        src = self.std_source(bit)
        if not src:
            return ''
        txt = src
        d = self.describe(src)
        if d:
            txt += f" '{' '.join(d.split())}'"
        ws = self.std_writers(src)
        if ws:
            parts = []
            for prog, rout, n, ins, contacts in ws[:max_writers]:
                cs = ', '.join(c + (f" '{' '.join(self.describe(c).split())}'" if self.describe(c) else '') for c in contacts[:4])
                where = f'{prog}/{rout}' + (f' R{n}' if n is not None else '')
                parts.append(f'{where} {ins}' + (f': {cs}' if cs else ''))
            txt += ' ← ' + '; '.join(parts)
        return txt

    # ----------------------------------------------------------------- reaction time
    def input_connection(self, dev: Device):
        m = self.module_of(dev.phys_a) if dev.phys_a else None
        if not m:
            return None, None
        return m, m.connection('input')

    def max_lag(self, dev: str) -> int:
        """Largest scan-order lag (in SafetyTask periods) over the cells of a device."""
        return max((c.lag for (d, _), c in self.cells.items() if d == dev), default=self.devices[dev].channel_lag)

    def output_connection(self, e: Effect):
        op = e.outputs[0] if e.outputs else e.var
        m = self.module_of(op)
        if not m:
            return None, None
        return m, m.connection('output')

    @property
    def task_period(self) -> Optional[float]:
        return self.task.rate_ms if self.task else None

    @property
    def task_watchdog(self) -> Optional[float]:
        return self.task.watchdog_ms if self.task else None

    # ----------------------------------------------------------------- effect metadata
    def effect_rung(self, e: Effect) -> Optional[Loc]:
        if e.instr:
            return self.lm.outputs[e.instr].loc
        return self._def_loc(e.var)

    def enable_of(self, e: Effect) -> Tuple[str, Optional[Loc], str]:
        """(enable tag or permissive text, rung of the enable logic, permissive expression)."""
        if e.instr:
            oi = self.lm.outputs[e.instr]
            en = oi.roles.get(INS.SAFETY_INSTRUCTIONS[oi.instr].extra.get('enable', 'Enable'), '')
            loc = self._def_loc(en)
            return en, loc, self.permissive_text(en)
        loc = self._def_loc(e.var)
        return self.permissive_text(e.var), loc, self.permissive_text(e.var)

    def permissive_text(self, tag: str) -> str:
        loc = self._def_loc(tag)
        if not loc:
            return '—'
        r = self.rung(loc)
        if not r:
            return '—'
        toks = r[2]
        txt = format_condition(toks, tag, self.is_reset_like, self.is_status)
        if not txt:
            legs = seal_in_legs(toks, tag) or []
            sets = [' · '.join(op for op in leg if not self.is_status(op)) for leg in legs if tag not in leg]
            sets = [x for x in sets if x]
            if sets:
                txt = 'SET: ' + ' ∥ '.join(sets) + ' (+ seal-in)'
        return txt or '—'

    def seal_in(self, e: Effect) -> Optional[List[List[str]]]:
        loc = self._def_loc(e.var)
        r = self.rung(loc) if loc else None
        if not r:
            return None
        return seal_in_legs(r[2], e.var)

    def restart_legs(self, e: Effect) -> Tuple[List[str], List[str]]:
        """Seal-in OR group of an output rung split into (edge/reset tags, level tags that restart automatically)."""
        legs = self.seal_in(e) or []
        manual, auto = [], []
        for leg in legs:
            if e.var in leg:
                continue
            for op in leg:
                if self.is_status(op):
                    continue
                d = self.lm.first_def(op)
                if d and d[0][0] == 'edge' or op in self._reset_tags() or RESET_NAME_RE.search(op):
                    manual.append(op)
                elif op.endswith('.O1') or op in self.devices:
                    auto.append(op)
                else:
                    manual.append(op)
        return manual, auto

    def stop_category(self, cells: List[Cell]) -> str:
        delays = [c.delay_ms for c in cells]
        if not delays:
            return '—'
        if all(d is None for d in delays):
            return '0'
        if all(d is not None for d in delays):
            vals = sorted({d for d in delays})
            return '1 (' + '/'.join(f'{v:g}' for v in vals) + ' ms)'
        return '0/1'

    def drive_module(self, e: Effect) -> Optional[Module]:
        io = io_parts(e.var)
        return self.p.module_by_prefix(io[0]) if io else None
