import pandas as pd
import datetime
import calendar

LOT_SIZE = {"NIFTY": 50, "BANKNIFTY": 25, "AXISBANK": 1200,
            "HDFCBANK": 550, "SBIN": 1500, "TATAPOWER": 3375}


class DataModifier:
    def __init__(self) -> None:
        pass

    # Reset index
    def reset_index(df):
        df.reset_index(drop=True, inplace=True)

    def find_interval(df):
        length = len(df['strikeprice'])
        print(df)
        return (int(df.at[length//2, 'strikeprice']) - int(df.at[length//2-1, 'strikeprice']))

    def column_drop(df):
        df = df.drop(columns=['ce_chart', 'ce_net_change', 'ce_bid_qty', 'ce_bid_price', 'ce_ask_price',
                     'ce_ask_quantity', 'pe_bid_qty', 'pe_bid_price', 'pe_ask_price', 'pe_ask_qty', 'pe_net_change', 'pe_chart'])
        return df

    def column_rename(df):
        # Rename columns
        df = df.rename(columns={'ce_oi': 'ce_openinterest',
                                'ce_change_in_oi': 'ce_changeinopeninterest',
                                'ce_volume': 'ce_totaltradedvolume',
                                'ce_iv': 'ce_impliedvolatility',
                                'ce_ltp': 'ce_lastprice',
                                'strike_price': 'strikeprice',
                                'pe_ltp': 'pe_lastprice',
                                'pe_iv': 'pe_impliedvolatility',
                                'pe_volume': 'pe_totaltradedvolume',
                                'pe_change_in_oi': 'pe_changeinopeninterest',
                                'pe_oi': 'pe_openinterest'})
        return df

    def next_thursdays():
        # Get the current date and time
        now = datetime.datetime.now()

        # Get the day of the week for the current date
        day_of_week = calendar.day_name[now.weekday()]

        # Check if the current day is Thursday
        if day_of_week != 'Thursday':
            # Change the date to the next Thursday
            next_thursday = now + datetime.timedelta((3-now.weekday()) % 7)
        else:
            next_thursday = now

        thursdays = []
        thursdays.append(next_thursday.strftime('%d-%b-%Y'))

        for i in range(2):
            next_thursday = next_thursday + datetime.timedelta(7)
            thursdays.append(next_thursday.strftime('%d-%b-%Y'))

        return thursdays

    def format_value(df):
        columns = ['pe_openinterest', 'pe_changeinopeninterest', 'pe_totaltradedvolume', 'pe_impliedvolatility',
                   'pe_lastprice', 'strikeprice', 'ce_openinterest', 'ce_changeinopeninterest',	'ce_totaltradedvolume',	'ce_impliedvolatility',  'ce_lastprice']
        for col in columns:
            if col == 'pe_lastprice' or col == 'ce_lastprice' or col == 'pe_impliedvolatility' or col == 'ce_impliedvolatility':
                df[col] = df[col].map('{:,.2f}'.format)
            else:
                df[col] = df[col].apply(lambda x: int(round(x)))

    def convert_oi_size(df, ticker):
        lot_size = LOT_SIZE[ticker]
        columns = ['pe_openinterest', 'pe_changeinopeninterest',
                   'ce_openinterest', 'ce_changeinopeninterest',]
        for col in columns:
            df[col] = df[col] / lot_size

        return df

    def extract_mkt_price(span_element):
        # Find the b element within the span element
        b_element = span_element.find('b')

        # Extract the text from the b element
        text = b_element.text

        # Split the text by the space character
        parts = text.split(' ')

        # Extract the second element of the list
        marketPrice = parts[1]

        return float(marketPrice)
    
    def round_off_mkt_price(marketPrice, strikePriceInterval):
        # Divide the number by strikePriceInterval
        rounded_number = round(marketPrice / strikePriceInterval)

        # Multiply the rounded number by strikePriceInterval to get the nearest multiple of strikePriceInterval
        return (rounded_number * strikePriceInterval)
