# Selected industry is used as a search term in Yahoo! Finance, where subsequently the
# top "x" companies by market cap are gathered, analyzed for P/E multiples, trimmed into
# a group of "x" companies within "y" std. dev. of the median P/E multiples, and then exported
# into EITHER the Excel model, the scraper script, or both. AFTER trimming peer group and
# storing average variables, THEN run the rest of the scripts for each company.

#https://finance.yahoo.com/screener/predefined/sec-ind_ind-largest-equities_software-infrastructure

# Import Tkinter for GUI, ttk for Combobox
from tkinter import *
from tkinter import ttk
root = Tk()

# Create list of sectors, and each sector's contained industries
sectors = ['Technology', 'Financial Services', 'Consumer Cyclical', 'Healthcare', 'Industrials', 'Communication Services', 'Consumer Defensive', 'Energy', 'Basic Materials', 'Real Estate', 'Utilities']
tech_inds = ['Software - Infrastructure', 'Semiconductors', 'Consumer Electronics', 'Software - Application', 'Information Technology Services', 'Semiconductor Equipment & Materials', 'Communication Equipment', 'Electronic Components', 'Computer Hardware', 'Scientific & Technical Instruments', 'Solar', 'Electronics & Computer Distribution']
fin_inds = ['Banks - Regional', 'Banks - Diversified', 'Insurance - Diversified', 'Credit Services', 'Asset Management', 'Insurance - Life', 'Capital Markets', 'Financial Data & Stock Exchanges', 'Insurance - Property & Casualty', 'Insurance Brokers', 'Insurance - Reinsurance', 'Insurance - Specialty', 'Shell Companies', 'Mortgage Finance', 'Financial Conglomerates']
cyclic_inds = ['']
health_inds = ['']
indust_inds = ['']
comm_inds = ['']
defense_inds = ['']
energy_inds = ['']
mater_inds = ['']
estate_inds = ['']
utils_inds = ['']
industries = [tech_inds, fin_inds, cyclic_inds, health_inds, indust_inds, comm_inds, defense_inds, energy_inds, mater_inds, estate_inds, utils_inds]

# Create a dictionary assigning each sector to a list of its industries
paired = dict(zip(sectors, industries))

# Create OptionMenu
choices = sectors
variable = StringVar(root)
variable.set('Technology')
w = ttk.Combobox(root, values = choices)
w.pack(); root.mainloop()

# INPUTS

# Target industry
# 

# Number of companies to include in industry group for valuation
# peers = 20

# Include companies within this many std. dev. of group's median P/E ratio
# range_factor = 3

