import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
from datetime import datetime, time

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
if st.sidebar.button("Logout"):
    st.session_state["authenticated"] = False
    st.rerun()
# --- LOGIN SYSTEM END ---

st.sidebar.markdown("---")
st_autorefresh(interval=30000, limit=None, key="sector_refresh")

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
    clean_symbol = str(symbol).replace('.NS', '').replace('.BO', '').strip()
    url = f"https://in.tradingview.com/chart/?symbol=NSE:{clean_symbol}"
    return f'<a href="{url}" target="_blank" style="text-decoration:none; color:#58a6ff; font-weight:bold;">{clean_symbol} ↗</a>'

def is_market_open():
    now = datetime.now()
    if now.weekday() < 5 and time(9, 15) <= now.time() <= time(15, 30):
        return True
    return False

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
                
                if df.empty or len(df) < 20:
                    continue
                
                df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
                df['RSI'] = calculate_rsi(df['Close'], 14)
                
                current_price = df['Close'].iloc[-1]
                prev_close = df['Close'].iloc[0]
                pct_change = ((current_price - prev_close) / prev_close) * 100
                
                ema20_val = df['EMA20'].iloc[-1]
                rsi_val = df['RSI'].iloc[-1]
                
                vol_recent = df['Volume'].iloc[-5:].mean()
                vol_avg = df['Volume'].mean()
                r_fact = round((vol_recent / vol_avg), 2) if vol_avg > 0 else 1.0
                
                above_ema = current_price > ema20_val
                
                if above_ema and rsi_val > 55 and r_fact > 1.2:
                    signal = '<span class="badge-strong-buy">🚀 ⬆️ Strong Buy</span>'
                elif above_ema and rsi_val > 50:
                    signal = '<span class="badge-buy">⬆️ Buy</span>'
                elif not above_ema and rsi_val < 40 and r_fact > 1.2:
                    signal = '<span class="badge-strong-sell">🚀 ⬇️ Strong Sell</span>'
                elif not above_ema and rsi_val < 45:
                    signal = '<span class="badge-sell">⬇️ Sell</span>'
                else:
                    signal = '<span class="badge-hold">❌ Hold</span>'
                
                symbol_clean = ticker.replace('.NS', '')
                
                # Dynamic Last Candle Time Formatting
                last_candle_time = df.index[-1]
                formatted_time = last_candle_time.strftime('%H:%M') if hasattr(last_candle_time, 'strftime') else str(last_candle_time)[11:16]
                
                all_stocks.append({
                    'Sector': sector,
                    'Symbol': symbol_clean,
                    'Chart': make_tradingview_link(symbol_clean),
                    'Price': round(current_price, 2),
                    'Change %': round(pct_change, 2),
                    'Abs Change': abs(pct_change) + 0.1,
                    'R Fact': r_fact,
                    'Signal': signal,
                    'Time': formatted_time
                })
            except Exception:
                continue
                
    return pd.DataFrame(all_stocks)

st.title("💡 Sector Scope — Smart Scanner")

with st.spinner("Calculating Indicators & Live Market Scans..."):
    df_data = fetch_sector_analytics()

