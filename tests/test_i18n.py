# =============================================================================
# Project : Safety Matrix Generator (GuardLogix SafetyTask -> Cause & Effect)
# File    : tests/test_i18n.py
# Author  : Robert Pietroń
# Revision: 1.0.0 (2026-10-18)
# Changes :
#   1.0.0 (2026-10-18) - Completeness of the PL / EN / FR / DA catalogues and of
#                        the keys used by the code.
# =============================================================================
import os
import re
import string
import unittest

from safety_matrix import instructions as INS
from safety_matrix.i18n import LANGS, Tr, catalog

from .helpers import ROOT


def fields(s):
    return sorted({f[1] for f in string.Formatter().parse(s) if f[1]})


class TestCatalogues(unittest.TestCase):
    def test_same_keys_and_placeholders(self):
        en = catalog('en')
        for lang in LANGS:
            cat = catalog(lang)
            self.assertEqual(set(cat), set(en), lang)
            for k, v in en.items():
                if isinstance(v, str):
                    self.assertEqual(fields(v), fields(cat[k]), f'{lang}:{k}')
                else:
                    self.assertEqual([len(r) for r in v], [len(r) for r in cat[k]], f'{lang}:{k}')

    def test_static_keys_exist(self):
        en = catalog('en')
        missing = set()
        for dirpath, _, files in os.walk(os.path.join(ROOT, 'safety_matrix')):
            for f in files:
                if not f.endswith('.py') or 'locales' in dirpath:
                    continue
                src = open(os.path.join(dirpath, f), encoding='utf-8').read()
                for k in re.findall(r"(?:self\.t|T|self\.tr|\btr|self\.tr\.table)\('([a-z_][a-z_0-9.]+)'", src):
                    if k not in en and not k.endswith('.'):
                        missing.add(k)
        self.assertEqual(missing, set())

    def test_dynamic_keys_exist(self):
        en = catalog('en')
        for t in INS.DEVICE_TYPES:
            for p in ('type.', 'typedesc.', 'fn.', 'act.'):
                self.assertIn(p + t, en)
        for k in ('ROUT', 'CROUT', 'OUT', 'STO', 'SS1', 'SBC', 'SLS', 'INFO'):
            self.assertIn('kind.' + k, en)
            self.assertIn('kindshort.' + k, en)
        for c in ('X', 'X1', 'XB', 'XC', 'XM', 'N', 'S', 'SB', 'SC', 'SM', 'none'):
            self.assertIn(f'code.{c}.short', en)
            self.assertIn(f'code.{c}.full', en)
        src = open(os.path.join(ROOT, 'safety_matrix', 'audit.py'), encoding='utf-8').read()
        rules = set(re.findall(r"self\.add\((?:ALARM|DEAD|VERIFY|sev), '([a-z_0-9]+)',", src))
        rules |= {'reset_std_auto', 'reset_std', 'aux_not_energized', 'aux_no_device', 'free_cmp', 'free_data', 'free_latch',
                  'free_unk', 'free_mute', 'free_ext', 'direct_direct', 'direct_external', 'unused_inputs', 'unused_outputs'}
        for r in rules:
            self.assertIn('f.' + r, en, r)
        for c in set(re.findall(r"cls='([a-z_]+)'", src)):
            self.assertIn('cls.' + c, en)

    def test_translator(self):
        tr = Tr(['pl', 'en'])
        self.assertEqual(tr('w.zone_n', n=3), {'pl': 'STREFA 3', 'en': 'ZONE 3'})
        self.assertEqual(len(tr.table('abbr')), len(catalog('en')['abbr']))


if __name__ == '__main__':
    unittest.main()
