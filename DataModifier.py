import pandas as pd

LOT_SIZE = {"NIFTY": 50, "BANKNIFTY": 25, "AXISBANK": 1200,
            "HDFCBANK": 550, "SBIN": 1500, "TATAPOWER": 3375,
            "ICICIBANK": 1375, "INDUSINDBK": 450, "TATASTEEL": 5500,
            "TVSMOTOR": 700, "HINDALCO": 1400, "LT": 300, 'KOTAKBANK': 400}


class DataModifier:
    def __init__(self) -> None:
        pass

    # Reset index
    def reset_index(df):
        df.reset_index(drop=True, inplace=True)

    def find_interval(df):
        length = len(df['strikePrice'])
        # print(df)
        return (int(df.at[length//2, 'strikePrice']) - int(df.at[length//2-1, 'strikePrice']))

    def column_rename(df):
        # Rename columns
        df = df.rename(columns={'ce_oi': 'ce_openinterest',
                                'ce_change_in_oi': 'ce_changeinopeninterest',
                                'ce_volume': 'ce_totaltradedvolume',
                                'ce_iv': 'ce_impliedvolatility',
                                'ce_ltp': 'ce_lastprice',
                                'strike_price': 'strikePrice',
                                'pe_ltp': 'pe_lastprice',
                                'pe_iv': 'pe_impliedvolatility',
                                'pe_volume': 'pe_totaltradedvolume',
                                'pe_change_in_oi': 'pe_changeinopeninterest',
                                'pe_oi': 'pe_openinterest'})
        return df

    def format_value(df):
        columns = ['pe_openinterest', 'pe_changeinopeninterest', 'pe_totaltradedvolume', 'pe_impliedvolatility',
                   'pe_lastprice', 'strikeprice', 'ce_openinterest', 'ce_changeinopeninterest',	'ce_totaltradedvolume',	'ce_impliedvolatility',  'ce_lastprice']
        for col in columns:
            if col == 'pe_lastprice' or col == 'ce_lastprice' or col == 'pe_impliedvolatility' or col == 'ce_impliedvolatility':
                df[col] = df[col].map('{:,.2f}'.format)
            else:
                df[col] = df[col].apply(lambda x: int(round(x) if pd.notnull(x) else 0))

    def convert_oi_size(df, ticker):
        lot_size = LOT_SIZE[ticker]
        columns = ['pe_openinterest', 'pe_changeinopeninterest',
                   'ce_openinterest', 'ce_changeinopeninterest',]
        for col in columns:
            df[col] = df[col] / lot_size

        return df

    def round_off_mkt_price(marketPrice, strikePriceInterval):
        # Divide the number by strikePriceInterval
        rounded_number = round(marketPrice / strikePriceInterval)

        # Multiply the rounded number by strikePriceInterval to get the nearest multiple of strikePriceInterval
        return (rounded_number * strikePriceInterval)


    def data_extractor(df, expiryDate, marketPrice):
        strikePriceCount = 8
        # Filter the data to only include rows where the 'CE.expiryDate' column is equal to expiry
        filtered_df = df[df['expiryDate'] == expiryDate]
        filtered_df.reset_index(drop=True, inplace=True)
                
        # Find the Strike Price increment interval
        strikePriceDiff = DataModifier.find_interval(filtered_df)
        print(strikePriceDiff)
        #  Convert Market price to nearest strike price
        marketPrice = DataModifier.round_off_mkt_price(marketPrice, strikePriceDiff)

        # OI range
        range = strikePriceDiff * strikePriceCount

        # Filtering the desired range of OI data
        filtered_df = filtered_df[filtered_df['strikePrice'] >= (
            marketPrice - range)]
        filtered_df = filtered_df[filtered_df['strikePrice'] <= (
            marketPrice + range)]

        # Drop unnecessary columns
        filtered_df = filtered_df.drop(columns=['expiryDate', 'PE.strikePrice', 'PE.expiryDate', 'PE.underlying', 'PE.identifier', 
                                                'PE.pchangeinOpenInterest', 'PE.change', 'PE.pChange', 'PE.totalBuyQuantity', 
                                                'PE.totalSellQuantity', 'PE.bidQty', 'PE.bidprice', 'PE.askQty', 'PE.askPrice', 
                                                'PE.underlyingValue', 'CE.strikePrice', 'CE.expiryDate', 'CE.underlying', 
                                                'CE.identifier', 'CE.pchangeinOpenInterest', 'CE.change', 'CE.pChange', 
                                                'CE.totalBuyQuantity', 'CE.totalSellQuantity', 'CE.bidQty', 'CE.bidprice', 
                                                'CE.askQty', 'CE.askPrice', 'CE.underlyingValue'])
        
        # Converting the OI  Size to Lot size instead of per shares
        # df = convert_oi_size(df, self.ticker)

        filtered_df.columns = filtered_df.columns.str.strip().str.lower() \
            .str.replace('.', '_').str.replace('(', '').str.replace(')', '').str.replace(' ', '_')

        # Reset the index
        DataModifier.reset_index(filtered_df)
        # print(filtered_df)

        # Rename the colunms
        # filtered_df = DataModifier.column_rename(filtered_df)

        # Reorder the columns
        filtered_df = filtered_df[['ce_openinterest',
                                'ce_changeinopeninterest',
                                'ce_totaltradedvolume',
                                'ce_impliedvolatility',
                                'ce_lastprice',
                                'strikeprice',
                                'pe_lastprice',
                                'pe_impliedvolatility',
                                'pe_totaltradedvolume',
                                'pe_changeinopeninterest',
                                'pe_openinterest']]
        
        return filtered_df
        