if not df_data.empty:
    
    # --- 1. TOP FILTER BAR ---
    st.subheader("🔥 Market Pulse Scanners")
    
    f_col1, f_col2, f_col3, f_col4 = st.columns(4)
    
    with f_col1:
        trend_filter = st.selectbox("↕️ Trend", ["Neutral (All)", "Bullish Only 🟢", "Bearish Only 🔴"], key="trend_f")
    with f_col2:
        price_filter = st.selectbox("₹ Price Range", ["All Prices", "< ₹500", "₹500 - ₹2000", "> ₹2000"], key="price_f")
    with f_col3:
        vol_filter = st.selectbox("⚡ Volume Spike (R.Fac)", ["All", "High Spike (> 1.5)", "Super Spike (> 3.0)"], key="vol_f")
    with f_col4:
        sector_filter = st.selectbox("🎯 Sector Filter", ["All Sectors"] + list(SECTOR_DATA.keys()), key="sector_f")
    
    # FILTER LOGIC
    filtered_df = df_data.copy()
    
    if trend_filter == "Bullish Only 🟢":
        filtered_df = filtered_df[filtered_df['Change %'] >= 0]
    elif trend_filter == "Bearish Only 🔴":
        filtered_df = filtered_df[filtered_df['Change %'] < 0]
        
    if price_filter == "< ₹500":
        filtered_df = filtered_df[filtered_df['Price'] < 500]
    elif price_filter == "₹500 - ₹2000":
        filtered_df = filtered_df[(filtered_df['Price'] >= 500) & (filtered_df['Price'] <= 2000)]
    elif price_filter == "> ₹2000":
        filtered_df = filtered_df[filtered_df['Price'] > 2000]
        
    if vol_filter == "High Spike (> 1.5)":
        filtered_df = filtered_df[filtered_df['R Fact'] >= 1.5]
    elif vol_filter == "Super Spike (> 3.0)":
        filtered_df = filtered_df[filtered_df['R Fact'] >= 3.0]
        
    if sector_filter != "All Sectors":
        filtered_df = filtered_df[filtered_df['Sector'] == sector_filter]

    st.markdown("<br>", unsafe_allow_html=True)
    
    # MARKET PULSE DISPLAY CARDS
    col1, col2 = st.columns(2)
    
    # Data Preparation for Cards
    beacon_df = filtered_df.copy()
    beacon_df['Signal %'] = (beacon_df['Change %'].abs() * 1.2).round(2)
    beacon_df['Beacon_Signal'] = beacon_df['Change %'].apply(lambda x: '<span class="badge-bull">BULL</span>' if x >= 0 else '<span class="badge-bear">BEAR</span>')
    beacon_df['Change_Badge'] = beacon_df['Change %'].apply(lambda x: f'<span class="badge-val-green">{x:+.2f}%</span>' if x >= 0 else f'<span class="badge-val-red">{x:.2f}%</span>')
    
    top_breakouts = beacon_df.sort_values(by='Signal %', ascending=False).drop_duplicates(subset=['Symbol']).head(8)
    
    boost_df = filtered_df.copy().sort_values(by='R Fact', ascending=False).drop_duplicates(subset=['Symbol']).head(8)
    boost_df['Boost_Signal'] = boost_df['Change %'].apply(lambda x: '🟢 ⬆️' if x >= 0 else '🔴 ⬇️')
    boost_df['Change_Badge'] = boost_df['Change %'].apply(lambda x: f'<span class="badge-val-green">{x:+.2f}%</span>' if x >= 0 else f'<span class="badge-val-red">{x:.2f}%</span>')
    
    # Dynamic Market Status Badge
    market_badge = '<span style="font-size:12px; color:#3fb950; border:1px solid #238636; padding:2px 6px; border-radius:4px;">● LIVE</span>' if is_market_open() else '<span style="font-size:12px; color:#f85149; border:1px solid #da3633; padding:2px 6px; border-radius:4px;">🔴 MARKET CLOSED</span>'

    with col1:
        st.markdown(f"""
        <div class="pulse-card">
            <div class="pulse-header">🔥 BREAKOUT BEACON 💡 {market_badge}</div>
        </div>
        """, unsafe_allow_html=True)
        
        display_beacon = top_breakouts[['Beacon_Signal', 'Chart', 'Change_Badge', 'Signal %', 'Time']].rename(
            columns={'Beacon_Signal': 'Signal', 'Chart': 'Symbol', 'Change_Badge': '%', 'Signal %': 'Signal %'}
        )
        st.write(display_beacon.to_html(escape=False, index=False), unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="pulse-card">
            <div class="pulse-header">⚡ INTRADAY BOOST 🚀 {market_badge}</div>
        </div>
        """, unsafe_allow_html=True)
        
        display_boost = boost_df[['Chart', 'Change_Badge', 'R Fact', 'Boost_Signal']].rename(
            columns={'Chart': 'Symbol', 'Change_Badge': '%', 'R Fact': 'R.Fac ⚡', 'Boost_Signal': 'Signal'}
        )
        st.write(display_boost.to_html(escape=False, index=False), unsafe_allow_html=True)

    st.markdown("---")

    # --- 2. SECTOR HEATMAP ---
    st.subheader("🗺️ Sector Heatmap")
    fig_map = px.treemap(
        df_data,
        path=[px.Constant("Sector Scope"), 'Sector', 'Symbol'],
        values='Abs Change',
        color='Change %',
        color_continuous_scale=['#FF1744', '#1c2128', '#00E676'],
        color_continuous_midpoint=0,
        custom_data=['Change %']
    )
    fig_map.update_traces(texttemplate="<b>%{label}</b><br>%{customdata[0]:+.2f}%")
    fig_map.update_layout(template="plotly_dark", margin=dict(t=30, l=10, r=10, b=10), height=550, paper_bgcolor="#0d1117", plot_bgcolor="#0d1117")
    st.plotly_chart(fig_map, use_container_width=True)

    st.markdown("---")

    # --- 3. SECTOR MOMENTUM RANKING ---
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
        go.Bar(
            x=sector_summary['Sector'], y=sector_summary['Strength Score'],
            text=sector_summary['Strength Score'], textposition='outside',
            marker_color=bar_colors, width=0.45
        )
    ])
    fig_bar.update_layout(
        template="plotly_dark", height=450, paper_bgcolor="#0d1117", plot_bgcolor="#0d1117",
        xaxis=dict(tickangle=0, showgrid=False, title=None, tickfont=dict(size=11, color='#c9d1d9')),
        yaxis=dict(title="Strength Score (-10 to +10)", range=[-12, 12], showgrid=True, gridcolor="#21262d"),
        margin=dict(t=30, b=50, l=40, r=20)
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")

    # --- 4. SECTOR DRILL-DOWN TABLE ---
    st.subheader("🎯 Sector Drill-down")
    selected_sector = st.selectbox("Select Sector to Inspect:", options=sector_summary['Sector'].tolist())
    sector_stocks = df_data[df_data['Sector'] == selected_sector]
    display_sector = sector_stocks[['Chart', 'Price', 'Change %', 'R Fact', 'Signal']].sort_values(by='Change %', ascending=False).rename(columns={'Chart': 'Symbol ↗'})
    st.write(display_sector.to_html(escape=False, index=False), unsafe_allow_html=True)

else:
    st.error("Data fetch nahi ho raha hai, thodi der baad refresh karein.")
