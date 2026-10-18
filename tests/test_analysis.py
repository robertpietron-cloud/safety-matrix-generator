# =============================================================================
# Project : Safety Matrix Generator (GuardLogix SafetyTask -> Cause & Effect)
# File    : tests/test_analysis.py
# Author  : Robert Pietroń
# Revision: 1.0.0 (2026-10-18)
# Changes :
#   1.0.0 (2026-10-18) - Expected cause & effect matrix of the DemoCell export
#                        and the automatic audit findings.
# =============================================================================
import unittest

from safety_matrix.audit import run_audit

from .helpers import demo_analysis

STO_R = 'Robot_Drive:SO.SafeTorqueOff'
STO_P = 'Press_Drive:SO.SafeTorqueOff'
SERVICE = 'Local:2:O.Pt05Data'
INFO = 'Safety_ToStd[0].0'
DIRECT = 'Local:1:I.Pt06Data'

EXPECTED = {
    ('EStop_Panel', 'K1K2_Main'): 'X', ('EStop_Robot', 'K1K2_Main'): 'X', ('EStop_Spare', 'K1K2_Main'): 'N',
    ('Door_Robot', 'K1K2_Main'): 'X',
    ('EStop_Panel', 'Valve_Press'): 'X', ('Door_Press', 'Valve_Press'): 'XM',
    ('EStop_Panel', STO_R): 'X', ('EStop_Robot', STO_R): 'X', ('EStop_Spare', STO_R): 'N', ('Door_Robot', STO_R): 'X',
    ('Gate_Infeed', STO_R): 'X1', ('LC_Infeed', STO_R): 'XB',
    ('EStop_Panel', STO_P): 'X', ('Door_Press', STO_P): 'XM', (DIRECT, STO_P): 'X1',
    ('EStop_Panel', SERVICE): 'X', ('Door_Robot', SERVICE): 'XC', ('LC_Infeed', SERVICE): 'XC',
    ('EStop_Panel', INFO): 'S', ('EStop_Robot', INFO): 'S', ('EStop_Spare', INFO): 'N', ('Door_Robot', INFO): 'S',
}


class TestMatrix(unittest.TestCase):
    def setUp(self):
        self.A = demo_analysis()

    def test_devices(self):
        A = self.A
        self.assertEqual(len(A.devices), 9)
        self.assertEqual(A.devices['Door_Robot'].instr, 'DCS')
        self.assertEqual((A.devices['Door_Robot'].ch_a, A.devices['Door_Robot'].reset), ('Local:1:I.Pt04Data', 'Reset_Edge'))
        self.assertFalse(A.devices['Door_Robot'].heuristic)
        self.assertIs(A.devices['EStop_Robot'].reset_manual, False)
        self.assertTrue(A.devices['EStop_Spare'].const_channels)
        self.assertTrue(A.devices['Gate_Infeed'].equal_channels)
        self.assertEqual(A.devices[DIRECT].kind, 'direct')
        self.assertEqual(A.devices['LC_Infeed'].type, 'LIGHT CURTAIN')
        self.assertEqual(A.devices['Switch_Unused'].n_eff, 0)

    def test_effects(self):
        keys = [e.key for e in self.A.matrix_effects()]
        self.assertEqual(sorted(keys), sorted(['K1K2_Main', 'Valve_Press', STO_R, STO_P, SERVICE, INFO]))
        k1 = self.A.effect('K1K2_Main')
        self.assertEqual((k1.kind, k1.outputs), ('ROUT', ['Local:2:O.Pt00Data', 'Local:2:O.Pt01Data']))
        self.assertEqual(self.A.effect('Valve_Press').kind, 'CROUT')
        lock = self.A.effect('Local:2:O.Pt04Data')
        self.assertEqual((lock.in_matrix, lock.reason), (False, 'no_device'))

    def test_cells_exact(self):
        got = {k: c.code for k, c in self.A.cells.items()}
        self.assertEqual(got, EXPECTED)

    def test_cell_details(self):
        A = self.A
        self.assertEqual(A.cells[('LC_Infeed', STO_R)].bypass, ['Safety_FromStd[0].2', 'Safety_FromStd[0].3'])
        self.assertEqual(A.cells[('Door_Robot', SERVICE)].partners, ['LC_Infeed'])
        self.assertEqual(A.cells[('Door_Press', 'Valve_Press')].conditions, ['EQU(Press_Mode,2)'])
        self.assertEqual(A.cells[('EStop_Panel', STO_P)].delay_ms, 2000.0)
        self.assertIsNone(A.cells[(DIRECT, STO_P)].delay_ms)
        self.assertEqual(A.stop_category([A.cells[('EStop_Panel', STO_P)]]), '1 (2000 ms)')

    def test_metadata(self):
        A = self.A
        e = A.effect(STO_R)
        manual, auto = A.restart_legs(e)
        self.assertEqual((manual, auto), (['Reset_Edge'], []))
        self.assertEqual(A.enable_of(A.effect('K1K2_Main'))[0], 'Zone_Robot_OK')
        self.assertEqual(A.std_source('Safety_FromStd[0].0'), 'Std_ToSafety[0].0')
        self.assertIn("MainProgram/MainRoutine R0 OTE: Reset_PB 'Reset push button -S9'", A.std_trace('Safety_FromStd[0].0'))
        m, c = A.input_connection(A.devices['Gate_Infeed'])
        self.assertEqual(c.reaction_time_limit_ms, 1600.0)


class TestAudit(unittest.TestCase):
    def test_findings(self):
        F = run_audit(demo_analysis(), 1000)
        keys = {(f.severity, f.key) for f in F}
        for k in [('ALARM', 'const_channels'), ('ALARM', 'std_bypass'), ('ALARM', 'std_mute'), ('ALARM', 'std_parallel'),
                  ('ALARM', 'estop_auto'), ('ALARM', 'equal_channels'), ('ALARM', 'afi'), ('ALARM', 'const_branch'),
                  ('DEAD', 'dead_device'), ('DEAD', 'unused_tags'), ('DEAD', 'uncalled_routine'), ('DEAD', 'unused_inputs'),
                  ('VERIFY', 'crtl_inputs'), ('VERIFY', 'or_devices'), ('VERIFY', 'free_cmp'), ('VERIFY', 'direct_direct'),
                  ('VERIFY', 'stop_cat1'), ('VERIFY', 'aux_no_device'), ('VERIFY', 'reset_std'), ('VERIFY', 'completeness')]:
            self.assertIn(k, keys)
        pri = [f for f in F if f.priority]
        self.assertEqual(len(pri), 1)
        self.assertEqual(pri[0].params['crtl'], '1600')
        afi = next(f for f in F if f.key == 'afi')
        self.assertEqual((afi.routine, afi.rungs), ('Inputs', '15'))
        sev = [f.severity for f in F]
        self.assertEqual(sev, sorted(sev, key=['ALARM', 'DEAD', 'VERIFY'].index))


if __name__ == '__main__':
    unittest.main()
