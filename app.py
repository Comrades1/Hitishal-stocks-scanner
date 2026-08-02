import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# 1. Page Configuration
st.set_page_config(page_title="Sector Scope - Smart Scanner", layout="wide", initial_sidebar_state="expanded")

# --- LOGIN SYSTEM START ---
USER_CREDENTIALS = {
    "admin": "12345",
    "ASHWAJIT": "pass123",
    "HARSHAL": "Shalvi@3009"
}

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

def login():
    st.title("🔒 Dashboard Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state["authenticated"] = True
            st.success("Login Successful!")
            st.rerun()
        else:
            st.error("Invalid Username or Password!")

if not st.session_state["authenticated"]:
    login()
    st.stop()  # Stop execution until user logs in

# Sidebar Logout Button
st.sidebar.write(f"Logged in successfully!")
if st.sidebar.button("Logout"):
    st.session_state["authenticated"] = False
    st.rerun()
# --- LOGIN SYSTEM END ---

# Auto-refresh every 30 seconds
st_autorefresh(interval=30000, limit=None, key="sector_refresh")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    div[data-testid="stMetricValue"] { font-size: 20px; }
    </style>
""", unsafe_allow_html=True)

# Helper function to generate TradingView clickable link
def make_tradingview_link(symbol):
    clean_symbol = str(symbol).replace('.NS', '').replace('.BO', '').strip()
    url = f"https://in.tradingview.com/chart/?symbol=NSE:{clean_symbol}"
    return f'<a href="{url}" target="_blank" style="text-decoration:none; color:#1E88E5; font-weight:bold;">{clean_symbol} ↗</a>'

# 2. Sector & Stock Mappings
SECTOR_DATA = {
    'AUTO': ['TATAMOTORS.NS', 'M&M.NS', 'BAJAJ-AUTO.NS', 'HEROMOTOCO.NS', 'EICHERMOT.NS', 'ASHOKLEY.NS', 'TVSMOTOR.NS', 'BHARATFORG.NS'],
    'FIN SERVICE': ['BAJFINANCE.NS', 'BAJAJFINSV.NS', 'MUTHOOTFIN.NS', 'CHOLAFIN.NS', 'JIOFIN.NS', 'LICHSGFIN.NS', 'BSE.NS', 'PFC.NS'],
    'NIFTY 50': ['RELIANCE.NS', 'HDFCBANK.NS', 'ICICIBANK.NS', 'INFY.NS', 'TCS.NS', 'ITC.NS', 'LT.NS', 'AXISBANK.NS'],
    'SENSEX': ['RELIANCE.NS', 'HDFCBANK.NS', 'ICICIBANK.NS', 'INFY.NS', 'TCS.NS', 'BHARTIARTL.NS', 'SBIN.NS', 'KOTAKBANK.NS'],
    'ENERGY': ['RELIANCE.NS', 'NTPC.NS', 'POWERGRID.NS', 'ONGC.NS', 'GAIL.NS', 'BPCL.NS', 'TATAPOWER.NS', 'SUZLON.NS'],
    'PHARMA': ['SUNPHARMA.NS', 'CIPLA.NS', 'DRREDDY.NS', 'DIVISLAB.NS', 'LUPIN.NS', 'ZYDUSLIFE.NS', 'TORNTPHARM.NS', 'MANKIND.NS'],
    'IT': ['TCS.NS', 'INFY.NS', 'HCLTECH.NS', 'WIPRO.NS', 'TECHM.NS', 'LTIM.NS', 'COFORGE.NS', 'PERSISTENT.NS'],
    'NIFTY MID SELECT': ['FEDERALBNK.NS', 'IDFCFIRSTB.NS', 'AUROPHARMA.NS', 'PERSISTENT.NS', 'COFORGE.NS', 'ASHOKLEY.NS', 'POLYCAB.NS', 'CUMMINSIND.NS'],
    'BANK': ['HDFCBANK.NS', 'ICICIBANK.NS', 'SBIN.NS', 'KOTAKBANK.NS', 'AXISBANK.NS', 'INDUSINDBK.NS', 'PNB.NS', 'BANKBARODA.NS'],
    'PSU BANK': ['SBIN.NS', 'PNB.NS', 'BANKBARODA.NS', 'CANBK.NS', 'UNIONBANK.NS', 'IOB.NS', 'CENTRALBK.NS', 'MAHABANK.NS'],
    'PVT BANK': ['HDFCBANK.NS', 'ICICIBANK.NS', 'KOTAKBANK.NS', 'AXISBANK.NS', 'INDUSINDBK.NS', 'FEDERALBNK.NS', 'IDFCFIRSTB.NS', 'BANDHANBNK.NS'],
    'REALTY': ['DLF.NS', 'LODHA.NS', 'GODREJPROP.NS', 'PHOENIXLTD.NS', 'OBEROIRLTY.NS', 'PRESTIGE.NS', 'BRIGADE.NS'],
    'CEMENT': ['ULTRACEMCO.NS', 'GRASIM.NS', 'AMBUJACEM.NS', 'ACC.NS', 'DALBHARAT.NS', 'SHREECEM.NS', 'RAMCOCEM.NS', 'JKCEMENT.NS'],
    'FMCG': ['ITC.NS', 'HINDUNILVR.NS', 'BRITANNIA.NS', 'DABUR.NS', 'NESTLEIND.NS', 'VBL.NS', 'GODREJCP.NS', 'TATACONSUM.NS'],
    'METAL': ['TATASTEEL.NS', 'JINDALSTEL.NS', 'HINDALCO.NS', 'VEDL.NS', 'NATIONALUM.NS', 'SAIL.NS', 'NMDC.NS', 'APLAPOLLO.NS']
}

# Helper function to calculate RSI
def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# 3. Data Fetcher Engine
@st.cache_data(ttl=25)
def fetch_sector_analytics():
    all_stocks = []
    
    for sector, tickers in SECTOR_DATA.items():
        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                df = stock.history(period='5d', interval='5m')
                
                if df.empty or len(df) < 20:
                    continue
                
                # RSI aur EMA background me calculate honge
                df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
                df['RSI'] = calculate_rsi(df['Close'], 14)
                
                current_price = df['Close'].iloc[-1]
                prev_close = df['Close'].iloc[0]
                pct_change = ((current_price - prev_close) / prev_close) * 100
                
                ema20_val = df['EMA20'].iloc[-1]
                rsi_val = df['RSI'].iloc[-1]
                
                # Relative Volume Spike Factor
                vol_recent = df['Volume'].iloc[-5:].mean()
                vol_avg = df['Volume'].mean()
                r_fact = round((vol_recent / vol_avg), 2) if vol_avg > 0 else 1.0
                
                above_ema = current_price > ema20_val
                if above_ema and rsi_val > 55 and r_fact > 1.2:
                    signal = '🚀 Super Bullish'
                elif above_ema and rsi_val > 50:
                    signal = '🟢 Bullish (Above EMA)'
                elif not above_ema and rsi_val < 45:
                    signal = '🔴 Bearish (Below EMA)'
                else:
                    signal = '🟡 Neutral / Sideways'
                
                symbol_clean = ticker.replace('.NS', '')
                
                all_stocks.append({
                    'Sector': sector,
                    'Symbol': symbol_clean,
                    'Chart': make_tradingview_link(symbol_clean),
                    'Price': round(current_price, 2),
                    'Change %': round(pct_change, 2),
                    'R Fact': r_fact,
                    'Signal': signal
                })
            except Exception:
                continue
                
    return pd.DataFrame(all_stocks)

# App Main Section
st.title("💡 Sector Scope — Advanced Scanner")

with st.spinner("Calculating Indicators & Live Data..."):
    df_data = fetch_sector_analytics()

if not df_data.empty:
    # --- TOP BREAKOUT SECTION (>2% GAINERS) ---
    st.subheader("🔥 Top Momentum Breakouts (> +2.0% Movers)")
    
    min_gain = st.slider("Minimum Gain Threshold (%):", min_value=1.0, max_value=5.0, value=2.0, step=0.5)
    
    top_movers = df_data[df_data['Change %'] >= min_gain].sort_values(by='Change %', ascending=False)
    
    if not top_movers.empty:
        st.success(f"Total **{len(top_movers)} stocks** moving above +{min_gain}% right now!")
        
        display_top = top_movers[['Sector', 'Chart', 'Price', 'Change %', 'R Fact', 'Signal']].rename(columns={'Chart': 'Symbol ↗'})
        st.write(display_top.to_html(escape=False, index=False), unsafe_allow_html=True)
    else:
        st.info(f"Abhi koi bhi stock +{min_gain}% se zyada move nahi kar raha hai.")

    st.markdown("---")

    # Sector Ranking
    sector_summary = df_data.groupby('Sector').agg(
        Avg_Change=('Change %', 'mean'),
        Bullish_Count=('Change %', lambda x: (x > 0).sum()),
        Total_Count=('Symbol', 'count')
    ).reset_index()

    sector_summary['Strength Score'] = round(sector_summary['Avg_Change'] * (sector_summary['Bullish_Count'] / sector_summary['Total_Count']) * 10, 2)
    sector_summary = sector_summary.sort_values(by='Strength Score', ascending=False)

    st.subheader("📊 Sector Momentum Ranking")
    fig_bar = px.bar(
        sector_summary, 
        x='Sector', 
        y='Strength Score',
        color='Strength Score',
        color_continuous_scale=['#ef5350', '#26a69a'],
        text='Strength Score'
    )
    fig_bar.update_layout(template="plotly_dark", height=350, coloraxis_showscale=False)
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")

    # Sector Drill-down Table
    st.subheader("🎯 Sector Drill-down")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_sector = st.selectbox("Select Sector to Inspect:", options=sector_summary['Sector'].tolist())
    with col2:
        only_high_movers = st.checkbox(f"Show only >+{min_gain}% Gainers", value=False)

    sector_stocks = df_data[df_data['Sector'] == selected_sector]
    
    if only_high_movers:
        sector_stocks = sector_stocks[sector_stocks['Change %'] >= min_gain]

    display_sector = sector_stocks[['Chart', 'Price', 'Change %', 'R Fact', 'Signal']].sort_values(by='Change %', ascending=False).rename(columns={'Chart': 'Symbol ↗'})
    
    st.write(display_sector.to_html(escape=False, index=False), unsafe_allow_html=True)

else:
    st.error("Data fetch nahi ho raha hai, thodi der baad refresh karein.")
