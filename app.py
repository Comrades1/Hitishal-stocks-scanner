# --- PYTHON 3.14 PKG_RESOURCES COMPATIBILITY PATCH (MUST BE AT LINE 1) ---
import sys
try:
    import pkg_resources
except ModuleNotFoundError:
    try:
        import setuptools
        import pkg_resources
    except ModuleNotFoundError:
        import types
        pkg_resources = types.ModuleType("pkg_resources")
        pkg_resources.resource_filename = lambda *args, **kwargs: ""
        sys.modules["pkg_resources"] = pkg_resources
# -------------------------------------------------------------------------

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
from datetime import datetime, time, timedelta
import os
import time as time_lib
import threading
from fyers_apiv3 import fyersModel
from fyers_apiv3.FyersWebsocket import data_ws

# 1. Page Configuration
st.set_page_config(page_title="Sector Scope - Fyers Smart Scanner", layout="wide", initial_sidebar_state="expanded")

# --- CLIENT CONFIG & COMPLETE SECTOR DATA ---
CLIENT_ID = "O21QCP3N13-100"

SECTOR_DATA = {
    'BANK': [
        'NSE:SBIN-EQ', 'NSE:BANKBARODA-EQ', 'NSE:PNB-EQ', 'NSE:CANBK-EQ', 
        'NSE:UNIONBANK-EQ', 'NSE:INDIANB-EQ', 'NSE:IOB-EQ', 'NSE:UCOBANK-EQ', 
        'NSE:BANKINDIA-EQ', 'NSE:CENTRALBK-EQ', 'NSE:MAHABANK-EQ', 'NSE:PSB-EQ',
        'NSE:HDFCBANK-EQ', 'NSE:ICICIBANK-EQ', 'NSE:KOTAKBANK-EQ', 'NSE:AXISBANK-EQ', 
        'NSE:INDUSINDBK-EQ', 'NSE:FEDERALBNK-EQ', 'NSE:IDFCFIRSTB-EQ', 'NSE:BANDHANBNK-EQ', 
        'NSE:RBLBANK-EQ', 'NSE:AUBANK-EQ', 'NSE:CITYUNIONB-EQ', 'NSE:KARURVYSYA-EQ'
    ],
    'AUTO': [
        'NSE:M&M-EQ', 'NSE:MOTHERSON-EQ', 'NSE:MARUTI-EQ', 'NSE:TATAMOTORS-EQ', 
        'NSE:BAJAJ-AUTO-EQ', 'NSE:HEROMOTOCO-EQ', 'NSE:TVSMOTOR-EQ', 'NSE:EICHERMOT-EQ', 
        'NSE:ASHOKLEY-EQ', 'NSE:BOSCHLTD-EQ', 'NSE:BHARATFORG-EQ', 'NSE:TIINDIA-EQ', 
        'NSE:MRF-EQ', 'NSE:BALKRISIND-EQ', 'NSE:SONACOMS-EQ'
    ],
    'FIN SERVICE': [
        'NSE:BAJFINANCE-EQ', 'NSE:BAJAJFINSV-EQ', 'NSE:MUTHOOTFIN-EQ', 'NSE:CHOLAFIN-EQ', 
        'NSE:JIOFIN-EQ', 'NSE:HDFCLIFE-EQ', 'NSE:SBILIFE-EQ', 'NSE:ICICIPRULI-EQ', 
        'NSE:PFC-EQ', 'NSE:REC-EQ', 'NSE:HDFCAMC-EQ', 'NSE:SHRIRAMFIN-EQ', 
        'NSE:LICHSGFIN-EQ', 'NSE:ICICIGI-EQ'
    ],
    'NIFTY 50': [
        'NSE:RELIANCE-EQ', 'NSE:HDFCBANK-EQ', 'NSE:ICICIBANK-EQ', 'NSE:INFY-EQ', 
        'NSE:TCS-EQ', 'NSE:ITC-EQ', 'NSE:LTIM-EQ', 'NSE:LT-EQ', 'NSE:AXISBANK-EQ', 
        'NSE:KOTAKBANK-EQ', 'NSE:SBIN-EQ', 'NSE:BHARTIARTL-EQ', 'NSE:HINDUNILVR-EQ', 
        'NSE:BAJFINANCE-EQ', 'NSE:MARUTI-EQ', 'NSE:HCLTECH-EQ', 'NSE:SUNPHARMA-EQ', 
        'NSE:TATAMOTORS-EQ', 'NSE:NTPC-EQ', 'NSE:POWERGRID-EQ', 'NSE:TITAN-EQ', 
        'NSE:ULTRACEMCO-EQ', 'NSE:ASIANPAINT-EQ', 'NSE:COALINDIA-EQ', 'NSE:TATASTEEL-EQ', 
        'NSE:M&M-EQ', 'NSE:ADANIENT-EQ', 'NSE:ADANIPORTS-EQ', 'NSE:GRASIM-EQ', 
        'NSE:BAJAJFINSV-EQ', 'NSE:ONGC-EQ', 'NSE:HINDALCO-EQ', 'NSE:TECHM-EQ', 
        'NSE:JSWSTEEL-EQ', 'NSE:INDUSINDBK-EQ', 'NSE:DRREDDY-EQ', 'NSE:CIPLA-EQ', 
        'NSE:HEROMOTOCO-EQ', 'NSE:WIPRO-EQ', 'NSE:NESTLEIND-EQ', 'NSE:BRITANNIA-EQ', 
        'NSE:EICHERMOT-EQ', 'NSE:DIVISLAB-EQ', 'NSE:BPCL-EQ', 'NSE:APOLLOHOSP-EQ', 
        'NSE:TATACONSUM-EQ', 'NSE:SBILIFE-EQ', 'NSE:HDFCLIFE-EQ', 'NSE:BEL-EQ', 'NSE:TRENT-EQ'
    ],
    'ENERGY': [
        'NSE:RELIANCE-EQ', 'NSE:NTPC-EQ', 'NSE:POWERGRID-EQ', 'NSE:ONGC-EQ', 
        'NSE:GAIL-EQ', 'NSE:BPCL-EQ', 'NSE:TATAPOWER-EQ', 'NSE:IOC-EQ', 
        'NSE:COALINDIA-EQ', 'NSE:ADANIGREEN-EQ', 'NSE:ADANIPOWER-EQ', 'NSE:SUZLON-EQ', 
        'NSE:HINDPETRO-EQ', 'NSE:JSWENERGY-EQ', 'NSE:NHPC-EQ', 'NSE:IGL-EQ', 
        'NSE:GUJGASLTD-EQ', 'NSE:PETRONET-EQ'
    ],
    'PHARMA': [
        'NSE:SUNPHARMA-EQ', 'NSE:CIPLA-EQ', 'NSE:DRREDDY-EQ', 'NSE:DIVISLAB-EQ', 
        'NSE:LUPIN-EQ', 'NSE:TORNTPHARM-EQ', 'NSE:MANKIND-EQ', 'NSE:ZYDUSLIFE-EQ', 
        'NSE:ALKEM-EQ', 'NSE:AUROPHARMA-EQ', 'NSE:BIOCON-EQ', 'NSE:GLENMARK-EQ', 
        'NSE:IPCALAB-EQ', 'NSE:SYNGENE-EQ', 'NSE:LAURUSLABS-EQ'
    ],
    'IT': [
        'NSE:TCS-EQ', 'NSE:INFY-EQ', 'NSE:HCLTECH-EQ', 'NSE:WIPRO-EQ', 
        'NSE:TECHM-EQ', 'NSE:LTIM-EQ', 'NSE:COFORGE-EQ', 'NSE:PERSISTENT-EQ', 
        'NSE:MPHASIS-EQ', 'NSE:LTTS-EQ', 'NSE:TATAELXSI-EQ', 'NSE:OFSS-EQ'
    ],
    'REALTY': [
        'NSE:DLF-EQ', 'NSE:LODHA-EQ', 'NSE:GODREJPROP-EQ', 'NSE:PHOENIXLTD-EQ', 
        'NSE:OBEROIRLTY-EQ', 'NSE:PRESTIGE-EQ', 'NSE:BRIGADE-EQ', 'NSE:SOBHA-EQ', 
        'NSE:SIGNATURE-EQ', 'NSE:RAYMOND-EQ'
    ],
    'CEMENT': [
        'NSE:ULTRACEMCO-EQ', 'NSE:GRASIM-EQ', 'NSE:AMBUJACEM-EQ', 'NSE:ACC-EQ', 
        'NSE:DALBHARAT-EQ', 'NSE:SHREECEM-EQ', 'NSE:RAMCOCEM-EQ', 'NSE:JKCEMENT-EQ', 
        'NSE:BIRLACORPN-EQ', 'NSE:HEIDELBERG-EQ'
    ],
    'FMCG': [
        'NSE:ITC-EQ', 'NSE:HINDUNILVR-EQ', 'NSE:BRITANNIA-EQ', 'NSE:DABUR-EQ', 
        'NSE:NESTLEIND-EQ', 'NSE:VBL-EQ', 'NSE:TATACONSUM-EQ', 'NSE:GODREJCP-EQ', 
        'NSE:MARICO-EQ', 'NSE:COLPAL-EQ', 'NSE:PGHH-EQ', 'NSE:PATANJALI-EQ', 
        'NSE:RADICO-EQ', 'NSE:UBL-EQ'
    ],
    'METAL': [
        'NSE:TATASTEEL-EQ', 'NSE:JINDALSTEL-EQ', 'NSE:HINDALCO-EQ', 'NSE:VEDL-EQ', 
        'NSE:NATIONALUM-EQ', 'NSE:SAIL-EQ', 'NSE:JSWSTEEL-EQ', 'NSE:NMDC-EQ', 
        'NSE:APLAPOLLO-EQ', 'NSE:JSL-EQ', 'NSE:HINDZINC-EQ', 'NSE:RATNAMANI-EQ'
    ]
}

