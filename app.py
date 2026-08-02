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

# --- SIDEBAR NAVIGATION (Added as requested) ---
st.sidebar.title("🧭 Dashboard Navigation")
app_mode = st.sidebar.radio("Choose Section:", ["Market Pulse", "Sector Scope"])

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

# FIXED & COMPLETE SECTOR DATA
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
                    else:
                        moderate_breakouts = df_morning[(df_morning['Pct_From_Open'].abs() >= 1.0) & (df_morning['Vol_Ratio'] >= 1.2)]
                        if not moderate_breakouts.empty:
                            first_dt = moderate_breakouts.index[0]
                            first_breakout_time = first_dt.strftime('%H:%M') if hasattr(first_dt, 'strftime') else str(first_dt)[11:16]
                            morning_change = moderate_breakouts['Pct_From_Open'].iloc[0]
                            morning_vol_spike = round(moderate_breakouts['Vol_Ratio'].iloc[0], 2)
                        elif not df_morning.empty:
                            morning_max = df_morning['High'].max()
                            morning_change = ((morning_max - open_price) / open_price) * 100
                            max_dt = df_morning['High'].idxmax()
                            first_breakout_time = max_dt.strftime('%H:%M') if hasattr(max_dt, 'strftime') else str(max_dt)[11:16]

                current_price = df['Close'].iloc[-1]
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
                    'Signal': signal,
                    'Time': formatted_time,
                    'Morning_Change': round(morning_change, 2),
                    'Morning_Time': first_breakout_time,
                    'Morning_Vol_Spike': morning_vol_spike
                })
            except Exception:
                continue
                
    return pd.DataFrame(all_stocks)

st.title("💡 Sector Scope — Smart Scanner")

with st.spinner("Calculating Momentum Indicators & Live Market Scans..."):
    df_data = fetch_sector_analytics()

if not df_data.empty:
    
    market_badge = '<span style="font-size:12px; color:#3fb950; border:1px solid #238636; padding:2px 6px; border-radius:4px;">● LIVE</span>' if is_market_open() else '<span style="font-size:12px; color:#f85149; border:1px solid #da3633; padding:2px 6px; border-radius:4px;">🔴 MARKET CLOSED</span>'

    # --- 1. MARKET PULSE SECTION ---
    if app_mode == "Market Pulse":
        st.subheader("🔥 Market Pulse Scanners")
        
        col1, col2 = st.columns(2)

        # --- LEFT COLUMN: BREAKOUT BEACON ---
        with col1:
            st.markdown(f"""
            <div class="pulse-card">
                <div class="pulse-header">🔥 BREAKOUT BEACON 💡 {market_badge}</div>
            </div>
            """, unsafe_allow_html=True)
            
            session_choice = st.selectbox(
                "⏱️ Select Time Window", 
                ["🌅 Morning Session (09:15 - 11:30 AM)", "📈 Full Day / Live Market"],
                key="beacon_session"
            )
            
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

            display_boost = boost_df[['Chart', 'Change_Badge', 'R Fact', 'Boost_Signal']].rename(
                columns={'Chart': 'Symbol', 'Change_Badge': '%', 'R Fact': 'R.Fac ⚡', 'Boost_Signal': 'Signal'}
            )
            st.write(display_boost.to_html(escape=False, index=False), unsafe_allow_html=True)

    # --- 2. SECTOR SCOPE SECTION ---
    elif app_mode == "Sector Scope":
        st.subheader("MAP Sector Heatmap")
        fig_map = px.treemap(
            df_data,
            path=[px.Constant("Sector Scope"), 'Sector', 'Symbol'],
            values='Abs Change',
            color='Change %',
            color_continuous_scale=['#FF1744', '#1c2128', '#00E676'],
            color_continuous_midpoint=0,
            custom_data=['Change %']
        )
        fig_map.update_traces(
            texttemplate="<b>%{label}</b><br>%{customdata[0]:.2f}%"
        )
        fig_map.update_layout(
            template="plotly_dark", 
            margin=dict(t=30, l=10, r=10, b=10), 
            height=550, 
            paper_bgcolor="#0d1117", 
            plot_bgcolor="#0d1117"
        )
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

        st.subheader("🎯 Sector Drill-down")
        selected_sector = st.selectbox("Select Sector to Inspect:", options=sector_summary['Sector'].tolist())
        sector_stocks = df_data[df_data['Sector'] == selected_sector]
        display_sector = sector_stocks[['Chart', 'Price', 'Change %', 'R Fact', 'Signal']].sort_values(by='Change %', ascending=False).rename(columns={'Chart': 'Symbol ↗'})
        st.write(display_sector.to_html(escape=False, index=False), unsafe_allow_html=True)

else:
    st.error("Data fetch nahi ho raha hai, thodi der baad refresh karein.")
