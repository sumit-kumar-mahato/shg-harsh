"""
Deep Analytics & Risk Assessment Page
=======================================
Multi-metric radar comparison, parallel coordinates, financial correlations,
predictive risk scoring, group maturity trends, and digital adoption insights.
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

from app.utils.helpers import load_dataset
from app.utils.styles import get_css, PLOTLY_TEMPLATE, PERF_COLORS

# ── Page Configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="SHG Deep Analytics",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Inject Custom CSS ──────────────────────────────────────────────────────
st.markdown(get_css(), unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <div class="main-header-inner">
        <h1>🔬 Deep Analytics & Risk Assessment Studio</h1>
        <p>Multidimensional Diagnostic Profiling, Risk Categorization & Livelihood Trends</p>
    </div>
</div>
""", unsafe_allow_html=True)


def _apply_theme(fig, height=400):
    fig.update_layout(**PLOTLY_TEMPLATE["layout"], height=height)
    return fig


# ── Load Dataset ────────────────────────────────────────────────────────────
df = load_dataset()

if df is None:
    st.error("❌ Dataset not found. Please run `python data/generate_shg_dataset.py` first.")
    st.stop()

# ── Analytics Tabs ──────────────────────────────────────────────────────────
tabs = st.tabs(["📊 Performance Profile", "💰 Financial Diagnostics", "⚠️ Risk Scoring", "📈 Maturity Trends", "📱 Digital Adoption"])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1: Performance Profile
# ════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown('<div class="section-header">📊 Normalized Multidimensional Radar Profile</div>', unsafe_allow_html=True)
    
    metrics = ["repayment_rate_pct", "meeting_attendance_pct", "savings_regularity_pct",
               "member_retention_rate", "digital_literacy_score", "number_of_trainings"]
    avail = [m for m in metrics if m in df.columns]
    radar_data = df.groupby("performance_category")[avail].mean()
    radar_norm = (radar_data - radar_data.min()) / (radar_data.max() - radar_data.min() + 1e-8)
    
    fig = go.Figure()
    for cat in radar_norm.index:
        vals = radar_norm.loc[cat].values.tolist()
        vals.append(vals[0])
        labels = [m.replace("_", " ").title()[:18] for m in avail] + [avail[0].replace("_", " ").title()[:18]]
        fig.add_trace(go.Scatterpolar(
            r=vals, theta=labels, fill='toself', name=cat,
            line_color=PERF_COLORS.get(cat, "#6C63FF"), opacity=0.75
        ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1], gridcolor='rgba(255,255,255,0.06)', tickfont=dict(color='#9CA3AF')),
            angularaxis=dict(gridcolor='rgba(255,255,255,0.06)', tickfont=dict(color='#D1D5DB'))
        ),
        showlegend=True, legend=dict(font=dict(color='#D1D5DB'))
    )
    st.plotly_chart(_apply_theme(fig, 480), use_container_width=True)
    
    st.markdown('<div class="section-header">📐 Multi-Indicator Parallel Coordinates</div>', unsafe_allow_html=True)
    perf_map = {"High Performance": 2, "Medium Performance": 1, "Low Performance": 0}
    sample = df.sample(min(600, len(df)), random_state=42).copy()
    sample["perf_enc"] = sample["performance_category"].map(perf_map)
    dims = [
        dict(label="Savings Regularity (%)", values=sample["savings_regularity_pct"]),
        dict(label="Repayment Rate (%)", values=sample["repayment_rate_pct"]),
        dict(label="Meeting Attendance (%)", values=sample["meeting_attendance_pct"]),
        dict(label="Trainings Completed", values=sample["number_of_trainings"]),
        dict(label="Digital Score (0-10)", values=sample["digital_literacy_score"]),
    ]
    fig_p = go.Figure(data=go.Parcoords(
        line=dict(color=sample["perf_enc"],
                  colorscale=[[0, "#FF6B6B"], [0.5, "#FFB347"], [1, "#00D4AA"]],
                  showscale=True, cmin=0, cmax=2),
        dimensions=dims
    ))
    st.plotly_chart(_apply_theme(fig_p, 420), use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 2: Financial Diagnostics
# ════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="section-header">💰 Financial Distribution & Liquidity Analysis</div>', unsafe_allow_html=True)
    fc1, fc2 = st.columns(2)
    with fc1:
        fig_s = px.histogram(
            df, x="cumulative_savings", nbins=45, color="performance_category",
            color_discrete_map=PERF_COLORS, title="Cumulative Savings Density by Performance Tier",
            barmode="overlay", opacity=0.7
        )
        st.plotly_chart(_apply_theme(fig_s, 380), use_container_width=True)
    with fc2:
        fig_l = px.histogram(
            df[df["external_loan_amount"] > 0], x="external_loan_amount", nbins=45,
            color="performance_category", color_discrete_map=PERF_COLORS,
            title="External Credit Linkage Distribution", barmode="overlay", opacity=0.7
        )
        st.plotly_chart(_apply_theme(fig_l, 380), use_container_width=True)
    
    st.markdown('<div class="section-header">📊 Multivariable Correlation Heatmap</div>', unsafe_allow_html=True)
    fin = ["cumulative_savings", "external_loan_amount", "repayment_rate_pct",
           "monthly_savings_per_member", "savings_regularity_pct", "meeting_attendance_pct",
           "number_of_trainings", "digital_literacy_score", "group_age_years"]
    avail_f = [m for m in fin if m in df.columns]
    corr = df[avail_f].corr()
    fig_c = px.imshow(
        corr.values,
        x=[m.replace("_", " ").title()[:18] for m in avail_f],
        y=[m.replace("_", " ").title()[:18] for m in avail_f],
        color_continuous_scale=[[0, '#FF6B6B'], [0.5, '#121124'], [1, '#00D4AA']],
        title="Inter-Feature Correlation Matrix", aspect="auto", zmin=-1, zmax=1
    )
    st.plotly_chart(_apply_theme(fig_c, 480), use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 3: Risk Scoring
# ════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="section-header">⚠️ Early-Warning Risk Assessment & NPA Exposure</div>', unsafe_allow_html=True)
    dr = df.copy()
    dr["risk_score"] = 0
    dr["risk_score"] += (dr["repayment_rate_pct"] < 60).astype(int) * 30
    dr["risk_score"] += (dr["meeting_attendance_pct"] < 60).astype(int) * 20
    dr["risk_score"] += (dr["savings_regularity_pct"] < 60).astype(int) * 15
    dr["risk_score"] += (dr["bank_linked"] == 0).astype(int) * 10
    dr["risk_score"] += (dr["member_retention_rate"] < 0.7).astype(int) * 15
    dr["risk_score"] += (dr["number_of_trainings"] == 0).astype(int) * 10
    dr["risk_category"] = pd.cut(dr["risk_score"], bins=[-1, 20, 40, 60, 100],
                                  labels=["Low Risk", "Medium Risk", "High Risk", "Critical Risk"])
    
    r1, r2, r3, r4 = st.columns(4)
    rc = dr["risk_category"].value_counts()
    with r1: st.metric("🟢 Low Risk", f"{rc.get('Low Risk', 0):,}")
    with r2: st.metric("🟡 Medium Risk", f"{rc.get('Medium Risk', 0):,}")
    with r3: st.metric("🟠 High Risk", f"{rc.get('High Risk', 0):,}")
    with r4: st.metric("🔴 Critical Risk", f"{rc.get('Critical Risk', 0):,}")
    
    rc1, rc2 = st.columns(2)
    with rc1:
        risk_colors = {"Low Risk": "#00D4AA", "Medium Risk": "#FFB347", "High Risk": "#FF6B6B", "Critical Risk": "#C53030"}
        fig_rp = px.pie(values=rc.values, names=rc.index, title="Portfolio Risk Classification",
                       color=rc.index, color_discrete_map=risk_colors, hole=0.45)
        fig_rp.update_traces(textfont_color='#FFFFFF', marker=dict(line=dict(color='#1A1A2E', width=2)))
        st.plotly_chart(_apply_theme(fig_rp, 380), use_container_width=True)
    with rc2:
        rs = dr.groupby("state")["risk_score"].mean().sort_values(ascending=False)
        fig_rs = px.bar(x=rs.values, y=rs.index, orientation="h", title="Average Risk Score by State",
                       labels={"x": "Avg Vulnerability Score", "y": "State"},
                       color=rs.values, color_continuous_scale=[[0, '#1A1A2E'], [0.5, '#FFB347'], [1, '#FF6B6B']])
        fig_rs.update_layout(coloraxis_showscale=False, showlegend=False)
        st.plotly_chart(_apply_theme(fig_rs, 380), use_container_width=True)
    
    st.markdown("### 🔴 Priority Intervention Watchlist (High & Critical Risk)")
    hr = dr[dr["risk_score"] >= 40].nlargest(20, "risk_score")
    st.dataframe(hr[["shg_id", "shg_name", "state", "risk_score", "risk_category",
                     "repayment_rate_pct", "meeting_attendance_pct"]],
                 use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 4: Maturity Trends
# ════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="section-header">📈 Group Vintage & Capacity Building Impact</div>', unsafe_allow_html=True)
    tc1, tc2 = st.columns(2)
    s = df.sample(min(1000, len(df)), random_state=42)
    with tc1:
        fig_as = px.scatter(s, x="group_age_years", y="cumulative_savings",
                           color="performance_category", color_discrete_map=PERF_COLORS,
                           title="Group Vintage (Years) vs Cumulative Savings",
                           labels={"group_age_years": "Group Age (Years)", "cumulative_savings": "Savings (₹)"},
                           opacity=0.6)
        st.plotly_chart(_apply_theme(fig_as, 380), use_container_width=True)
    with tc2:
        fig_ar = px.scatter(s, x="group_age_years", y="repayment_rate_pct",
                           color="performance_category", color_discrete_map=PERF_COLORS,
                           title="Group Vintage (Years) vs Loan Repayment Rate",
                           labels={"group_age_years": "Group Age (Years)", "repayment_rate_pct": "Repayment Rate (%)"},
                           opacity=0.6)
        st.plotly_chart(_apply_theme(fig_ar, 380), use_container_width=True)
    
    st.markdown('<div class="section-header">🎓 Training & Enterprise Multiplier Effect</div>', unsafe_allow_html=True)
    ti1, ti2 = st.columns(2)
    cats = ["High Performance", "Medium Performance", "Low Performance"]
    with ti1:
        trained = df[df["financial_literacy_training"] == 1]["performance_category"].value_counts(normalize=True) * 100
        untrained = df[df["financial_literacy_training"] == 0]["performance_category"].value_counts(normalize=True) * 100
        fig_t = go.Figure()
        fig_t.add_trace(go.Bar(name="Trained", x=cats, y=[trained.get(c, 0) for c in cats], marker_color="#00D4AA"))
        fig_t.add_trace(go.Bar(name="Untrained", x=cats, y=[untrained.get(c, 0) for c in cats], marker_color="#FF6B6B"))
        fig_t.update_layout(barmode="group", title="Financial Literacy Training Impact on Tier")
        st.plotly_chart(_apply_theme(fig_t, 380), use_container_width=True)
    with ti2:
        ey = df[df["has_micro_enterprise"] == 1]["performance_category"].value_counts(normalize=True) * 100
        en = df[df["has_micro_enterprise"] == 0]["performance_category"].value_counts(normalize=True) * 100
        fig_e = go.Figure()
        fig_e.add_trace(go.Bar(name="With Enterprise", x=cats, y=[ey.get(c, 0) for c in cats], marker_color="#6C63FF"))
        fig_e.add_trace(go.Bar(name="Without Enterprise", x=cats, y=[en.get(c, 0) for c in cats], marker_color="#FFB347"))
        fig_e.update_layout(barmode="group", title="Micro-Enterprise Ownership Impact on Tier")
        st.plotly_chart(_apply_theme(fig_e, 380), use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 5: Digital Adoption
# ════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="section-header">📱 Digital Tool Penetration & Financial Inclusion</div>', unsafe_allow_html=True)
    da1, da2 = st.columns(2)
    with da1:
        fig_dd = px.histogram(df, x="digital_literacy_score", nbins=20,
                             color="performance_category", color_discrete_map=PERF_COLORS,
                             title="Digital Literacy Score Spread",
                             labels={"digital_literacy_score": "Digital Score (0-10)"},
                             barmode="overlay", opacity=0.7)
        st.plotly_chart(_apply_theme(fig_dd, 380), use_container_width=True)
    with da2:
        dc = ["has_digital_payment", "uses_mobile_banking", "has_whatsapp_group", "uses_social_media_marketing"]
        adc = [c for c in dc if c in df.columns]
        ad = []
        for cat in cats:
            sub = df[df["performance_category"] == cat]
            for col in adc:
                ad.append({"Category": cat, "Tool": col.replace("_", " ").title().replace("Has ", "").replace("Uses ", ""), "Rate": sub[col].mean() * 100})
        fig_ad = px.bar(pd.DataFrame(ad), x="Tool", y="Rate", color="Category", barmode="group",
                       color_discrete_map=PERF_COLORS, title="Adoption Rate (%) by Digital Channel")
        st.plotly_chart(_apply_theme(fig_ad, 380), use_container_width=True)
    
    st.markdown('<div class="section-header">💹 Digital Literacy vs Cumulative Savings</div>', unsafe_allow_html=True)
    sd = df.sample(min(500, len(df)), random_state=42)
    fig_b = px.scatter(sd, x="digital_literacy_score", y="cumulative_savings",
                      size="active_members", color="performance_category",
                      color_discrete_map=PERF_COLORS, opacity=0.6, size_max=20,
                      title="Digital Literacy vs Cumulative Savings (Bubble Size = Active Members)",
                      labels={"digital_literacy_score": "Digital Literacy Score", "cumulative_savings": "Savings (₹)"})
    st.plotly_chart(_apply_theme(fig_b, 440), use_container_width=True)

st.markdown("---")
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Export Complete Research Dataset (.csv)", csv, "shg_analytics_dataset.csv", "text/csv", use_container_width=True)

# ── Footer ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <p><strong>SHG Deep Analytics Studio</strong> • Module 4 of Intelligent SHG Performance Platform</p>
</div>
""", unsafe_allow_html=True)
