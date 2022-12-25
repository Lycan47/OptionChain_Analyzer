import pandas as pd
import datetime
import calendar


class DataCleaner:
    def __init__(self) -> None:
        pass

    # simple function to make headers nicer
    def clean_header(df):
        df.columns = df.columns.str.strip().str.lower().str.replace(
            '.', '_').str.replace('(', '').str.replace(')', '').str.replace(' ', '_')

    # Reset index
    def reset_index(df):
        df.reset_index(drop=True, inplace=True)

    def find_interval(df):
        length = len(df['strikeprice'])
        print(df)
        return (int(df.at[length//2, 'strikeprice']) - int(df.at[length//2-1, 'strikeprice']))

    def column_drop(df):
        df = df.drop(columns=['expirydate', 'pe_strikeprice', 'pe_expirydate', 'pe_underlying', 'pe_identifier', 'pe_pchangeinopeninterest', 'pe_change', 'pe_pchange', 'pe_totalbuyquantity', 'pe_totalsellquantity', 'pe_bidqty', 'pe_bidprice', 'pe_askqty', 'pe_askprice',
                     'pe_underlyingvalue', 'ce_strikeprice', 'ce_expirydate', 'ce_underlying', 'ce_identifier', 'ce_pchangeinopeninterest', 'ce_change', 'ce_pchange', 'ce_totalbuyquantity', 'ce_totalsellquantity', 'ce_bidqty', 'ce_bidprice', 'ce_askqty', 'ce_askprice', 'ce_underlyingvalue'], inplace=True)

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
        columns = ['strikeprice',	'pe_openinterest',	'pe_changeinopeninterest',	'pe_totaltradedvolume',	'pe_impliedvolatility',	'pe_lastprice', 'ce_openinterest',	'ce_changeinopeninterest',	'ce_totaltradedvolume',	'ce_impliedvolatility',  'ce_lastprice']
        for col in columns:
            if col == 'pe_lastprice' or col == 'ce_lastprice':
                df[col] = df[col].apply(lambda x: round(x, 2))
            else:
                df[col] = df[col].apply(lambda x: int(round(x)))