# =============================================================================
# Project : Safety Matrix Generator (GuardLogix SafetyTask -> Cause & Effect)
# File    : safety_matrix/config.py
# Author  : Robert Pietroń
# Revision: 1.0.0 (2026-10-18)
# Changes :
#   1.0.0 (2026-10-18) - First universal release: optional YAML project
#                        configuration (document data, languages, zones,
#                        effect groups, device/effect overrides, analysis
#                        options) and the presentation layout derived from it.
# =============================================================================
"""Project configuration (YAML) and matrix layout (zones, groups, IDs, descriptions)."""
from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from . import instructions as INS
from .analysis import Analysis, Options
from .i18n import ML, Tr


@dataclass
class Config:
    title: object = None                     # str or {lang: str}
    author: str = ''
    revision: str = '1.0'
    date: str = ''
    revisions: List[dict] = field(default_factory=list)
    languages: List[str] = field(default_factory=lambda: ['pl', 'en', 'fr', 'da'])
    default_language: str = 'pl'
    info_effects: List[str] = field(default_factory=list)
    include_effects: List[str] = field(default_factory=list)
    exclude_effects: List[str] = field(default_factory=list)
    crtl_priority_ms: float = 1000.0
    direct_inputs: bool = True
    zones: List[dict] = field(default_factory=list)
    effect_groups: List[dict] = field(default_factory=list)
    devices: Dict[str, dict] = field(default_factory=dict)
    effects: Dict[str, dict] = field(default_factory=dict)
    comments: bool = True

    def options(self) -> Options:
        return Options(info_effects=list(self.info_effects), include_effects=list(self.include_effects),
                       exclude_effects=list(self.exclude_effects), direct_inputs=self.direct_inputs,
                       device_types={k: v['type'] for k, v in self.devices.items() if isinstance(v, dict) and v.get('type')})


def load_config(path: Optional[str]) -> Config:
    cfg = Config()
    if not path:
        cfg.date = _dt.date.today().isoformat()
        return cfg
    import yaml
    with open(path, encoding='utf-8') as f:
        data = yaml.safe_load(f) or {}
    doc = data.get('document', {}) or {}
    cfg.title = doc.get('title')
    cfg.author = str(doc.get('author', '') or '')
    cfg.revision = str(doc.get('revision', cfg.revision))
    cfg.date = str(doc.get('date') or _dt.date.today().isoformat())
    cfg.revisions = list(doc.get('revisions', []) or [])
    cfg.comments = bool(doc.get('cell_comments', True))
    if data.get('languages'):
        cfg.languages = [str(l).lower() for l in data['languages']]
    cfg.default_language = str(data.get('default_language', cfg.languages[0])).lower()
    an = data.get('analysis', {}) or {}
    cfg.info_effects = list(an.get('info_effects', []) or [])
    cfg.include_effects = list(an.get('include_effects', []) or [])
    cfg.exclude_effects = list(an.get('exclude_effects', []) or [])
    cfg.crtl_priority_ms = float(an.get('crtl_priority_ms', cfg.crtl_priority_ms))
    cfg.direct_inputs = bool(an.get('direct_inputs', True))
    cfg.zones = list(data.get('zones', []) or [])
    cfg.effect_groups = list(data.get('effect_groups', []) or [])
    cfg.devices = dict(data.get('devices', {}) or {})
    cfg.effects = dict(data.get('effects', {}) or {})
    return cfg


# ======================================================================= layout
@dataclass
class Zone:
    number: int
    name: ML
    devices: List[str]


@dataclass
class Group:
    name: ML
    effects: List[str]


