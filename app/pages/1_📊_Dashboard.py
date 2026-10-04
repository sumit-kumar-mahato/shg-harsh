"""
SHG Performance BI Dashboard Page
===================================
Interactive visual intelligence dashboard with KPIs, Plotly charts,
geographic distribution, filters, and export tools.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys, os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)

from app.utils.helpers import (
    load_dataset, format_currency, format_percentage,
    get_performance_color, get_state_coordinates
)
from app.utils.styles import get_css, get_metric_card_html, PLOTLY_TEMPLATE, PERF_COLORS

# ── Page Configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="SHG BI Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Inject Custom CSS ──────────────────────────────────────────────────────
st.markdown(get_css(), unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <div class="main-header-inner">
        <h1>📊 SHG Performance BI Dashboard</h1>
        <p>Real-Time Operational, Financial & Governance Metrics Across India</p>
    </div>
</div>
""", unsafe_allow_html=True)


def _apply_theme(fig, height=400):
    """Apply dark theme to a Plotly figure."""
    fig.update_layout(**PLOTLY_TEMPLATE["layout"], height=height)
    return fig


# ── Load Dataset ────────────────────────────────────────────────────────────
df = load_dataset()

if df is None:
    st.error("❌ Dataset not found. Please run `python data/generate_shg_dataset.py` first.")
    st.stop()

# ── Sidebar Filters ─────────────────────────────────────────────────────────
st.sidebar.markdown("### 🔍 Dashboard Filters")

states = ["All"] + sorted(df["state"].unique().tolist())
selected_states = st.sidebar.multiselect("Select States", states, default=["All"])

perf_categories = ["All"] + sorted(df["performance_category"].unique().tolist())
selected_perf = st.sidebar.multiselect("Performance Category", perf_categories, default=["All"])

bank_filter = st.sidebar.selectbox("Bank Linkage Status", ["All", "Linked", "Not Linked"])

age_range = st.sidebar.slider(
    "Group Age (years)", 
    float(df["group_age_years"].min()), float(df["group_age_years"].max()),
    (float(df["group_age_years"].min()), float(df["group_age_years"].max()))
)

# Apply filters
filtered = df.copy()
if "All" not in selected_states:
    filtered = filtered[filtered["state"].isin(selected_states)]
if "All" not in selected_perf:
    filtered = filtered[filtered["performance_category"].isin(selected_perf)]
if bank_filter == "Linked":
    filtered = filtered[filtered["bank_linked"] == 1]
elif bank_filter == "Not Linked":
    filtered = filtered[filtered["bank_linked"] == 0]
filtered = filtered[
    (filtered["group_age_years"] >= age_range[0]) &
    (filtered["group_age_years"] <= age_range[1])
]

st.sidebar.markdown(f"""
<div style="background:rgba(108,99,255,0.08); border:1px solid rgba(108,99,255,0.25);
    border-radius:10px; padding:0.8rem 1rem; margin-top:1rem; text-align:center;">
    <span style="color:#A8A0FF !important; font-weight:800; font-size:1.4rem;">
        {len(filtered):,}
    </span>
    <span style="color:#A0A5BA !important; font-size:0.85rem;"><br>of {len(df):,} SHGs displayed</span>
</div>
""", unsafe_allow_html=True)

# ── Row 1: KPI Cards ────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📈 Key Performance Indicators</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(get_metric_card_html("Total Monitored SHGs", f"{len(filtered):,}", "🏘️", "purple"), unsafe_allow_html=True)
with c2:
    st.markdown(get_metric_card_html("Active Rural Women", f"{filtered['active_members'].sum():,}", "👥", "blue"), unsafe_allow_html=True)
with c3:
    st.markdown(get_metric_card_html("Cumulative Group Savings", format_currency(filtered["cumulative_savings"].sum()), "💰", "green"), unsafe_allow_html=True)
with c4:
    st.markdown(get_metric_card_html("Avg Loan Repayment Rate", format_percentage(filtered["repayment_rate_pct"].mean()), "📈", "gold"), unsafe_allow_html=True)

c5, c6, c7, c8 = st.columns(4)
with c5:
    bank_pct = (filtered["bank_linked"].sum() / len(filtered) * 100) if len(filtered) > 0 else 0
    st.markdown(get_metric_card_html("Bank Linkage Rate", format_percentage(bank_pct), "🏦", "blue"), unsafe_allow_html=True)
