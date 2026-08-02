import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
from datetime import datetime, time

# 1. Page Configuration
st.set_page_config(page_title="HITISHAL SCANNER — Market Pulse", page_icon="🦄", layout="wide", initial_sidebar_state="expanded")

# --- LOGIN SYSTEM START ---
USER_CREDENTIALS = {
    "admin": "12345",
    "ASHWAJIT": "pass123",
    "HARSHAL": "Shalvi@3009"
}

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

def login():
    st.markdown("<h2 style='text-align: center; color: #38bdf8;'>🔒 HITISHAL SCANNER Login 🦄</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True):
            if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
                st.session_state["authenticated"] = True
                st.success("Login Successful!")
                st.rerun()
            else:
                st.error("Invalid Username or Password!")

if not st.session_state["authenticated"]:
    login()
    st.stop()
# --- LOGIN SYSTEM END ---

# Auto-refresh every 30 seconds
st_autorefresh(interval=30000, limit=None, key="market_refresh")

# --- ULTRA MODERN UI STYLING ---
st.markdown("""
    <style>
    /* Dark Theme Core Background */
    .stApp {
        background-color: #090d16 !important;
        color: #94a3b8;
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit Header/Footer Padding */
    header[data-testid="stHeader"] { background: transparent !important; }
    .block-container { padding-top: 1rem !important; padding-bottom: 2rem !important; }

    /* Top Marquee Ticker Bar */
    .ticker-wrap {
        width: 100%;
        overflow: hidden;
        background-color: #0f172a;
        border-bottom: 1px solid #1e293b;
        white-space: nowrap;
        padding: 8px 0;
        margin-bottom: 15px;
    }
    .ticker {
        display: inline-block;
        animation: marquee 35s linear infinite;
    }
    .ticker-item {
        display: inline-block;
        padding: 0 15px;
        font-size: 12px;
        font-weight: 600;
    }
    .up-val { color: #4ade80; }
    .down-val { color: #f87171; }
    @keyframes marquee {
        0% { transform: translate3d(0, 0, 0); }
        100% { transform: translate3d(-50%, 0, 0); }
    }

    /* Sidebar Custom Styling */
    section[data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid #1e293b;
    }
    .sidebar-brand {
        font-size: 20px;
        font-weight: 800;
        color: #f8fafc;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 20px;
        background: linear-gradient(90deg, #a855f7, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sidebar-section {
        font-size: 11px;
        text-transform: uppercase;
        color: #64748b;
        font-weight: 700;
        letter-spacing: 0.8px;
        margin-top: 15px;
        margin-bottom: 5px;
    }

    /* Card Containers */
    .trade-card {
        background: #121824;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    .card-title-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }
    .card-title {
        font-size: 16px;
        font-weight: 700;
        color: #f8fafc;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Custom HTML Table Styling */
    table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0 6px;
        font-size: 13px;
    }
    th {
        color: #64748b;
        text-align: left;
        padding: 8px 12px;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        border: none;
    }
    td {
        padding: 8px 12px;
        background-color: #0f172a;
        color: #e2e8f0;
        font-weight: 500;
    }
    td:first-child { border-radius: 8px 0 0 8px; }
    td:last-child { border-radius: 0 8px 8px 0; }
    tr:hover td { background-color: #1e293b; }

    /* Pill Badges (BULL/BEAR) */
    .badge-pill-bull {
        background-color: #143522;
        color: #4ade80;
        padding: 4px 16px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 11px;
        display: inline-block;
        border: 1px solid #166534;
    }
    .badge-pill-bear {
        background-color: #3b1719;
        color: #f87171;
        padding: 4px 16px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 11px;
        display: inline-block;
        border: 1px solid #991b1b;
    }

    /* Percentage Value Badges */
    .pct-box-green {
        background-color: #143522;
        color: #4ade80;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 12px;
        display: inline-block;
        min-width: 60px;
        text-align: center;
    }
    .pct-box-red {
        background-color: #3b1719;
        color: #f87171;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 12px;
        display: inline-block;
        min-width: 60px;
        text-align: center;
    }
    
    .live-badge {
        background: #ef4444;
        color: white;
        font-size: 10px;
        font-weight: 800;
        padding: 2px 6px;
        border-radius: 4px;
        margin-left: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. TOP TICKER MARQUEE BAR ---
st.markdown("""
<div class="ticker-wrap">
  <div class="ticker">
    <div class="ticker-item">FTSE <b>10,872.5</b> <span class="down-val">-66.8 (-0.61%)</span></div>
    <div class="ticker-item">S&P 500 <b>7,476.1</b> <span class="up-val">+31.4 (+0.42%)</span></div>
    <div class="ticker-item">DOW JONES <b>52,410.00</b> <span class="up-val">+154.00 (+0.29%)</span></div>
    <div class="ticker-item">NIKKEI <b>62,828</b> <span class="down-val">-764 (-1.20%)</span></div>
    <div class="ticker-item">BTC/USD <b>63,118.19</b> <span class="up-val">+343.43 (+0.55%)</span></div>
    <div class="ticker-item">HSI <b>25,884.43</b> <span class="up-val">+25.55 (+0.10%)</span></div>
    <div class="ticker-item">DAX <b>25,612.03</b> <span class="up-val">+151.55 (+0.60%)</span></div>
  </div>
</div>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR NAVIGATION WITH UNICORN BRANDING ---
with st.sidebar:
    st.markdown('<div class="sidebar-brand">🦄 HITISHAL SCANNER</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-section">📊 Stocks</div>', unsafe_allow_html=True)
    page = st.radio(
        "Stocks Menu", 
        ["Market Pulse", "Insider Strategy", "Sector Scope", "Swing Spectrum"], 
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    if st.button("Logout", use_container_width=True):
        st.session_state["authenticated"] = False
        st.rerun()

def make_tradingview_link(symbol):
    clean_symbol = str(symbol).replace('.NS', '').replace('.BO', '').strip()
    url = f"https://in.tradingview.com/chart/?symbol=NSE:{clean_symbol}"
    return f'<a href="{url}" target="_blank" style="text-decoration:none; color:#38bdf8; font-weight:700;">📈 {clean_symbol}</a>'

# SECTOR DATA DICTIONARY
SECTOR_DATA = {
    'AUTO': [
        'M&M.NS', 'MOTHERSON.NS', 'SAMVARDHANA.NS', 'MARUTI.NS', 'TATAMOTORS.NS', 
        'BAJAJ-AUTO.NS', 'HEROMOTOCO.NS', 'TVSMOTOR.NS', 'EICHERMOT.NS', 'ASHOKLEY.NS', 
        'BHARATFORG.NS', 'BOSCHLTD.NS', 'UNOMINDA.NS', 'TIINDIA.NS', 'EXIDEIND.NS', 
        'BALKRISIND.NS', 'APOLLOTYRE.NS', 'MRF.NS', 'SONACOMS.NS', 'FORCEMOT.NS', 'HYUNDAI.NS'
    ],
    'FIN SERVICE': ['BAJFINANCE.NS', 'BAJAJFINSV.NS', 'MUTHOOTFIN.NS', 'CHOLAFIN.NS', 'JIOFIN.NS', 'LICHSGFIN.NS', 'BSE.NS', 'PFC.NS'],
    'NIFTY 50': ['RELIANCE.NS', 'HDFCBANK.NS', 'ICICIBANK.NS', 'INFY.NS', 'TCS.NS', 'ITC.NS', 'LT.NS', 'AXISBANK.NS'],
    'SENSEX': ['RELIANCE.NS', 'HDFCBANK.NS', 'ICICIBANK.NS', 'INFY.NS', 'TCS.NS', 'BHARTIARTL.NS', 'SBIN.NS', 'KOTAKBANK.NS'],
    'ENERGY': ['RELIANCE.NS', 'NTPC.NS', 'POWERGRID.NS', 'ONGC.NS', 'GAIL.NS', 'BPCL.NS', 'TATAPOWER.NS', 'SUZLON.NS'],
    'PHARMA': ['SUNPHARMA.NS', 'CIPLA.NS', 'DRREDDY.NS', 'DIVISLAB.NS', 'LUPIN.NS', 'ZYDUSLIFE.NS', 'TORNTPHARM.NS', 'MANKIND.NS'],
    'IT': ['TCS.NS', 'INFY.NS', 'HCLTECH.NS', 'WIPRO.NS', 'TECHM.NS', 'LTIM.NS', 'COFORGE.NS', 'PERSISTENT.NS'],
    'BANK': ['HDFCBANK.NS', 'ICICIBANK.NS', 'SBIN.NS', 'KOTAKBANK.NS', 'AXISBANK.NS', 'INDUSINDBK.NS', 'PNB.NS', 'BANKBARODA.NS'],
    'REALTY': ['DLF.NS', 'LODHA.NS', 'GODREJPROP.NS', 'PHOENIXLTD.NS', 'OBEROIRLTY.NS', 'PRESTIGE.NS', 'BRIGADE.NS'],
    'METAL': ['TATASTEEL.NS', 'JINDALSTEL.NS', 'HINDALCO.NS', 'VEDL.NS', 'NATIONALUM.NS', 'SAIL.NS', 'NMDC.NS', 'APLAPOLLO.NS']
}

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

@st.cache_data(ttl=25)
def fetch_sector_analytics():
    all_stocks = []
    for sector, tickers in SECTOR_DATA.items():
        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                df = stock.history(period='5d', interval='5m')
                if df.empty or len(df) < 5:
                    df = stock.history(period='5d', interval='1d')
                    if df.empty:
                        continue
                
                df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean() if len(df) >= 20 else df['Close']
                df['RSI'] = calculate_rsi(df['Close'], 14) if len(df) >= 14 else 50.0
                
                today_date = df.index[-1].date()
                df_today = df[df.index.date == today_date].copy()
                
                morning_change = 0.0
                morning_vol_spike = 1.0
                first_breakout_time = "09:15"
                
                if not df_today.empty:
                    open_price = df_today['Open'].iloc[0]
                    df_today['VWAP'] = (df_today['Volume'] * (df_today['High'] + df_today['Low'] + df_today['Close']) / 3).cumsum() / (df_today['Volume'].cumsum().replace(0, 1))
                    df_today['Pct_From_Open'] = ((df_today['Close'] - open_price) / open_price) * 100
                    mean_vol = df_today['Volume'].mean()
                    df_today['Vol_Ratio'] = df_today['Volume'] / (mean_vol if mean_vol > 0 else 1)
                    df_today['Rolling_Vol_Ratio'] = df_today['Vol_Ratio'].rolling(window=2, min_periods=1).mean()
                    
                    df_morning = df_today.between_time('09:15', '11:30')
                    strong_breakouts = df_morning[
                        (df_morning['Close'] >= df_morning['VWAP']) & 
                        (df_morning['Pct_From_Open'].abs() >= 1.2) & 
                        (df_morning['Rolling_Vol_Ratio'] >= 1.5)
                    ]
                    
                    if not strong_breakouts.empty:
                        first_dt = strong_breakouts.index[0]
                        first_breakout_time = first_dt.strftime('%H:%M') if hasattr(first_dt, 'strftime') else str(first_dt)[11:16]
                        morning_change = strong_breakouts['Pct_From_Open'].iloc[0]
                        morning_vol_spike = round(strong_breakouts['Rolling_Vol_Ratio'].iloc[0], 2)
                    elif not df_morning.empty:
                        morning_max = df_morning['High'].max()
                        morning_change = ((morning_max - open_price) / open_price) * 100
                        max_dt = df_morning['High'].idxmax()
                        first_breakout_time = max_dt.strftime('%H:%M') if hasattr(max_dt, 'strftime') else str(max_dt)[11:16]

                current_price = df['Close'].iloc[-1]
                prev_close = df['Close'].iloc[0]
                pct_change = round(((current_price - prev_close) / prev_close) * 100, 2)
                
                if not df_today.empty:
                    vol_recent = df_today['Volume'].iloc[-5:].mean()
                    vol_today_avg = df_today['Volume'].mean()
                    r_fact = round((vol_recent / vol_today_avg), 2) if vol_today_avg > 0 else 1.0
                else:
                    vol_recent = df['Volume'].iloc[-5:].mean()
                    vol_avg = df['Volume'].mean()
                    r_fact = round((vol_recent / vol_avg), 2) if vol_avg > 0 else 1.0

                symbol_clean = ticker.replace('.NS', '')
                last_candle_time = df.index[-1]
                formatted_time = last_candle_time.strftime('%H:%M') if hasattr(last_candle_time, 'strftime') else str(last_candle_time)[11:16]
                
                all_stocks.append({
                    'Sector': sector,
                    'Symbol': symbol_clean,
                    'Chart': make_tradingview_link(symbol_clean),
                    'Price': round(current_price, 2),
                    'Change %': pct_change,
                    'Abs Change': abs(pct_change) + 0.1,
                    'R Fact': r_fact,
                    'Time': formatted_time,
                    'Morning_Change': round(morning_change, 2),
                    'Morning_Time': first_breakout_time,
                    'Morning_Vol_Spike': morning_vol_spike
                })
            except Exception:
                continue
                
    return pd.DataFrame(all_stocks)

# DATA FETCHING
with st.spinner("Fetching Market Data..."):
    df_data = fetch_sector_analytics()

# ==============================================================================
# PAGE 1: MARKET PULSE
# ==============================================================================
if page == "Market Pulse":
    st.markdown("<h1 style='color:#f8fafc; font-size:28px; font-weight:800; margin-bottom:15px;'>Market Pulse 🦄</h1>", unsafe_allow_html=True)

    if not df_data.empty:
        col1, col2 = st.columns(2)
        
        # --- BREAKOUT BEACON CARD ---
        with col1:
            st.markdown("""
            <div class="trade-card">
                <div class="card-title-row">
                    <div class="card-title">🔥 BREAKOUT BEACON 💡 <span class="live-badge">LIVE</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            session_choice = st.selectbox(
                "Time Window", 
                ["🌅 Morning Session (09:15 - 11:30 AM)", "📈 Full Day / Live Market"],
                key="beacon_session"
            )
            
            beacon_df = df_data.copy()
            if session_choice == "🌅 Morning Session (09:15 - 11:30 AM)":
                beacon_df['Score'] = (beacon_df['Morning_Change'].abs() * beacon_df['Morning_Vol_Spike']).round(2)
                beacon_df['Signal'] = beacon_df['Morning_Change'].apply(lambda x: '<span class="badge-pill-bull">BULL</span>' if x >= 0 else '<span class="badge-pill-bear">BEAR</span>')
                beacon_df['Change'] = beacon_df['Morning_Change'].apply(lambda x: f'<span class="pct-box-green">{x:+.2f}%</span>' if x >= 0 else f'<span class="pct-box-red">{x:.2f}%</span>')
                
                top_breakouts = beacon_df.sort_values(by='Score', ascending=False).drop_duplicates(subset=['Symbol']).head(9)
                display_beacon = top_breakouts[['Signal', 'Chart', 'Change', 'Score', 'Morning_Time']].rename(
                    columns={'Chart': 'Symbol', 'Change': '%', 'Score': 'Signal %', 'Morning_Time': 'Time'}
                )
            else:
                beacon_df['Score'] = (beacon_df['Change %'].abs() * 1.2).round(2)
                beacon_df['Signal'] = beacon_df['Change %'].apply(lambda x: '<span class="badge-pill-bull">BULL</span>' if x >= 0 else '<span class="badge-pill-bear">BEAR</span>')
                beacon_df['Change'] = beacon_df['Change %'].apply(lambda x: f'<span class="pct-box-green">{x:+.2f}%</span>' if x >= 0 else f'<span class="pct-box-red">{x:.2f}%</span>')
                
                top_breakouts = beacon_df.sort_values(by='Score', ascending=False).drop_duplicates(subset=['Symbol']).head(9)
                display_beacon = top_breakouts[['Signal', 'Chart', 'Change', 'Score', 'Time']].rename(
                    columns={'Chart': 'Symbol', 'Change': '%', 'Score': 'Signal %'}
                )
                
            st.write(display_beacon.to_html(escape=False, index=False), unsafe_allow_html=True)

        # --- INTRADAY BOOST CARD ---
        with col2:
            st.markdown("""
            <div class="trade-card">
                <div class="card-title-row">
                    <div class="card-title">⚡ INTRADAY BOOST 🚀 <span class="live-badge">LIVE</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                trend_filter = st.selectbox("Trend", ["Neutral (All)", "Bullish Only 🟢", "Bearish Only 🔴"], key="boost_trend")
            with f_col2:
                vol_filter = st.selectbox("Volume Surge", ["All", "High (> 1.5)", "Super (> 3.0)"], key="boost_vol")
            
            boost_df = df_data.copy()
            if trend_filter == "Bullish Only 🟢":
                boost_df = boost_df[boost_df['Change %'] >= 0]
            elif trend_filter == "Bearish Only 🔴":
                boost_df = boost_df[boost_df['Change %'] < 0]
                
            if vol_filter == "High (> 1.5)":
                boost_df = boost_df[boost_df['R Fact'] >= 1.5]
            elif vol_filter == "Super (> 3.0)":
                boost_df = boost_df[boost_df['R Fact'] >= 3.0]

            top_boost = boost_df.sort_values(by='R Fact', ascending=False).drop_duplicates(subset=['Symbol']).head(9)
            top_boost['Change'] = top_boost['Change %'].apply(lambda x: f'<span class="pct-box-green">{x:+.2f}%</span>' if x >= 0 else f'<span class="pct-box-red">{x:.2f}%</span>')
            top_boost['Signal'] = top_boost['Change %'].apply(lambda x: '🟢 ⬆️' if x >= 0 else '🔴 ⬇️')

            display_boost = top_boost[['Chart', 'Change', 'R Fact', 'Signal']].rename(
                columns={'Chart': 'Symbol', 'Change': '%', 'R Fact': 'R.Fac ⚡'}
            )
            st.write(display_boost.to_html(escape=False, index=False), unsafe_allow_html=True)
    else:
        st.error("Market data load nahi ho pa raha hai.")

# ==============================================================================
# PAGE 2: SECTOR SCOPE
# ==============================================================================
elif page == "Sector Scope":
    st.markdown("<h1 style='color:#f8fafc; font-size:28px; font-weight:800; margin-bottom:15px;'>Sector Scope</h1>", unsafe_allow_html=True)
    if not df_data.empty:
        fig_map = px.treemap(
            df_data,
            path=[px.Constant("HITISHAL SCANNER"), 'Sector', 'Symbol'],
            values='Abs Change',
            color='Change %',
            color_continuous_scale=['#f87171', '#0f172a', '#4ade80'],
            color_continuous_midpoint=0,
            custom_data=['Change %']
        )
        fig_map.update_traces(texttemplate="<b>%{label}</b><br>%{customdata[0]:.2f}%")
        fig_map.update_layout(
            template="plotly_dark", 
            margin=dict(t=20, l=0, r=0, b=0), 
            height=550, 
            paper_bgcolor="#090d16", 
            plot_bgcolor="#090d16"
        )
        st.plotly_chart(fig_map, use_container_width=True)

# ==============================================================================
# PAGE 3 & 4: OTHER SECTIONS
# ==============================================================================
elif page == "Insider Strategy":
    st.markdown("<h1 style='color:#f8fafc; font-size:28px; font-weight:800;'>Insider Strategy</h1>", unsafe_allow_html=True)
    st.info("🎯 High Institutional Activity & Block Deals Scanner - Coming Soon.")

elif page == "Swing Spectrum":
    st.markdown("<h1 style='color:#f8fafc; font-size:28px; font-weight:800;'>Swing Spectrum</h1>", unsafe_allow_html=True)
    st.info("📈 Multi-day Swing Trade setups & EMA Crossover Scanner - Coming Soon.")
