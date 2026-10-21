# =============================================================================
# Project : Safety Matrix Generator (GuardLogix SafetyTask -> Cause & Effect)
# File    : safety_matrix/logic.py
# Author  : Robert Pietroń
# Revision: 1.1.0 (2026-10-21)
# Changes :
#   1.0.0 (2026-10-18) - First universal release: boolean expression model of
#                        ladder logic (AND/OR/NOT, edges, timers, comparisons)
#                        and a deterministic evaluator with leaf classes
#                        (device, constant, standard-mapped, free).
#   1.1.0 (2026-10-21) - expr_text(): readable form of an expression.
# =============================================================================
"""Boolean expressions built from ladder rungs and their evaluation.

Expressions are tuples:
  ('const', bool) | ('var', name) | ('not', e) | ('and', a, b) | ('or', *legs)
  ('edge', e)                     one-shot (OSR/OSF/ONS) - always False in steady state
  ('timer', kind, preset, e, tag) timer done bit - steady state equals e
  ('cmp', text)                   comparison / data-dependent condition (free leaf)
"""
from __future__ import annotations

from typing import Callable, Dict, Iterable, List, Optional, Set, Tuple

TRUE = ('const', True)
FALSE = ('const', False)


def AND(a, b):
    if a == TRUE:
        return b
    if b == TRUE:
        return a
    if a == FALSE or b == FALSE:
        return FALSE
    return ('and', a, b)


def OR(*legs):
    legs = tuple(legs)
    if any(x == TRUE for x in legs):
        return TRUE
    legs = tuple(x for x in legs if x != FALSE)
    if not legs:
        return FALSE
    return legs[0] if len(legs) == 1 else ('or',) + legs


def VAR(name):
    return ('var', name)


def NOT(e):
    if e == TRUE:
        return FALSE
    if e == FALSE:
        return TRUE
    return ('not', e)


def vars_in(e, include_edges=False) -> List[str]:
    k = e[0]
    if k == 'var':
        return [e[1]]
    if k in ('and', 'or'):
        return [v for x in e[1:] for v in vars_in(x, include_edges)]
    if k == 'not':
        return vars_in(e[1], include_edges)
    if k == 'timer':
        return vars_in(e[3], include_edges)
    if k == 'edge' and include_edges:
        return vars_in(e[1], include_edges)
    if k == 'cmp':
        return [e[1]]
    return []


def expr_text(e) -> str:
    """Readable form: AND = ' · ', OR = '( a ∥ b )', NOT x, ↑(edge), constants 1/0."""
    k = e[0]
    if k == 'const':
        return '1' if e[1] else '0'
    if k == 'var':
        return e[1]
    if k == 'not':
        return 'NOT ' + expr_text(e[1])
    if k == 'and':
        return ' · '.join(expr_text(x) for x in e[1:])
    if k == 'or':
        return '(' + ' ∥ '.join(expr_text(x) for x in e[1:]) + ')'
    if k == 'edge':
        return '↑(' + expr_text(e[1]) + ')'
    if k == 'timer':
        return f'{e[4]}.DN'
    if k == 'cmp':
        return e[1]
    return '?'


class Evaluator:
    """Steady-state evaluation of tags defined in the ladder model.

    `defs`     tag -> list of definitions (expr, loc, instr); the last one wins (scan order)
    `leaf`     callable(name) -> ('const', bool) | ('dev', tag) | ('free', class)
    Self-references (seal-in contacts) evaluate True: the machine is assumed running.
    """

    def __init__(self, defs: Dict[str, list], leaf: Callable[[str], Tuple[str, object]]):
        self.defs = defs
        self.leaf = leaf
        self._leaf_cache: Dict[str, Tuple[str, object]] = {}

    def leaf_info(self, name):
        if name not in self._leaf_cache:
            self._leaf_cache[name] = self.leaf(name)
        return self._leaf_cache[name]

    def defined(self, name) -> bool:
        return name in self.defs and not name.startswith('DEV:')

    def expr_of(self, name):
        return self.defs[name][-1][0]

    # ----------------------------------------------------------------- evaluation
    def value(self, name, dev_off: Iterable[str] = (), free: Optional[Dict[str, bool]] = None) -> bool:
        sc = (frozenset(dev_off), free or {})
        memo: Dict[str, bool] = {}
        return self._ev(VAR(name), sc, frozenset(), memo)[0]

    def _ev(self, e, sc, stack, memo):
        k = e[0]
        if k == 'const':
            return e[1], False
        if k == 'not':
            v, c = self._ev(e[1], sc, stack, memo)
            return (not v), c
        if k == 'and':
            v1, c1 = self._ev(e[1], sc, stack, memo)
            if not v1:
                return False, c1
            v2, c2 = self._ev(e[2], sc, stack, memo)
            return v2, c1 or c2
        if k == 'or':
            cyc = False
            for x in e[1:]:
                v, c = self._ev(x, sc, stack, memo)
                cyc = cyc or c
                if v:
                    return True, cyc
            return False, cyc
        if k == 'edge':
            return False, False
        if k == 'timer':
            return self._ev(e[3], sc, stack, memo)
        if k == 'cmp':
            return bool(sc[1].get(e[1], False)), False
        if k == 'var':
            name = e[1]
            if name in stack:
                return True, True
            if name in memo:
                return memo[name], False
            if self.defined(name):
                v, c = self._ev(self.expr_of(name), sc, stack | {name}, memo)
                if not c:
                    memo[name] = v
                return v, c
            kind, val = self.leaf_info(name)
            if kind == 'dev':
                return (val not in sc[0]), False
            if kind == 'const':
                return bool(val), False
            return bool(sc[1].get(name, False)), False
        raise ValueError(f'bad expression {e!r}')

    # ----------------------------------------------------------------- structure
    def cone(self, name) -> Tuple[Set[str], Set[str]]:
        """(device tags, free leaves) that can influence `name` (edges excluded)."""
        devs, free, seen = set(), set(), set()
        stack = [VAR(name)]
        while stack:
            e = stack.pop()
            k = e[0]
            if k in ('and', 'or'):
                stack.extend(e[1:])
            elif k == 'not':
                stack.append(e[1])
            elif k == 'timer':
                stack.append(e[3])
            elif k == 'cmp':
                free.add(e[1])
            elif k == 'var':
                n = e[1]
                if n in seen:
                    continue
                seen.add(n)
                if self.defined(n):
                    stack.append(self.expr_of(n))
                else:
                    kind, val = self.leaf_info(n)
                    if kind == 'dev':
                        devs.add(val)
                    elif kind == 'free':
                        free.add(n)
        return devs, free

    def find_path(self, name, dev_tag, seen=frozenset()):
        """List of tags from `name` down to the device instruction output (edges excluded)."""
        if name in seen:
            return None
        if not self.defined(name):
            kind, val = self.leaf_info(name)
            return [] if (kind == 'dev' and val == dev_tag) else None
        for v in vars_in(self.expr_of(name)):
            p = self.find_path(v, dev_tag, seen | {name})
            if p is not None:
                return [name] + p
        return None

    def find_leaf_path(self, name, leaf, seen=frozenset()):
        """Like find_path but to an arbitrary leaf name (e.g. a standard-mapped bit)."""
        if name == leaf:
            return []
        if name in seen or not self.defined(name):
            return None
        for v in vars_in(self.expr_of(name)):
            p = self.find_leaf_path(v, leaf, seen | {name})
            if p is not None:
                return [name] + p
        return None
