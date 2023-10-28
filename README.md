Execute main script. User inputs industry to create a portfolio in. Sorts industry by market cap, and for each company in range:

Executes comps scraper. Populates peer data, calculates average beta, and find multiples within *x* std. dev. of median. Fills Excel model with ticker. Output undervalue/overvalue for each, entered in JSON.

Executes DCF scraper to get income statements and cash flows. For each company in industry, also finds WACC inputs. Fills Excel model with inputs. Outputs overvalue/undervalue for each, entered in JSON.

Executes efficient frontier portfolio script. User selects a point along the curve, and selects a portfolio type (**risky/moderate/safe**). Calculates an optimally weighted portfolio and prints a buy list.

Risky: only one undervaluation required per stock

Moderate: DCF must be undervalued, comps dont matter

Safe: Both DCF and comps must be undervalued
