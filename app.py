# -*- coding: utf-8 -*-
import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import os
from datetime import datetime

# --- 1. THE KUMPEL NITRY DESIGN SYSTEM ---
st.set_page_config(page_title="KUMPEL NITRY CORE", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;500;700&display=swap');

    [data-testid="stAppViewContainer"] { background: #030507; color: #f0f0f0; font-family: 'Space Grotesk', sans-serif; }
    [data-testid="stSidebar"] { background: #07090c; border-right: 1px solid #1a1e23; }
    
    /* 3D "KN" Logo Design */
    .kn-logo {
        width: 80px; height: 80px; margin: 0 auto;
        background: linear-gradient(135deg, #3b82f6 0%, #00ff88 100%);
        border-radius: 18px; display: flex; align-items: center; justify-content: center;
        font-size: 34px; font-weight: 800; color: #000;
        box-shadow: 0 10px 40px rgba(59, 130, 246, 0.4);
        transform: perspective(500px) rotateX(5deg);
    }

    /* Glass Bento Tiles */
    .bento-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px; padding: 25px; margin-bottom: 20px;
        transition: 0.3s ease-in-out;
    }
    .bento-card:hover { border: 1px solid #00ff88; transform: translateY(-3px); }

    .kn-label { color: #94a3b8; font-size: 11px; text-transform: uppercase; letter-spacing: 2.5px; font-weight: 700; }
    .kn-value { font-size: 32px; font-weight: 700; color: #fff; margin-top: 5px; }
    
    .news-card { 
        background: linear-gradient(90deg, #1e293b55, #0f172a55); 
        border-left: 5px solid #3b82f6; padding: 20px; border-radius: 12px; margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CLOUD-READY DATABASE ENGINE ---
DB_PATH = os.path.join(os.getcwd(), 'kn_v7.db')

def get_db():
    # check_same_thread=False is essential for multi-user Streamlit apps
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_db()
    c = conn.cursor()
    # Market Logic
    c.execute('CREATE TABLE IF NOT EXISTS market (item TEXT PRIMARY KEY, price REAL)')
    c.execute("INSERT OR IGNORE INTO market VALUES ('Inflation', 8.5), ('Milk', 65), ('Unga', 195)")
    # News & Communication
    c.execute('CREATE TABLE IF NOT EXISTS news (id INTEGER PRIMARY KEY, content TEXT, date TEXT)')
    c.execute("INSERT OR IGNORE INTO news (id, content, date) VALUES (1, 'KUMPEL NITRY CORE System Online. Welcome Comrade.', '00:00')")
    # Users
    c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, role TEXT)')
    conn.commit()
    conn.close()

init_db()

# Session Memory
if 'auth' not in st.session_state: st.session_state.update({'auth': False, 'user': 'Guest', 'role': 'User'})

# --- 3. ACCESS GATEWAY ---
if not st.session_state['auth']:
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<br><br><div class='kn-logo'>KN</div>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center; letter-spacing:3px;'>KUMPEL NITRY</h2>", unsafe_allow_html=True)
        u = st.text_input("Comrade ID")
        p = st.text_input("Security Key", type="password")
        if st.button("AUTHENTICATE"):
            if u == "admin" and p == "admin":
                st.session_state.update({'auth': True, 'user': 'Admin', 'role': 'Admin'})
            else:
                st.session_state.update({'auth': True, 'user': u, 'role': 'User'})
            st.rerun()
    st.stop()

# --- 4. COMMAND SIDEBAR ---
with st.sidebar:
    st.markdown("<div class='kn-logo' style='width:50px; height:50px; font-size:18px;'>KN</div>", unsafe_allow_html=True)
    st.divider()
    if st.session_state['role'] == "Admin":
        nav = st.radio("Management Console", ["Global Oversight", "News Desk", "Market Pulse"])
    else:
        nav = st.radio("Intelligence Hub", ["Hustle Dashboard", "Credit Risk Analyst", "Campus Rankings"])
    
    st.divider()
    if st.button("TERMINATE SESSION"):
        st.session_state.update({'auth': False})
        st.rerun()

# --- 5. ADMIN BACKEND (COMMAND CENTER) ---
if st.session_state['role'] == "Admin":
    if nav == "Global Oversight":
        st.title("Network Governance")
        c1, c2, c3 = st.columns(3)
        c1.markdown("<div class='bento-card'><p class='kn-label'>Total Liquidity</p><p class='kn-value'>KES 8.2M</p></div>", unsafe_allow_html=True)
        c2.markdown("<div class='bento-card'><p class='kn-label'>Active Nodes</p><p class='kn-value'>4,820</p></div>", unsafe_allow_html=True)
        c3.markdown("<div class='bento-card'><p class='kn-label'>Health Score</p><p class='kn-value' style='color:#00ff88;'>OPTIMAL</p></div>", unsafe_allow_html=True)
        
        st.markdown("<div class='bento-card'>", unsafe_allow_html=True)
        st.subheader("Global Expenditure Trends")
        st.line_chart(np.random.randn(20, 2))
        st.markdown("</div>", unsafe_allow_html=True)

    elif nav == "News Desk":
        st.title("Broadcast Intelligence")
        msg = st.text_area("Update Global Feed:")
        if st.button("Push Broadcast"):
            conn = get_db(); c = conn.cursor()
            c.execute("INSERT INTO news (content, date) VALUES (?,?)", (msg, datetime.now().strftime("%H:%M")))
            conn.commit(); conn.close()
            st.toast("Global News Updated.")

    elif nav == "Market Pulse":
        st.title("Market Variable Control")
        conn = get_db(); c = conn.cursor()
        items = c.execute("SELECT * FROM market").fetchall()
        for item, price in items:
            new_val = st.number_input(f"Global {item} Index", value=float(price))
            if st.button(f"Update {item}"):
                c.execute("UPDATE market SET price = ? WHERE item = ?", (new_val, item))
                conn.commit(); st.toast(f"Market Sync: {item}")
        conn.close()

# --- 6. USER FRONTEND (STUDENT INTERFACE) ---
else:
    st.title("Intelligence Hub")
    
    # Live News Feed
    conn = get_db(); c = conn.cursor()
    feed = c.execute("SELECT content, date FROM news ORDER BY id DESC LIMIT 1").fetchone()
    if feed:
        st.markdown(f"<div class='news-card'><p class='kn-label' style='color:#3b82f6;'>LIVE BROADCAST | {feed[1]}</p>{feed[0]}</div>", unsafe_allow_html=True)
    
    if nav == "Hustle Dashboard":
        col_1, col_2 = st.columns([2, 1])
        with col_1:
            st.markdown("<div class='bento-card'>", unsafe_allow_html=True)
            st.markdown("<p class='kn-label'>Wallet Management</p>", unsafe_allow_html=True)
            budget = st.number_input("Liquid Cash (Bob)", value=150)
            
            # Smart Logic from Admin Market Matrix
            inf = c.execute("SELECT price FROM market WHERE item='Inflation'").fetchone()[0]
            st.write(f"Current Market Inflation: `{inf}%`.")
            
            if budget < 100 * (1 + inf/100):
                st.error("🚨 MSOTO ALERT: Budget insufficient for standard nutrition. AI suggests: Cereal Base.")
            else:
                st.success("💎 MDOSI STATUS: Capital levels are nominal for balanced protein.")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='bento-card'>", unsafe_allow_html=True)
            st.subheader("HELB Disbursement Tracker")
            st.progress(0.35)
            st.caption("22 Days remaining until next projected disbursement.")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_2:
            st.markdown("<div class='bento-card'><p class='kn-label'>Nitry Points</p><p class='kn-value' style='color:#00ff88;'>1,850</p></div>", unsafe_allow_html=True)
            st.markdown("<div class='bento-card'><p class='kn-label'>Campus Rank</p><p class='kn-value' style='color:#3b82f6;'>#1 JKUAT</p></div>", unsafe_allow_html=True)
    conn.close()

    if nav == "Credit Risk Analyst":
        st.markdown("<div class='bento-card'>", unsafe_allow_html=True)
        st.subheader("Loan Debt Forecaster")
        principal = st.number_input("Loan Amount", value=2000)
        interest = st.slider("Interest Rate (%)", 1, 30, 15)
        st.metric("Repayment Amount", f"KES {principal * (1 + interest/100):,.2f}")
        if interest > 12: st.error("Predatory Interest Flagged.")
        st.markdown("</div>", unsafe_allow_html=True)