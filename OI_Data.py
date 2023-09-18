import pandas as pd
import requests
import json


class OI_Data_ticker:
    def __init__(self) -> None:
        pass

    def get_OI_data(ticker):
        # define indices names
        indices = ["NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY"]
        # Set Headers and  cookies
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; '
                   'x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}

        main_url = "https://www.nseindia.com/"
        response = requests.get(main_url, headers=headers)
        cookies = response.cookies

        # Set the instrument type of the option chain page for data
        if ticker in indices:
            instrument = 'option-chain-indices'
        else:
            instrument = 'option-chain-equities'
            
        # Set the URL of the option chain data
        url = "https://www.nseindia.com/api/" + instrument + "?symbol=" + ticker

        print(url)
        # Send a GET request to the page
        response = requests.get(url, headers=headers, cookies=cookies)

        # Deserialize the response
        data = response.json()

        # Open the file in write mode
        with open('data.json', 'w') as file:
            # Write the data to the file
            json.dump(data, file)

        # Open the JSON file in read mode and load data
        with open('data.json', 'r') as file:
            # Load the contents of the file
            data = json.load(file)

        records = data['records']
        # Normalize the JSON data and create a DataFrame
        df_data = pd.json_normalize(records['data'])
        expiryDates = records['expiryDates']

        # Current Market Price
        marketPrice = records['underlyingValue']

        return df_data, expiryDates, marketPrice