ALL_SYMBOLS = list(set([symbol for list_symbols in SECTOR_DATA.values() for symbol in list_symbols]))

# --- LIVE WEBSOCKET ENGINE ---
if "live_ticks" not in st.session_state:
    st.session_state["live_ticks"] = {}

def start_fyers_websocket(access_token):
    def on_message(message):
        if isinstance(message, dict) and (message.get("type") == "sf" or "ltp" in message):
            symbol = message.get("symbol")
            ltp = message.get("ltp")
            if symbol and ltp is not None:
                st.session_state["live_ticks"][symbol] = ltp

    def on_error(message):
        pass

    def on_close(message):
        pass

    def on_open():
        fyers_ws.subscribe(symbols=ALL_SYMBOLS, data_type="SymbolUpdate")
        fyers_ws.keep_running()

    fyers_ws = data_ws.FyersDataSocket(
        access_token=f"{CLIENT_ID}:{access_token}",
        log_path="",
        ltype="pro",
        on_connect=on_open,
        on_close=on_close,
        on_error=on_error,
        on_message=on_message
    )
    fyers_ws.connect()

if "ws_started" not in st.session_state:
    if os.path.exists("fyers_token.txt"):
        with open("fyers_token.txt", "r") as f:
            tok = f.read().strip()
        if tok:
            ws_thread = threading.Thread(target=start_fyers_websocket, args=(tok,), daemon=True)
            ws_thread.start()
            st.session_state["ws_started"] = True

