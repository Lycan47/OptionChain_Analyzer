import streamlit as st
import pandas as pd
from OI_Data import OI_Data
from Logger import Logger
from DataModifier import DataModifier as dm


log = Logger()

# -- Set page config
apptitle = "Lycan's Option Chain Analyzer"
st.set_page_config(page_title=apptitle, page_icon="chart_with_upwards_trend")

# Title the app
st.title("Lycan's Option Chain Analyzer")

st.markdown("""
 * Our app is the ultimate tool for options traders looking to make informed decisions.
 * With our option chain analysis feature, you can easily evaluate the potential risks and rewards of different options trades.
 * Simply select the index, and our app will provide a detailed list of all the relevant options and there details, including their prices, expiration dates, and OI data.
""")

st.sidebar.markdown("## Select Index, Expiry Date and enter current price")
# -- Get list of events
# Ticker input
tickers = ['NIFTY', 'BANKNIFTY', 'FINNIFTY', 'MIDCPNIFTY', 'AXISBANK', 'ICICIBANK',
           'HDFCBANK', 'SBIN', 'TATAPOWER', 'KOTAKBANK', 'INDUSINDBK', 'TATASTEEL', 'TVSMOTOR', 'HINDALCO', 'LT']

ticker_name = st.sidebar.selectbox("Select the Ticker", tickers)

oi_data, expiryDates, marketPrice = OI_Data.get_OI_data(ticker_name)
# print(expiryDates, marketPrice)

# Select Expiry Date
expiryDate = st.sidebar.selectbox('Expiry date:', expiryDates)

# Take Current Market Price input from the user
# mktPrice = st.sidebar.number_input('Enter current market price:', step=100)

# Add user enters Submit button on the sidebar, then execute
if st.sidebar.button('Submit'):
    df_oi = dm.data_extractor(oi_data, expiryDate, marketPrice)

    # Display the dataframe as a table
    st.table(df_oi)

    # Calculate the sum of ChangeINOI PE and CE
    changeinPE_sum = df_oi['pe_changeinopeninterest'].sum()
    changeinCE_sum = df_oi['ce_changeinopeninterest'].sum()

    values = [
        ['Change in PE Sum', changeinPE_sum],
        ['Change in CE Sum', changeinCE_sum],
        ['PCR', changeinPE_sum/changeinCE_sum]
    ]

    # Create a DataFrame with the values
    df_predict = pd.DataFrame(values, columns=['Property', 'Value'])
    # Format the values in the DataFrame
    df_predict['Value'] = df_predict['Value'].map('{:,.2f}'.format)

    # CSS to inject contained in a string
    hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """

    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)

    # Print the DataFrame in a table, and specify the column formatting
    st.table(df_predict)
