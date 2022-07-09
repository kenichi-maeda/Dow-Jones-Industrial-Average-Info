import streamlit as st
import pandas as pd
import yfinance as yf

st.title('Dow Jones Industrial Average')

st.markdown("""
This app shows the list of the **Dow Jones Industrial Average** and its corresponding **stock price data** (e.g., 
volume, opening price)
* **Data:** [Wikipedia](https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average)
* **Libraries:** pandas, streamlit, and yfinance
""")

st.sidebar.header('Search from industry')


# Retrieve data from wikipedia
@st.cache
def loadData():
    URL = 'https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average#Components'
    html = pd.read_html(URL, header=0)
    data = html[1]
    return data


data = loadData()
sector = data.groupby('Industry')

# Sidebar
sector_unique = sorted(data['Industry'].unique())
selected_sector = st.sidebar.multiselect('Sector', sector_unique, sector_unique)

# Filtering data
df_selected_sector = data[(data['Industry'].isin(selected_sector))]

# Show the list
st.header('The list of the Dow Jones Industrial Average')
st.write("30 companies")
st.dataframe(df_selected_sector)

# Create a selectbox
company = st.selectbox("Symbol", (
    "AXP", "AMGN", "AAPL", "BA", "CAT", "CVX", "CSCO", "KO", "DIS", "DOW", "GS", "HD", "HON", "IBM", "INTC", "JNJ",
    "JPM", "MCD", "MMM", "MRK", "MSFT", "NKE", "PG", "CRM", "TRV", "UNH", "VZ", "V", "WBA", "WMT"))

# If the button is pushed, show the stock price information.
if st.button('Show Plots'):
    with st.container():
        st.write("""--------""")
        tickerSymbol = company
        tickerData = yf.Ticker(tickerSymbol)
        tickerDf = tickerData.history(period='1m', start='2000-1-1', end='2022-7-1')

        st.write("""### Open """)
        st.line_chart(tickerDf.Open)
        st.write("""### Close""")
        st.line_chart(tickerDf.Close)
        st.write("""### Volume""")
        st.line_chart(tickerDf.Volume)
        st.write("""### High""")
        st.line_chart(tickerDf.High)
        st.write("""### Low""")
        st.line_chart(tickerDf.Low)