with c6:
    ent_pct = (filtered["has_micro_enterprise"].sum() / len(filtered) * 100) if len(filtered) > 0 else 0
    st.markdown(get_metric_card_html("Micro-Enterprise Rate", format_percentage(ent_pct), "🏭", "green"), unsafe_allow_html=True)
with c7:
    st.markdown(get_metric_card_html("Avg Meeting Attendance", format_percentage(filtered["meeting_attendance_pct"].mean()), "📋", "purple"), unsafe_allow_html=True)
with c8:
    st.markdown(get_metric_card_html("Total External Credit", format_currency(filtered["external_loan_amount"].sum()), "💳", "gold"), unsafe_allow_html=True)

st.markdown("")

# ── Row 2: Performance Distribution & State Distribution ───────────────────
st.markdown('<div class="section-header">📊 Performance & Geographic Breakdown</div>', unsafe_allow_html=True)

col_a, col_b = st.columns(2)

with col_a:
    perf_counts = filtered["performance_category"].value_counts()
    fig_pie = px.pie(
        values=perf_counts.values, names=perf_counts.index,
        title="SHG Performance Tier Distribution",
        color=perf_counts.index, color_discrete_map=PERF_COLORS,
        hole=0.45
    )
    fig_pie.update_traces(
        textinfo='label+percent+value',
        textfont_color='#FFFFFF',
        marker=dict(line=dict(color='#1A1A2E', width=2))
    )
    st.plotly_chart(_apply_theme(fig_pie, 380), use_container_width=True)

with col_b:
    state_counts = filtered["state"].value_counts().head(12)
    fig_bar = px.bar(
        x=state_counts.values, y=state_counts.index, orientation='h',
        title="Top States by Active SHG Count",
        labels={"x": "Number of SHGs", "y": "State"},
        color=state_counts.values,
        color_continuous_scale=[[0, '#1A1A2E'], [0.5, '#6C63FF'], [1, '#00D4AA']]
    )
    fig_bar.update_layout(showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(_apply_theme(fig_bar, 380), use_container_width=True)

# ── Row 3: Savings Trend & Scatter Plot ─────────────────────────────────────
col_c, col_d = st.columns(2)

with col_c:
    fc = filtered.copy()
    fc["age_bin"] = pd.cut(
        fc["group_age_years"], bins=[0, 2, 5, 10, 15, 20],
        labels=["0-2 yrs", "2-5 yrs", "5-10 yrs", "10-15 yrs", "15-20 yrs"]
    )
    age_sav = fc.groupby("age_bin", observed=True)["cumulative_savings"].mean().reset_index()
    fig_line = px.bar(
        age_sav, x="age_bin", y="cumulative_savings",
        title="Average Cumulative Savings by Group Age",
        labels={"age_bin": "Maturity Vintage", "cumulative_savings": "Avg Savings (₹)"},
        color="cumulative_savings",
        color_continuous_scale=[[0, '#1A1A2E'], [0.5, '#00D4AA'], [1, '#4ECB71']]
    )
    fig_line.update_layout(showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(_apply_theme(fig_line, 380), use_container_width=True)

with col_d:
    sample = filtered.sample(min(1000, len(filtered)), random_state=42)
    fig_sc = px.scatter(
        sample, x="cumulative_savings", y="repayment_rate_pct",
        color="performance_category", color_discrete_map=PERF_COLORS,
        title="Cumulative Savings vs Loan Repayment Rate",
        labels={"cumulative_savings": "Cumulative Savings (₹)", "repayment_rate_pct": "Repayment Rate (%)"},
        opacity=0.65
    )
    st.plotly_chart(_apply_theme(fig_sc, 380), use_container_width=True)

# ── Row 4: Heatmap & Box Plot ───────────────────────────────────────────────
col_e, col_f = st.columns(2)

with col_e:
    ht = pd.crosstab(filtered["state"], filtered["performance_category"])
    ht = ht.reindex(columns=["High Performance", "Medium Performance", "Low Performance"], fill_value=0)
    fig_ht = px.imshow(
        ht.values, x=ht.columns.tolist(), y=ht.index.tolist(),
        color_continuous_scale=[[0, '#121124'], [0.5, '#6C63FF'], [1, '#FF6B6B']],
        title="State vs Performance Tier Heatmap", aspect="auto"
    )
    st.plotly_chart(_apply_theme(fig_ht, 420), use_container_width=True)

with col_f:
    fig_box = px.box(
        filtered, x="performance_category", y="monthly_savings_per_member",
        color="performance_category", color_discrete_map=PERF_COLORS,
        title="Monthly Savings per Member Distribution"
    )
    fig_box.update_layout(showlegend=False)
    st.plotly_chart(_apply_theme(fig_box, 420), use_container_width=True)

# ── Row 5: Enterprise Breakdown & Repayment Gauge ──────────────────────────
col_g, col_h = st.columns(2)

with col_g:
    ent = filtered[filtered["enterprise_type"] != "None"]["enterprise_type"].value_counts()
    fig_ent = px.bar(
        x=ent.index, y=ent.values,
        title="Micro-Enterprise Sector Distribution",
        labels={"x": "Sector", "y": "Number of SHGs"},
        color=ent.index,
        color_discrete_sequence=['#6C63FF', '#00D4AA', '#FFB347', '#FF6B6B', '#4EA8DE', '#9D4EDD', '#4ECB71']
    )
    fig_ent.update_layout(showlegend=False)
    st.plotly_chart(_apply_theme(fig_ent, 380), use_container_width=True)

with col_h:
    avg_rep = filtered["repayment_rate_pct"].mean()
    fig_g = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=avg_rep,
        title={"text": "Overall Average Repayment Rate (%)", "font": {"color": "#F3F4F6", "family": "Poppins"}},
        delta={"reference": 80, "increasing": {"color": "#00D4AA"}, "font": {"size": 15}},
        number={"font": {"color": "#FFFFFF", "size": 42}, "suffix": "%"},
        gauge={
            "axis": {"range": [0, 100], "tickfont": {"color": "#9CA3AF"}},
            "bar": {"color": "#6C63FF"},
            "bgcolor": "rgba(255,255,255,0.03)",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 50], "color": "rgba(255,107,107,0.25)"},
                {"range": [50, 75], "color": "rgba(255,179,71,0.2)"},
                {"range": [75, 100], "color": "rgba(0,212,170,0.2)"},
            ],
            "threshold": {"line": {"color": "#FF6B6B", "width": 3}, "thickness": 0.75, "value": 80}
        }
    ))
    st.plotly_chart(_apply_theme(fig_g, 380), use_container_width=True)

