import streamlit as st
import yfinance as yf
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# Page setup
st.set_page_config(page_title="Stock Scanner", layout="wide")

# Refresh automatically every 60 seconds during live market
st_autorefresh(interval=60 * 1000, key="datarefresh")

st.title("📈 Live Stock & Sector Scanner")

# Helper function to generate TradingView URL
def make_tradingview_link(symbol):
    clean_symbol = str(symbol).replace('.NS', '').replace('.BO', '').strip()
    url = f"https://in.tradingview.com/chart/?symbol=NSE:{clean_symbol}"
    return f'<a href="{url}" target="_blank" style="text-decoration: none; color: #1E88E5; font-weight: bold;">{clean_symbol} ↗</a>'

# Sample Stocks List (Aapki requirement ke hisab se symbols replace kar sakte hain)
stock_list = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS', 'ICICIBANK.NS', 'TATASTEEL.NS']

@st.cache_data(ttl=60)
def fetch_stock_data(tickers):
    data = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="2d")
            if len(hist) >= 2:
                prev_close = hist['Close'].iloc[-2]
                curr_price = hist['Close'].iloc[-1]
                pct_change = ((curr_price - prev_close) / prev_close) * 100
                
                data.append({
                    "Ticker": ticker,
                    "Price": round(curr_price, 2),
                    "Change (%)": round(pct_change, 2)
                })
        except Exception as e:
            pass
    return pd.DataFrame(data)

# Fetch Data
df = fetch_stock_data(stock_list)

if not df.empty:
    # TradingView Link Column Create Kar Rahe Hain
    df['Chart'] = df['Ticker'].apply(make_tradingview_link)
    
    # Re-order and drop raw ticker if needed
    display_df = df[['Chart', 'Price', 'Change (%)']]
    
    # Render table with clickable HTML links
    st.write(
        display_df.to_html(escape=False, index=False), 
        unsafe_allow_html=True
    )
else:
    st.info("Data fetch ho raha hai, kripya thoda wait karein...")
