"""
Intelligent SHG Performance & Digital Market Support Platform
=============================================================
Main Executive Home & Navigation Hub.
"""

import streamlit as st
import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from app.utils.styles import get_css, get_metric_card_html, PLOTLY_TEMPLATE, PERF_COLORS
from app.utils.helpers import load_dataset, format_currency, format_percentage
import plotly.express as px

# ── Page Configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="SHG Platform | Home",
    page_icon="🏘️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Inject Custom CSS ──────────────────────────────────────────────────────
st.markdown(get_css(), unsafe_allow_html=True)

# ── Sidebar Branding ───────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style="text-align:center; padding:0.5rem 0 1rem 0;">
    <span style="font-size:2.8rem;">🏘️</span>
    <h2 style="margin:0.3rem 0 0 0; font-size:1.3rem; 
        background: linear-gradient(90deg, #A8A0FF, #00D4AA);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        SHG Platform
    </h2>
    <p style="color:#8E95AA !important; font-size:0.8rem; margin:0.2rem 0 0 0;">
        AI & BI for SHG Empowerment
    </p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.info("👉 Use the navigation menu above to access all platform modules.")

# ── Header ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <div class="main-header-inner">
        <h1>🏘️ Intelligent SHG Performance Platform</h1>
        <p>Unified AI & Business Intelligence Ecosystem for Rural Self Help Groups</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Load Dataset for Quick Overview ─────────────────────────────────────────
df = load_dataset()

if df is not None:
    # ── High-Level Snapshot Cards ──────────────────────────────────────────
    st.markdown('<div class="section-header">🌐 National SHG Ecosystem Snapshot</div>', unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(get_metric_card_html("Total Monitored SHGs", f"{len(df):,}", "🏘️", "purple"), unsafe_allow_html=True)
    with c2:
        st.markdown(get_metric_card_html("Active Rural Women", f"{df['active_members'].sum():,}", "👥", "blue"), unsafe_allow_html=True)
    with c3:
        st.markdown(get_metric_card_html("Cumulative Savings", format_currency(df["cumulative_savings"].sum()), "💰", "green"), unsafe_allow_html=True)
    with c4:
        st.markdown(get_metric_card_html("Avg Loan Repayment", format_percentage(df["repayment_rate_pct"].mean()), "📈", "gold"), unsafe_allow_html=True)

    st.markdown("")
    
    # ── Quick Feature Navigation Grid ───────────────────────────────────────
    st.markdown('<div class="section-header">🚀 Platform Core Modules</div>', unsafe_allow_html=True)
    
    m1, m2 = st.columns(2)
    with m1:
        st.markdown("""
        <div class="content-card">
            <h3 style="margin-top:0;">📊 1. BI Performance Dashboard</h3>
            <p style="color:#C0C5D6; font-size:0.92rem; line-height:1.5;">
                Interactive visual intelligence across 15+ states with 8 dynamic KPIs, savings trends, state rankings, 
                and India geographic heatmaps.
            </p>
            <p style="color:#00D4AA; font-weight:600; font-size:0.88rem;">👉 Open <b>1_📊_Dashboard</b> from the sidebar</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="content-card">
            <h3 style="margin-top:0;">🤖 2. ML Performance Predictor</h3>
            <p style="color:#C0C5D6; font-size:0.92rem; line-height:1.5;">
                Trained machine learning models (89.3% accuracy) providing real-time creditworthiness & performance 
                classification (High / Medium / Low) with actionable advisory guidance.
            </p>
            <p style="color:#6C63FF; font-weight:600; font-size:0.88rem;">👉 Open <b>2_🤖_Prediction</b> from the sidebar</p>
        </div>
        """, unsafe_allow_html=True)
        
    with m2:
        st.markdown("""
        <div class="content-card">
            <h3 style="margin-top:0;">🎨 3. AI Branding & Marketing Studio</h3>
            <p style="color:#C0C5D6; font-size:0.92rem; line-height:1.5;">
                Autonomous digital marketing studio for rural micro-enterprises. Generates localized brand names, 
                taglines, story product descriptions, WhatsApp broadcasts, and Instagram campaigns.
            </p>
            <p style="color:#FFB347; font-weight:600; font-size:0.88rem;">👉 Open <b>3_🎨_Branding</b> from the sidebar</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="content-card">
            <h3 style="margin-top:0;">🔬 4. Deep Analytics & Risk Engine</h3>
            <p style="color:#C0C5D6; font-size:0.92rem; line-height:1.5;">
                Advanced statistical analytics featuring multidimensional radar profiles, risk scoring algorithms, 
                training impact assessments, and digital literacy correlations.
            </p>
            <p style="color:#FF6B6B; font-weight:600; font-size:0.88rem;">👉 Open <b>4_🔬_Analytics</b> from the sidebar</p>
        </div>
        """, unsafe_allow_html=True)

    # ── Quick Visual Preview ────────────────────────────────────────────────
    st.markdown('<div class="section-header">📈 Performance Tier Overview</div>', unsafe_allow_html=True)
    
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        perf_counts = df["performance_category"].value_counts()
        fig_p = px.pie(
            values=perf_counts.values, names=perf_counts.index,
            title="National SHG Performance Tier Share",
            color=perf_counts.index, color_discrete_map=PERF_COLORS,
            hole=0.45
        )
        fig_p.update_layout(**PLOTLY_TEMPLATE["layout"], height=350)
        st.plotly_chart(fig_p, use_container_width=True)
        
    with col_chart2:
        top_states = df.groupby("state")["cumulative_savings"].sum().nlargest(8).reset_index()
        fig_s = px.bar(
            top_states, x="cumulative_savings", y="state", orientation="h",
            title="Top 8 States by Cumulative Savings",
            labels={"cumulative_savings": "Total Savings (₹)", "state": "State"},
            color="cumulative_savings",
            color_continuous_scale=[[0, '#1A1A2E'], [0.5, '#6C63FF'], [1, '#00D4AA']]
        )
        fig_s.update_layout(**PLOTLY_TEMPLATE["layout"], height=350, showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig_s, use_container_width=True)

else:
    st.error("❌ Dataset not found at `data/raw/shg_performance_dataset.csv`. Please generate it using `python data/generate_shg_dataset.py`.")

# ── Footer ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <p><strong>Intelligent SHG Performance and Digital Market Support Platform</strong></p>
    <p>Using AI and Business Intelligence • Built for National Rural Livelihood Empowerment • © 2025</p>
</div>
""", unsafe_allow_html=True)
