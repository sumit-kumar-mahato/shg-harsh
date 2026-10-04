"""
SHG Performance Prediction Page
=================================
Real-time machine learning prediction of SHG performance tier
with confidence breakdown, probability bars, and automated recommendations.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os, sys

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)

from app.utils.helpers import (
    load_model, load_preprocessor, get_performance_badge,
    get_recommendations
)
from app.utils.styles import get_css, get_metric_card_html, PLOTLY_TEMPLATE, PERF_COLORS

# ── Page Configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="SHG ML Prediction",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Inject Custom CSS ──────────────────────────────────────────────────────
st.markdown(get_css(), unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <div class="main-header-inner">
        <h1>🤖 AI Performance & Creditworthiness Predictor</h1>
        <p>Pre-Trained Machine Learning Inference with Automated Advisory Engine</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    <strong>💡 How it works:</strong> Enter the SHG operational, financial, and governance parameters below.
    Our pre-trained Machine Learning model analyzes 50+ multidimensional indicators to predict whether the SHG 
    is in the <b>High</b>, <b>Medium</b>, or <b>Low</b> performance category, and generates targeted capacity-building guidance.
</div>
""", unsafe_allow_html=True)

# Load model and preprocessors
model = load_model()
scaler = load_preprocessor("scaler")
encoders = load_preprocessor("label_encoders")
feature_list = load_preprocessor("feature_list")
target_encoder = load_preprocessor("target_encoder")

if model is None:
    st.warning("⚠️ ML model artifacts not found. Please run `python ml/model_training.py` first to train and serialize the model.")
    st.stop()

# ── Input Form ──────────────────────────────────────────────────────────────
st.markdown("### 📝 Enter SHG Parameters")

