import pandas as pd
import json
import requests
from DataCleaner import DataCleaner as dc

thursdays = dc.next_thursdays()

class OI_Data:
    def __init__(self,  marketPrice, index_name, expirydate=thursdays[0],  strikePriceCount=4):
        self.index_name = index_name
        self.marketPrice = marketPrice
        self.expirydate = expirydate
        self.strikePriceCount = strikePriceCount

    def get_OI_data(self):
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; '
                   'x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}

        main_url = "https://www.nseindia.com/"
        response = requests.get(main_url, headers=headers)
        cookies = response.cookies

        url = "https://www.nseindia.com/api/option-chain-indices?symbol=" + self.index_name
        oi_data = requests.get(url, headers=headers, cookies=cookies)

        # Deserialize the response
        data = oi_data.json()

        # Extract the desired Records data node
        records = data['records']

        # Normalize the JSON data and create a DataFrame
        df = pd.json_normalize(records['data'])

        # Clean header
        dc.clean_header(df)
        
        # Filter the data to only include rows where the 'CE.expirydate' column is equal to expiry
        filtered_df = df[df['expirydate'] == self.expirydate]

        dc.reset_index(filtered_df)

        # Find the Strike Price increment interval
        strikePriceDiff = dc.find_interval(filtered_df)

        # OI range
        range = strikePriceDiff * self.strikePriceCount

        # Filtering the desired range of OI data
        filtered_df = filtered_df[filtered_df['strikeprice'] >= (
            self.marketPrice - range)]
        filtered_df = filtered_df[filtered_df['strikeprice'] <= (
            self.marketPrice + range)]

        dc.reset_index(filtered_df)

        dc.column_drop(filtered_df)

        return filtered_df
