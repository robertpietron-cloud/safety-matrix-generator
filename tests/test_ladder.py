# =============================================================================
# Project : Safety Matrix Generator (GuardLogix SafetyTask -> Cause & Effect)
# File    : tests/test_ladder.py
# Author  : Robert Pietroń
# Revision: 1.0.0 (2026-10-18)
# Changes :
#   1.0.0 (2026-10-18) - Tests of the neutral-text tokenizer, the scan-order
#                        walker and the boolean evaluator.
# =============================================================================
import unittest

from safety_matrix.ladder import Instr, format_condition, seal_in_legs, split_args, tokenize
from safety_matrix.logic import AND, OR, VAR, Evaluator

from .helpers import demo_analysis


class TestTokenizer(unittest.TestCase):
    def test_nested_branches_and_args(self):
        t = tokenize('[XIC(a) XIC(b[1,2].3) ,XIO(c) [XIC(d),XIC(e)] ]CPT(x,(a+b)*2)OTE(y);'.rstrip(';'))
        self.assertEqual(t[0], '[')
        self.assertEqual(t[2], Instr('XIC', ['b[1,2].3']))
        self.assertEqual(t[-2], Instr('CPT', ['x', '(a+b)*2']))
        self.assertEqual(split_args('a, b[1,2], f(x,y)'), ['a', 'b[1,2]', 'f(x,y)'])

    def test_format_and_seal_in(self):
        toks = tokenize('[XIC(Reset_Edge) ,XIC(Out) ]XIC(Zone)XIO(Drive:SI.ConnectionFaulted)OTE(Out)')
        self.assertEqual(format_condition(toks, 'Out', lambda t: t == 'Reset_Edge', lambda t: 'Faulted' in t), 'Zone')
        self.assertEqual(seal_in_legs(toks, 'Out'), [['Reset_Edge'], ['Out']])


class TestEvaluator(unittest.TestCase):
    def test_seal_in_and_or(self):
        defs = {'out': [(AND(OR(VAR('rst'), VAR('out')), VAR('DEV:d1')), None, 'OTE')]}
        ev = Evaluator(defs, lambda n: ('dev', n[4:]) if n.startswith('DEV:') else ('free', 'std'))
        self.assertTrue(ev.value('out'))                       # seal-in: machine running
        self.assertFalse(ev.value('out', dev_off=['d1']))
        self.assertEqual(ev.find_path('out', 'd1'), ['out'])


class TestWalker(unittest.TestCase):
    def test_scan_order_and_aoi_inline(self):
        A = demo_analysis()
        self.assertEqual([r for _, r in A.lm.executed], ['MainRoutine', 'Inputs', 'Outputs'])
        self.assertIn('TwoOfTwo_1.Out', A.lm.defs)
        self.assertIn('Cell_OK', A.lm.defs)
        path = [t for t, _ in A.cells[('Gate_Infeed', 'Robot_Drive:SO.SafeTorqueOff')].path]
        self.assertEqual(path, ['Gate_Infeed.O1', 'Zone_Infeed_OK', 'TwoOfTwo_1.In2', 'TwoOfTwo_1.Both', 'TwoOfTwo_1.Out',
                                'Cell_OK', 'Robot_Drive:SO.SafeTorqueOff'])
        self.assertEqual(A.lm.flow[0][1], 'AFI')


if __name__ == '__main__':
    unittest.main()
