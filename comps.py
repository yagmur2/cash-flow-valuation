# Selected industry is used as a search term in Yahoo! Finance, where subsequently the
# top "x" companies by market cap are gathered, analyzed for P/E multiples, trimmed into
# a group of "x" companies within "y" std. dev. of the median P/E multiples, and then exported
# into EITHER the Excel model, the scraper script, or both. AFTER trimming peer group and
# storing average variables, THEN run the rest of the scripts for each company.

# https://finance.yahoo.com/screener/predefined/sec-ind_ind-largest-equities_software-infrastructure

# Import Tkinter for GUI, ttk for Combobox
from tkinter import *
from tkinter import ttk

# Create list of sectors, and each sector's contained industries
sectors = ['Technology', 'Financial Services', 'Consumer Cyclical', 'Healthcare', 'Industrials', 'Communication Services', 'Consumer Defensive', 'Energy', 'Basic Materials', 'Real Estate', 'Utilities']
tech_inds = ['Software - Infrastructure', 'Semiconductors', 'Consumer Electronics', 'Software - Application', 'Information Technology Services', 'Semiconductor Equipment & Materials', 'Communication Equipment', 'Electronic Components', 'Computer Hardware', 'Scientific & Technical Instruments', 'Solar', 'Electronics & Computer Distribution']
fin_inds = ['Banks - Regional', 'Banks - Diversified', 'Insurance - Diversified', 'Credit Services', 'Asset Management', 'Insurance - Life', 'Capital Markets', 'Financial Data & Stock Exchanges', 'Insurance - Property & Casualty', 'Insurance Brokers', 'Insurance - Reinsurance', 'Insurance - Specialty', 'Shell Companies', 'Mortgage Finance', 'Financial Conglomerates']
cyclic_inds = ['Internet Retail','Auto Manufacturers', 'Luxury Goods', 'Restaurants', 'Home Improvement Retail','Apparel Retail','Auto Parts','Specialty Retail', 'Travel Services','Footwear & Accessories', 'Leisure', 'Residential Construction','Resorts & Casinos', 'Lodging', 'Packaging & Containers', 'Gambling', 'Furnishings, Fixtures, & Appliances', 'Department Stores', 'Apparel Manufacturing', 'Auto & Truck Dealerships', 'Personal Services', 'Recreational Vehicles', 'Textile Manufacturing']
health_inds = ['Drug Manufacturers - General', 'Biotechnology', 'Healthcare Plans', 'Medical Devices', 'Diagnostics & Research', 'Medical Instruments & Supplies', 'Drug Manufacturers - Specialty & Generic','Medical Care Facilities', 'Medical Distribution', 'Health Information Services', 'Pharmaceutical Retailers']
indust_inds = ['Specialty Industrial Machinery', 'Aerospace & Defense', 'Conglomerates', 'Railroads', 'Farm & Heavy Construction Machinery', 'Specialty Business Services', 'Engineering & Construction', 'Integrated Freight & Logistics', 'Building Products & Equipment', 'Electrical Equipment & Parts', 'Staffing & Employment Services', 'Airlines', 'Waste Management', 'Marine Shipping', 'Industrial Distribution', 'Rental & Leasing Services', 'Consulting Services', 'Airports & Air Services', 'Tools & Accessories', 'Trucking', 'Infrastructure Operations', 'Security & Protection Services', 'Pollution & Treatment Controls', 'Metal Fabrication', 'Business Equipment & Supplies']
comm_inds = ['Internet Content & Information', 'Telecom Services', 'Entertainment', 'Electronic Gaming & Multimedia', 'Advertising Agencies', 'Publishing', 'Broadcasting']
defense_inds = ['Household & Personal Products', 'Packaged Foods', 'Discount Stores', 'Beverages - Non-Alcoholic', 'Beverages - Brewers', 'Tobacco', 'Grocery Stores', 'Beverages - Wineries & Distilleries', 'Confectioners', 'Farm Products', 'Food Distribution', 'Education & Training Services']
energy_inds = ['Oil & Gas Integrated', 'Oil & Gas E&P', 'Oil & Gas Midstream', 'Oil & Gas Refining & Marketing', 'Oil & Gas Equipment & Services', 'Thermal Coal', 'Uranium', 'Oil & Gas Drilling']
mater_inds = ['Specialty Chemicals', 'Other Industrial Metals & Mining', 'Gold', 'Building Materials', 'Steel', 'Chemicals', 'Copper', 'Agricultural Inputs', 'Paper & Paper Products', 'Aluminum' ,'Other Precious Metals & Mining', 'Lumber & Wood Production', 'Coking Coal', 'Silver']
estate_inds = ['Real Estate Services', 'REIT - Specialty', 'REIT - Industrial', 'REIT - Retail', 'Real Estate - Development', 'REIT - Residential', 'Real Estate - Diversified', 'REIT - Diversified', 'REIT - Healthcare Facilities', 'REIT - Office', 'REIT - Mortgage', 'REIT - Hotel & Motel']
utils_inds = ['Utilities - Regulated Electric', 'Utilities - Diversified', 'Utilities - Renewable', 'Utilities - Regulated Gas', 'Utilities - Independent Power Producers', 'Utilities - Regulated Water']
industries = [tech_inds, fin_inds, cyclic_inds, health_inds, indust_inds, comm_inds, defense_inds, energy_inds, mater_inds, estate_inds, utils_inds]

