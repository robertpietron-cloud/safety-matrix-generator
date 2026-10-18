# =============================================================================
# Project : Safety Matrix Generator (GuardLogix SafetyTask -> Cause & Effect)
# File    : tests/test_cli_headers.py
# Author  : Robert Pietroń
# Revision: 1.0.0 (2026-10-18)
# Changes :
#   1.0.0 (2026-10-18) - CLI smoke tests and the rule that every repository file
#                        carries a header (name, author, revision, changes).
# =============================================================================
import contextlib
import io
import os
import sys
import tempfile
import unittest

from safety_matrix.cli import main

from .helpers import DEMO_L5K, ROOT

sys.path.insert(0, os.path.join(ROOT, 'tools'))


class TestCLI(unittest.TestCase):
    def test_analyze_init_dump(self):
        with tempfile.TemporaryDirectory() as d:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(main(['analyze', DEMO_L5K, '-o', os.path.join(d, 'm.xlsx'), '--lang', 'en']), 0)
                self.assertEqual(main(['analyze', DEMO_L5K, '-o', os.path.join(d, 'm2.xlsx'), '--lang', 'da', '--fail-on-alarm']), 2)
                self.assertEqual(main(['init-config', DEMO_L5K, '-o', os.path.join(d, 'c.yaml')]), 0)
                self.assertEqual(main(['dump', DEMO_L5K, '--routine', 'Outputs']), 0)
            self.assertIn('9 devices', out.getvalue())
            self.assertTrue(os.path.exists(os.path.join(d, 'c.yaml')))
            self.assertEqual(main(['analyze', DEMO_L5K, '-c', os.path.join(d, 'c.yaml'), '-o', os.path.join(d, 'm3.xlsx')]), 0)


class TestHeaders(unittest.TestCase):
    def test_every_file_has_header(self):
        import check_headers
        self.assertEqual(check_headers.missing(ROOT), [])


if __name__ == '__main__':
    unittest.main()