# --- LOGIN SYSTEM ---
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
if st.sidebar.button("Logout"):
    st.session_state["authenticated"] = False
    st.rerun()

st.sidebar.markdown("---")

# --- NAVIGATION & AUTO-REFRESH ---
st.sidebar.title("🧭 Dashboard Navigation")
app_mode = st.sidebar.radio("Choose Section:", ["Market Pulse", "Sector Scope"])

st_autorefresh(interval=1000, limit=None, key="live_tick_refresh")

# Custom UI Styling
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 10px 0;
        font-size: 14px;
        background-color: #161b22;
        border-radius: 8px;
        overflow: hidden;
    }
    th {
        background-color: #21262d;
        color: #8b949e;
        text-align: left;
        padding: 10px 12px;
        font-weight: 600;
        border-bottom: 1px solid #30363d;
    }
    td {
        padding: 8px 12px;
        border-bottom: 1px solid #21262d;
    }
    tr:hover { background-color: #1c2128; }
    
    .pulse-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 10px;
    }
    .pulse-header {
        font-size: 18px;
        font-weight: bold;
        color: #ffffff;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
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
    clean_symbol = str(symbol).replace('NSE:', '').replace('-EQ', '').strip()
    url = f"https://in.tradingview.com/chart/?symbol=NSE:{clean_symbol}"
    return f'<a href="{url}" target="_blank" style="text-decoration:none; color:#58a6ff; font-weight:bold;">{clean_symbol} ↗</a>'

def is_market_open():
    now = datetime.now()
    if now.weekday() < 5 and time(9, 15) <= now.time() <= time(15, 30):
        return True
    return False

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

@st.cache_data(ttl=60)
def fetch_base_analytics():
    if not os.path.exists("fyers_token.txt"):
        st.error("❌ 'fyers_token.txt' not found! Please run your token generation script first.")
        return pd.DataFrame()
        
    with open("fyers_token.txt", "r") as f:
        access_token = f.read().strip()
        
    fyers = fyersModel.FyersModel(client_id=CLIENT_ID, token=access_token, log_path="")
    
    symbol_data_cache = {}
    to_date = datetime.now().strftime('%Y-%m-%d')
    from_date = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
    
    for ticker in ALL_SYMBOLS:
        try:
            data = {
                "symbol": ticker,
                "resolution": "5",
                "date_format": "1",
                "range_from": from_date,
                "range_to": to_date,
                "cont_flag": "1"
            }
            
            response = fyers.history(data=data)
            time_lib.sleep(0.005)
            
            if response.get("s") == "ok" and response.get("candles"):
                candles = response["candles"]
                df = pd.DataFrame(candles, columns=['Epoch', 'Open', 'High', 'Low', 'Close', 'Volume'])
                df['Datetime'] = pd.to_datetime(df['Epoch'], unit='s').dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata')
                df.set_index('Datetime', inplace=True)
                
                if not df.empty and len(df) >= 5:
                    df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean() if len(df) >= 20 else df['Close']
                    df['RSI'] = calculate_rsi(df['Close'], 14) if len(df) >= 14 else 50.0
                    symbol_data_cache[ticker] = df
        except Exception:
            continue

    all_stocks = []
    
    for sector, tickers in SECTOR_DATA.items():
        for ticker in tickers:
            if ticker not in symbol_data_cache:
                continue
                
            df = symbol_data_cache[ticker]
            today_date = df.index[-1].date()
            df_today = df[df.index.date == today_date].copy()
            
            morning_change = 0.0
            morning_vol_spike = 1.0
            first_breakout_time = "09:15"
            vwap_val = df['Close'].iloc[-1]
            buildup_status = "NEUTRAL"
            
            if not df_today.empty:
                # VWAP Calculation
                df_today['Typical_Price'] = (df_today['High'] + df_today['Low'] + df_today['Close']) / 3
                df_today['VP'] = df_today['Typical_Price'] * df_today['Volume']
                cum_vol = df_today['Volume'].cumsum()
                df_today['VWAP'] = df_today['VP'].cumsum() / (cum_vol.replace(0, 1))
                vwap_val = round(df_today['VWAP'].iloc[-1], 2)

                # --- LOGIC 4: DERIVATIVES PRICE-VOLUME BUILDUP CONFLUENCE ---
                price_diff = df_today['Close'].diff()
                vol_diff = df_today['Volume'].diff()
                if not price_diff.empty and not vol_diff.empty:
                    last_p_diff = price_diff.iloc[-1]
                    last_v_diff = vol_diff.iloc[-1]
                    if last_p_diff > 0 and last_v_diff > 0:
                        buildup_status = "LONG_BUILDUP"
                    elif last_p_diff < 0 and last_v_diff > 0:
                        buildup_status = "SHORT_BUILDUP"
                    elif last_p_diff > 0 and last_v_diff < 0:
                        buildup_status = "SHORT_COVERING"
                    else:
                        buildup_status = "LONG_UNWINDING"

                open_price = df_today['Open'].iloc[0]
                df_today['Pct_From_Open'] = ((df_today['Close'] - open_price) / open_price) * 100
                mean_vol = df_today['Volume'].mean()
                df_today['Vol_Ratio'] = df_today['Volume'] / (mean_vol if mean_vol > 0 else 1)
                
                df_orb_range = df_today.between_time('09:15', '09:30')
                if not df_orb_range.empty:
                    orb_high = df_orb_range['High'].max()
                    orb_low = df_orb_range['Low'].min()
                    df_post_orb = df_today.between_time('09:35', '11:30')
                    
                    # ORB + VWAP Confirmation Filter
                    orb_breakouts = df_post_orb[
                        ((df_post_orb['Close'] > orb_high) & (df_post_orb['Close'] > df_post_orb['VWAP'])) | 
                        ((df_post_orb['Close'] < orb_low) & (df_post_orb['Close'] < df_post_orb['VWAP']))
                    ]
                    
                    if not orb_breakouts.empty:
                        first_dt = orb_breakouts.index[0]
                        first_breakout_time = first_dt.strftime('%H:%M')
                        morning_change = orb_breakouts['Pct_From_Open'].iloc[0]
                        morning_vol_spike = round(orb_breakouts['Vol_Ratio'].iloc[0], 2)
                    else:
                        df_morning = df_today.between_time('09:15', '11:30')
                        if not df_morning.empty:
                            morning_max = df_morning['High'].max()
                            morning_change = ((morning_max - open_price) / open_price) * 100
                            max_dt = df_morning['High'].idxmax()
                            first_breakout_time = max_dt.strftime('%H:%M')

            current_price = df['Close'].iloc[-1]
            prev_day_df = df[df.index.date < today_date]
            prev_close = prev_day_df['Close'].iloc[-1] if not prev_day_df.empty else open_price
            
            ema20_val = df['EMA20'].iloc[-1]
            rsi_val = df['RSI'].iloc[-1]
            
            if not df_today.empty:
                vol_recent = df_today['Volume'].iloc[-5:].mean()
                vol_today_avg = df_today['Volume'].mean()
                r_fact = round((vol_recent / vol_today_avg), 2) if vol_today_avg > 0 else 1.0
            else:
                r_fact = 1.0

            symbol_clean = ticker.replace('NSE:', '').replace('-EQ', '')
            
            all_stocks.append({
                'FullSymbol': ticker,
                'Sector': sector,
                'Symbol': symbol_clean,
                'Chart': make_tradingview_link(symbol_clean),
                'Price': round(current_price, 2),
                'PrevClose': prev_close,
                'EMA20': ema20_val,
                'VWAP': vwap_val,
                'RSI': rsi_val,
                'R Fact': r_fact,
                'Buildup': buildup_status,
                'Time': df.index[-1].strftime('%H:%M'),
                'Morning_Change': round(morning_change, 2),
                'Morning_Time': first_breakout_time,
                'Morning_Vol_Spike': morning_vol_spike
            })
            
    df_result = pd.DataFrame(all_stocks)

    # --- LOGIC 3: SECTOR ALIGNMENT CALCULATION ---
    if not df_result.empty:
        df_result['Change %'] = ((df_result['Price'] - df_result['PrevClose']) / df_result['PrevClose'] * 100).round(2)
        sector_means = df_result.groupby('Sector')['Change %'].transform('mean')
        df_result['Sector_Avg_Change'] = sector_means.round(2)
    
    return df_result

def get_live_data():
    df_data = fetch_base_analytics().copy()
    if df_data.empty:
        return df_data

    live_ticks = st.session_state.get("live_ticks", {})
    
    def update_price(row):
        symbol = row['FullSymbol']
        if symbol in live_ticks:
            return live_ticks[symbol]
        return row['Price']

    df_data['Price'] = df_data.apply(update_price, axis=1)
    df_data['Change %'] = ((df_data['Price'] - df_data['PrevClose']) / df_data['PrevClose'] * 100).round(2)
    df_data['Abs Change'] = df_data['Change %'].abs() + 0.1

    def generate_signal(row):
        price = row['Price']
        above_ema = price > row['EMA20']
        above_vwap = price > row['VWAP']
        rsi_val = row['RSI']
        r_fact = row['R Fact']
        
        if above_ema and above_vwap and rsi_val > 55 and r_fact > 1.2:
            return '<span class="badge-strong-buy">Strong Buy</span>'
        elif above_ema and above_vwap and rsi_val > 50:
            return '<span class="badge-buy">Buy</span>'
            
        elif not above_ema and not above_vwap and rsi_val < 40 and r_fact > 1.2:
            return '<span class="badge-strong-sell">Strong Sell</span>'
        elif not above_ema and not above_vwap and rsi_val < 45:
            return '<span class="badge-sell">Sell</span>'
        else:
            return '<span class="badge-hold">Hold</span>'

    df_data['Signal'] = df_data.apply(generate_signal, axis=1)
    return df_data

# --- APP UI MAIN RENDER ---
st.title("💡 Sector Scope — Fyers Smart Scanner")

df_data = get_live_data()

if not df_data.empty:
    market_badge = '<span style="font-size:12px; color:#3fb950; border:1px solid #238636; padding:2px 6px; border-radius:4px;">⚡ LIVE WEBSOCKET</span>' if is_market_open() else '<span style="font-size:12px; color:#f85149; border:1px solid #da3633; padding:2px 6px; border-radius:4px;">🔴 MARKET CLOSED</span>'

    if app_mode == "Market Pulse":
        st.subheader("🔥 Market Pulse Scanners")
        
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div class="pulse-card">
                <div class="pulse-header">🔥 BREAKOUT BEACON (ORB) 💡 {market_badge}</div>
            </div>
            """, unsafe_allow_html=True)
            
            session_choice = st.selectbox(
                "⏱️ Select Time Window", 
                ["🌅 Morning Session (ORB Based)", "📈 Full Day / Live Market"],
                key="beacon_session"
            )
            
            beacon_df = df_data.copy()
            
            # --- LOGIC 3 + LOGIC 4 MULTI-CONFLUENCE FILTERING IN BEACON ---
            if session_choice == "🌅 Morning Session (ORB Based)":
                # Sector Alignment Filter: Stock Trend & Sector Trend In Sync
                beacon_df = beacon_df[
                    ((beacon_df['Morning_Change'] >= 0) & (beacon_df['Sector_Avg_Change'] >= 0)) | 
                    ((beacon_df['Morning_Change'] < 0) & (beacon_df['Sector_Avg_Change'] < 0))
                ]
                
                beacon_df['Score'] = (beacon_df['Morning_Change'].abs() * beacon_df['Morning_Vol_Spike']).round(2)
                beacon_df['Beacon_Signal'] = beacon_df['Morning_Change'].apply(lambda x: '<span class="badge-bull">BULL</span>' if x >= 0 else '<span class="badge-bear">BEAR</span>')
                beacon_df['Change_Badge'] = beacon_df['Morning_Change'].apply(lambda x: f'<span class="badge-val-green">{x:+.2f}%</span>' if x >= 0 else f'<span class="badge-val-red">{x:.2f}%</span>')
                
                top_breakouts = beacon_df.sort_values(by='Score', ascending=False).drop_duplicates(subset=['Symbol']).head(9)
                display_beacon = top_breakouts[['Beacon_Signal', 'Chart', 'Price', 'Change_Badge', 'Score', 'Morning_Time']].rename(
                    columns={'Beacon_Signal': 'Signal', 'Chart': 'Symbol', 'Change_Badge': '%', 'Score': 'Signal %', 'Morning_Time': 'Time'}
                )
            else:
                # Live Market Mode: VWAP + Sector Alignment Filter
                beacon_df = beacon_df[
                    (((beacon_df['Change %'] >= 0) & (beacon_df['Price'] >= beacon_df['VWAP']) & (beacon_df['Sector_Avg_Change'] >= 0)) | 
                    ((beacon_df['Change %'] < 0) & (beacon_df['Price'] < beacon_df['VWAP']) & (beacon_df['Sector_Avg_Change'] < 0)))
                ]
                beacon_df['Score'] = (beacon_df['Change %'].abs() * 1.2).round(2)
                beacon_df['Beacon_Signal'] = beacon_df['Change %'].apply(lambda x: '<span class="badge-bull">BULL</span>' if x >= 0 else '<span class="badge-bear">BEAR</span>')
                beacon_df['Change_Badge'] = beacon_df['Change %'].apply(lambda x: f'<span class="badge-val-green">{x:+.2f}%</span>' if x >= 0 else f'<span class="badge-val-red">{x:.2f}%</span>')
                
                top_breakouts = beacon_df.sort_values(by='Score', ascending=False).drop_duplicates(subset=['Symbol']).head(9)
                display_beacon = top_breakouts[['Beacon_Signal', 'Chart', 'Price', 'Change_Badge', 'Score', 'Time']].rename(
                    columns={'Beacon_Signal': 'Signal', 'Chart': 'Symbol', 'Change_Badge': '%', 'Score': 'Signal %', 'Time': 'Time'}
                )
                
            st.write(display_beacon.to_html(escape=False, index=False), unsafe_allow_html=True)

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
                vol_filter = st.selectbox("⚡ Volume", ["All", "High (> 1.5)", "Super (> 3.0)"], key="boost_vol")
            with f_col4:
                sector_filter = st.selectbox("🎯 Sector", ["All Sectors"] + list(SECTOR_DATA.keys()), key="boost_sector")
            
            boost_filtered_df = df_data.copy()
            
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
                
            if vol_filter == "High (> 1.5)":
                boost_filtered_df = boost_filtered_df[boost_filtered_df['R Fact'] >= 1.5]
            elif vol_filter == "Super (> 3.0)":
                boost_filtered_df = boost_filtered_df[boost_filtered_df['R Fact'] >= 3.0]
                
            if sector_filter != "All Sectors":
                boost_filtered_df = boost_filtered_df[boost_filtered_df['Sector'] == sector_filter]

            boost_df = boost_filtered_df.sort_values(by='R Fact', ascending=False).drop_duplicates(subset=['Symbol']).head(9)
            boost_df['Boost_Signal'] = boost_df['Change %'].apply(lambda x: '🟢 ⬆️' if x >= 0 else '🔴 ⬇️')
            boost_df['Change_Badge'] = boost_df['Change %'].apply(lambda x: f'<span class="badge-val-green">{x:+.2f}%</span>' if x >= 0 else f'<span class="badge-val-red">{x:.2f}%</span>')

            display_boost = boost_df[['Chart', 'Price', 'Change_Badge', 'R Fact', 'Boost_Signal']].rename(
                columns={'Chart': 'Symbol', 'Change_Badge': '%', 'R Fact': 'R.Fac ⚡', 'Boost_Signal': 'Signal'}
            )
            st.write(display_boost.to_html(escape=False, index=False), unsafe_allow_html=True)

    elif app_mode == "Sector Scope":
        st.subheader("📊 Sector Heatmap (Sorted by Top Performers)")
        
        sector_perf = df_data.groupby('Sector')['Change %'].mean().reset_index()
        sector_perf.rename(columns={'Change %': 'Sector_Avg_Change'}, inplace=True)
        
        df_sorted = pd.merge(df_data, sector_perf, on='Sector')
        df_sorted = df_sorted.sort_values(by=['Sector_Avg_Change', 'Change %'], ascending=[False, False])

        fig_map = px.treemap(
            df_sorted,
            path=[px.Constant("Sector Scope"), 'Sector', 'Symbol'],
            values='Abs Change',
            color='Change %',
            color_continuous_scale=['#FF1744', '#1c2128', '#00E676'],
            color_continuous_midpoint=0,
            custom_data=['Change %', 'Price']
        )
        fig_map.update_traces(texttemplate="<b>%{label}</b><br>₹%{customdata[1]}<br>%{customdata[0]:.2f}%")
        fig_map.update_layout(template="plotly_dark", margin=dict(t=30, l=10, r=10, b=10), height=550, paper_bgcolor="#0d1117", plot_bgcolor="#0d1117")
        st.plotly_chart(fig_map, use_container_width=True)

        st.markdown("---")

        sector_summary = df_data.groupby('Sector').agg(
            Avg_Change=('Change %', 'mean'),
            Bullish_Count=('Change %', lambda x: (x > 0).sum()),
            Total_Count=('Symbol', 'count')
        ).reset_index()

        sector_summary['Raw_Score'] = sector_summary['Avg_Change'] * (sector_summary['Bullish_Count'] / sector_summary['Total_Count'])
        max_val = sector_summary['Raw_Score'].abs().max()
        sector_summary['Strength Score'] = (sector_summary['Raw_Score'] / max_val * 10).round(2) if max_val > 0 else 0
        sector_summary = sector_summary.sort_values(by='Strength Score', ascending=False)

        bar_colors = ['#00E676' if score >= 0 else '#FF1744' for score in sector_summary['Strength Score']]

        st.subheader("📊 Sector Momentum Ranking")
        fig_bar = go.Figure(data=[
            go.Bar(x=sector_summary['Sector'], y=sector_summary['Strength Score'], text=sector_summary['Strength Score'], textposition='outside', marker_color=bar_colors, width=0.45)
        ])
        fig_bar.update_layout(
            template="plotly_dark", height=450, paper_bgcolor="#0d1117", plot_bgcolor="#0d1117",
            xaxis=dict(tickangle=0, showgrid=False, title=None, tickfont=dict(size=11, color='#c9d1d9')),
            yaxis=dict(title="Strength Score (-10 to +10)", range=[-12, 12], showgrid=True, gridcolor="#21262d"),
            margin=dict(t=30, b=50, l=40, r=20)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("---")

        st.subheader("🎯 Sector Drill-down")
        selected_sector = st.selectbox("Select Sector to Inspect:", options=sector_summary['Sector'].tolist())
        sector_stocks = df_data[df_data['Sector'] == selected_sector]
        display_sector = sector_stocks[['Chart', 'Price', 'Change %', 'R Fact', 'Signal']].sort_values(by='Change %', ascending=False).rename(columns={'Chart': 'Symbol ↗'})
        st.write(display_sector.to_html(escape=False, index=False), unsafe_allow_html=True)

else:
    st.error("⚠️ Fyers data fetch nahi ho raha hai. Check karein ki 'fyers_token.txt' mein valid token hai ya nahi!")