class Layout:
    """Zones (device columns/rows), effect groups, IDs and descriptions."""

    def __init__(self, A: Analysis, cfg: Config, tr: Tr):
        self.A, self.cfg, self.tr = A, cfg, tr
        self.zones: List[Zone] = []
        self.groups: List[Group] = []
        self.dev_id: Dict[str, str] = {}
        self.dev_desc: Dict[str, ML] = {}
        self.eff_desc: Dict[str, ML] = {}
        self.valves = set()
        self._zones()
        self._groups()
        self._descriptions()

    # ----------------------------------------------------------------- zones
    def _routine_of(self, tag) -> str:
        d = self.A.devices[tag]
        return d.loc.routine if d.loc else ''

    def _sorted(self, tags):
        scan = list(self.A.devices)
        return sorted(tags, key=lambda t: (INS.DEVICE_TYPES.index(self.A.devices[t].type)
                                           if self.A.devices[t].type in INS.DEVICE_TYPES else 99, scan.index(t)))

    def _zones(self):
        left = list(self.A.devices)
        raw = []
        for z in self.cfg.zones:
            explicit = [t for t in (z.get('devices') or []) if t in left]
            for t in explicit:
                left.remove(t)
            by_routine = [t for t in left if self._routine_of(t) in (z.get('routines') or [])]
            for t in by_routine:
                left.remove(t)
            raw.append((z.get('name'), explicit + self._sorted(by_routine)))
        if not self.cfg.zones:
            routines = []
            for prog, r in self.A.lm.executed:
                if r not in routines:
                    routines.append(r)
            for r in routines:
                tags = [t for t in left if self._routine_of(t) == r]
                if tags:
                    raw.append(({'_routine': r}, self._sorted(tags)))
                    left = [t for t in left if t not in tags]
        if left:
            raw.append(({'_other': True}, self._sorted(left)))
        for i, (name, tags) in enumerate([x for x in raw if x[1]], 1):
            if isinstance(name, dict) and '_routine' in name:
                ml = self.tr('zone.routine', n=i, routine=name['_routine'])
            elif isinstance(name, dict) and '_other' in name:
                ml = self.tr('zone.other', n=i)
            else:
                ml = self.tr.ml(name)
            self.zones.append(Zone(i, ml, tags))
        for z in self.zones:
            cnt = {}
            for t in z.devices:
                d = self.A.devices[t]
                over = (self.cfg.devices.get(t) or {}).get('id') if isinstance(self.cfg.devices.get(t), dict) else None
                cnt[d.type] = cnt.get(d.type, 0) + 1
                d.zone = str(z.number)
                d.id = over or f'{INS.TYPE_ABBR.get(d.type, "SI")} {z.number}.{cnt[d.type]}'
                self.dev_id[t] = d.id

    def zone_of(self, tag) -> Optional[Zone]:
        return next((z for z in self.zones if tag in z.devices), None)

    # ----------------------------------------------------------------- groups
    def _groups(self):
        effs = [e.key for e in self.A.matrix_effects()]
        left = list(effs)
        raw = []
        for g in self.cfg.effect_groups:
            explicit = [k for k in (g.get('effects') or []) if k in left]
            for k in explicit:
                left.remove(k)
            by_r = [k for k in left if (self.A.effect_rung(self.A.effect(k)) or _NoLoc).routine in (g.get('routines') or [])]
            for k in by_r:
                left.remove(k)
            raw.append((self.tr.ml(g.get('name')), explicit + by_r))
        if not self.cfg.effect_groups:
            info = [k for k in left if self.A.effect(k).info]
            left = [k for k in left if k not in info]
            routines = []
            for k in left:
                r = (self.A.effect_rung(self.A.effect(k)) or _NoLoc).routine
                if r not in routines:
                    routines.append(r)
            for r in routines:
                ks = [k for k in left if (self.A.effect_rung(self.A.effect(k)) or _NoLoc).routine == r]
                raw.append((self.tr('group.routine', routine=r), ks))
            left = info
            if info:
                raw.append((self.tr('group.info'), info))
                left = []
        if left:
            raw.append((self.tr('group.other'), left))
        self.groups = [Group(n, ks) for n, ks in raw if ks]
        for k, v in self.cfg.effects.items():
            if isinstance(v, dict) and v.get('valve'):
                self.valves.add(k)

    # ----------------------------------------------------------------- descriptions
    def _descriptions(self):
        A = self.A
        for t, d in A.devices.items():
            over = self.cfg.devices.get(t)
            if isinstance(over, dict) and over.get('description'):
                self.dev_desc[t] = self.tr.ml(over['description'])
                continue
            base = ''
            if d.kind == 'instr':
                tagobj = A.find_tag(t)
                base = (tagobj.description if tagobj else '') or _first_line(A.rung_comment(d.loc))
            ca, cb = A.io_comment(d.ch_a) if d.ch_a else '', A.io_comment(d.ch_b) if d.ch_b else ''
            io = ' / '.join(x for x in dict.fromkeys([ca, cb]) if x)
            if d.kind != 'instr' and not io:
                io = A.describe(t)
            txt = base
            if io and io != base:
                txt = (txt + '  ' if txt else '') + f"[I/O: '{io}']"
            self.dev_desc[t] = self.tr.ml(_clean(txt) or t)
        for e in A.matrix_effects():
            over = self.cfg.effects.get(e.key)
            if isinstance(over, dict) and over.get('description'):
                self.eff_desc[e.key] = self.tr.ml(over['description'])
                continue
            if e.kind in ('ROUT', 'CROUT', 'OUT'):
                cm = ' / '.join(dict.fromkeys(c for c in (A.io_comment(o) for o in e.outputs) if c))
                self.eff_desc[e.key] = self.tr('effdesc.' + ('OUT' if e.kind == 'OUT' else 'ROUT'), tag=e.key, instr=e.kind,
                                               io=f"'{_clean(cm)}'" if cm else '—')
            elif e.info:
                self.eff_desc[e.key] = self.tr('effdesc.INFO', tag=e.key, io=f"'{_clean(A.describe(e.key))}'" if A.describe(e.key) else '—')
            else:
                m = A.drive_module(e)
                cat = _clean(m.catalog) if m else ''
                self.eff_desc[e.key] = self.tr('effdesc.DRIVE', kind='' if e.kind in cat.upper() else e.kind,
                                               name=m.name if m else e.key.split(':')[0], catalog=cat,
                                               desc=_clean(m.description) if m and m.description else '').map(_clean)

    # ----------------------------------------------------------------- helpers
    def effect_label(self, key) -> str:
        """Short column label of an effect (tag of the drive / ROUT / output)."""
        e = self.A.effect(key)
        if e.kind in ('STO', 'SS1', 'SBC', 'SLS'):
            return key.split(':')[0]
        return key

    def group_of(self, key) -> Optional[Group]:
        return next((g for g in self.groups if key in g.effects), None)

    def ordered_devices(self) -> List[str]:
        return [t for z in self.zones for t in z.devices]

    def ordered_effects(self) -> List[str]:
        return [k for g in self.groups for k in g.effects]


class _NoLoc:
    routine = ''


def _first_line(s: str) -> str:
    for line in (s or '').splitlines():
        if line.strip():
            return line.strip()
    return ''


def _clean(s: str) -> str:
    return ' '.join((s or '').split())
