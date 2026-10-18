# =============================================================================
# Project : Safety Matrix Generator (GuardLogix SafetyTask -> Cause & Effect)
# File    : safety_matrix/i18n.py
# Author  : Robert Pietroń
# Revision: 1.0.0 (2026-10-18)
# Changes :
#   1.0.0 (2026-10-18) - First universal release: multi-language texts (PL, EN,
#                        FR, DA) with English fallback; ML value type used by
#                        the workbook writer for the in-workbook language switch.
# =============================================================================
"""Translations.

Every user-visible text is looked up by key in ``safety_matrix/locales/<lang>.py``
(dictionary ``TEXT``).  A missing key falls back to English.  Values are
``str.format`` templates; list values (legend tables) must have the same length
in every language.
"""
from __future__ import annotations

import importlib
from typing import Callable, Dict, Iterable, List, Sequence

LANGS = ('pl', 'en', 'fr', 'da')
LANG_NAMES = {'pl': 'polski', 'en': 'English', 'fr': 'français', 'da': 'dansk'}
EXCEL_LANG = {'pl': 'pl-PL', 'en': 'en-GB', 'fr': 'fr-FR', 'da': 'da-DK'}

_CATALOGS: Dict[str, dict] = {}


def catalog(lang: str) -> dict:
    if lang not in _CATALOGS:
        _CATALOGS[lang] = importlib.import_module(f'{__package__}.locales.{lang}').TEXT
    return _CATALOGS[lang]


class ML(dict):
    """A text in several languages: {'pl': '...', 'en': '...'}."""

    def __add__(self, other):
        if isinstance(other, ML):
            return ML({k: v + other.get(k, other.get('en', '')) for k, v in self.items()})
        return ML({k: v + str(other) for k, v in self.items()})

    def __radd__(self, other):
        return ML({k: str(other) + v for k, v in self.items()})

    def same(self) -> bool:
        return len(set(self.values())) <= 1

    def first(self) -> str:
        return next(iter(self.values()), '')

    def map(self, fn: Callable[[str], str]) -> 'ML':
        return ML({k: fn(v) for k, v in self.items()})


def text_of(value, lang: str) -> str:
    """Language view of a str / ML / config dict value."""
    if isinstance(value, dict):
        return value.get(lang) or value.get('en') or next(iter(value.values()), '')
    return '' if value is None else str(value)


class Tr:
    """Translator bound to a list of output languages."""

    def __init__(self, langs: Sequence[str]):
        unknown = [l for l in langs if l not in LANGS]
        if unknown:
            raise ValueError(f'unsupported language(s): {unknown}; available: {LANGS}')
        self.langs = list(langs)

    def s(self, lang: str, key: str, **kw) -> str:
        cat = catalog(lang)
        tpl = cat.get(key)
        if tpl is None:
            tpl = catalog('en').get(key)
        if tpl is None:
            raise KeyError(f'missing text key: {key}')
        if not kw:
            return tpl
        kw2 = {k: text_of(v, lang) for k, v in kw.items()}
        return tpl.format(**kw2)

    def __call__(self, key: str, **kw) -> ML:
        return ML({l: self.s(l, key, **kw) for l in self.langs})

    def has(self, key: str) -> bool:
        return key in catalog('en')

    def of(self, fn: Callable[[str], str]) -> ML:
        """Build an ML from a function of the language code."""
        return ML({l: fn(l) for l in self.langs})

    def ml(self, value) -> ML:
        """Config value (str or {lang: str}) -> ML."""
        return ML({l: text_of(value, l) for l in self.langs})

    def table(self, key: str) -> List[List[ML]]:
        """List-valued entry -> rows of ML cells (all languages must have the same shape)."""
        base = catalog('en')[key]
        rows = []
        for i, row in enumerate(base):
            cells = []
            for j, _ in enumerate(row):
                cells.append(ML({l: (catalog(l).get(key) or base)[i][j] for l in self.langs}))
            rows.append(cells)
        return rows

    def join(self, sep, items: Iterable) -> ML:
        items = list(items)
        return self.of(lambda l: (text_of(sep, l)).join(text_of(i, l) for i in items))
