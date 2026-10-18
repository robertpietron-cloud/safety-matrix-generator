# =============================================================================
# Project : Safety Matrix Generator (GuardLogix SafetyTask -> Cause & Effect)
# File    : safety_matrix/audit.py
# Author  : Robert Pietroń
# Revision: 1.0.0 (2026-10-18)
# Changes :
#   1.0.0 (2026-10-18) - First universal release: automatic validation report
#                        (critical alarms, dead inputs/outputs/tags, items to
#                        verify) with routine and rung of every finding; rules
#                        generalised from the manual PortalSaw audit rev 1.0-1.4.
# =============================================================================
"""Automatic audit of the safety task (Step 5 of the method)."""
from __future__ import annotations

import re
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Tuple

from . import instructions as INS
from .analysis import Analysis, Effect
from .ladder import Instr, Loc
from .logic import vars_in
from .model import io_parts, split_operand

ALARM, DEAD, VERIFY = 'ALARM', 'DEAD', 'VERIFY'


@dataclass
class Finding:
    severity: str
    key: str                      # catalog key: f.<key> (text), f.<key>.rec (recommendation)
    routine: str
    rungs: str
    element: str
    params: Dict[str, object] = field(default_factory=dict)
    cls: str = ''                 # classification key for DEAD items (cls.<name>)
    priority: bool = False


def group_locs(locs: Iterable[Optional[Loc]], multi=False) -> Tuple[str, str]:
    """[(Press, 3), (Press, 23), (Robot, 5)] -> ('Press / Robot', 'Press 3, 23; Robot 5')."""
    by = OrderedDict()
    for l in locs:
        if l is None or l.rung < 0:
            continue
        r = f'{l.program}/{l.routine}' if multi else l.routine
        by.setdefault(r, [])
        if l.rung not in by[r]:
            by[r].append(l.rung)
    if not by:
        return '—', '—'
    if len(by) == 1:
        r, ns = next(iter(by.items()))
        return r, ', '.join(str(n) for n in sorted(ns))
    return ' / '.join(by), '; '.join(f"{r} {', '.join(str(n) for n in sorted(ns))}" for r, ns in by.items())


def ranges(nums: List[int]) -> str:
    nums = sorted(set(nums))
    out = []
    for n in nums:
        if out and n == out[-1][1] + 1:
            out[-1][1] = n
        else:
            out.append([n, n])
    return ', '.join(f'{a:02d}' if a == b else f'{a:02d}–{b:02d}' for a, b in out)


