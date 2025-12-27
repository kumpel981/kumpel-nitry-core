# -*- coding: utf-8 -*-
import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import os
from datetime import datetime

# --- 1. THE ELITE DESIGN SYSTEM (CSS) ---
st.set_page_config(page_title="KN CORE | COMMAND", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;500;800&display=swap');

    /* Global Stealth Theme */
    [data-testid="stAppViewContainer"] { background: radial-gradient(circle at top, #0d1117 0%, #05070a 100%); color: #e6edf3; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #0b0e14 !important; border-right: 1px solid #30363d; }

    /* MASSIVE 3D KN LOGO */
    .kn-logo-container {
        display: flex; justify-content: center; padding: 40px 0;
        perspective: 1000px;
    }
    .kn-logo-3d {
        width: 120px; height: 120px;
        background: linear-gradient(135deg, #00ff88 0%, #3b82f6 100%);
        border-radius: 24px;
        display: flex; align-items: center; justify-content: center;
        font-family: 'Orbitron', sans-serif; font-size: 50px; font-weight: 900; color: #000;
        box-shadow: 0 20px 50px rgba(0, 255, 136, 0.3), inset 0 0 20px rgba(255,255,255,0.4);
        transform: rotateY(-15deg) rotateX(10deg);
        animation: float 4s ease-in-out infinite;
    }
    @keyframes float { 0%, 100% { transform: translateY(0) rotateY(-15deg); } 50% { transform: translateY(-15px) rotateY(5deg); } }

    /* BENTO GRID ANIMATIONS */
    .bento-card {
        background: rgba(22, 27, 34, 0.6);
        backdrop-filter: blur(15px);
        border: 1px solid #30363d;
        border-radius: 24px; padding: 30px; margin-bottom: 20px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .bento-card:hover { 
        border: 1px solid #00ff88; 
        box-shadow: 0 0 30px rgba(0, 255, 136, 0.15);
        transform: scale(1.02);
    }

    /* TYPOGRAPHY */
    .label-accent { color: #8b949e; font-size: 10px; text-transform: uppercase; letter-spacing: 4px; font-weight: 800; }
    .value-heavy { font-size: 40px; font-weight: 800; color: #ffffff; font-family: 'Orbitron', sans-serif; }
    
    /* SUCCESS/ADMIN GLOW */
    .admin-glow { color: #00ff88; text-shadow: 0 0 10px rgba(0,255,136,0.5); }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BACKEND & SESSION FIXES ---
DB_PATH = os.path.join(os.getcwd(), 'kn_production.db')

def get_db():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_db(); c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS system_config (key TEXT PRIMARY KEY, val REAL)')
    c.execute("INSERT OR IGNORE INTO system_config VALUES ('inflation', 8.5), ('price_egg', 20), ('price_milk', 65)")
    c.execute('CREATE TABLE IF NOT EXISTS broadcast (id INTEGER PRIMARY KEY, msg TEXT, stamp TEXT)')
    conn.commit(); conn.close()

init_db()

if 'auth' not in st.session_state: st.session_state.update({'auth': False, 'role': 'User'})

# --- 3. THE GATEWAY ---
if not st.session_state['auth']:
    st.markdown("<div class='kn-logo-container'><div class='kn-logo-3d'>KN</div></div>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1, 1])
    with col:
        u = st.text_input("IDENTITY ID")
        p = st.text_input("SECURITY KEY", type="password")
        if st.button("AUTHENTICATE NODE"):
            if u == "admin" and p == "admin":
                st.session_state.update({'auth': True, 'role': 'Admin'})
            else:
                st.session_state.update({'auth': True, 'role': 'User'})
            st.rerun()
    st.stop()

# --- 4. NAVIGATION LOGIC ---
with st.sidebar:
    st.markdown("<div class='kn-logo-3d' style='width:60px; height:60px; font-size:24px; margin:0 auto;'>KN</div>", unsafe_allow_html=True)
    st.divider()
    if st.session_state['role'] == "Admin":
        nav = st.selectbox("COMMAND CENTER", ["Oversight", "Market Control", "Broadcast Hub"])
    else:
        nav = st.selectbox("USER INTEL", ["Dashboard", "Loan Engine", "Rankings"])
    
    if st.button("TERMINATE"):
        st.session_state['auth'] = False
        st.rerun()

# --- 5. ADMIN COMMAND PANEL (IF ADMIN) ---
if st.session_state['role'] == "Admin":
    st.markdown(f"<h1>SYSTEM <span class='admin-glow'>GOVERNANCE</span></h1>", unsafe_allow_html=True)
    
    if nav == "Oversight":
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown("<div class='bento-card'><p class='label-accent'>Network Liquidity</p><p class='value-heavy'>KES 12.4M</p></div>", unsafe_allow_html=True)
        with c2: st.markdown("<div class='bento-card'><p class='label-accent'>Active Nodes</p><p class='value-heavy'>5,109</p></div>", unsafe_allow_html=True)
        with c3: st.markdown("<div class='bento-card'><p class='label-accent'>Health</p><p class='value-heavy' style='color:#00ff88;'>100%</p></div>", unsafe_allow_html=True)
        st.markdown("<div class='bento-card'>", unsafe_allow_html=True)
        st.subheader("Global Expenditure Flow")
        st.area_chart(np.random.randn(20, 2))
        st.markdown("</div>", unsafe_allow_html=True)

    elif nav == "Market Control":
        st.markdown("<div class='bento-card'>", unsafe_allow_html=True)
        st.subheader("Global Economic Variables")
        conn = get_db(); c = conn.cursor()
        items = c.execute("SELECT * FROM system_config").fetchall()
        for key, val in items:
            new_v = st.number_input(f"Edit {key}", value=float(val))
            if st.button(f"Update {key}"):
                c.execute("UPDATE system_config SET val = ? WHERE key = ?", (new_v, key))
                conn.commit(); st.success(f"{key} updated")
        conn.close()
        st.markdown("</div>", unsafe_allow_html=True)

    elif nav == "Broadcast Hub":
        st.markdown("<div class='bento-card'>", unsafe_allow_html=True)
        st.subheader("Emergency Transmission")
        msg = st.text_area("Global Message")
        if st.button("TRANSMIT"):
            conn = get_db(); c = conn.cursor()
            c.execute("INSERT INTO broadcast (msg, stamp) VALUES (?,?)", (msg, datetime.now().strftime("%H:%M")))
            conn.commit(); conn.close()
            st.toast("Message sent to all comrades!")
        st.markdown("</div>", unsafe_allow_html=True)

# --- 6. USER DASHBOARD (IF USER) ---
else:
    st.markdown("<h1>KUMPEL <span class='admin-glow'>NITRY</span> CORE</h1>", unsafe_allow_html=True)
    
    # Check for Broadcasts
    conn = get_db(); c = conn.cursor()
    last_msg = c.execute("SELECT msg, stamp FROM broadcast ORDER BY id DESC LIMIT 1").fetchone()
    if last_msg:
        st.warning(f"**CORE ALERT [{last_msg[1]}]:** {last_msg[0]}")
    
    if nav == "Dashboard":
        col_l, col_r = st.columns([2, 1])
        with col_l:
            st.markdown("<div class='bento-card'>", unsafe_allow_html=True)
            st.markdown("<p class='label-accent'>Hustle Intelligence</p>", unsafe_allow_html=True)
            budget = st.number_input("Liquid Bob", value=150)
            inf = c.execute("SELECT val FROM system_config WHERE key='inflation'").fetchone()[0]
            if budget < (100 * (1 + inf/100)):
                st.error("🚨 HALI NI MSOTO: Switch to high-efficiency calories (Nduma/Eggs).")
            else:
                st.success("💎 HALI NI MDOSI: Budget is optimal for meat-based protein.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_r:
            st.markdown("<div class='bento-card'><p class='label-accent'>Nitry Tokens</p><p class='value-heavy' style='color:#00ff88;'>2,400</p></div>", unsafe_allow_html=True)
    conn.close()