# ── Row 6: Geographic Distribution Map ──────────────────────────────────────
st.markdown('<div class="section-header">🗺️ National Geographic Distribution Map</div>', unsafe_allow_html=True)

coords = get_state_coordinates()
sd = filtered["state"].value_counts().reset_index()
sd.columns = ["state", "count"]
sd["lat"] = sd["state"].map(lambda x: coords.get(x, (20, 78))[0])
sd["lon"] = sd["state"].map(lambda x: coords.get(x, (20, 78))[1])

fig_map = px.scatter_geo(
    sd, lat="lat", lon="lon", size="count",
    hover_name="state", hover_data={"count": True, "lat": False, "lon": False},
    title="SHG Density Across Indian States",
    size_max=38, color="count",
    color_continuous_scale=[[0, '#1A1A2E'], [0.3, '#6C63FF'], [0.7, '#00D4AA'], [1, '#4ECB71']]
)
fig_map.update_geos(
    scope="asia", center={"lat": 22, "lon": 82}, projection_scale=3.5,
    showland=True, landcolor="#1A1A2E",
    showocean=True, oceancolor="#0F0E17",
    showcountries=True, countrycolor="rgba(255,255,255,0.15)",
    showframe=False
)
st.plotly_chart(_apply_theme(fig_map, 480), use_container_width=True)

# ── Row 7: Data Table & CSV Export ──────────────────────────────────────────
st.markdown('<div class="section-header">📋 Top Performing SHGs (Micro-Level Records)</div>', unsafe_allow_html=True)

display_cols = ["shg_id", "shg_name", "state", "performance_category",
                "cumulative_savings", "repayment_rate_pct", "meeting_attendance_pct",
                "active_members", "has_micro_enterprise"]
avail = [c for c in display_cols if c in filtered.columns]
st.dataframe(filtered.nlargest(25, "cumulative_savings")[avail], use_container_width=True, height=360)

csv_data = filtered.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Filtered Data as CSV", csv_data, "shg_filtered_data.csv", "text/csv")

# ── Footer ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <p><strong>SHG BI Dashboard</strong> • Module 1 of Intelligent SHG Performance Platform</p>
</div>
""", unsafe_allow_html=True)
