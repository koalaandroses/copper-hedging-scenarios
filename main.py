"""Illustrative one-period copper buyer futures hedge, no live market data."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent

def simulate(tonnes=100, spot_initial=9000, futures_initial=9050,
             contract_tonnes=25, hedge_ratios=(0,0.5,1.0)):
    if min(tonnes, spot_initial, futures_initial, contract_tonnes) <= 0:
        raise ValueError('Exposure, prices and contract size must be positive')
    rows = []
    for change in np.linspace(-0.25,0.25,11):
        spot_final = spot_initial*(1+change)
        for basis_final in (-150, 0, 150):
            # Basis convention: cash spot minus futures.
            futures_final = spot_final - basis_final
            for ratio in hedge_ratios:
                if not 0 <= ratio <= 1:
                    raise ValueError('Hedge ratio must lie within [0,1]')
                contracts = int(np.floor(tonnes*ratio/contract_tonnes))
                hedged_tonnes = contracts*contract_tonnes
                pnl = hedged_tonnes*(futures_final-futures_initial)
                cash_cost = tonnes*spot_final
                rows.append(dict(spot_change_pct=round(change*100, 6), basis_final_usd_per_tonne=basis_final,
                    target_hedge_ratio=ratio, contracts=contracts, effective_hedge_ratio=hedged_tonnes/tonnes,
                    unhedged_cost_usd=cash_cost, long_futures_pnl_usd=pnl,
                    net_procurement_cost_usd=cash_cost-pnl))
    return pd.DataFrame(rows)

def run():
    out = ROOT/'outputs'
    out.mkdir(exist_ok=True)
    scenarios = simulate()
    scenarios.to_csv(out/'scenarios.csv', index=False)
    fig, ax = plt.subplots(figsize=(9,5))
    for ratio, group in scenarios[scenarios.basis_final_usd_per_tonne==0].groupby('target_hedge_ratio'):
        ax.plot(group.spot_change_pct, group.net_procurement_cost_usd, marker='o', label=f'{ratio:.0%} hedge')
    ax.set(title='Copper buyer: net procurement cost at zero ending basis',
           xlabel='Change in spot price (%)', ylabel='Net cost (USD)')
    ax.legend()
    fig.tight_layout()
    fig.savefig(out/'hedge_comparison.png', dpi=170)
    plt.close(fig)
    summary = scenarios.groupby(['target_hedge_ratio','basis_final_usd_per_tonne']).net_procurement_cost_usd.agg(['min','max'])
    summary['range_usd'] = summary['max'] - summary['min']
    summary.to_csv(out/'cost_ranges.csv')
    text = '''# Scenario findings (illustrative assumptions)

A future copper buyer is exposed to rising spot prices and uses LONG futures.
Exposure is 100 tonnes; initial spot is USD 9,000/t; initial futures USD 9,050/t.
Assumed contract size is 25 tonnes (model parameter, not a verified exchange specification).
33 price/basis combinations are evaluated at 0%, 50% and 100% target hedge ratios.

For a full hedge, net cost = exposure * (initial futures + ending basis).
Price sensitivity disappears only under the model's matched quantities and horizon;
ending basis still matters. A hedge stabilizes cost and may forgo benefits of falling prices.
Whole-contract sizing uses floor rounding, so other exposure inputs may underhedge.

This is scenario analysis, not a forecast or a backtest. Costs, margin liquidity,
rolls, FX, taxes, delivery constraints and counterparty considerations are omitted.
No trading recommendation, real customer data or current market prices are included.
'''
    (out/'results.md').write_text(text)
    print(text)
    return scenarios

if __name__ == '__main__':
    run()
