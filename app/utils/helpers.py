"""
Helper Utilities for the SHG Platform Streamlit App
=====================================================
Common functions for data loading, model loading, and formatting.
"""

import os
import sys
import pandas as pd
import numpy as np
import streamlit as st

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)


# ── Data Loading ────────────────────────────────────────────────────────────

@st.cache_data(ttl=3600)
def load_dataset(path: str = None) -> pd.DataFrame:
    """Load and cache the SHG dataset."""
    if path is None:
        path = os.path.join(PROJECT_ROOT, "data", "raw", "shg_performance_dataset.csv")
    
    if not os.path.exists(path):
        return None
    
    df = pd.read_csv(path)
    return df


@st.cache_resource
def load_model(path: str = None):
    """Load and cache the trained ML model."""
    import joblib
    if path is None:
        path = os.path.join(PROJECT_ROOT, "ml", "saved_models", "best_model.joblib")
    
    if not os.path.exists(path):
        return None
    return joblib.load(path)


@st.cache_resource
def load_preprocessor(artifact_name: str = "scaler"):
    """Load a preprocessing artifact (scaler, encoders, feature_list)."""
    import joblib
    path = os.path.join(PROJECT_ROOT, "ml", "saved_models", f"{artifact_name}.joblib")
    
    if not os.path.exists(path):
        return None
    return joblib.load(path)


# ── State Coordinates ───────────────────────────────────────────────────────

def get_state_coordinates() -> dict:
    """Return approximate lat/long for Indian states (for map visualization)."""
    return {
        "Uttar Pradesh": (26.8467, 80.9462),
        "Bihar": (25.0961, 85.3131),
        "Madhya Pradesh": (23.4735, 77.9479),
        "Rajasthan": (27.0238, 74.2179),
        "Jharkhand": (23.6102, 85.2799),
        "Odisha": (20.9517, 85.0985),
        "Andhra Pradesh": (15.9129, 79.7400),
        "Telangana": (18.1124, 79.0193),
        "Tamil Nadu": (11.1271, 78.6569),
        "Karnataka": (15.3173, 75.7139),
        "Maharashtra": (19.7515, 75.7139),
        "West Bengal": (22.9868, 87.8550),
        "Assam": (26.2006, 92.9376),
        "Kerala": (10.8505, 76.2711),
        "Gujarat": (22.2587, 71.1924),
    }


# ── Formatting ──────────────────────────────────────────────────────────────

def format_currency(amount) -> str:
    """Format a number as Indian Rupees with commas."""
    try:
        amount = float(amount)
        if amount >= 10000000:  # 1 Crore
            return f"₹{amount/10000000:.2f} Cr"
        elif amount >= 100000:  # 1 Lakh
            return f"₹{amount/100000:.2f} L"
        elif amount >= 1000:
            return f"₹{amount:,.0f}"
        else:
            return f"₹{amount:.0f}"
    except (ValueError, TypeError):
        return "₹0"


def format_percentage(value) -> str:
    """Format a number as a percentage."""
    try:
        return f"{float(value):.1f}%"
    except (ValueError, TypeError):
        return "0.0%"


def get_performance_color(category: str) -> str:
    """Return color hex for performance category."""
    colors = {
        "High Performance": "#38a169",
        "Medium Performance": "#d69e2e",
        "Low Performance": "#e53e3e",
    }
    return colors.get(category, "#718096")


def get_performance_badge(category: str) -> str:
    """Return HTML badge for performance category."""
    classes = {
        "High Performance": "perf-high",
        "Medium Performance": "perf-medium",
        "Low Performance": "perf-low",
    }
    css_class = classes.get(category, "perf-medium")
    emoji = {"High Performance": "🟢", "Medium Performance": "🟡", "Low Performance": "🔴"}
    em = emoji.get(category, "⚪")
    return f'<span class="perf-badge {css_class}">{em} {category}</span>'


def create_download_link(df: pd.DataFrame, filename: str = "data.csv") -> bytes:
    """Create CSV bytes for download."""
    return df.to_csv(index=False).encode('utf-8')


# ── Recommendations ─────────────────────────────────────────────────────────

def get_recommendations(prediction: str, inputs: dict) -> list:
    """
    Generate actionable recommendations based on prediction and inputs.
    """
    recommendations = []
    
    if prediction == "Low Performance":
        recommendations.append("🚨 **Urgent: Improve meeting regularity** — Aim for 12 meetings/year with 80%+ attendance.")
        recommendations.append("📚 **Enroll in financial literacy training** through NRLM or local NGOs.")
        recommendations.append("🏦 **Prioritize bank linkage** — Open a savings account and apply for credit linkage.")
        recommendations.append("📒 **Improve book-keeping** — Maintain regular records of savings, loans, and meetings.")
        recommendations.append("💰 **Increase savings regularity** — Ensure all members contribute monthly.")
    
    elif prediction == "Medium Performance":
        recommendations.append("📈 **Increase savings per member** — Consider raising monthly contribution by ₹50-100.")
        recommendations.append("🏢 **Start a micro-enterprise** — Explore group income-generating activities.")
        recommendations.append("📱 **Adopt digital tools** — Start using digital payments and WhatsApp for coordination.")
        recommendations.append("🎯 **Seek skill training** — Apply for enterprise development programs.")
        recommendations.append("🔗 **Join a federation** — Connect with cluster/block level federations for better support.")
    
    else:  # High Performance
        recommendations.append("🌟 **Maintain excellence** — Continue strong governance and financial discipline.")
        recommendations.append("📊 **Expand market linkages** — Explore online selling platforms for products.")
        recommendations.append("🤝 **Mentor other SHGs** — Share best practices with newer groups.")
        recommendations.append("💻 **Go digital** — Build a social media presence for products.")
        recommendations.append("🏆 **Apply for awards** — Nominate for NABARD/NRLM best SHG awards.")
    
    return recommendations
