# Selected industry is used as a search term in Yahoo! Finance, where subsequently the
# top "x" companies by market cap are gathered, analyzed for P/E multiples, trimmed into
# a group of "x" companies within "y" std. dev. of the median P/E multiples, and then exported
# into EITHER the Excel model, the scraper script, or both. AFTER trimming peer group and
# storing average variables, THEN run following scripts for each company.