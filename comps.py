# Selected industry is used as a search term in Yahoo! Finance, where subsequently the
# top "x" companies by market cap are gathered, analyzed for P/E multiples, trimmed into
# a group of "x" companies within "y" std. dev. of the median P/E multiples, and then exported
# into EITHER the Excel model, the scraper script, or both. AFTER trimming peer group and
# storing average variables, THEN run the rest of the scripts for each company.

# -----------------------------GLOBAL VARIABLES-----------------------------
# Import Tkinter for GUI, ttk for Combobox
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
import json

# Request headers to simulate browser request
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

# Once we get our list of industry tickers, we store it here
industry_path = 'data/ind-sample.json'

# The URL of the industry's top 100 Market Caps TODO: Make this dynamically change based on user selected sector/industry
url = "https://finance.yahoo.com/screener/predefined/sec-ind_ind-largest-equities_software-infrastructure?offset=0&count=100"

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

# Create a dictionary assigning each sector to a list of its industries
paired = dict(zip(sectors, industries))

# Target sector and industry variables
target_sector = ''
target_industry = ''

# Number of companies to include in industry group for valuation
peersize = 20

# Include companies within this many std. dev. of group's median P/E ratio
range_factor = 3
# --------------------------------------------------------------------------

# ---------------------------------FUNCTIONS--------------------------------
# Initialize GUI window
window = ctk.CTk()
window.title('Comps Inputs')
window.geometry('500x250')

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
    window.destroy()

# Checks user input for sample P/E std. dev. Only accepts integers greater than zero.
def check_rangebox():
    global range_factor

    # tries to convert input to int
    try: 
        # if it converts and is > 0, sets peer size
        if int(rangebox.get()) > 0:
            range_factor = int(rangebox.get())
        # otherwise is nonzero
        else: print('ERROR: Must be a nonzero integer')

    # if input can't be changed to int, invalid
    except: print('ERROR: Must be a nonzero integer')

    print(range_factor)#DEBUG
    window2.destroy()

# TODO: Dynamically change requests URL based on selected industry
def industryURL(x):
    print(True)
# -------------------------------------------------------------------------

# -----------------------------DEBUG ASSISTANCE----------------------------
def print_sector():
    print(target_sector)

sec_butt= ctk.CTkButton(window, text="(DEBUG) Print sector", command=print_sector)

def print_industry():
    print(target_industry)

ind_butt = ctk.CTkButton(window, text="(DEBUG) Print industry", command=print_industry)
# -------------------------------------------------------------------------

# --------------------------------INDUSTRY SELECTION-----------------------
# Create Combobox for industry selection
industrybox = ttk.Combobox(window, justify='center')

# When industry is selected, run check_ibox method to assign target_industry
industrybox.bind('<<ComboboxSelected>>', check_ibox)

# Create Combobox for sector selection, with values set as dict keys
sectorbox = ttk.Combobox(window, values = list(paired.keys()), justify='center')

# When sector is selected, run check_sbox method to assign target_sector
sectorbox.bind('<<ComboboxSelected>>', check_sbox)

# Create sample size entry field
peerbox = ttk.Entry(window, width=24, justify='center')
peerbox.insert(0, str(peersize))
peer_butt = ctk.CTkButton(window, text = 'Confirm Inputs', command=check_peerbox)

sectorbox.pack(); sec_butt.pack(); industrybox.pack(); ind_butt.pack(); peerbox.pack(); peer_butt.pack(); window.mainloop()
# -------------------------------------------------------------------------

# --------------------------------TRIMMING MODIFIERS-----------------------
# Create 2nd window
window2 = ctk.CTk()
window2.title("Raw Sample Analysis")
window2.geometry('500x500')

# Create entry field for P/E std. dev. range and button to validate input
rangebox = ttk.Entry(window2, width=24, justify='center')
rangebox.insert(0, str(range_factor))
range_butt = ctk.CTkButton(window2, text = 'Confirm P/E range', command = check_rangebox)

rangebox.pack(); range_butt.pack(); window2.mainloop()
# -------------------------------------------------------------------------

# --------------------------------SYMBOL RETRIEVAL-------------------------
# Send a GET request to the url and get the response
response = requests.get(url, headers=headers)

# Parse the response content as HTML using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find the table element that contains the ticker information
table = soup.find("table", class_="W(100%)")

# Find all the table rows that contain the ticker information
rows = table.find_all("tr", class_="simpTblRow")

# Create an empty list to store the tickers
tickers = []

# Loop through each row and extract the ticker symbol
for row in rows:
    # Find the first table cell element that has the class "Va(m)"
    td = row.find("td", class_="Va(m)")
    # Get the text content of the td element
    ticker = td.text
    # Append the ticker to the list
    tickers.append(ticker)

# Print the list of tickers
print(tickers)

# Open the file in write mode
with open(industry_path, "w") as f:
    # Dump the list of tickers as a json array
    json.dump(tickers, f)

# Print a success message
print(f"Saved {len(tickers)} tickers to {industry_path}")
# ------------------------------------------------------------------------

