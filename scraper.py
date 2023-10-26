### script to pull income statement data from HTML tags on Yahoo! Finance and store it for use in an Excel model.

from datetime import datetime
import lxml
from lxml import html
import requests
import numpy as np
import pandas as pd

### set up request headers to simulate browser request

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'close',
    'DNT': '1', # Do Not Track Request Header 
    'Pragma': 'no-cache',
    'Referrer': 'https://google.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
}

### select target company to evaluate and get its statement URLs

symbol =  'CRSP'
print(symbol)#DEBUG

fin_url = f'https://finance.yahoo.com/quote/{symbol}/financials?p={symbol}'
cf_url = f'https://finance.yahoo.com/quote/{symbol}/cash-flow?p={symbol}'
print(fin_url)#DEBUG
print (cf_url)#DEBUG

### find target company income statements

# fetch the page
fin_page = requests.get(fin_url, headers=headers)
print(fin_page)#DEBUG

# parse the page with lxml
fin_tree = html.fromstring(fin_page.content)
print(fin_tree)#DEBUG

fin_tree.xpath("//h1/text()")

### find target company cash flows

# fetch the page
cf_page = requests.get(cf_url, headers=headers)
print(cf_page)#DEBUG

# parse the page with lxml
cf_tree = html.fromstring(cf_page.content)
print(cf_tree)#DEBUG

cf_tree.xpath("//h1/text()")

### store enterprise value, cash flows, EBIT (net income + interest + tax), EBITDA (EBIT + depreciation + amortization), and industry

### find industry peers

### find industry peer multiples
    ## EV/EBITDA, EV/EBIT, P/E

### find industry peer cash flows

###