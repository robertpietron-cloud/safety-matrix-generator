# =============================================================================
# Project : Safety Matrix Generator (GuardLogix SafetyTask -> Cause & Effect)
# File    : tests/test_parser.py
# Author  : Robert Pietroń
# Revision: 1.0.0 (2026-10-18)
# Changes :
#   1.0.0 (2026-10-18) - Tests of the L5K / L5X / DOCX loaders and the model.
# =============================================================================
import os
import tempfile
import unittest
import zipfile

from safety_matrix.parsers import load_project, parse_l5k
from safety_matrix.parsers.l5k import parse_value, unescape

from .helpers import DEMO_L5K, DEMO_L5X, demo_project


class TestL5K(unittest.TestCase):
    def test_controller_and_tasks(self):
        p = demo_project()
        self.assertEqual(p.controller, 'DemoCell')
        self.assertEqual(p.processor, '5069-L320ERMS2')
        self.assertEqual(p.safety_tag_map, {'Std_ToSafety': 'Safety_FromStd'})
        self.assertEqual(p.safety_task.name, 'SafetyTask')
        self.assertEqual((p.safety_task.rate_ms, p.safety_task.watchdog_ms), (20.0, 20.0))
        self.assertEqual([x.name for x in p.safety_programs()], ['SafetyProgram'])

    def test_routines_and_comments(self):
        sp = demo_project().programs['SafetyProgram']
        self.assertEqual({k: len(v.rungs) for k, v in sp.routines.items()},
                         {'Inputs': 16, 'MainRoutine': 2, 'Outputs': 10, 'Old_Logic': 1})
        r0 = sp.routines['Inputs'].rungs[0]
        self.assertTrue(r0.comment.startswith('Reset from the control desk'))
        self.assertEqual(r0.text, 'XIC(Safety_FromStd[0].0)OSR(Reset_Storage,Reset_Edge)')

    def test_modules_prefix_and_connections(self):
        p = demo_project()
        self.assertEqual(p.modules['SafeIn_1'].tag_prefix, 'Local:1')
        self.assertEqual(p.modules['RemoteSafeIn'].tag_prefix, 'Remote_IO:1')
        self.assertEqual(p.modules['Robot_Drive'].tag_prefix, 'Robot_Drive')
        m = p.module_by_prefix('Remote_IO:1')
        con = m.connection('input')
        self.assertEqual((con.rpi_ms, con.timeout_multiplier, con.network_delay_multiplier, con.reaction_time_limit_ms),
                         (200.0, 4.0, 400.0, 1600.0))
        self.assertEqual(m.channel_comment('I', 'Pt00Data'), '-B30 infeed gate')
        self.assertEqual(m.channel_counts, (8, 0))
        self.assertEqual(p.top_adapter(m).name, 'Remote_IO')
        so = p.modules['Robot_Drive'].connection('output')
        self.assertEqual((so.tag_suffix, so.reaction_time_limit_ms, so.safety), ('SO', 60.064, True))

    def test_tags_values_and_comments(self):
        p = demo_project()
        t = p.tags['Std_ToSafety']
        self.assertEqual(t.comments['[0].0'], 'Reset push button -S9 (control desk)')
        sp = p.programs['SafetyProgram']
        self.assertTrue(sp.tags['Maintenance_Jumper'].bit_value(''))
        self.assertFalse(p.tags['Safety_FromStd'].bit_value('[0].3'))

    def test_aoi(self):
        a = demo_project().aois['TwoOfTwo']
        self.assertEqual([x.name for x in a.call_parameters()], ['In1', 'In2', 'Out'])
        self.assertEqual(len(a.logic.rungs), 2)

    def test_helpers(self):
        self.assertEqual(unescape('a$Nb$\'c$$'), "a\nb'c$")
        self.assertEqual(parse_value('[1,[2,3],16#FF]'), [1, [2, 3], 255])

    def test_word_paste_with_blank_lines(self):
        """An L5K pasted into Word (one paragraph per line, blank lines between) must parse identically."""
        lines = open(DEMO_L5K, encoding='utf-8').read().split('\n')
        paras = ''.join(f'<w:p><w:r><w:t xml:space="preserve">{_x(l)}</w:t></w:r></w:p><w:p/>' for l in lines)
        xml = ('<?xml version="1.0" encoding="UTF-8"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
               f'<w:body>{paras}</w:body></w:document>')
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, 'DemoCell.L5K.docx')
            with zipfile.ZipFile(path, 'w') as z:
                z.writestr('word/document.xml', xml)
            p = load_project(path)
        ref = demo_project()
        self.assertEqual({k: [r.text for r in v.routines['Inputs'].rungs] for k, v in p.programs.items() if v.is_safety},
                         {k: [r.text for r in v.routines['Inputs'].rungs] for k, v in ref.programs.items() if v.is_safety})

    def test_alias_scope_and_pending_edits(self):
        txt = '''CONTROLLER C (ProcessorType := "1756-L83ES", SafetyTagMap := "")
        TAG
          E1 : EMERGENCY_STOP (Class := Safety) := [0];
          ChA OF Local:1:I.Pt00Data (Description := "alias A");
        END_TAG
        PROGRAM SP (Class := Safety, MAIN := "M")
          TAG
            Ok : BOOL := 0;
          END_TAG
          ROUTINE M
            N: ESTOP(E1,MANUAL,ChA,Local:1:I.Pt01Data,R,R);
            I: XIC(E1.O1)OTE(Pending);
            N: XIC(E1.O1)OTE(Local:2:O.Pt00Data);
          END_ROUTINE
        END_PROGRAM
        TASK S (Class := Safety, Rate := 10, Watchdog := 10)
          SP;
        END_TASK
        END_CONTROLLER'''
        from safety_matrix.analysis import Analysis
        A = Analysis(parse_l5k(txt, 'inline.L5K'))
        self.assertEqual(A.devices['E1'].ch_a, 'Local:1:I.Pt00Data')       # alias resolved
        self.assertNotIn('Pending', A.lm.defs)                              # pending insert not executed
        self.assertEqual(A.code('E1', 'Local:2:O.Pt00Data'), 'X')


class TestL5X(unittest.TestCase):
    def test_l5x_equals_l5k(self):
        from safety_matrix.analysis import Analysis
        a = Analysis(load_project(DEMO_L5K))
        b = Analysis(load_project(DEMO_L5X))
        self.assertEqual(b.p.source_format, 'L5X')
        self.assertEqual({k: v.code for k, v in a.cells.items()}, {k: v.code for k, v in b.cells.items()})
        self.assertEqual(b.p.module_by_prefix('Remote_IO:1').connection('input').reaction_time_limit_ms, 1600.0)
        self.assertEqual(b.p.modules['SafeIn_1'].channel_comment('I', 'Pt04Data'), '-B10 robot door ch.A')


def _x(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


if __name__ == '__main__':
    unittest.main()