class Auditor:
    def __init__(self, A: Analysis, crtl_priority_ms: float = 1000.0):
        self.A = A
        self.lm = A.lm
        self.multi = A.lm.multi_program
        self.crtl_priority_ms = crtl_priority_ms
        self.findings: List[Finding] = []

    def add(self, sev, key, locs, element, cls='', priority=False, **params):
        r, n = group_locs(locs, self.multi)
        self.findings.append(Finding(sev, key, r, n, element, params, cls, priority))

    def run(self) -> List[Finding]:
        for fn in (self.r_const_channels, self.r_std_channels, self.r_std_bypass, self.r_std_mute, self.r_std_parallel,
                   self.r_estop_auto, self.r_equal_channels, self.r_afi, self.r_const_branch,
                   self.r_dead_devices, self.r_dead_muting, self.r_aux_outputs, self.r_const_tags, self.r_unused_tags,
                   self.r_unused_channels, self.r_uncalled, self.r_modules_outside,
                   self.r_crtl, self.r_double_write, self.r_rout_reset_fp, self.r_or_devices, self.r_auto_restart,
                   self.r_auto_reset_guard, self.r_reset_std, self.r_std_not_written, self.r_missing_comments,
                   self.r_free_conditions, self.r_direct, self.r_heuristic, self.r_flow, self.r_pair_mismatch,
                   self.r_loads, self.r_stop_category, self.r_forces, self.r_completeness):
            fn()
        order = {ALARM: 0, DEAD: 1, VERIFY: 2}
        self.findings.sort(key=lambda f: (order[f.severity], not f.priority))
        return self.findings

    # ----------------------------------------------------------------- helpers
    def uses_of(self, tag) -> List[Loc]:
        return list(OrderedDict.fromkeys(self.lm.reads.get(tag, [])))

    def hits(self, dev: str, codes=('X', 'X1', 'XB', 'XM', 'N')) -> List[Effect]:
        return [e for e in self.A.matrix_effects(safety_only=True) if self.A.code(dev, e.key) in codes]

    def eff_names(self, effs: List[Effect]) -> str:
        return ', '.join(e.key for e in effs) or '—'

    def std_trace(self, bit: str) -> str:
        return self.A.std_trace(bit)

    # ================================================================= ALARM
    def r_const_channels(self):
        for d in self.A.devices.values():
            if d.const_channels:
                self.add(ALARM, 'const_channels', [d.loc] + self.uses_of(d.tag + '.O1'), f'{d.tag} ({d.instr})',
                         instr=d.instr, tag=d.tag, cha=d.ch_a, chb=d.ch_b,
                         uses=', '.join(self.A.loc_label(l) for l in self.uses_of(d.tag + '.O1')) or '—')

    def r_std_channels(self):
        for d in self.A.devices.values():
            if d.std_channels and not d.const_channels:
                srcs = '; '.join(self.std_trace(c) for c in (d.ch_a, d.ch_b) if self.A.is_std(c))
                self.add(ALARM, 'std_channels', [d.loc], f'{d.tag} ({d.instr})', instr=d.instr, tag=d.tag,
                         cha=d.ch_a, chb=d.ch_b, src=srcs or '—')

    def r_std_bypass(self):
        by_bit = OrderedDict()
        for (dev, ek), c in self.A.cells.items():
            if c.raw != 'XB':
                continue
            for b in c.bypass:
                g = by_bit.setdefault(b, {'devs': [], 'effs': []})
                if dev not in g['devs']:
                    g['devs'].append(dev)
                if ek not in g['effs']:
                    g['effs'].append(ek)
        self._xb_bits = set(by_bit)
        for b, g in by_bit.items():
            self.add(ALARM, 'std_bypass', self.uses_of(b), f"{b} ∥ {', '.join(x + '.O1' if x in self.lm.devices else x for x in g['devs'])}",
                     bit=b, src=self.std_trace(b) or b, devices=', '.join(g['devs']), effects=', '.join(g['effs']))

    def r_std_mute(self):
        for d in self.A.devices.values():
            if d.mute and not INS.looks_literal(d.mute):
                _, free = self.A.ev.cone(d.mute)
                std = sorted(f for f in free if self.A.leaf_class(f) == 'std') or ([d.mute] if self.A.is_std(d.mute) else [])
                if std:
                    self.add(ALARM, 'std_mute', [d.loc] + [self.A._def_loc(d.mute)], f'{d.mute} → {d.tag}.Mute',
                             tag=d.tag, instr=d.instr, operand=d.mute, bits=', '.join(std),
                             src='; '.join(self.std_trace(s) for s in std))
            elif d.mute == '1':
                self.add(ALARM, 'mute_const', [d.loc], f'{d.tag}.Mute = 1', tag=d.tag)
        for m in self.lm.mutings.values():
            std = set()
            for a in m.args[1:]:
                if a == m.light_curtain or INS.looks_literal(a) or a.isupper():
                    continue
                if self.A.is_std(a):
                    std.add(a)
                elif a in self.lm.defs:
                    std |= {f for f in self.A.ev.cone(a)[1] if self.A.leaf_class(f) == 'std'}
            if std:
                self.add(ALARM, 'std_mute', [m.loc], f'{m.tag} ({m.instr})', tag=m.tag, instr=m.instr,
                         operand='—', bits=', '.join(sorted(std)), src='; '.join(self.std_trace(s) for s in sorted(std)))

    def r_std_parallel(self):
        """A standard bit alone can switch on a tag whose logic otherwise needs safety signals."""
        xb = getattr(self, '_xb_bits', set())
        targets = set()
        for e in self.A.effects:
            for o in e.outputs:
                targets.add(o)
        seen, reported = set(), set()
        stack = list(targets)
        while stack:
            v = stack.pop()
            if v in seen or not self.A.ev.defined(v):
                continue
            seen.add(v)
            expr = self.A.ev.expr_of(v)
            stack.extend(x for x in vars_in(expr) if self.A.ev.defined(x))
            devs, free = self.A.ev.cone(v)
            std = [f for f in free if self.A.leaf_class(f) == 'std' and f not in xb]
            safety = devs or [f for f in free if self.A.leaf_class(f) in ('input', 'ext')]
            if not std or not safety or self.A.ev.value(v):
                continue
            for s in sorted(std):
                if (s, v) in reported:
                    continue
                if self.A.ev.value(v, free={s: True}):
                    reported.add((s, v))
                    self.add(ALARM, 'std_parallel', [self.A._def_loc(v)], f'{v} ← … ∥ {s}', tag=v, bit=s,
                             src=self.std_trace(s) or s, expr=self.A.permissive_text(v))

    def r_estop_auto(self):
        groups = OrderedDict()
        for d in self.A.devices.values():
            if d.type == 'EMERGENCY STOP' and d.reset_manual is False:
                groups.setdefault(d.loc.routine if d.loc else '', []).append(d)
        for r, ds in groups.items():
            effs = OrderedDict()
            for d in ds:
                for e in self.hits(d.tag, ('X', 'X1', 'XB', 'XM')):
                    effs[e.key] = e
            self.add(ALARM, 'estop_auto', [d.loc for d in ds], ', '.join(f'{d.tag}' for d in ds) + f' ({ds[0].instr}, AUTOMATIC)',
                     tags=', '.join(d.tag for d in ds), effects=', '.join(effs) or '—')

    def r_equal_channels(self):
        for d in self.A.devices.values():
            if d.equal_channels and d.kind == 'instr':
                self.add(ALARM, 'equal_channels', [d.loc], f'{d.tag} ({d.instr})', tag=d.tag, instr=d.instr, ch=d.ch_a,
                         n=len(self.hits(d.tag)))

    def r_afi(self):
        for loc, what in self.lm.flow:
            if what == 'AFI':
                self.add(ALARM, 'afi', [loc], 'AFI', rung=self.A.loc_label(loc))

    def r_const_branch(self):
        rep = set()
        for v, lst in self.lm.defs.items():
            expr, loc, _ = lst[-1]
            for leg in _or_legs(expr):
                vs = vars_in(leg)
                if vs and all(self.A.ev.leaf_info(x)[0] == 'const' and not self.A.ev.defined(x) for x in vs):
                    if self.A.ev._ev(leg, (frozenset(), {}), frozenset(), {})[0] and (v, loc) not in rep:
                        rep.add((v, loc))
                        self.add(ALARM, 'const_branch', [loc], v, tag=v, consts=', '.join(vs))

    # ================================================================= DEAD
    def r_dead_devices(self):
        for d in self.A.devices.values():
            if d.n_eff == 0 and not d.const_channels:
                uses = []
                for loc in self.uses_of(d.tag + '.O1'):
                    r = self.A.rung(loc)
                    outs = [t.args[0] for t in (r[2] if r else []) if isinstance(t, Instr) and t.name.upper() == 'OTE' and t.args]
                    uses.append(f"{self.A.loc_label(loc)}: {', '.join(outs) or '—'}")
                self.add(DEAD, 'dead_device', [d.loc] + self.uses_of(d.tag + '.O1'), f'{d.tag} ({d.instr}, {d.ch_a}/{d.ch_b})',
                         cls='dead_input', tag=d.tag, uses='; '.join(uses) or '—')

    def r_dead_muting(self):
        for m in self.lm.mutings.values():
            if not self.lm.reads.get(m.tag + '.O1'):
                self.add(DEAD, 'dead_muting', [m.loc], f'{m.tag} ({m.instr})', cls='dead_block', tag=m.tag)

    def r_aux_outputs(self):
        for e in self.A.effects:
            if e.in_matrix:
                continue
            key = 'aux_not_energized' if e.reason == 'not_energized' else 'aux_no_device'
            self.add(VERIFY, key, [self.A.effect_rung(e)], e.key, tag=e.key, expr=self.A.permissive_text(e.var))

    def _used_roots(self):
        roots = set()
        for d in (self.lm.reads, self.lm.writes, self.lm.defs):
            for t in d:
                roots.add(split_operand(t)[0].split('\\')[-1])
        for x in list(self.lm.devices) + list(self.lm.outputs) + list(self.lm.mutings) + list(self.lm.timers):
            roots.add(split_operand(x)[0].split('\\')[-1])
        return roots

    def r_const_tags(self):
        items = []
        locs = []
        for t, lst in self.lm.reads.items():
            if t in self.lm.defs or t in self.lm.writes or self.A.is_std(t):
                continue
            k, v = self.A.ev.leaf_info(t)
            if k == 'const' and not (re.search(r'(Fault|Status|\.FP|Ready|Required|Disabled)', t) or io_parts(t)):
                items.append(f'{t} = {int(bool(v))}')
                locs += lst
        if items:
            self.add(DEAD, 'const_tags', locs, ', '.join(sorted(items)), cls='const_tag', tags=', '.join(sorted(items)))

    def r_unused_tags(self):
        used = self._used_roots()
        names = []
        for prog in self.A.p.safety_programs():
            for t in prog.tags.values():
                if t.name not in used and not t.alias_for:
                    names.append(t.name)
        for t in self.A.p.tags.values():
            if t.tag_class == 'Safety' and t.name not in used and t.name not in self.A.std_dests and t.usage != 'Produced':
                names.append(t.name)
        if names:
            self.add(DEAD, 'unused_tags', [], ', '.join(sorted(set(names))), cls='dead_tags', tags=', '.join(sorted(set(names))))

    def r_unused_channels(self):
        refs = set(self.lm.reads) | set(self.lm.writes) | set(self.lm.defs)
        for d in self.A.devices.values():
            refs |= {d.ch_a, d.ch_b, d.reset}
        for o in self.lm.outputs.values():
            refs |= set(o.roles.values())
        for m in self.A.p.modules.values():
            if not m.is_safety or not m.channel_counts:
                continue
            nin, nout = m.channel_counts
            px = m.tag_prefix
            for kind, n in (('I', nin), ('O', nout)):
                if not n:
                    continue
                used = {int(mm.group(1)) for r in refs if r
                        for mm in [re.match(re.escape(px) + rf':{kind}\.Pt(\d+)Data$', r)] if mm}
                unused = [i for i in range(n) if i not in used]
                if used and unused:
                    self.add(DEAD, 'unused_inputs' if kind == 'I' else 'unused_outputs', [],
                             f"{px}:{kind}.Pt{ranges(unused)}", cls='dead_channel', module=f'{px} ({m.catalog})',
                             channels=', '.join(f'Pt{i:02d}' + (f" '{m.channel_comment(kind, f'Pt{i:02d}Data')}'" if m.channel_comment(kind, f'Pt{i:02d}Data') else '') for i in unused))
                elif not used and m.connection('input' if kind == 'I' else 'output') and kind == 'I':
                    self.add(DEAD, 'unused_module', [], f'{px} ({m.catalog})', cls='dead_channel', module=f'{px} ({m.catalog})')

    def r_uncalled(self):
        ex = set(self.lm.executed)
        for prog in self.A.p.safety_programs():
            for r in prog.routines:
                if (prog.name, r) not in ex:
                    self.add(DEAD, 'uncalled_routine', [], f'{prog.name}/{r}', cls='dead_routine', routine=r,
                             n=len(prog.routines[r].rungs))

    def r_modules_outside(self):
        refs = set()
        for t in list(self.lm.reads) + list(self.lm.writes) + list(self.lm.defs):
            io = io_parts(t)
            if io:
                refs.add(io[0])
        drives_hw = []
        for m in self.A.p.modules.values():
            is_drive = bool(re.search(r'PowerFlex|Kinetix|Drive|ArmorStart', m.catalog, re.I))
            if m.is_safety and m.tag_prefix not in refs and any(c.safety for c in m.connections) and not m.inhibited:
                if is_drive:
                    self.add(DEAD, 'drive_unused', [], f'{m.name} ({m.catalog})', cls='outside_code', module=m.name)
                elif not m.channel_counts:
                    self.add(DEAD, 'module_unused', [], f'{m.name} ({m.catalog})', cls='outside_code', module=m.name)
            elif is_drive and not any(c.safety for c in m.connections):
                drives_hw.append(f'{m.name} ({m.catalog})')
        if drives_hw:
            self.add(DEAD, 'drives_hardwired', [], ', '.join(drives_hw), cls='outside_code', modules=', '.join(drives_hw))

    # ================================================================= VERIFY
    def r_crtl(self):
        A = self.A
        per = A.task_period or 0
        wd = A.task_watchdog or 0
        groups = OrderedDict()
        for d in A.devices.values():
            m, c = A.input_connection(d)
            if not m or not c:
                continue
            ad = A.p.top_adapter(m)
            key = (ad.name, c.rpi_ms, c.timeout_multiplier, c.network_delay_multiplier, c.reaction_time_limit_ms)
            g = groups.setdefault(key, {'mods': OrderedDict(), 'devs': [], 'total': 0.0, 'locs': []})
            g['mods'][m.tag_prefix.split(':')[-1] if ':' in m.tag_prefix else m.tag_prefix] = m.catalog
            g['devs'].append(d.tag)
            outs = [A.output_connection(e)[1] for e in self.hits(d.tag, ('X', 'X1', 'XB', 'XM', 'XC'))]
            out_max = max((o.reaction_time_limit_ms or 0 for o in outs if o), default=0)
            tot = (c.reaction_time_limit_ms or 0) + (d.filter_ms or 0) + per + wd + out_max
            g['total'] = max(g['total'], tot)
        for (ad, rpi, tm, ndm, crtl), g in groups.items():
            pri = (crtl or 0) >= self.crtl_priority_ms
            cats = sorted(set(g['mods'].values()))
            self.add(VERIFY, 'crtl_inputs', [], f"{ad}: {', '.join(cats)} (slot {', '.join(g['mods'])})", priority=pri,
                     adapter=ad, rpi=_g(rpi), tm=_g(tm), ndm=_g(ndm), crtl=_g(crtl), total=_g(g['total']),
                     period=_g(per), watchdog=_g(wd), devices=', '.join(g['devs']))
        outs = OrderedDict()
        for e in A.matrix_effects(safety_only=True):
            m, c = A.output_connection(e)
            if not m or not c:
                continue
            kind = 'drive' if e.kind in ('STO', 'SS1', 'SBC', 'SLS') else 'out'
            outs.setdefault((kind, c.rpi_ms, c.timeout_multiplier, c.network_delay_multiplier, c.reaction_time_limit_ms), []).append(
                m.name if kind == 'drive' else m.tag_prefix)
        for (kind, rpi, tm, ndm, crtl), mods in outs.items():
            mods = list(OrderedDict.fromkeys(mods))
            self.add(VERIFY, 'crtl_drives' if kind == 'drive' else 'crtl_outputs', [], ', '.join(mods), rpi=_g(rpi), tm=_g(tm),
                     ndm=_g(ndm), crtl=_g(crtl), modules=', '.join(mods))

    def r_double_write(self):
        for tag, ws in self.lm.writes.items():
            ote = [l for l, w in ws if w == 'OTE']
            edge = [l for l, w in ws if w in ('OSF', 'OSR')]
            same = [l for l in ote if l in edge]
            if same:
                self.add(VERIFY, 'osf_ote', same, tag, tag=tag)
            elif len(ote) > 1:
                self.add(VERIFY, 'double_ote', ote, tag, tag=tag, n=len(ote))

    def r_rout_reset_fp(self):
        for o in self.lm.outputs.values():
            spec = INS.SAFETY_INSTRUCTIONS[o.instr]
            rst = o.roles.get(spec.reset, '')
            srcs, locs = self.A.reset_sources(rst)
            other = [s for s in srcs if s.endswith('.FP') and s.rsplit('.', 1)[0] != o.tag and s.rsplit('.', 1)[0] in self.lm.outputs]
            if other:
                self.add(VERIFY, 'rout_reset_fp', locs, rst, tag=o.tag, reset=rst, other=', '.join(other))

    def r_or_devices(self):
        seen = set()
        for (dev, ek), c in self.A.cells.items():
            if c.raw != 'XC':
                continue
            for p in c.partners:
                k = frozenset((dev, p))
                if k in seen:
                    continue
                seen.add(k)
                effs = [e for (d2, e2), c2 in self.A.cells.items() if d2 == dev and c2.raw == 'XC' and p in c2.partners
                        for e in [e2]]
                locs = [l for t, l in c.path[1:2]]
                self.add(VERIFY, 'or_devices', locs, f'{dev} ∥ {p}', a=dev, b=p, effects=', '.join(effs))

    def r_auto_restart(self):
        for e in self.A.matrix_effects(safety_only=True):
            if e.instr:
                continue
            manual, auto = self.A.restart_legs(e)
            if auto:
                self.add(VERIFY, 'auto_restart', [self.A.effect_rung(e)], e.key, tag=e.key, levels=', '.join(auto))

    def r_auto_reset_guard(self):
        for d in self.A.devices.values():
            if d.type != 'EMERGENCY STOP' and d.reset_manual is False and d.n_eff:
                self.add(VERIFY, 'auto_reset_guard', [d.loc], f'{d.tag} ({d.instr}, AUTOMATIC)', tag=d.tag,
                         effects=self.eff_names(self.hits(d.tag)))

    def r_reset_std(self):
        """Resets initiated from standard control, grouped per standard bit."""
        groups = OrderedDict()
        for d in self.A.devices.values():
            if d.reset and not INS.looks_literal(d.reset):
                groups.setdefault(d.reset, []).append(d.tag)
        for o in self.lm.outputs.values():
            rst = o.roles.get(INS.SAFETY_INSTRUCTIONS[o.instr].reset, '')
            if rst:
                groups.setdefault(rst, []).append(o.tag)
        for e in self.A.matrix_effects(safety_only=True):
            manual, auto = self.A.restart_legs(e)
            for m in manual:
                groups.setdefault(m, []).append(e.key)
        by_bit = OrderedDict()
        for rst, users in groups.items():
            srcs, locs = self.A.reset_sources(rst)
            std = [s for s in srcs if self.A.is_std(s)] + ([rst] if self.A.is_std(rst) else [])
            for b in std:
                g = by_bit.setdefault(b, {'resets': OrderedDict(), 'locs': []})
                g['resets'].setdefault(rst, [])
                for u in users:
                    if u not in g['resets'][rst]:
                        g['resets'][rst].append(u)
                g['locs'] += locs or self.uses_of(rst)
        for b, g in by_bit.items():
            src = self.A.std_source(b)
            latched = any(w[3] in ('OTL', 'OTU') for w in self.A.std_writers(src)) if src else False
            written_by_safety = b in self.lm.writes
            sev, key = (ALARM, 'reset_std_auto') if (latched or written_by_safety) else (VERIFY, 'reset_std')
            self.add(sev, key, g['locs'] + [l for l, _ in self.lm.writes.get(b, [])], b, bit=b,
                     src=self.std_trace(b) or b, resets='; '.join(f"{r} → {', '.join(u)}" for r, u in g['resets'].items()))

    def r_std_not_written(self):
        if not self.A.p.standard_programs():
            return
        for b in self.A.std_bits:
            src = self.A.std_source(b)
            if src and not self.A.std_writers(src):
                self.add(VERIFY, 'std_not_written', self.uses_of(b), b, bit=b, src=src)

    def r_missing_comments(self):
        by_mod = OrderedDict()
        for d in self.A.devices.values():
            for ch in (d.ch_a, d.ch_b):
                if ch and io_parts(ch) and not self.A.io_comment(ch):
                    m = io_parts(ch)[0]
                    g = by_mod.setdefault(m, {'ch': [], 'who': [], 'locs': []})
                    member = io_parts(ch)[2].replace('Data', '')
                    if member not in g['ch']:
                        g['ch'].append(member)
                    if d.tag not in g['who']:
                        g['who'].append(d.tag)
                    g['locs'].append(d.loc)
        for o in self.lm.outputs.values():
            for k in ('Feedback1', 'Feedback2'):
                ch = o.roles.get(k, '')
                if ch and io_parts(ch) and not self.A.io_comment(ch):
                    m = io_parts(ch)[0]
                    g = by_mod.setdefault(m, {'ch': [], 'who': [], 'locs': []})
                    member = io_parts(ch)[2].replace('Data', '')
                    if member not in g['ch']:
                        g['ch'].append(member)
                    if f'{o.tag} (EDM)' not in g['who']:
                        g['who'].append(f'{o.tag} (EDM)')
                    g['locs'].append(o.loc)
        for m, g in by_mod.items():
            self.add(VERIFY, 'missing_comments', g['locs'], f"{m}:I.{', '.join(sorted(g['ch']))}", module=m,
                     channels=', '.join(sorted(g['ch'])), who=', '.join(g['who']))

    def r_free_conditions(self):
        leaves = OrderedDict()
        for e in self.A.matrix_effects():
            _, free = self.A.ev.cone(e.var)
            for f in free:
                cls = self.A.leaf_class(f)
                if cls in ('cmp', 'data', 'latch', 'unk', 'mute', 'ext'):
                    g = leaves.setdefault(f, {'cls': cls, 'effs': [], 'val': e.baseline.get(f, False)})
                    g['effs'].append(e.key)
        for f, g in leaves.items():
            locs = self.lm.comparisons.get(f) or self.uses_of(f)
            self.add(VERIFY, 'free_' + g['cls'], locs, f, leaf=f, effects=', '.join(g['effs'][:12]) + (' …' if len(g['effs']) > 12 else ''),
                     value=int(bool(g['val'])))

    def r_direct(self):
        for d in self.A.devices.values():
            if d.kind in ('direct', 'external'):
                self.add(VERIFY, 'direct_' + d.kind, self.uses_of(d.tag), d.tag, tag=d.tag,
                         effects=self.eff_names(self.hits(d.tag, ('X', 'X1', 'XB', 'XM', 'XC'))))

    def r_heuristic(self):
        for d in self.A.devices.values():
            if d.heuristic and d.kind == 'instr':
                self.add(VERIFY, 'heuristic', [d.loc], f'{d.tag} ({d.instr})', tag=d.tag, instr=d.instr,
                         roles=', '.join(f'{k}={v}' for k, v in d.roles.items() if k not in ('Tag',)))
            if d.conditional:
                self.add(VERIFY, 'device_conditional', [d.loc], d.tag, tag=d.tag)

    def r_flow(self):
        for loc, what in self.lm.flow:
            if what == 'AFI':
                continue
            if what in ('PROTECTED', 'ST', 'FBD', 'SFC'):
                self.add(VERIFY, 'routine_not_analysed', [], f'{loc.program}/{loc.routine}', routine=loc.routine, kind=what)
            elif what.startswith('AOI-COND:'):
                self.add(VERIFY, 'aoi_conditional', [loc], what.split(':', 1)[1], aoi=what.split(':', 1)[1])
            else:
                self.add(VERIFY, 'flow', [loc], what, instr=what)
        for loc, name in self.lm.unknown:
            self.add(VERIFY, 'unknown_instr', [loc], name, instr=name)
        for loc, aoi, inst, prot in self.lm.aoi_calls:
            if prot:
                self.add(VERIFY, 'aoi_protected', [loc], f'{aoi}({inst})', aoi=aoi, inst=inst)
        for loc, target, cond in self.lm.calls:
            if cond:
                self.add(VERIFY, 'jsr_conditional', [loc], f'JSR({target})', routine=target)

    def r_pair_mismatch(self):
        for e in self.A.matrix_effects():
            if len(e.outputs) < 2:
                continue
            ref = self.A.ev.cone(e.outputs[0])[0]
            for o in e.outputs[1:]:
                if self.A.ev.cone(o)[0] != ref:
                    self.add(VERIFY, 'pair_mismatch', [self.A.effect_rung(e)], e.key, tag=e.key, a=e.outputs[0], b=o)

    def r_loads(self):
        rs = [e for e in self.A.matrix_effects(safety_only=True) if e.kind in ('ROUT', 'CROUT', 'OUT')]
        if rs:
            self.add(VERIFY, 'loads', [self.A.effect_rung(e) for e in rs], 'ROUT / CROUT / OTE', outputs=', '.join(e.key for e in rs))

    def r_stop_category(self):
        if not self.lm.timers:
            self.add(VERIFY, 'stop_cat0', [], '—')
            return
        off = [t for t in self.lm.timers.values() if t.kind in INS.OFF_DELAY_TIMERS]
        if off:
            self.add(VERIFY, 'stop_cat1', [t.loc for t in off], ', '.join(t.tag for t in off),
                     timers=', '.join(f'{t.tag} ({t.kind}, {t.preset_raw} ms)' for t in off))
        else:
            self.add(VERIFY, 'stop_cat0', [], '—')

    def r_forces(self):
        self.add(VERIFY, 'forces', [], 'Forces')

    def r_completeness(self):
        parts = []
        for prog, r in self.lm.executed:
            rr = self.A.p.programs[prog].routines.get(r)
            parts.append(f'{r} {len(rr.rungs) if rr else 0}')
        self.add(VERIFY, 'completeness', [], self.A.p.source_name or '—', routines=', '.join(parts),
                 src=self.A.p.source_name or '—')


def _or_legs(e):
    k = e[0]
    if k == 'or':
        for x in e[1:]:
            yield x
            yield from _or_legs(x)
    elif k in ('and',):
        for x in e[1:]:
            yield from _or_legs(x)
    elif k == 'not':
        yield from _or_legs(e[1])
    elif k == 'timer':
        yield from _or_legs(e[3])


def _g(v):
    if v is None:
        return 'n/a'
    return f'{v:g}' if isinstance(v, float) else str(v)


def run_audit(A: Analysis, crtl_priority_ms: float = 1000.0) -> List[Finding]:
    return Auditor(A, crtl_priority_ms).run()