# Target sector and industry variables
target_sector = ''
target_industry = ''

# Number of companies to include in industry group for valuation
peersize = 20

# Include companies within this many std. dev. of group's median P/E ratio
range_factor = 3

# Create a dictionary assigning each sector to a list of its industries
paired = dict(zip(sectors, industries))

# Initialize GUI window
window = Tk()
window.title('Comps Inputs')
window.geometry('500x250')
ttk.Label(window, text = 'Sector/Industry Selection')

# Updates industry data to correspond to the sector chosen
# Checks current value of industrybox and assigns to global variable target_industry
def check_ibox(event):
    global target_industry
    industrybox['values'] = paired[sectorbox.get()]
    target_industry = industrybox.get()

# Updates industry data to correspond to the sector chosen
# Checks current value of sectorbox and assigns to global variable target_sector
def check_sbox(event):
    global target_sector
    industrybox['values'] = paired[sectorbox.get()]
    target_sector = sectorbox.get()

# Checks user input for industry peer group size. Only accepts integers greater than zero.
def check_peerbox():
    global peersize
    
    # tries to convert input to int
    try: 
        # if it converts and is > 0, sets peer size
        if int(peerbox.get()) > 0:
            peersize = int(peerbox.get())
        # otherwise is nonzero
        else: print('ERROR: Must be a nonzero integer')

    # if input can't be changed to int, invalid
    except: print('ERROR: Must be a nonzero integer')

    print(peersize)#DEBUG

#-----------------------------DEBUG ASSISTANCE----------------------------
def print_sector():
    print(target_sector)

sec_butt= Button(window, text="(DEBUG) Print sector", command=print_sector)

def print_industry():
    print(target_industry)

ind_butt = Button(window, text="(DEBUG) Print industry", command=print_industry)
#------------------------------------------------------------------------

# Create Combobox for industry selection
industrybox = ttk.Combobox(window)

# When industry is selected, run check_ibox method to assign target_industry
industrybox.bind('<<ComboboxSelected>>', check_ibox)

# Create Combobox for sector selection, with values set as dict keys
sectorbox = ttk.Combobox(window, values = list(paired.keys()))

# When sector is selected, run check_sbox method to assign target_sector
sectorbox.bind('<<ComboboxSelected>>', check_sbox)

peerbox = ttk.Entry(window, width=25)
peer_butt = Button(window, text = 'Confirm Inputs', command=check_peerbox)


sectorbox.pack(); sec_butt.pack(); industrybox.pack(); ind_butt.pack(); peerbox.pack(); peer_butt.pack(); window.mainloop()

# INPUTS

# (DONE) Target industry

# (DONE) Number of companies to include in industry group for valuation

# Include companies within this many std. dev. of group's median P/E ratio
# range_factor = 3

# OUTPUTS

# List of company tickers

