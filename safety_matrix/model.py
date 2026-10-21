# =============================================================================
# Project : Safety Matrix Generator (GuardLogix SafetyTask -> Cause & Effect)
# File    : safety_matrix/model.py
# Author  : Robert Pietroń
# Revision: 1.1.0 (2026-10-21)
# Changes :
#   1.0.0 (2026-10-18) - First universal release: format-neutral project model
#                        (controller, tasks, programs, routines, rungs, tags,
#                        modules, CIP Safety connections, SafetyTagMap, AOIs).
#   1.1.0 (2026-10-21) - split_operand keeps the 'Program\' prefix of program-
#                        scope operands (bit constants of program tags were not
#                        recognised); Routine.source keeps the text of ST/FBD/SFC
#                        routines; Tag.timer_preset(); Module.is_peripheral.
# =============================================================================
"""Format-neutral model of a Logix Designer project.

Both parsers (L5K and L5X) produce a :class:`Project`.  Everything the analysis
needs is kept here; nothing in this module depends on the source format.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Rung:
    number: int
    text: str                     # neutral text, without the trailing ';'
    comment: str = ''
    kind: str = 'N'               # N = normal rung


@dataclass
class Routine:
    name: str
    kind: str = 'RLL'             # RLL, ST, FBD, SFC
    rungs: List[Rung] = field(default_factory=list)
    protected: bool = False       # source-protected (encoded) routine
    description: str = ''
    source: List[str] = field(default_factory=list)   # ST/FBD/SFC: normalised source lines (see parsers)


@dataclass
class Tag:
    name: str
    data_type: str = ''
    scope: str = 'controller'     # 'controller' or the program name
    tag_class: str = ''           # 'Safety', 'Standard' or ''
    description: str = ''
    comments: Dict[str, str] = field(default_factory=dict)   # member/bit -> comment, e.g. '[0].1'
    value: object = None          # parsed initial value (int, list of ints, ...) or None
    alias_for: str = ''           # alias tags: base operand
    usage: str = ''               # 'Produced' / 'Consumed' / ''
    producer: str = ''            # consumed tags: producing controller
    remote_tag: str = ''

    def bit_value(self, member: str) -> Optional[bool]:
        """Initial value of a BOOL tag or of a bit of an integer tag/array ('', '.3', '[2].5')."""
        v = self.value
        if v is None:
            return None
        m = re.fullmatch(r'(?:\[(\d+)\])?(?:\.(\d+))?', member or '')
        if not m:
            return None
        idx, bit = m.group(1), m.group(2)
        try:
            if idx is not None:
                if not isinstance(v, list):
                    return None
                v = v[int(idx)]
            if isinstance(v, list):
                return None
            v = int(v)
        except (ValueError, IndexError, TypeError):
            return None
        if bit is not None:
            return bool((v >> int(bit)) & 1)
        if self.data_type.upper() == 'BOOL' or v in (0, 1):
            return bool(v)
        return None

    def timer_preset(self, member: str = '') -> Optional[float]:
        """PRE of a TIMER tag or of a TIMER array element ('', '[5]') from the initial value [CTL, PRE, ACC]."""
        v = self.value
        m = re.fullmatch(r'(?:\[(\d+)\])?', member or '')
        if v is None or not m:
            return None
        try:
            if m.group(1) is not None:
                v = v[int(m.group(1))]
            if isinstance(v, list) and len(v) >= 2 and not isinstance(v[1], list) and v[1] is not None:
                return float(v[1])
        except (IndexError, TypeError, ValueError):
            return None
        return None


@dataclass
class Connection:
    name: str
    kind: str = ''                # 'input' / 'output' / ''
    rpi_ms: Optional[float] = None
    timeout_multiplier: Optional[float] = None
    network_delay_multiplier: Optional[float] = None   # percent
    reaction_time_limit_ms: Optional[float] = None     # CRTL
    safety: bool = False
    tag_suffix: str = ''          # e.g. 'I', 'O', 'SI', 'SO'
    comments: Dict[str, str] = field(default_factory=dict)  # member (upper case, e.g. 'PT00DATA') -> comment


@dataclass
class Module:
    name: str
    parent: str = ''
    catalog: str = ''
    slot: Optional[int] = None
    address: str = ''             # IP address / node address
    port_label: str = ''
    description: str = ''
    safety_enabled: Optional[bool] = None
    inhibited: bool = False
    connections: List[Connection] = field(default_factory=list)
    comments: Dict[str, str] = field(default_factory=dict)   # '<suffix>.<MEMBER>' -> comment, e.g. 'I.PT00DATA'

    @property
    def tag_prefix(self) -> str:
        """Prefix of the module I/O tags: '<Name>' for network devices, '<Parent>:<Slot>' in a chassis."""
        if self.address:
            return self.name
        if self.slot is not None and self.parent:
            return f'{self.parent}:{self.slot}'
        return self.name

    @property
    def is_safety(self) -> bool:
        return any(c.safety for c in self.connections) or bool(self.safety_enabled)

    @property
    def is_peripheral(self) -> bool:
        """Internal sub-module of another device (e.g. '$NoName' drive peripheral of a PowerFlex)."""
        return self.name.startswith('$') or 'PERIPHERAL' in self.catalog.upper()

    def connection(self, kind: str) -> Optional[Connection]:
        """Safety connection of the given kind ('input'/'output'), falling back to any connection of that kind."""
        cands = [c for c in self.connections if c.kind == kind]
        safe = [c for c in cands if c.safety]
        return (safe or cands or [None])[0]

    def channel_comment(self, suffix: str, member: str) -> str:
        """I/O comment of a module member, e.g. ('I', 'Pt04Data')."""
        return self.comments.get(f'{suffix.upper()}.{member.upper()}', '')

    @property
    def channel_counts(self):
        """(inputs, outputs) derived from the catalog number, e.g. 1734-IB8S -> (8, 0); None if unknown."""
        cat = self.catalog.upper()
        mi = re.search(r'IB(\d+)', cat)
        mo = re.search(r'OBV?(\d+)', cat)
        if not mi and not mo:
            return None
        return (int(mi.group(1)) if mi else 0, int(mo.group(1)) if mo else 0)


@dataclass
class AOIParameter:
    name: str
    data_type: str = 'BOOL'
    usage: str = 'Input'          # Input / Output / InOut
    required: bool = False


@dataclass
class AOIDefinition:
    name: str
    aoi_class: str = ''           # 'Safety' / 'Standard'
    parameters: List[AOIParameter] = field(default_factory=list)
    local_tags: List[Tag] = field(default_factory=list)
    logic: Optional[Routine] = None
    protected: bool = False
    description: str = ''

    def call_parameters(self) -> List[AOIParameter]:
        """Parameters that appear as operands in a ladder call (after the instance tag)."""
        return [p for p in self.parameters if p.required or p.usage == 'InOut']


@dataclass
class Program:
    name: str
    program_class: str = 'Standard'
    main_routine: str = ''
    disabled: bool = False
    tags: Dict[str, Tag] = field(default_factory=dict)
    routines: Dict[str, Routine] = field(default_factory=dict)

    @property
    def is_safety(self) -> bool:
        return self.program_class.lower() == 'safety'


@dataclass
class Task:
    name: str
    task_class: str = 'Standard'
    task_type: str = ''
    rate_ms: Optional[float] = None
    watchdog_ms: Optional[float] = None
    programs: List[str] = field(default_factory=list)

    @property
    def is_safety(self) -> bool:
        return self.task_class.lower() == 'safety'


@dataclass
class Project:
    source_name: str = ''
    source_format: str = ''       # 'L5K' / 'L5X'
    software_version: str = ''
    controller: str = ''
    processor: str = ''
    safety_level: str = ''
    safety_locked: Optional[bool] = None
    safety_tag_map: Dict[str, str] = field(default_factory=dict)   # standard tag -> safety tag
    tags: Dict[str, Tag] = field(default_factory=dict)             # controller scope
    programs: Dict[str, Program] = field(default_factory=dict)
    tasks: Dict[str, Task] = field(default_factory=dict)
    modules: Dict[str, Module] = field(default_factory=dict)
    aois: Dict[str, AOIDefinition] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)

    # ----------------------------------------------------------------- helpers
    @property
    def safety_task(self) -> Optional[Task]:
        for t in self.tasks.values():
            if t.is_safety:
                return t
        return None

    def safety_programs(self) -> List[Program]:
        """Programs scheduled in the safety task (fallback: every program with Class = Safety)."""
        task = self.safety_task
        names = list(task.programs) if task else []
        progs = [self.programs[n] for n in names if n in self.programs]
        for p in self.programs.values():
            if p.is_safety and p not in progs:
                progs.append(p)
        return progs

    def standard_programs(self) -> List[Program]:
        return [p for p in self.programs.values() if not p.is_safety]

    def module_by_prefix(self, prefix: str) -> Optional[Module]:
        for m in self.modules.values():
            if m.tag_prefix == prefix:
                return m
        return None

    def top_adapter(self, module: Module) -> Module:
        """The network module (adapter or device with an address) a chassis module hangs on."""
        seen = set()
        m = module
        while not m.address and m.parent in self.modules and m.parent not in seen and m.parent != m.name:
            seen.add(m.name)
            m = self.modules[m.parent]
        return m


def split_operand(op: str):
    """'Adapter_1:3:I.Pt04Data' -> ('Adapter_1:3:I', '.Pt04Data');  'Tag[2].5' -> ('Tag', '[2].5');
    program-scope operands keep their prefix: 'Prog\\Tag.0' -> ('Prog\\Tag', '.0')."""
    m = re.match(r'^((?:[A-Za-z_]\w*\\)?[A-Za-z_][\w]*(?::[\w]+)*)(.*)$', op)
    if not m:
        return op, ''
    return m.group(1), m.group(2)


IO_TAG_RE = re.compile(r'^(?P<prefix>.+?):(?P<kind>I|O|SI|SO|C|S)\.(?P<member>.+)$')


def io_parts(op: str):
    """'Adapter_1:3:I.Pt04Data' -> ('Adapter_1:3', 'I', 'Pt04Data') or None for non-I/O operands."""
    m = IO_TAG_RE.match(op)
    if not m:
        return None
    return m.group('prefix'), m.group('kind'), m.group('member')
