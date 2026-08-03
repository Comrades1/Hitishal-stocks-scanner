import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, time
import random

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Smart Scanner - Live Research", layout="wide", initial_sidebar_state="collapsed")

# --- CUSTOM CSS FOR PREMIUM SAAS LOOK ---
st.markdown("""
<style>
/* Dark Theme Backgrounds */
.stApp { background-color: #0b0f19; color: #a0aec0; font-family: 'Inter', sans-serif; }

/* Hide default Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Header Typography */
.main-title { font-size: 32px; font-weight: 800; color: #ffffff; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 1px;}
.main-title span { color: #f5b82e; } /* Yellow Accent */
.sub-title { font-size: 14px; color: #718096; margin-bottom: 25px; max-width: 600px;}

/* Feature Badges */
.feature-row { display: flex; gap: 40px; margin-bottom: 30px; font-size: 13px; font-weight: 500; color: #cbd5e0; }
.feature-item { display: flex; align-items: center; gap: 8px; }
.feature-icon { color: #f5b82e; font-size: 16px; }

/* Top Cards Container */
.status-container { display: flex; gap: 15px; margin-bottom: 20px; }
.status-card { 
    background-color: #111827; border: 1px solid #1f2937; border-radius: 12px; 
    padding: 16px 20px; flex: 1; display: flex; align-items: center; gap: 15px;
}
.status-icon { background-color: #1a202c; padding: 10px; border-radius: 8px; color: #f5b82e; }
.status-info p { margin: 0; font-size: 11px; color: #718096; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600;}
.status-info h4 { margin: 0; font-size: 16px; color: #ffffff; font-weight: 700; margin-top: 3px;}
.status-info span { font-size: 11px; color: #718096; }

/* Filter Bar */
.filter-bar { background-color: #111827; border: 1px solid #1f2937; border-radius: 12px; padding: 12px 20px; margin-bottom: 25px;}

/* Custom Table Styling */
.table-container { background-color: #111827; border-radius: 12px; border: 1px solid #1f2937; padding: 0; overflow: hidden; }
.table-header { padding: 15px 20px; border-bottom: 1px solid #1f2937; display: flex; justify-content: space-between; align-items: center;}
.table-header h3 { margin: 0; font-size: 14px; color: #ffffff; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;}

table { width: 100%; border-collapse: collapse; text-align: left; font-size: 13px; }
thead { background-color: #111827; color: #718096; font-size: 11px; text-transform: uppercase; }
th { padding: 15px 20px; border-bottom: 1px solid #1f2937; font-weight: 600;}
td { padding: 15px 20px; border-bottom: 1px solid #1f2937; color: #cbd5e0; vertical-align: middle; }
tr:hover { background-color: #1a202c; }
tr:last-child td { border-bottom: none; }

/* Badges & Indicators */
.stock-name { font-weight: 700; color: #ffffff; font-size: 14px; display: block; }
.stock-desc { font-size: 11px; color: #718096; }

.trend-bullish { color: #10b981; font-weight: 600; display: flex; align-items: center; gap: 5px; }
.trend-bearish { color: #ef4444; font-weight: 600; display: flex; align-items: center; gap: 5px; }

.strength-score { font-weight: 700; color: #ffffff; font-size: 14px; }
.strength-conf { font-size: 11px; color: #718096; }
.progress-bar { width: 40px; height: 4px; background-color: #374151; border-radius: 2px; margin-top: 4px; display: inline-block; }
.progress-fill { height: 100%; background-color: #f5b82e; border-radius: 2px; }

.risk-high { background-color: rgba(239, 68, 68, 0.1); color: #ef4444; padding: 4px 10px; border-radius: 4px; font-size: 10px; font-weight: 700; border: 1px solid rgba(239, 68, 68, 0.2); }
.risk-med { background-color: rgba(245, 184, 46, 0.1); color: #f5b82e; padding: 4px 10px; border-radius: 4px; font-size: 10px; font-weight: 700; border: 1px solid rgba(245, 184, 46, 0.2); }

.btn-view { border: 1px solid #374151; background: transparent; color: #ffffff; padding: 6px 12px; border-radius: 6px; font-size: 12px; font-weight: 600; text-decoration: none; display: inline-flex; align-items: center; gap: 5px; transition: 0.2s;}
.btn-view:hover { background-color: #374151; }
</style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---
def get_market_status():
    now = datetime.now()
    if now.weekday() < 5 and time(9, 15) <= now.time() <= time(15, 30):
        return "Market Open", "Closes 03:30 PM", True
    return "Market Closed", "Opens 09:15 AM (Mon-Fri)", False

def generate_mock_data():
    """Fetching lightweight real data mixed with custom logic for trial UI"""
    tickers = ['LTIM.NS', 'TCS.NS', 'SBIN.NS', 'RELIANCE.NS', 'M&M.NS', 'TATAMOTORS.NS', 'SUNPHARMA.NS', 'ITC.NS']
    data = []
    
    for i, t in enumerate(tickers):
        try:
            stock = yf.Ticker(t)
            hist = stock.history(period="5d")
            if hist.empty: continue
            
            close = hist['Close'].iloc[-1]
            prev = hist['Close'].iloc[-2]
            change = ((close - prev) / prev) * 100
            
            # Simulated logic for UI display
            trend = "Bullish" if change >= 0 else "Bearish"
            strength = round(min(10.0, abs(change) * 3 + random.uniform(2, 5)), 1)
            conf = min(99, int(strength * 10))
            risk = "HIGH" if abs(change) > 2 else "MED"
            
            clean_sym = t.replace(".NS", "")
            
            data.append({
                "id": i + 1,
                "symbol": clean_sym,
                "desc": f"{clean_sym} • Equity",
                "trend": trend,
                "strength": f"{strength}/10",
                "conf": f"Conf {conf}%",
                "fill": min(100, int((strength/10)*100)),
                "reason": "Auto analysis • Vol Breakout" if change > 0 else "Auto analysis • Trend Reversal",
                "risk": risk,
                "published": datetime.now().strftime("%I:%M %p").lower()
            })
        except:
            continue
            
    # Sort to show high strength top
    data = sorted(data, key=lambda x: float(x['strength'].split('/')[0]), reverse=True)[:7]
    return data

# --- MAIN UI RENDER ---

# 1. Header Section
st.markdown("""
<div class="main-title">SMART <span>SCANNER</span> LIVE RESEARCH</div>
<div class="sub-title">Out of thousands of listed stocks, our algorithm hand-picks only high-conviction momentum opportunities for you.</div>

<div class="feature-row">
    <div class="feature-item"><span class="feature-icon">🛡️</span> Expert Logic</div>
    <div class="feature-item"><span class="feature-icon">📈</span> High Probability Setups</div>
    <div class="feature-item"><span class="feature-icon">⚡</span> Data + Price Action</div>
    <div class="feature-item"><span class="feature-icon">⏱️</span> Time Saving</div>
</div>
""", unsafe_allow_html=True)

# 2. Status Cards
status, sub_status, is_open = get_market_status()
current_date = datetime.now().strftime("%d %B %Y")
current_day = datetime.now().strftime("%A")
last_updated = datetime.now().strftime("%I:%M %p")

st.markdown(f"""
<div class="status-container">
    <div class="status-card">
        <div class="status-icon">📅</div>
        <div class="status-info">
            <p>Date</p>
            <h4>{current_date}</h4>
            <span>{current_day}</span>
        </div>
    </div>
    <div class="status-card">
        <div class="status-icon">🕒</div>
        <div class="status-info">
            <p>Market Status</p>
            <h4>{status}</h4>
            <span>{sub_status}</span>
        </div>
    </div>
    <div class="status-card">
        <div class="status-icon">✨</div>
        <div class="status-info">
            <p>Today's Research</p>
            <h4>7</h4>
            <span>Top momentum picks</span>
        </div>
    </div>
    <div class="status-card">
        <div class="status-icon">🔄</div>
        <div class="status-info">
            <p>Last Updated</p>
            <h4>{last_updated}</h4>
            <span>Auto-refreshes live</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 3. Filter Bar (Mockup for UI)
cols = st.columns([3, 1.5, 1.5, 1.5, 1, 1])
with cols[0]: st.text_input("🔍 Search symbol or name", label_visibility="collapsed", placeholder="Search symbol or name...")
with cols[1]: st.selectbox("Sectors", ["All sectors", "IT", "Bank", "Auto"], label_visibility="collapsed")
with cols[2]: st.selectbox("Risk", ["All risk", "High", "Med", "Low"], label_visibility="collapsed")
with cols[3]: st.selectbox("Trend", ["All trend", "Bullish", "Bearish"], label_visibility="collapsed")
with cols[4]: st.selectbox("Score", ["Score", "Top"], label_visibility="collapsed")
with cols[5]: st.selectbox("Conf", ["Conf", "> 80%"], label_visibility="collapsed")

# 4. Table Render
stocks = generate_mock_data()

table_html = """<div class="table-container">
<div class="table-header">
<h3>Research Picks</h3>
<span style="color: #718096; font-size: 12px;">7 stocks</span>
</div>
<table>
<thead>
<tr>
<th>#</th>
<th>Stock</th>
<th>Trend</th>
<th>Strength</th>
<th>Why Selected?</th>
<th>Risk</th>
<th>Published</th>
<th>Chart</th>
</tr>
</thead>
<tbody>"""

for idx, stock in enumerate(stocks):
    trend_class = "trend-bullish" if stock['trend'] == "Bullish" else "trend-bearish"
    trend_icon = "↗" if stock['trend'] == "Bullish" else "↘"
    risk_class = "risk-high" if stock['risk'] == "HIGH" else "risk-med"
    
    chart_url = f"https://in.tradingview.com/chart/?symbol=NSE:{stock['symbol']}"
    
    row = f"""<tr>
<td>{idx + 1}.</td>
<td>
<span class="stock-name">{stock['symbol']}</span>
<span class="stock-desc">{stock['desc']}</span>
</td>
<td><span class="{trend_class}">{trend_icon} {stock['trend']}</span></td>
<td>
<span class="strength-score">{stock['strength']}</span><br>
<div class="progress-bar"><div class="progress-fill" style="width: {stock['fill']}%;"></div></div><br>
<span class="strength-conf">{stock['conf']}</span>
</td>
<td style="font-size: 12px;">{stock['reason']}</td>
<td><span class="{risk_class}">{stock['risk']}</span></td>
<td style="font-size: 12px; font-family: monospace;">{stock['published']}</td>
<td><a href="{chart_url}" target="_blank" class="btn-view">View ↗</a></td>
</tr>"""
    table_html += row

table_html += """</tbody>
</table>
</div>"""

st.markdown(table_html, unsafe_allow_html=True)
