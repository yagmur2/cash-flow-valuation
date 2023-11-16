### script to pull income statement data from HTML tags on (WSJ Markets? Use something with free 5+ year data) Yahoo! Finance and store it for use in valuation.

from datetime import datetime
import lxml
from lxml import html
import requests
import numpy_financial as np
import pandas as pd
import yfinance as yf

# Forecast length
years = 5
n = 1
print('Short-term forecast length: ' + str(years) + ' years' + '\n')

# Long term growth rate
lg = .02
print('Terminal growth rate: ' + str(lg) + '\n')

# stock currently examined TODO: make dynamic from list in ind-sample.json
peer = yf.Ticker("MSFT")
price = peer.history()['Close'].iloc[-1]

# WACC inputs TODO: make beta and any other retrievables dynamic

# Risk-free rate
rf = .04
# Beta of stock
beta = 1.1
# Expected return of market
rm = .1
# Weight of equity for company
pct_eq = .8
# Weight of liabilities for company
pct_debt = 1 - pct_eq
# Cost of equity
cost_eq = rf + beta * (rm - rf)
# Cost of debt
cost_debt = .1
# Tax rate
tax = .2
# Weighted average cost of capital (Discount rate)
wacc = pct_eq * cost_eq + pct_debt * cost_debt * (1 - tax)
print('WACC/Discount rate: ' + str(wacc) + '\n')

# take fcf column and reverse dates
fcf = peer.cashflow.iloc[0]
fcf = fcf[::-1]
print('Free cash flows for past 5 years of ' + str(peer) + ': \n' + str(fcf) + '\n')

# short term growth rate
sg = fcf.pct_change()
sg = sg.fillna(0).tolist()
sg = sum(sg)/4
print('Short term growth rate: ' + str(sg) + '\n')

# Calculate short-term cash flow forecasts
future_fcf = [0] * years
future_fcf[0] = fcf[-1] * (1 + sg)
while n < years :
    future_fcf[n] = future_fcf[n - 1] * (1 + sg)
    n += 1
print('Short term forecasted cash flows: ' + str(future_fcf) + '\n')

# Calculate perpetuity and add to previous cash flows
tv = (future_fcf[-1] * (1 + lg))/(wacc - lg)
print('Terminal value: ' + str(tv) + '\n')

valuation = np.npv(wacc, future_fcf) + np.pv(wacc, 1, 0, tv)
print('Market cap valuation: ' + str(valuation) + '\n')

# Create verdict
if valuation < peer.fast_info['market_cap'] :
    print('Overvalued')
else : print('Undervalued')

### store enterprise value, cash flows, EBIT (net income + interest + tax), EBITDA (EBIT + depreciation + amortization), and industry

### find industry peers

### find industry peer multiples
    ## EV/EBITDA, EV/EBIT, P/E

### find industry peer cash flows

###