with st.form("prediction_form"):
    # Group Demographics
    st.markdown("#### 👥 1. Group Demographics & Membership")
    g1, g2, g3 = st.columns(3)
    with g1:
        group_size = st.number_input("Total Registered Members", 10, 20, 12)
        is_women_shg = st.selectbox("All-Women SHG?", [1, 0], format_func=lambda x: "Yes" if x else "No")
    with g2:
        active_members = st.number_input("Active Participating Members", 5, 20, 11)
        is_tribal_shg = st.selectbox("Tribal Community SHG?", [0, 1], format_func=lambda x: "Yes" if x else "No")
    with g3:
        group_age_years = st.number_input("Group Vintage / Age (Years)", 0.5, 20.0, 4.5, 0.5)
        category = st.selectbox("Socio-Economic Category", ["OBC", "SC", "ST", "General", "Minority"])
    
    st.markdown("---")
    
    # Financial Metrics
    st.markdown("#### 💰 2. Financial Discipline & Savings")
    f1, f2, f3 = st.columns(3)
    with f1:
        monthly_savings = st.number_input("Monthly Savings / Member (₹)", 50, 1000, 200, 50)
        savings_regularity = st.slider("Savings Regularity Rate (%)", 40.0, 100.0, 85.0, 1.0)
        number_of_loans = st.number_input("Number of External Loans Taken", 0, 10, 2)
    with f2:
        cumulative_savings = st.number_input("Cumulative Group Savings (₹)", 1000, 2000000, 120000, 5000)
        external_loan = st.number_input("Total Loan Disbursed (₹)", 0, 1000000, 150000, 10000)
        loan_outstanding = st.number_input("Current Loan Outstanding (₹)", 0, 500000, 25000, 5000)
    with f3:
        repayment_rate = st.slider("Historical Loan Repayment Rate (%)", 30.0, 100.0, 88.0, 1.0)
        loan_demand_met = st.slider("Internal Member Credit Demand Met (%)", 30.0, 100.0, 75.0, 1.0)
        bank_balance = st.number_input("Current Bank Account Balance (₹)", 500, 500000, 35000, 2000)
    
    st.markdown("---")
    
    # Bank Linkage
    st.markdown("#### 🏦 3. Institutional Banking Linkage")
    b1, b2, b3 = st.columns(3)
    with b1:
        bank_linked = st.selectbox("Bank Linked?", [1, 0], format_func=lambda x: "Yes" if x else "No")
        bank_name = st.selectbox("Partner Bank", ["SBI", "PNB", "Bank of Baroda", "Canara Bank", 
                                                 "IOB", "Union Bank", "Central Bank", "None"])
    with b2:
        credit_linkages = st.number_input("Number of Credit Linkage Cycles", 0, 5, 2)
        credit_amount = st.number_input("Cumulative Credit Linkage Amount (₹)", 0, 2000000, 200000, 25000)
    with b3:
        savings_account = st.selectbox("Active Savings Bank Account?", [1, 0], format_func=lambda x: "Yes" if x else "No")
        bank_linkage_year = st.number_input("Year of First Bank Linkage", 2005, 2024, 2019)
    
    st.markdown("---")
    
    # Governance
    st.markdown("#### 📋 4. Group Governance & Record Keeping")
    m1, m2, m3 = st.columns(3)
    with m1:
        meetings = st.number_input("Group Meetings Held in Last Year", 0, 12, 11)
        attendance = st.slider("Average Meeting Attendance (%)", 30.0, 100.0, 82.0, 1.0)
    with m2:
        books = st.selectbox("Book-Keeping Quality", ["Good", "Excellent", "Average", "Poor"])
        audit_grade = st.selectbox("Social/Financial Audit Grade", ["A", "B", "C", "D", "Not Audited"])
    with m3:
        minutes_recorded = st.selectbox("Meeting Minutes Book Maintained?", [1, 0], format_func=lambda x: "Yes" if x else "No")
        has_leaders = st.selectbox("Democratically Elected Leaders?", [1, 0], format_func=lambda x: "Yes" if x else "No")
        leader_rotation = st.selectbox("Periodic Leadership Rotation?", [1, 0], format_func=lambda x: "Yes" if x else "No")
        audit_completed = st.selectbox("Annual Audit Completed?", [1, 0], format_func=lambda x: "Yes" if x else "No")
    
    st.markdown("---")
    
    # Training
    st.markdown("#### 🎓 5. Training & Capacity Building")
    t1, t2, t3 = st.columns(3)
    with t1:
        fin_literacy = st.selectbox("Financial Literacy Training Attended?", [1, 0], format_func=lambda x: "Yes" if x else "No")
    with t2:
        skill_training = st.selectbox("Vocational Skill Training Attended?", [1, 0], format_func=lambda x: "Yes" if x else "No")
    with t3:
        enterprise_training = st.selectbox("Micro-Enterprise Training Received?", [1, 0], format_func=lambda x: "Yes" if x else "No")
    
    t4, t5 = st.columns(2)
    with t4:
        num_trainings = st.number_input("Total Formal Trainings Completed", 0, 15, 3)
    with t5:
        training_org = st.selectbox("Primary Training Agency", ["NRLM", "NGO", "Bank", "Government", "None"])
    
    st.markdown("---")
    
    # Enterprise
    st.markdown("#### 🏭 6. Livelihood & Micro-Enterprise Activities")
    e1, e2, e3 = st.columns(3)
    with e1:
        has_enterprise = st.selectbox("Active Micro-Enterprise Activity?", [1, 0], format_func=lambda x: "Yes" if x else "No")
        enterprise_type = st.selectbox("Enterprise Sector", 
                                       ["Agriculture", "Dairy", "Handicrafts", "Tailoring",
                                        "Food Processing", "Retail", "Services", "None"])
    with e2:
        enterprise_income = st.number_input("Avg Monthly Enterprise Revenue (₹)", 0, 100000, 8500, 1000)
        enterprise_age = st.number_input("Enterprise Operational Age (Months)", 0, 120, 24)
    with e3:
        market_linkage = st.selectbox("Formal Market / Buyer Linkage?", [1, 0], format_func=lambda x: "Yes" if x else "No")
        income_sources = st.number_input("Distinct Group Income Streams", 1, 6, 2)
    
    st.markdown("---")
    
    # Digital & Federation
    st.markdown("#### 📱 7. Digital Adoption & Federation Network")
    d1, d2, d3 = st.columns(3)
    with d1:
        digital_payment = st.selectbox("Uses UPI / Digital Payments?", [1, 0], format_func=lambda x: "Yes" if x else "No")
        mobile_banking = st.selectbox("Uses Mobile / Internet Banking?", [1, 0], format_func=lambda x: "Yes" if x else "No")
    with d2:
        whatsapp = st.selectbox("Active WhatsApp Group for Members?", [1, 0], format_func=lambda x: "Yes" if x else "No")
        social_media = st.selectbox("Social Media Marketing Usage?", [0, 1], format_func=lambda x: "Yes" if x else "No")
    with d3:
        digital_score = st.slider("Digital Literacy Score (0-10)", 0.0, 10.0, 4.5, 0.5)
        is_federated = st.selectbox("Part of Village/Cluster Federation?", [1, 0], format_func=lambda x: "Yes" if x else "No")
        federation_level = st.selectbox("Federation Affiliation Level", ["None", "Primary", "Cluster", "Block"])
        connected_nrlm = st.selectbox("NRLM Portal Integration?", [1, 0], format_func=lambda x: "Yes" if x else "No")
        nrlm_grade = st.selectbox("NRLM Official Grade", ["A", "B", "C", "Not Graded"])
    
    state = st.selectbox("State of Registration", sorted([
        "Uttar Pradesh", "Bihar", "Madhya Pradesh", "Rajasthan", "Jharkhand",
        "Odisha", "Andhra Pradesh", "Telangana", "Tamil Nadu", "Karnataka",
        "Maharashtra", "West Bengal", "Assam", "Kerala", "Gujarat"
    ]), index=2)
    
    submitted = st.form_submit_button("🔮 Predict SHG Performance", use_container_width=True, type="primary")

