import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# 1. Page Configuration
st.set_page_config(page_title="HITISHAL SCANNER — Market Pulse", page_icon="🦄", layout="wide", initial_sidebar_state="expanded")

# --- LOGIN SYSTEM ---
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

# Auto-refresh every 30 seconds
st_autorefresh(interval=30000, limit=None, key="market_refresh")

# --- ULTRA MODERN UI & COMPACT FILTER STYLING ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0d0f12 !important;
        color: #94a3b8;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    header[data-testid="stHeader"] { background: transparent !important; }
    .block-container { padding-top: 1rem !important; padding-bottom: 2rem !important; }

    /* Top Marquee Ticker Bar */
    .ticker-wrap {
        width: 100%;
        overflow: hidden;
        background-color: #12161f;
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

    /* Outer Scanner Box */
    .scanner-box {
        background-color: #111317;
        border: 1px solid #23272f;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 15px;
    }

    /* Compact Header Row matching Image */
    .card-header-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 10px;
        flex-wrap: wrap;
        gap: 10px;
    }
    .card-title-group {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .card-title-text {
        font-size: 15px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: 0.5px;
    }
    .how-to-use {
        color: #38bdf8;
        font-size: 11px;
        font-weight: 600;
        text-decoration: none;
    }
    .live-badge-pill {
        background: #ef4444;
        color: white;
        font-size: 9px;
        font-weight: 800;
        padding: 2px 6px;
        border-radius: 10px;
    }

    /* Streamlit Widget Compact Adjustments */
    div[data-baseweb="select"] > div {
        background-color: #1a1d24 !important;
        border-color: #2a2e39 !important;
        color: #ffffff !important;
        min-height: 30px !important;
        font-size: 12px !important;
        border-radius: 6px !important;
    }
    div[data-baseweb="select"] span {
        color: #ffffff !important;
        font-size: 12px !important;
    }
    
    /* Input Search Box Styling */
    div[data-baseweb="input"] > div {
        background-color: #1a1d24 !important;
        border-color: #2a2e39 !important;
        border-radius: 6px !important;
        min-height: 30px !important;
    }
    div[data-baseweb="input"] input {
        color: #ffffff !important;
        font-size: 12px !important;
        padding: 4px 8px !important;
    }

    /* TABLE STYLING */
    .custom-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 8px;
    }
    .custom-table th {
        background-color: #1a1d24;
        color: #8b949e;
        padding: 8px 10px;
        font-size: 11px;
        font-weight: 600;
        text-align: left;
        border-bottom: 1px solid #23272f;
    }
    .custom-table td {
        padding: 7px 10px;
        vertical-align: middle;
        font-size: 12px;
        font-weight: 600;
        border-bottom: 1px solid #181b20;
    }

    /* Signal Pills (BULL / BEAR) */
    .pill-bull {
        background-color: #c2f0c2;
        color: #155724;
        padding: 3px 12px;
        border-radius: 20px;
        font-weight: 800;
        font-size: 10px;
        display: inline-block;
        text-align: center;
        min-width: 55px;
    }
    .pill-bear {
        background-color: #ffcdd2;
        color: #721c24;
        padding: 3px 12px;
        border-radius: 20px;
        font-weight: 800;
        font-size: 10px;
        display: inline-block;
        text-align: center;
        min-width: 55px;
    }

    /* Percentage Oval Badges */
    .pct-pill-green {
        background-color: #c2f0c2;
        color: #0f401b;
        padding: 3px 10px;
        border-radius: 14px;
        font-weight: 800;
        font-size: 11px;
        display: inline-block;
        min-width: 55px;
        text-align: center;
    }
    .pct-pill-red {
        background-color: #ffcdd2;
        color: #5c131a;
        padding: 3px 10px;
        border-radius: 14px;
        font-weight: 800;
        font-size: 11px;
        display: inline-block;
        min-width: 55px;
        text-align: center;
    }

    /* Symbol + Chart Button */
    .sym-flex {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 6px;
    }
    .sym-text {
        color: #ffffff;
        font-weight: 700;
        font-size: 12px;
    }
    .chart-icon-btn {
        background-color: #0d6efd;
        color: #ffffff !important;
        font-size: 10px;
        padding: 2px 5px;
        border-radius: 4px;
        text-decoration: none;
        font-weight: bold;
        display: inline-flex;
        align-items: center;
        gap: 2px;
    }

    .signal-pct-text { color: #ffffff; font-weight: 700; }
    .time-text { color: #e2e8f0; font-size: 11px; }
    .arrow-up { color: #22c55e; font-size: 15px; }
    .arrow-down { color: #ef4444; font-size: 15px; }
    </style>
""", unsafe_allow_html=True)

# Top Marquee Bar
st.markdown("""
<div class="ticker-wrap">
  <div class="ticker">
    <div class="ticker-item">FTSE <b>10,872.5</b> <span class="down-val">-66.8 (-0.61%)</span></div>
    <div class="ticker-item">S&P 500 <b>7,476.1</b> <span class="up-val">+31.4 (+0.42%)</span></div>
    <div class="ticker-item">DOW JONES <b>52,410.00</b> <span class="up-val">+154.00 (+0.29%)</span></div>
    <div class="ticker-item">NIKKEI <b>62,828</b> <span class="down-val">-764 (-1.20%)</span></div>
    <div class="ticker-item">BTC/USD <b>63,118.19</b> <span class="up-val">+343.43 (+0.55%)</span></div>
  </div>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<div style="font-size:18px; font-weight:800; color:#fff; margin-bottom:20px;">🦄 HITISHAL SCANNER</div>', unsafe_allow_html=True)
    page = st.radio("Navigation", ["Market Pulse", "Insider Strategy", "Sector Scope", "Swing Spectrum"], label_visibility="collapsed")
    st.markdown("---")
    if st.button("Logout", use_container_width=True):
        st.session_state["authenticated"] = False
        st.rerun()

SECTOR_DATA = {
    'AUTO': ['M&M.NS', 'MARUTI.NS', 'TATAMOTORS.NS', 'BAJAJ-AUTO.NS', 'EICHERMOT.NS'],
    'FIN SERVICE': ['BAJFINANCE.NS', 'BAJAJFINSV.NS', 'JIOFIN.NS', 'BAJAJHLDNG.NS'],
    'NIFTY 50': ['DELHIVERY.NS', 'INDUSTOWER.NS', 'DIXON.NS', 'APLAPOLLO.NS', 'KAYNES.NS', 'PREMIERENE.NS', 'GAIL.NS', 'INOXWIND.NS', 'PERSISTENT.NS', 'TORNTPHARM.NS', 'MOTHERSON.NS']
}

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
                
                current_price = df['Close'].iloc[-1]
                prev_close = df['Close'].iloc[0]
                pct_change = round(((current_price - prev_close) / prev_close) * 100, 2)
                
                today_date = df.index[-1].date()
                df_today = df[df.index.date == today_date].copy()
                
                if not df_today.empty:
                    vol_recent = df_today['Volume'].iloc[-5:].mean()
                    vol_today_avg = df_today['Volume'].mean()
                    r_fact = round((vol_recent / vol_today_avg), 2) if vol_today_avg > 0 else 1.0
                else:
                    r_fact = 1.0

                symbol_clean = ticker.replace('.NS', '')
                last_time = df.index[-1].strftime('%H:%M') if hasattr(df.index[-1], 'strftime') else "09:25"
                
                all_stocks.append({
                    'Sector': sector,
                    'Symbol': symbol_clean,
                    'Price': round(current_price, 2),
                    'Change %': pct_change,
                    'R Fact': r_fact,
                    'Time': last_time,
                    'Signal %': round(abs(pct_change) * 1.15, 2)
                })
            except Exception:
                continue
    return pd.DataFrame(all_stocks)

with st.spinner("Loading Live Market Feed..."):
    df_data = fetch_sector_analytics()

if page == "Market Pulse":
    st.markdown("<h1 style='color:#f8fafc; font-size:24px; font-weight:800; margin-bottom:12px;'>Market Pulse 🦄</h1>", unsafe_allow_html=True)

    if not df_data.empty:
        col1, col2 = st.columns(2)

        # --- 1. BREAKOUT BEACON ---
        with col1:
            st.markdown("""
            <div class="card-header-row">
                <div class="card-title-group">
                    <span style="font-size:16px;">🕯️🔥</span>
                    <span class="card-title-text">BREAKOUT BEACON</span>
                    <span>💡</span>
                    <span class="how-to-use">How to use ▶</span>
                    <span class="live-badge-pill">LIVE</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            b_f1, b_f2, b_f3 = st.columns([1.2, 1.2, 1.6])
            with b_f1:
                b_trend = st.selectbox("Trend", ["Neutral", "Bullish 🟢", "Bearish 🔴"], key="b_tr", label_visibility="collapsed")
            with b_f2:
                b_sec = st.selectbox("Sector", ["All Sectors", "AUTO", "FIN SERVICE", "NIFTY 50"], key="b_sec", label_visibility="collapsed")
            with b_f3:
                b_search = st.text_input("Search", placeholder="🔍 Search...", key="b_sr", label_visibility="collapsed")

            b_df = df_data.copy()
            if b_search:
                b_df = b_df[b_df['Symbol'].str.contains(b_search.upper(), na=False)]
            if b_sec != "All Sectors":
                b_df = b_df[b_df['Sector'] == b_sec]
            if b_trend == "Bullish 🟢":
                b_df = b_df[b_df['Change %'] >= 0]
            elif b_trend == "Bearish 🔴":
                b_df = b_df[b_df['Change %'] < 0]

            table_html = """
            <table class="custom-table">
                <thead>
                    <tr>
                        <th>Signal</th>
                        <th>Symbol</th>
                        <th style="text-align:center;">%</th>
                        <th>Signal % 🪟</th>
                        <th>Time</th>
                    </tr>
                </thead>
                <tbody>
            """
            
            for _, row in b_df.head(9).iterrows():
                sig_html = '<span class="pill-bull">BULL</span>' if row['Change %'] >= 0 else '<span class="pill-bear">BEAR</span>'
                pct_html = f'<span class="pct-pill-green">{row["Change %"]:+.2f}</span>' if row['Change %'] >= 0 else f'<span class="pct-pill-red">{row["Change %"]:.2f}</span>'
                chart_link = f'https://in.tradingview.com/chart/?symbol=NSE:{row["Symbol"]}'
                
                table_html += f"""
                <tr>
                    <td>{sig_html}</td>
                    <td>
                        <div class="sym-flex">
                            <span class="sym-text">{row['Symbol']}</span>
                            <a href="{chart_link}" target="_blank" class="chart-icon-btn">📊+</a>
                        </div>
                    </td>
                    <td style="text-align:center;">{pct_html}</td>
                    <td class="signal-pct-text">{row['Signal %']}</td>
                    <td class="time-text">{row['Time']}</td>
                </tr>
                """
            table_html += "</tbody></table>"  # FIXED HERE (added closing /)
            st.markdown(table_html, unsafe_allow_html=True)

        # --- 2. INTRADAY BOOST ---
        with col2:
            st.markdown("""
            <div class="card-header-row">
                <div class="card-title-group">
                    <span style="font-size:16px;">🚀🔥</span>
                    <span class="card-title-text">INTRADAY BOOST</span>
                    <span>💡</span>
                    <span class="how-to-use">How to use ▶</span>
                    <span class="live-badge-pill">LIVE</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            i_f1, i_f2, i_f3 = st.columns([1.2, 1.2, 1.6])
            with i_f1:
                i_trend = st.selectbox("Trend", ["Neutral", "Bullish 🟢", "Bearish 🔴"], key="i_tr", label_visibility="collapsed")
            with i_f2:
                i_sec = st.selectbox("Sector", ["All Sectors", "AUTO", "FIN SERVICE", "NIFTY 50"], key="i_sec", label_visibility="collapsed")
            with i_f3:
                i_search = st.text_input("Search", placeholder="🔍 Search...", key="i_sr", label_visibility="collapsed")

            i_df = df_data.copy()
            if i_search:
                i_df = i_df[i_df['Symbol'].str.contains(i_search.upper(), na=False)]
            if i_sec != "All Sectors":
                i_df = i_df[i_df['Sector'] == i_sec]
            if i_trend == "Bullish 🟢":
                i_df = i_df[i_df['Change %'] >= 0]
            elif i_trend == "Bearish 🔴":
                i_df = i_df[i_df['Change %'] < 0]

            table_html_boost = """
            <table class="custom-table">
                <thead>
                    <tr>
                        <th>Symbol</th>
                        <th style="text-align:center;">%</th>
                        <th>R.Fac 🪟</th>
                        <th style="text-align:center;">Signal</th>
                    </tr>
                </thead>
                <tbody>
            """
            
            for _, row in i_df.head(9).iterrows():
                pct_html = f'<span class="pct-pill-green">{row["Change %"]:+.2f}</span>' if row['Change %'] >= 0 else f'<span class="pct-pill-red">{row["Change %"]:.2f}</span>'
                arrow_html = '<span class="arrow-up">⬆</span>' if row['Change %'] >= 0 else '<span class="arrow-down">⬇</span>'
                chart_link = f'https://in.tradingview.com/chart/?symbol=NSE:{row["Symbol"]}'
                
                table_html_boost += f"""
                <tr>
                    <td>
                        <div class="sym-flex">
                            <span class="sym-text">{row['Symbol']}</span>
                            <a href="{chart_link}" target="_blank" class="chart-icon-btn">📊+</a>
                        </div>
                    </td>
                    <td style="text-align:center;">{pct_html}</td>
                    <td class="signal-pct-text">{row['R Fact']}</td>
                    <td style="text-align:center;">{arrow_html}</td>
                </tr>
                """
            table_html_boost += "</tbody></table>"  # FIXED HERE (added closing /)
            st.markdown(table_html_boost, unsafe_allow_html=True)

elif page == "Sector Scope":
    st.markdown("<h1 style='color:#f8fafc; font-size:24px; font-weight:800;'>Sector Scope</h1>", unsafe_allow_html=True)
    if not df_data.empty:
        fig_map = px.treemap(
            df_data,
            path=[px.Constant("SCANNER"), 'Sector', 'Symbol'],
            values='Price',
            color='Change %',
            color_continuous_scale=['#f87171', '#0f172a', '#4ade80']
        )
        st.plotly_chart(fig_map, use_container_width=True)
