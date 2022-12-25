import streamlit as st
import pandas as pd
from OI_Data import OI_Data
from Logger import Logger
from DataCleaner import DataCleaner as dc


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
# Index input
index_name = st.sidebar.radio("Select the Index",
                             ('NIFTY', 'BANKNIFTY'))

thursdays = dc.next_thursdays()

# Select Expiry Date
expiry_date = st.sidebar.selectbox('Choose expiry date:', thursdays)

# Take Current Market Price input from the user
mktPrice = st.sidebar.number_input('Enter current market price:', step=100)

# Add user enters Submit button on the sidebar, then execute
if st.sidebar.button('Submit'):
    oi_data = OI_Data(mktPrice, index_name, expiry_date)
    df_oi = oi_data.get_OI_data()
    
    # Format values as integer instead float with .0000
    dc.format_value(df_oi)

    # Display the dataframe as a table
    st.table(df_oi)

    # Calculate the sum of ChangeINOI PE and CE
    changeinPE_sum = df_oi['pe_changeinopeninterest'].sum()
    changeinCE_sum = df_oi['ce_changeinopeninterest'].sum()

    st.table([
    ['Change in PE Sum', round(changeinPE_sum, 2)],
    ['Change in CE Sum', round(changeinCE_sum, 2)],
    ['PCR', round(changeinPE_sum/changeinCE_sum, 2)]
    ])