# -*- coding: utf-8 -*-
import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import os
from datetime import datetime

# --- 1. ELITE CYBER-FINANCE DESIGN SYSTEM ---
st.set_page_config(page_title="KN | SOVEREIGN CORE", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@700&family=JetBrains+Mono:wght@300;500;800&display=swap');

    /* Global Foundation */
    [data-testid="stAppViewContainer"] { background: #020406; color: #d1d5db; font-family: 'JetBrains Mono', monospace; }
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 2px solid #10b981; }

    /* THE MONOLITH LOGO (3D & GLOWING) */
    .kn-monolith {
        width: 160px; height: 160px; margin: 20px auto;
        background: linear-gradient(135deg, #10b981 0%, #3b82f6 100%);
        border-radius: 20px; display: flex; align-items: center; justify-content: center;
        font-family: 'Syncopate', sans-serif; font-size: 60px; font-weight: 900; color: #000;
        box-shadow: 0 0 80px rgba(16, 185, 129, 0.4), inset 0 0 30px rgba(255,255,255,0.5);
        transform: rotateX(20deg) rotateZ(-5deg);
        animation: float-logo 5s ease-in-out infinite;
    }
    @keyframes float-logo { 0%, 100% { transform: translateY(0) rotateX(20deg); } 50% { transform: translateY(-20px) rotateX(10deg); } }

    /* BENTO-GLASS TILES */
    .bento-node {
        background: rgba(17, 24, 39, 0.7);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-radius: 24px; padding: 35px; margin-bottom: 25px;
        transition: all 0.4s ease;
    }
    .bento-node:hover { border: 1px solid #10b981; box-shadow: 0 0 35px rgba(16, 185, 129, 0.2); transform: scale(1.01); }

    /* DATA TYPOGRAPHY */
    .stat-label { color: #6b7280; font-size: 10px; text-transform: uppercase; letter-spacing: 4px; font-weight: 800; }
    .stat-value { font-size: 42px; font-weight: 800; color: #ffffff; letter-spacing: -2px; }
    .sheng-badge { background: #10b98122; color: #10b981; padding: 4px 12px; border-radius: 6px; font-size: 11px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE SOVEREIGN BACKEND ---
DB_PATH = os.path.join(os.getcwd(), 'kn_sovereign.db')
def get_db(): return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_db(); c = conn.cursor()
    # Market Constants (Admin-Controlled)
    c.execute('CREATE TABLE IF NOT EXISTS market_pulse (item TEXT PRIMARY KEY, price REAL)')
    defaults = [('inflation', 8.2), ('unga_price', 185.0), ('egg_price', 20.0), ('milk_price', 65.0)]
    for item, price in defaults: c.execute("INSERT OR IGNORE INTO market_pulse VALUES (?,?)", (item, price))
    
    # Global Messaging
    c.execute('CREATE TABLE IF NOT EXISTS terminal_news (id INTEGER PRIMARY KEY, msg TEXT, level TEXT)')
    conn.commit(); conn.close()

init_db()

# Session Core
if 'auth' not in st.session_state: st.session_state.update({'auth': False, 'role': 'User'})

# --- 3. ACCESS GATEWAY ---
if not st.session_state['auth']:
    st.markdown("<div class='kn-monolith'>KN</div>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.1, 1])
    with col:
        st.markdown("<h3 style='text-align:center;'>SOVEREIGN ACCESS</h3>", unsafe_allow_html=True)
        u = st.text_input("NODE ID")
        p = st.text_input("SECURE KEY", type="password")
        if st.button("INITIALIZE SYSTEM"):
            if u == "admin" and p == "admin": st.session_state.update({'auth': True, 'role': 'Admin'})
            else: st.session_state.update({'auth': True, 'role': 'User'})
            st.rerun()
    st.stop()

# --- 4. SYSTEM NAVIGATION ---
with st.sidebar:
    st.markdown("<div class='kn-monolith' style='width:60px; height:60px; font-size:22px;'>KN</div>", unsafe_allow_html=True)
    st.divider()
    nav_options = ["Terminal Home", "Risk Matrix", "Campus Ranks", "Admin Command"] if st.session_state['role'] == "Admin" else ["Terminal Home", "Risk Matrix", "Campus Ranks"]
    nav = st.radio("CORE NAVIGATION", nav_options)
    if st.button("TERMINATE SESSION"):
        st.session_state['auth'] = False
        st.rerun()

# --- 5. TERMINAL HOME (AI REASONING ENGINE) ---
if nav == "Terminal Home":
    st.title("NITRY | INTELLIGENCE FEED")
    
    conn = get_db(); c = conn.cursor()
    news = c.execute("SELECT msg, level FROM terminal_news ORDER BY id DESC LIMIT 1").fetchone()
    if news:
        color = "#10b981" if news[1] == "INFO" else "#ef4444"
        st.markdown(f"<div style='border-left: 4px solid {color}; padding-left: 15px; margin-bottom: 20px;'>{news[0]}</div>", unsafe_allow_html=True)

    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown("<div class='bento-node'>", unsafe_allow_html=True)
        st.markdown("<span class='sheng-badge'>AI REASONING ENGINE v4.0</span>", unsafe_allow_html=True)
        budget = st.number_input("Input Daily Budget (KES)", value=150, step=10)
        
        # Pull Prices from Admin Backend
        unga = c.execute("SELECT price FROM market_pulse WHERE item='unga_price'").fetchone()[0]
        egg = c.execute("SELECT price FROM market_pulse WHERE item='egg_price'").fetchone()[0]
        inf = c.execute("SELECT price FROM market_pulse WHERE item='inflation'").fetchone()[0]
        
        st.write(f"**Market Context:** Inflation at `{inf}%` | Current Egg: `KES {egg}`")
        
        # REALISTIC COMRADE MEAL LOGIC
        if budget < egg * 2:
            st.error("🚨 **CRITICAL MSOTO:** Budget cannot sustain hot meals. AI Strategy: Buy half-loaf (45/-) and strong tea. Save remaining capital.")
        elif budget < 120:
            st.warning("⚠️ **SURVIVAL MODE:** AI Strategy: 1 Egg (20/-), Quarter Unga (50/-), Greens (20/-). Total: 90/-. Sustainable.")
        elif budget < 250:
            st.success("✅ **NOMINAL STATUS:** AI Strategy: Kibanda Beef/Ugali combo (150/-) or Omena/Managu. Capital security confirmed.")
        else:
            st.info("💎 **MDOSI LEVEL:** High liquidity. AI Strategy: Balanced protein + Fruit. Consider moving excess to Akiba Vault.")
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown(f"<div class='bento-node'><p class='stat-label'>Capital Rank</p><p class='stat-value' style='color:#10b981;'>PLATINUM</p></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='bento-node'><p class='stat-label'>Akiba Points</p><p class='stat-value'>2,450</p></div>", unsafe_allow_html=True)
    conn.close()

# --- 6. RISK MATRIX (LOAN ENGINE) ---
elif nav == "Risk Matrix":
    st.title("CREDIT RISK ANALYST")
    st.markdown("<div class='bento-node'>", unsafe_allow_html=True)
    st.subheader("Predatory Loan Breakdown")
    p = st.number_input("Principal Amount", value=2000)
    r = st.slider("Interest Rate (%)", 1, 40, 15)
    days = st.number_input("Days to Repay", value=7)
    
    total = p + (p * (r/100))
    st.metric("Total Debt Liability", f"KES {total:,.2f}")
    
    if r > 12:
        st.error("PREDATORY ALERT: This loan is designed to trap student nodes. Avoid at all costs.")
    else:
        st.success("FAIR RATE: This credit is within comrade-safety limits.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 7. CAMPUS RANKS (PRE-FILLED) ---
elif nav == "Campus Ranks":
    st.title("NATIONAL CAPITAL LEADERBOARD")
    st.markdown("<div class='bento-node'>", unsafe_allow_html=True)
    df = pd.DataFrame({
        "UNIVERSITY": ["JKUAT", "KISII UNIVERSITY", "UON", "STRATHMORE", "MOI", "KU"],
        "NET SAVINGS (M)": [12.4, 10.8, 9.2, 8.5, 7.1, 6.8],
        "TIER": ["GOD-TIER", "ELITE", "SURGING", "NOMINAL", "DEFICIT", "DEFICIT"]
    })
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.bar_chart(df.set_index("UNIVERSITY")["NET SAVINGS (M)"])
    st.markdown("</div>", unsafe_allow_html=True)

# --- 8. ADMIN COMMAND (GOD MODE) ---
elif nav == "Admin Command" and st.session_state['role'] == "Admin":
    st.title("GOVERNANCE OVERRIDE")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='bento-node'>", unsafe_allow_html=True)
        st.subheader("Global Price Control")
        conn = get_db(); c = conn.cursor()
        new_egg = st.number_input("Edit Egg Price", value=20.0)
        new_unga = st.number_input("Edit Unga Price", value=185.0)
        if st.button("PUSH PRICE UPDATE"):
            c.execute("UPDATE market_pulse SET price = ? WHERE item='egg_price'", (new_egg,))
            c.execute("UPDATE market_pulse SET price = ? WHERE item='unga_price'", (new_unga,))
            conn.commit(); st.toast("Global AI updated.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='bento-node'>", unsafe_allow_html=True)
        st.subheader("Emergency Broadcast")
        msg = st.text_area("Transmit Alert")
        level = st.selectbox("Alert Level", ["INFO", "DANGER"])
        if st.button("SEND BROADCAST"):
            c.execute("INSERT INTO terminal_news (msg, level) VALUES (?,?)", (msg, level))
            conn.commit(); st.toast("Broadcast Sent.")
        st.markdown("</div>", unsafe_allow_html=True)
    conn.close()