# Scenario findings (illustrative assumptions)

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
