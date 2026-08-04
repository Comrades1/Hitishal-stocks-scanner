# FILE: app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
from datetime import datetime, time
import time as tm
import os
from fyers_apiv3 import fyersModel

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
    st.stop()

st.sidebar.write("Logged in successfully!")

# Cache Clear Button to force refresh data
if st.sidebar.button("🧹 Clear Cache & Refresh"):
    st.cache_data.clear()
    st.success("Cache cleared successfully!")
    st.rerun()

if st.sidebar.button("Logout"):
    st.session_state["authenticated"] = False
    st.rerun()
# --- LOGIN SYSTEM END ---

st.sidebar.markdown("---")

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🧭 Dashboard Navigation")
app_mode = st.sidebar.radio("Choose Section:", ["Market Pulse", "Sector Scope"])

st_autorefresh(interval=30000, limit=None, key="sector_refresh")

# Custom UI Styling
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    
    table { width: 100%; border-collapse: collapse; margin: 10px 0; font-size: 14px; background-color: #161b22; border-radius: 8px; overflow: hidden; }
    th { background-color: #21262d; color: #8b949e; text-align: left; padding: 10px 12px; font-weight: 600; border-bottom: 1px solid #30363d; }
    td { padding: 8px 12px; border-bottom: 1px solid #21262d; }
    tr:hover { background-color: #1c2128; }
    
    .pulse-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 12px; margin-bottom: 10px; }
    .pulse-header { font-size: 18px; font-weight: bold; color: #ffffff; margin-bottom: 10px; display: flex; align-items: center; gap: 8px; }
    
    .badge-bull { background-color: #123020; color: #56d364; padding: 3px 8px; border-radius: 12px; font-weight: bold; font-size: 11px; }
    .badge-bear { background-color: #341a1a; color: #ff7b72; padding: 3px 8px; border-radius: 12px; font-weight: bold; font-size: 11px; }
    .badge-val-green { background-color: #0e4429; color: #3fb950; padding: 3px 8px; border-radius: 6px; font-weight: bold; }
    .badge-val-red { background-color: #4c1d1d; color: #f85149; padding: 3px 8px; border-radius: 6px; font-weight: bold; }
    
    .badge-strong-buy { background-color: #0e4429; color: #3fb950; padding: 4px 10px; border-radius: 6px; font-weight: bold; border: 1px solid #238636; }
    .badge-buy { background-color: #123020; color: #56d364; padding: 4px 10px; border-radius: 6px; font-weight: bold; }
    .badge-strong-sell { background-color: #4c1d1d; color: #f85149; padding: 4px 10px; border-radius: 6px; font-weight: bold; border: 1px solid #da3633; }
    .badge-sell { background-color: #341a1a; color: #ff7b72; padding: 4px 10px; border-radius: 6px; font-weight: bold; }
    .badge-hold { background-color: #21262d; color: #8b949e; padding: 4px 10px; border-radius: 6px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

def make_tradingview_link(symbol):
    clean_symbol = str(symbol).replace('.NS', '').replace('.BO', '').strip()
    url = f"https://in.tradingview.com/chart/?symbol=NSE:{clean_symbol}"
    return f'<a href="{url}" target="_blank" style="text-decoration:none; color:#58a6ff; font-weight:bold;">{clean_symbol} ↗</a>'

def is_market_open():
    now = datetime.now()
    if now.weekday() < 5 and time(9, 15) <= now.time() <= time(15, 30):
        return True
    return False

# SECTOR DATA
SECTOR_DATA = {
    'AUTO': ['M&M.NS', 'MOTHERSON.NS', 'SAMVARDHANA.NS', 'MARUTI.NS', 'TATAMOTORS.NS', 'BAJAJ-AUTO.NS', 'HEROMOTOCO.NS', 'TVSMOTOR.NS', 'EICHERMOT.NS', 'ASHOKLEY.NS', 'BHARATFORG.NS', 'BOSCHLTD.NS', 'UNOMINDA.NS', 'TIINDIA.NS', 'EXIDEIND.NS', 'BALKRISIND.NS', 'APOLLOTYRE.NS', 'MRF.NS', 'SONACOMS.NS', 'FORCEMOT.NS', 'HYUNDAI.NS'],
    'FIN SERVICE': ['BAJFINANCE.NS', 'BAJAJFINSV.NS', 'MUTHOOTFIN.NS', 'CHOLAFIN.NS', 'JIOFIN.NS', 'LICHSGFIN.NS', 'BSE.NS', 'PFC.NS'],
    'NIFTY 50': ['RELIANCE.NS', 'HDFCBANK.NS', 'ICICIBANK.NS', 'INFY.NS', 'TCS.NS', 'ITC.NS', 'LT.NS', 'AXISBANK.NS'],
    'SENSEX': ['RELIANCE.NS', 'HDFCBANK.NS', 'ICICIBANK.NS', 'INFY.NS', 'TCS.NS', 'BHARTIARTL.NS', 'SBIN.NS', 'KOTAKBANK.NS'],
    'ENERGY': ['RELIANCE.NS', 'NTPC.NS', 'POWERGRID.NS', 'ONGC.NS', 'GAIL.NS', 'BPCL.NS', 'TATAPOWER.NS', 'SUZLON.NS'],
    'PHARMA': ['SUNPHARMA.NS', 'CIPLA.NS', 'DRREDDY.NS', 'DIVISLAB.NS', 'LUPIN.NS', 'ZYDUSLIFE.NS', 'TORNTPHARM.NS', 'MANKIND.NS'],
    'IT': ['LTIM.NS', 'TCS.NS', 'INFY.NS', 'MPHASIS.NS', 'COFORGE.NS', 'WIPRO.NS', 'HCLTECH.NS', 'OFSS.NS', 'PERSISTENT.NS', 'TECHM.NS'],
    'NIFTY MID SELECT': ['FEDERALBNK.NS', 'IDFCFIRSTB.NS', 'AUROPHARMA.NS', 'PERSISTENT.NS', 'COFORGE.NS', 'POLYCAB.NS', 'CUMMINSIND.NS'],
    'BANK': ['HDFCBANK.NS', 'ICICIBANK.NS', 'SBIN.NS', 'KOTAKBANK.NS', 'AXISBANK.NS', 'INDUSINDBK.NS', 'PNB.NS', 'BANKBARODA.NS'],
    'PSU BANK': ['SBIN.NS', 'PNB.NS', 'BANKBARODA.NS', 'CANBK.NS', 'UNIONBANK.NS', 'IOB.NS', 'CENTRALBK.NS', 'MAHABANK.NS'],
    'PVT BANK': ['HDFCBANK.NS', 'ICICIBANK.NS', 'KOTAKBANK.NS', 'AXISBANK.NS', 'INDUSINDBK.NS', 'FEDERALBNK.NS', 'IDFCFIRSTB.NS', 'BANDHANBNK.NS'],
    'REALTY': ['DLF.NS', 'LODHA.NS', 'GODREJPROP.NS', 'PHOENIXLTD.NS', 'OBEROIRLTY.NS', 'PRESTIGE.NS', 'BRIGADE.NS'],
    'CEMENT': ['ULTRACEMCO.NS', 'GRASIM.NS', 'AMBUJACEM.NS', 'ACC.NS', 'DALBHARAT.NS', 'SHREECEM.NS', 'RAMCOCEM.NS', 'JKCEMENT.NS'],
    'FMCG': ['ITC.NS', 'HINDUNILVR.NS', 'BRITANNIA.NS', 'DABUR.NS', 'NESTLEIND.NS', 'VBL.NS', 'GODREJCP.NS', 'TATACONSUM.NS'],
    'METAL': ['TATASTEEL.NS', 'JINDALSTEL.NS', 'HINDALCO.NS', 'VEDL.NS', 'NATIONALUM.NS', 'SAIL.NS', 'NMDC.NS', 'APLAPOLLO.NS']
}

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# --- FYERS DATA FETCHING ENGINE ---
def get_fyers_data(symbol, client_id="YOUR_CLIENT_ID-100"): # Replace with your client ID
    try:
        if not os.path.exists("fyers_token.txt"):
            return pd.DataFrame()
        
        with open("fyers_token.txt", "r") as f:
            access_token = f.read().strip()
            
        fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, log_path="")
        clean_symbol = symbol.replace('.NS', '').replace('.BO', '')
        fyers_symbol = f"NSE:{clean_symbol}-EQ"
        
        range_to = int(tm.time())
        range_from = range_to - (5 * 24 * 60 * 60)
        
        data = {
            "symbol": fyers_symbol,
            "resolution": "5",
            "date_format": "0",
            "range_from": str(range_from),
            "range_to": str(range_to),
            "cont_flag": "1"
        }
        
        response = fyers.history(data=data)
        
        if response['s'] == 'ok' and len(response['candles']) > 0:
            cols = ['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']
            df = pd.DataFrame(response['candles'], columns=cols)
            # Convert Unix to IST timezone to match NSE time checks
            df['Datetime'] = pd.to_datetime(df['Datetime'], unit='s').dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata')
            df.set_index('Datetime', inplace=True)
            return df
        else:
            return pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()


@st.cache_data(ttl=25)
def fetch_sector_analytics():
    all_stocks = []
    
    for sector, tickers in SECTOR_DATA.items():
        for ticker in tickers:
            # Replaced yfinance logic entirely with FYERS engine
            df = get_fyers_data(ticker)
            
            if df.empty or len(df) < 10:
                continue
                
            df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean() if len(df) >= 20 else df['Close']
            df['RSI'] = calculate_rsi(df['Close'], 14) if len(df) >= 14 else 50.0
            
            today_date = df.index[-1].date()
            df_today = df[df.index.date == today_date].copy()
            
            morning_change = 0.0
            morning_vol_spike = 1.0
            first_breakout_time = "09:15"
            
            current_price = df['Close'].iloc[-1]
            if not df_today.empty:
                open_price = df_today['Open'].iloc[0]
                pct_change = round(((current_price - open_price) / open_price) * 100, 2)
                
                df_today['VWAP'] = (df_today['Volume'] * (df_today['High'] + df_today['Low'] + df_today['Close']) / 3).cumsum() / (df_today['Volume'].cumsum().replace(0, 1))
                mean_vol = df_today['Volume'].mean()
                df_today['Vol_Ratio'] = df_today['Volume'] / (mean_vol if mean_vol > 0 else 1)
                
                # Fetching morning range correctly now using local timezone
                df_morning = df_today.between_time('09:15', '11:30')
                if not df_morning.empty:
                    morning_max = df_morning['High'].max()
                    morning_change = ((morning_max - open_price) / open_price) * 100
                    max_dt = df_morning['High'].idxmax()
                    first_breakout_time = max_dt.strftime('%H:%M') if hasattr(max_dt, 'strftime') else str(max_dt)[11:16]
                    morning_vol_spike = round(df_morning['Vol_Ratio'].mean(), 2) if 'Vol_Ratio' in df_morning else 1.0
            else:
                prev_close = df['Close'].iloc[0]
                pct_change = round(((current_price - prev_close) / prev_close) * 100, 2)
            
            ema20_val = df['EMA20'].iloc[-1]
            rsi_val = df['RSI'].iloc[-1]
            
            if not df_today.empty:
                vol_recent = df_today['Volume'].iloc[-5:].mean()
                vol_today_avg = df_today['Volume'].mean()
                r_fact = round((vol_recent / vol_today_avg), 2) if vol_today_avg > 0 else 1.0
            else:
                vol_recent = df['Volume'].iloc[-5:].mean()
                vol_avg = df['Volume'].mean()
                r_fact = round((vol_recent / vol_avg), 2) if vol_avg > 0 else 1.0

            above_ema = current_price > ema20_val
            
            if above_ema and rsi_val > 55 and r_fact >= 1.6:
                signal = '<span class="badge-strong-buy">💥 🚀 Explosive Buy</span>'
            elif above_ema and rsi_val > 52 and r_fact > 1.2:
                signal = '<span class="badge-strong-buy">🚀 ⬆️ Strong Buy</span>'
            elif above_ema and rsi_val > 48:
                signal = '<span class="badge-buy">⬆️ Buy</span>'
            elif not above_ema and rsi_val < 42 and r_fact > 1.2:
                signal = '<span class="badge-strong-sell">🚀 ⬇️ Strong Sell</span>'
            elif not above_ema and rsi_val < 48:
                signal = '<span class="badge-sell">⬇️ Sell</span>'
            else:
                signal = '<span class="badge-hold">❌ Hold</span>'
            
            symbol_clean = ticker.replace('.NS', '').replace('.BO', '')
            last_candle_time = df.index[-1]
            formatted_time = last_candle_time.strftime('%H:%M')
            
            all_stocks.append({
                'Sector': sector,
                'Symbol': symbol_clean,
                'Chart': make_tradingview_link(symbol_clean),
                'Price': round(current_price, 2),
                'Change %': pct_change,
                'Abs Change': abs(pct_change) + 0.1,
                'R Fact': r_fact,
                'Signal': signal,
                'Time': formatted_time,
                'Morning_Change': round(morning_change, 2),
                'Morning_Time': first_breakout_time,
                'Morning_Vol_Spike': morning_vol_spike
            })
                
    return pd.DataFrame(all_stocks)

st.title("💡 Sector Scope — Smart Scanner")

with st.spinner("Calculating Momentum Indicators via FYERS Live Data..."):
    if not os.path.exists("fyers_token.txt"):
        st.error("⚠️ FYERS Token missing! Please run 'fyers_login.py' first to generate the access token.")
    else:
        df_data = fetch_sector_analytics()

        if not df_data.empty:
            
            sector_summary = df_data.groupby('Sector').agg(
                Avg_Change=('Change %', 'mean'),
                Bullish_Count=('Change %', lambda x: (x > 0).sum()),
                Total_Count=('Symbol', 'count')
            ).reset_index()

            sector_summary['Bearish_Count'] = sector_summary['Total_Count'] - sector_summary['Bullish_Count']
            sector_summary['Breadth_Ratio'] = (sector_summary['Bullish_Count'] - sector_summary['Bearish_Count']) / sector_summary['Total_Count']
            sector_summary['Raw_Score'] = sector_summary['Avg_Change'] * (1 + sector_summary['Breadth_Ratio'])
            
            max_val = sector_summary['Raw_Score'].abs().max()
            sector_summary['Strength Score'] = (sector_summary['Raw_Score'] / max_val * 10).round(2) if max_val > 0 else 0
            sector_summary = sector_summary.sort_values(by='Strength Score', ascending=False)

            top_sectors = sector_summary.head(8)['Sector'].tolist()

            market_badge = '<span style="font-size:12px; color:#3fb950; border:1px solid #238636; padding:2px 6px; border-radius:4px;">● LIVE</span>' if is_market_open() else '<span style="font-size:12px; color:#f85149; border:1px solid #da3633; padding:2px 6px; border-radius:4px;">🔴 MARKET CLOSED</span>'

            # --- 1. MARKET PULSE SECTION ---
            if app_mode == "Market Pulse":
                st.subheader("🔥 Market Pulse Scanners")
                
                col1, col2 = st.columns(2)

                # --- LEFT COLUMN: BREAKOUT BEACON ---
                with col1:
                    st.markdown(f"""
                    <div class="pulse-card">
                        <div class="pulse-header">🔥 BREAKOUT BEACON (Top Sectors) 💡 {market_badge}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    session_choice = st.selectbox(
                        "⏱️ Select Time Window", 
                        ["🌅 Morning Session (09:15 - 11:30 AM)", "📈 Full Day / Live Market"],
                        key="beacon_session"
                    )
                    
                    beacon_df = df_data[df_data['Sector'].isin(top_sectors)].copy()
                    if beacon_df.empty:
                        beacon_df = df_data.copy()
                    
                    if session_choice == "🌅 Morning Session (09:15 - 11:30 AM)":
                        beacon_df['Score'] = (beacon_df['Morning_Change'].abs() * beacon_df['Morning_Vol_Spike']).round(2)
                        beacon_df['Beacon_Signal'] = beacon_df['Morning_Change'].apply(lambda x: '<span class="badge-bull">BULL</span>' if x >= 0 else '<span class="badge-bear">BEAR</span>')
                        beacon_df['Change_Badge'] = beacon_df['Morning_Change'].apply(lambda x: f'<span class="badge-val-green">{x:+.2f}%</span>' if x >= 0 else f'<span class="badge-val-red">{x:.2f}%</span>')
                        
                        top_breakouts = beacon_df.sort_values(by='Score', ascending=False).drop_duplicates(subset=['Symbol']).head(9)
                        display_beacon = top_breakouts[['Beacon_Signal', 'Chart', 'Change_Badge', 'Score', 'Morning_Time']].rename(
                            columns={
                                'Beacon_Signal': 'Signal', 
                                'Chart': 'Symbol', 
                                'Change_Badge': '%', 
                                'Score': 'Signal %',
                                'Morning_Time': 'Time'
                            }
                        )
                    else:
                        beacon_df['Score'] = (beacon_df['Change %'].abs() * 1.2).round(2)
                        beacon_df['Beacon_Signal'] = beacon_df['Change %'].apply(lambda x: '<span class="badge-bull">BULL</span>' if x >= 0 else '<span class="badge-bear">BEAR</span>')
                        beacon_df['Change_Badge'] = beacon_df['Change %'].apply(lambda x: f'<span class="badge-val-green">{x:+.2f}%</span>' if x >= 0 else f'<span class="badge-val-red">{x:.2f}%</span>')
                        
                        top_breakouts = beacon_df.sort_values(by='Score', ascending=False).drop_duplicates(subset=['Symbol']).head(9)
                        display_beacon = top_breakouts[['Beacon_Signal', 'Chart', 'Change_Badge', 'Score', 'Time']].rename(
                            columns={
                                'Beacon_Signal': 'Signal', 
                                'Chart': 'Symbol', 
                                'Change_Badge': '%', 
                                'Score': 'Signal %',
                                'Time': 'Time'
                            }
                        )
                        
                    st.write(display_beacon.to_html(escape=False, index=False), unsafe_allow_html=True)

                # --- RIGHT COLUMN: INTRADAY BOOST ---
                with col2:
                    st.markdown(f"""
                    <div class="pulse-card">
                        <div class="pulse-header">⚡ INTRADAY BOOST 🚀 {market_badge}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    f_col1, f_col2, f_col3, f_col4 = st.columns(4)
                    with f_col1:
                        trend_filter = st.selectbox("↕️ Trend", ["Neutral (All)", "Bullish Only 🟢", "Bearish Only 🔴"], key="boost_trend")
                    with f_col2:
                        price_filter = st.selectbox("₹ Price", ["All Prices", "< ₹500", "₹500 - ₹2000", "> ₹2000"], key="boost_price")
                    with f_col3:
                        vol_filter = st.selectbox("⚡ Volume", ["All", "High (> 1.3)", "Super (> 2.0)", "💥 Explosive (> 1.6)"], key="boost_vol")
                    with f_col4:
                        sector_filter = st.selectbox("🎯 Sector", ["All Sectors"] + list(SECTOR_DATA.keys()), key="boost_sector")
                    
                    boost_filtered_df = df_data.copy()
                    
                    # Filtering Logic
                    if trend_filter == "Bullish Only 🟢":
                        boost_filtered_df = boost_filtered_df[boost_filtered_df['Change %'] >= 0]
                    elif trend_filter == "Bearish Only 🔴":
                        boost_filtered_df = boost_filtered_df[boost_filtered_df['Change %'] < 0]
                        
                    if price_filter == "< ₹500":
                        boost_filtered_df = boost_filtered_df[boost_filtered_df['Price'] < 500]
                    elif price_filter == "₹500 - ₹2000":
                        boost_filtered_df = boost_filtered_df[(boost_filtered_df['Price'] >= 500) & (boost_filtered_df['Price'] <= 2000)]
                    elif price_filter == "> ₹2000":
                        boost_filtered_df = boost_filtered_df[boost_filtered_df['Price'] > 2000]

                    if vol_filter == "High (> 1.3)":
                        boost_filtered_df = boost_filtered_df[boost_filtered_df['R Fact'] > 1.3]
                    elif vol_filter == "Super (> 2.0)":
                        boost_filtered_df = boost_filtered_df[boost_filtered_df['R Fact'] > 2.0]
                    elif vol_filter == "💥 Explosive (> 1.6)":
                        boost_filtered_df = boost_filtered_df[boost_filtered_df['R Fact'] > 1.6]

                    if sector_filter != "All Sectors":
                        boost_filtered_df = boost_filtered_df[boost_filtered_df['Sector'] == sector_filter]
                    
                    # Render Table for Intraday Boost
                    display_boost = boost_filtered_df[['Signal', 'Chart', 'Price', 'Change %', 'R Fact', 'Time']].rename(columns={'Chart': 'Symbol'})
                    st.write(display_boost.to_html(escape=False, index=False), unsafe_allow_html=True)
            
            # --- 2. SECTOR SCOPE SECTION ---
            elif app_mode == "Sector Scope":
                st.subheader("📊 Sector Breadth & Strength Dashboard")
                st.dataframe(sector_summary.style.background_gradient(cmap='RdYlGn', subset=['Strength Score']))
