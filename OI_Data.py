import pandas as pd
import requests
from bs4 import BeautifulSoup
from DataModifier import DataModifier as dm
import numpy as np

thursdays = dm.next_thursdays()


class OI_Data_Indices:
    def __init__(self,  ticker, expirydate=thursdays[0],  strikePriceCount=4):
        self.ticker = ticker
        self.expirydate = expirydate
        self.strikePriceCount = strikePriceCount

    def get_OI_data(self):
        # Set Headers and  cookies
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; '
                   'x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}

        main_url = "https://www.nseindia.com/"
        response = requests.get(main_url, headers=headers)
        cookies = response.cookies

        if self.ticker == 'NIFTY' or self.ticker == 'BANKNIFTY':
            instrument = 'OPTIDX'
            # Set the URL of the option chain page for INDEX
            url = "https://www1.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?segmentLink=17&instrument=" + \
                instrument + "&symbol=" + self.ticker + "&date=" + self.expirydate
        else:
            instrument = 'OPTSTK'
            # Set the URL of the option chain page for Equity
            url = "https://www1.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbolCode=-10002&symbol=" + \
                self.ticker + "&symbol=" + self.ticker + \
                "&instrument=-&date=-&segmentLink=17&symbolCount=2&segmentLink=17"

        print(url)
        # Send a GET request to the page
        response = requests.get(url, headers=headers, cookies=cookies)

        # Parse the HTML data from the response
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the span element for extracting current market price
        span_element = soup.find('span')

        marketPrice = dm.extract_mkt_price(span_element)

        # Find the table containing the option chain data
        table = soup.find('table', {'id': 'octable'})

        # Extract the rows from the table
        table_rows = table.find_all('tr')

        # Create an empty list to store the option chain data
        data = []

        # Iterate over the rows and extract the option chain data
        l = []
        for tr in table_rows:
            td = tr.find_all('td')
            if td:
                row = [tr.text for tr in td]
                l.append(row)

        def np_float(x):
            try:
                y = x.lstrip().rstrip().replace(',', '')
                return np.float64(y)
            except:
                return np.nan

        arr = []
        for r in l:
            row = [np_float(x) for x in r]
            arr.append(row)

        df = pd.DataFrame(arr)
        df.columns = ['ce_chart', 'ce_oi', 'ce_change_in_oi', 'ce_volume', 'ce_iv', 'ce_ltp', 'ce_net_change', 'ce_bid_qty', 'ce_bid_price', 'ce_ask_price', 'ce_ask_quantity',
                      'strike_price', 'pe_bid_qty', 'pe_bid_price', 'pe_ask_price', 'pe_ask_qty', 'pe_net_change', 'pe_ltp', 'pe_iv', 'pe_volume', 'pe_change_in_oi', 'pe_oi', 'pe_chart']

        # Drop unnecessary columns and rename them
        df = dm.column_drop(df)
        df = dm.column_rename(df)

        # Find the Strike Price increment interval
        strikePriceDiff = dm.find_interval(df)

        #  Convert Market price to nearest strike price
        marketPrice = dm.round_off_mkt_price(marketPrice, strikePriceDiff)

        # OI range
        range = strikePriceDiff * self.strikePriceCount

        # Filtering the desired range of OI data
        df = df[df['strikeprice'] >= (
            marketPrice - range)]
        df = df[df['strikeprice'] <= (
            marketPrice + range)]

        # Converting the OI  Size to Lot size instead of per shares
        # df = dm.convert_oi_size(df, self.ticker)

        dm.reset_index(df)

        return df