# ── Inference Execution ─────────────────────────────────────────────────────
if submitted:
    with st.spinner("🔄 Running multi-feature machine learning model..."):
        try:
            total_monthly_savings = monthly_savings * active_members
            member_retention = active_members / group_size if group_size > 0 else 0
            internal_lending = int(cumulative_savings * 0.8)
            interest_earned = int(internal_lending * 0.12)
            corpus_fund = cumulative_savings + interest_earned
            avg_loan_size = external_loan / number_of_loans if number_of_loans > 0 else 0
            npa_status = 1 if repayment_rate < 60 else 0
            
            input_data = {
                "state": state, "district": "Unknown",
                "group_age_years": group_age_years,
                "group_size": group_size, "active_members": active_members,
                "member_retention_rate": member_retention,
                "is_women_shg": is_women_shg, "is_tribal_shg": is_tribal_shg,
                "category": category,
                "monthly_savings_per_member": monthly_savings,
                "total_monthly_savings": total_monthly_savings,
                "cumulative_savings": cumulative_savings,
                "savings_regularity_pct": savings_regularity,
                "internal_lending_amount": internal_lending,
                "external_loan_amount": external_loan,
                "loan_outstanding": loan_outstanding,
                "repayment_rate_pct": repayment_rate,
                "loan_demand_met_pct": loan_demand_met,
                "npa_status": npa_status,
                "corpus_fund": corpus_fund,
                "interest_earned": interest_earned,
                "bank_account_balance": bank_balance,
                "number_of_loans_taken": number_of_loans,
                "average_loan_size": avg_loan_size,
                "bank_linked": bank_linked,
                "bank_name": bank_name if bank_linked else "None",
                "bank_linkage_year": bank_linkage_year,
                "credit_linkage_amount": credit_amount,
                "number_of_credit_linkages": credit_linkages,
                "savings_bank_account": savings_account,
                "meetings_held_last_year": meetings,
                "meeting_attendance_pct": attendance,
                "minutes_recorded": minutes_recorded,
                "books_maintained": books,
                "audit_completed": audit_completed,
                "audit_grade": audit_grade,
                "has_elected_leaders": has_leaders,
                "leadership_rotation": leader_rotation,
                "financial_literacy_training": fin_literacy,
                "skill_training_received": skill_training,
                "enterprise_training": enterprise_training,
                "number_of_trainings": num_trainings,
                "training_organization": training_org,
                "has_micro_enterprise": has_enterprise,
                "enterprise_type": enterprise_type,
                "monthly_enterprise_income": enterprise_income,
                "enterprise_age_months": enterprise_age,
                "market_linkage": market_linkage,
                "number_of_income_sources": income_sources,
                "has_digital_payment": digital_payment,
                "uses_mobile_banking": mobile_banking,
                "has_whatsapp_group": whatsapp,
                "uses_social_media_marketing": social_media,
                "digital_literacy_score": digital_score,
                "is_federated": is_federated,
                "federation_level": federation_level,
                "connected_to_nrlm": connected_nrlm,
                "nrlm_grade": nrlm_grade,
            }
            
            # Feature engineering
            input_data["savings_to_loan_ratio"] = cumulative_savings / external_loan if external_loan > 0 else cumulative_savings
            input_data["repayment_efficiency"] = repayment_rate * loan_demand_met / 100
            input_data["loan_utilization_rate"] = (external_loan - loan_outstanding) / external_loan if external_loan > 0 else 0
            input_data["per_member_savings"] = cumulative_savings / max(active_members, 1)
            input_data["per_member_loan"] = external_loan / max(active_members, 1)
            input_data["corpus_to_savings_ratio"] = corpus_fund / cumulative_savings if cumulative_savings > 0 else 1.0
            input_data["interest_to_lending_ratio"] = interest_earned / internal_lending if internal_lending > 0 else 0
            expected_sav = total_monthly_savings * group_age_years * 12
            input_data["savings_growth_rate"] = cumulative_savings / expected_sav if expected_sav > 0 else 0
            
            books_map = {"Excellent": 100, "Good": 75, "Average": 45, "Poor": 15}
            audit_map_val = {"A": 100, "B": 70, "C": 40, "D": 15, "Not Audited": 10}
            input_data["governance_score"] = (
                0.30 * attendance +
                0.20 * books_map.get(books, 50) +
                0.15 * audit_map_val.get(audit_grade, 10) +
                0.15 * (has_leaders * 100) +
                0.10 * (leader_rotation * 100) +
                0.10 * (minutes_recorded * 100)
            )
            input_data["digital_readiness_score"] = (
                25 * digital_payment + 25 * mobile_banking +
                20 * whatsapp + 30 * social_media
            )
            input_data["training_intensity"] = num_trainings / group_age_years if group_age_years > 0 else num_trainings
            
            input_data["savings_x_attendance"] = savings_regularity * attendance / 100
            input_data["loan_x_repayment"] = np.log1p(external_loan) * (repayment_rate / 100) if external_loan > 0 else 0
            input_data["enterprise_x_training"] = has_enterprise * num_trainings
            input_data["age_x_savings"] = np.log1p(group_age_years) * np.log1p(cumulative_savings)
            input_data["members_x_enterprise_income"] = active_members * np.log1p(enterprise_income)
            input_data["bank_x_governance"] = bank_linked * input_data["governance_score"]
            
            input_data["is_mature_group"] = 1 if group_age_years > 5 else 0
            if group_age_years < 2:
                input_data["age_category_encoded"] = 0
            elif group_age_years < 5:
                input_data["age_category_encoded"] = 1
            elif group_age_years < 10:
                input_data["age_category_encoded"] = 2
            else:
                input_data["age_category_encoded"] = 3
            
            input_df = pd.DataFrame([input_data])
            
            if encoders:
                from config import CATEGORICAL_COLUMNS
                for col in CATEGORICAL_COLUMNS:
                    if col in input_df.columns and col in encoders:
                        le = encoders[col]
                        val = input_df[col].iloc[0]
                        if val not in le.classes_:
                            val = "Unknown"
                        input_df[col] = le.transform([val])
            
            if feature_list:
                for feat in feature_list:
                    if feat not in input_df.columns:
                        input_df[feat] = 0
                input_df = input_df[feature_list]
            
            if scaler:
                input_scaled = pd.DataFrame(scaler.transform(input_df), columns=feature_list)
            else:
                input_scaled = input_df
            
            prediction_encoded = model.predict(input_scaled)[0]
            
            if target_encoder:
                prediction = target_encoder.inverse_transform([prediction_encoded])[0]
            else:
                class_map = {0: "High Performance", 1: "Low Performance", 2: "Medium Performance"}
                prediction = class_map.get(prediction_encoded, "Unknown")
            
            if hasattr(model, 'predict_proba'):
                probas = model.predict_proba(input_scaled)[0]
                class_names = target_encoder.classes_ if target_encoder else ["High Performance", "Low Performance", "Medium Performance"]
            else:
                probas = None
                class_names = []
            
            st.markdown("---")
            st.markdown("### 🎯 Model Inference Results")
            
            r1, r2 = st.columns([1, 2])
            
            with r1:
                st.markdown(get_performance_badge(prediction), unsafe_allow_html=True)
                st.markdown(f"<div style='margin-top:0.8rem; font-size:1.1rem; color:#FFFFFF;'><b>Predicted Classification:</b><br><span style='color:#A8A0FF;'>{prediction}</span></div>", unsafe_allow_html=True)
            
            with r2:
                if probas is not None:
                    fig_prob = go.Figure(go.Bar(
                        x=[f"{c}" for c in class_names],
                        y=[p * 100 for p in probas],
                        marker_color=[PERF_COLORS.get(c, "#6C63FF") for c in class_names],
                        text=[f"{p*100:.1f}%" for p in probas],
                        textposition='outside',
                        textfont=dict(color='#FFFFFF', size=13)
                    ))
                    fig_prob.update_layout(
                        **PLOTLY_TEMPLATE["layout"],
                        title="Model Prediction Probability Breakdown",
                        yaxis_title="Confidence Probability (%)",
                        height=280,
                        yaxis_range=[0, 108]
                    )
                    st.plotly_chart(fig_prob, use_container_width=True)
            
            st.markdown('<div class="section-header">💡 Actionable Advisory Recommendations</div>', unsafe_allow_html=True)
            recommendations = get_recommendations(prediction, input_data)
            for rec in recommendations:
                st.markdown(rec)
                
        except Exception as e:
            st.error(f"❌ Prediction failed with error: {str(e)}")
            st.exception(e)

# ── Footer ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <p><strong>SHG AI Predictor</strong> • Module 2 of Intelligent SHG Performance Platform</p>
</div>
""", unsafe_allow_html=True)
