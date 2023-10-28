# Selected industry is used as a search term in Yahoo! Finance, where subsequently the
# top "x" companies by market cap are gathered, analyzed for P/E multiples, trimmed into
# a group of "x" companies within "y" std. dev. of the median P/E multiples, and then exported
# into EITHER the Excel model, the scraper script, or both. AFTER trimming peer group and
# storing average variables, THEN run the rest of the scripts for each company.

#https://finance.yahoo.com/screener/predefined/sec-ind_ind-largest-equities_software-infrastructure

# Import Tkinter for GUI, ttk for Combobox
from tkinter import *
from tkinter import ttk


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

# Initialize GUI window
secwindow = Tk()
secwindow.title('Comps Industry')
secwindow.geometry('500x250')
ttk.Label(secwindow, text = 'Sector selection')

# Target sector and industry variables
target_sector = 'Technology'
target_industry = ''

# Check current value of sectorbox and assign to global variable target_sector
def check_sbox(event):
    global target_sector
    target_sector = sectorbox.get()

# Check current value of industrybox and assign to global variable target_industry
def check_ibox(event):
    global target_industry
    target_industry = industrybox.get()

def print_sector():#DEBUG
    print(target_sector)

def print_industry():#DEBUG
    print(target_industry)

# Create Combobox for sector selection
sector_choices = sectors
variable = StringVar(secwindow)
variable.set('Technology')
sectorbox = ttk.Combobox(secwindow, values = sector_choices)
sectorbox.bind('<<ComboboxSelected>>', check_sbox)
sec_butt= Button(secwindow, text="Print sector", command=print_sector)
sec_butt.pack()
sectorbox.pack(); secwindow.mainloop()

# Initialize GUI window
indwindow = Tk()
indwindow.title('Comps Industry')
indwindow.geometry('500x250')
ttk.Label(indwindow, text = 'Sector selection')

# Create Combobox for industry selection, with choices from chosen sector's paired industries
#industry_choices = paired[sectorbox.get()]
industry_choices = paired[target_sector]
industrybox = ttk.Combobox(indwindow, values = industry_choices, textvariable=variable)
industrybox.bind('<<ComboboxSelected>>', check_ibox)
ind_butt = Button(indwindow, text="Print industry", command=print_industry)
ind_butt.pack()
industrybox.pack(); indwindow.mainloop()

# INPUTS

# Target industry
# 

# Number of companies to include in industry group for valuation
# peers = 20

# Include companies within this many std. dev. of group's median P/E ratio
# range_factor = 3

