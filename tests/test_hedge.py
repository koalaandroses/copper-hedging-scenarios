import unittest
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from main import simulate

class HedgeTests(unittest.TestCase):
    def test_full_hedge_identity(self):
        data = simulate()
        full = data[data.target_hedge_ratio==1]
        np.testing.assert_allclose(full.net_procurement_cost_usd,
            100*(9050+full.basis_final_usd_per_tonne))
        self.assertEqual(len(data), 99)

    def test_unhedged_identity_and_long_direction(self):
        data = simulate()
        unhedged = data[data.target_hedge_ratio==0]
        np.testing.assert_allclose(unhedged.net_procurement_cost_usd, unhedged.unhedged_cost_usd)
        rising = data[(data.spot_change_pct==25)&(data.target_hedge_ratio==1)]
        self.assertTrue((rising.long_futures_pnl_usd>0).all())

    def test_rounding_and_bad_input(self):
        data = simulate(tonnes=110)
        full = data[data.target_hedge_ratio==1]
        self.assertTrue((full.contracts==4).all())
        self.assertTrue((full.effective_hedge_ratio<1).all())
        with self.assertRaises(ValueError):
            simulate(tonnes=-1)

if __name__ == '__main__':
    unittest.main()
