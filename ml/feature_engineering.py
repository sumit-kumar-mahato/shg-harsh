"""
SHG Feature Engineering Module
================================
Creates advanced derived features, interaction terms, and performs
feature selection for the SHG performance prediction model.
"""

import numpy as np
import pandas as pd
from sklearn.feature_selection import mutual_info_classif
from sklearn.ensemble import RandomForestClassifier


def create_financial_ratios(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create financial ratio features from raw financial columns.
    
    New features created:
        - savings_to_loan_ratio
        - repayment_efficiency
        - loan_utilization_rate
        - per_member_savings
        - per_member_loan
        - corpus_to_savings_ratio
        - interest_to_lending_ratio
        - savings_growth_rate
    """
    df = df.copy()
    
    # Savings to loan ratio
    df["savings_to_loan_ratio"] = np.where(
        df["external_loan_amount"] > 0,
        df["cumulative_savings"] / df["external_loan_amount"],
        df["cumulative_savings"] / 1  # Avoid division by zero
    )
    df["savings_to_loan_ratio"] = df["savings_to_loan_ratio"].clip(0, 50)
    
    # Repayment efficiency (repayment rate × loan demand met)
    df["repayment_efficiency"] = (
        df["repayment_rate_pct"] * df["loan_demand_met_pct"] / 100
    )
    
    # Loan utilization rate
    df["loan_utilization_rate"] = np.where(
        df["external_loan_amount"] > 0,
        (df["external_loan_amount"] - df["loan_outstanding"]) / df["external_loan_amount"],
        0
    )
    
    # Per member metrics
    active = df["active_members"].replace(0, 1)
    df["per_member_savings"] = df["cumulative_savings"] / active
    df["per_member_loan"] = df["external_loan_amount"] / active
    
    # Corpus to savings ratio (indicates interest income health)
    df["corpus_to_savings_ratio"] = np.where(
        df["cumulative_savings"] > 0,
        df["corpus_fund"] / df["cumulative_savings"],
        1.0
    )
    df["corpus_to_savings_ratio"] = df["corpus_to_savings_ratio"].clip(0, 5)
    
    # Interest to lending ratio (profitability of internal lending)
    df["interest_to_lending_ratio"] = np.where(
        df["internal_lending_amount"] > 0,
        df["interest_earned"] / df["internal_lending_amount"],
        0
    )
    df["interest_to_lending_ratio"] = df["interest_to_lending_ratio"].clip(0, 1)
    
    # Savings growth rate (proxy using cumulative / (monthly * age))
    expected_savings = df["total_monthly_savings"] * df["group_age_years"] * 12
    df["savings_growth_rate"] = np.where(
        expected_savings > 0,
        df["cumulative_savings"] / expected_savings,
        0
    )
    df["savings_growth_rate"] = df["savings_growth_rate"].clip(0, 5)
    
    print(f"  Created 8 financial ratio features")
    return df


def create_governance_scores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create composite governance and readiness scores.
    
    New features:
        - governance_score (0-100)
        - digital_readiness_score (0-100)
        - training_intensity (0-1)
    """
    df = df.copy()
    
    # Governance score composite
    # Encode books_maintained if still string
    if df["books_maintained"].dtype == 'object':
        books_map = {"Excellent": 100, "Good": 75, "Average": 45, "Poor": 15}
        books_val = df["books_maintained"].map(books_map).fillna(30)
    else:
        books_val = df["books_maintained"] * 25  # Scale encoded values
    
    # Encode audit_grade if still string
    if "audit_grade" in df.columns and df["audit_grade"].dtype == 'object':
        audit_map = {"A": 100, "B": 70, "C": 40, "D": 15, "Not Audited": 10}
        audit_val = df["audit_grade"].map(audit_map).fillna(10)
    else:
        audit_val = 50  # Default if encoded
    
    df["governance_score"] = (
        0.30 * df["meeting_attendance_pct"] +
        0.20 * books_val +
        0.15 * audit_val +
        0.15 * (df["has_elected_leaders"] * 100) +
        0.10 * (df["leadership_rotation"] * 100) +
        0.10 * (df["minutes_recorded"] * 100)
    )
    df["governance_score"] = df["governance_score"].clip(0, 100).round(2)
    
    # Digital readiness score
    df["digital_readiness_score"] = (
        25 * df["has_digital_payment"] +
        25 * df["uses_mobile_banking"] +
        20 * df["has_whatsapp_group"] +
        30 * df["uses_social_media_marketing"]
    )
    df["digital_readiness_score"] = df["digital_readiness_score"].clip(0, 100)
    
    # Training intensity (ratio of trainings to group age)
    df["training_intensity"] = np.where(
        df["group_age_years"] > 0,
        df["number_of_trainings"] / df["group_age_years"],
        df["number_of_trainings"]
    )
    df["training_intensity"] = df["training_intensity"].clip(0, 5)
    
    print(f"  Created 3 composite score features")
    return df


def create_interaction_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create feature interaction terms that capture combined effects.
    
    New features:
        - savings_x_attendance
        - loan_x_repayment
        - enterprise_x_training
        - age_x_savings
        - members_x_enterprise_income
        - bank_x_governance
    """
    df = df.copy()
    
    # Savings × Attendance — financially active AND well-governed
    df["savings_x_attendance"] = (
        df["savings_regularity_pct"] * df["meeting_attendance_pct"] / 100
    )
    
    # Loan × Repayment — credit discipline
    df["loan_x_repayment"] = np.where(
        df["external_loan_amount"] > 0,
        np.log1p(df["external_loan_amount"]) * (df["repayment_rate_pct"] / 100),
        0
    )
    
    # Enterprise × Training — productive capacity
    df["enterprise_x_training"] = (
        df["has_micro_enterprise"] * df["number_of_trainings"]
    )
    
    # Age × Savings — maturity-weighted wealth
    df["age_x_savings"] = np.log1p(df["group_age_years"]) * np.log1p(df["cumulative_savings"])
    
    # Members × Enterprise income — group economic output
    df["members_x_enterprise_income"] = (
        df["active_members"] * np.log1p(df["monthly_enterprise_income"])
    )
    
    # Bank linkage × Governance — institutional readiness
    df["bank_x_governance"] = (
        df["bank_linked"] * df.get("governance_score", df["meeting_attendance_pct"])
    )
    
    print(f"  Created 6 interaction features")
    return df


def create_age_based_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create age-based categorical and derived features.
    
    New features:
        - is_mature_group (>5 years)
        - age_category_encoded (New=0, Young=1, Mature=2, Old=3)
    """
    df = df.copy()
    
    # Binary maturity flag
    df["is_mature_group"] = (df["group_age_years"] > 5).astype(int)
    
    # Age category
    conditions = [
        df["group_age_years"] < 2,
        df["group_age_years"] < 5,
        df["group_age_years"] < 10,
        df["group_age_years"] >= 10,
    ]
    choices = [0, 1, 2, 3]  # New, Young, Mature, Old
    df["age_category_encoded"] = np.select(conditions, choices, default=1)
    
    print(f"  Created 2 age-based features")
    return df


def select_features(X: pd.DataFrame, y: pd.Series,
                    method: str = "importance", top_k: int = None) -> list:
    """
    Select top features using mutual information or random forest importance.
    
    Args:
        X: Feature matrix.
        y: Target vector.
        method: 'importance' or 'mutual_info'.
        top_k: Number of top features to select. None = return all ranked.
    
    Returns:
        List of selected feature names sorted by importance.
    """
    if method == "mutual_info":
        # Mutual Information
        mi_scores = mutual_info_classif(X, y, random_state=42)
        feature_scores = pd.Series(mi_scores, index=X.columns).sort_values(ascending=False)
    else:
        # Random Forest importance
        rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        rf.fit(X, y)
        feature_scores = pd.Series(
            rf.feature_importances_, index=X.columns
        ).sort_values(ascending=False)
    
    print(f"\n  Top 20 Features ({method}):")
    for i, (feat, score) in enumerate(feature_scores.head(20).items()):
        print(f"    {i+1:2d}. {feat:<40s} {score:.4f}")
    
    if top_k:
        selected = feature_scores.head(top_k).index.tolist()
        print(f"\n  Selected top {top_k} features")
        return selected
    
    return feature_scores.index.tolist()


def apply_feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply all feature engineering steps.
    
    Args:
        df: Input DataFrame (after preprocessing, before encoding).
    
    Returns:
        DataFrame with all engineered features added.
    """
    print("\n" + "=" * 60)
    print("FEATURE ENGINEERING")
    print("=" * 60)
    
    print("\n[Step 1] Creating financial ratios...")
    df = create_financial_ratios(df)
    
    print("\n[Step 2] Creating governance scores...")
    df = create_governance_scores(df)
    
    print("\n[Step 3] Creating interaction features...")
    df = create_interaction_features(df)
    
    print("\n[Step 4] Creating age-based features...")
    df = create_age_based_features(df)
    
    print(f"\nFeature engineering complete. Total columns: {len(df.columns)}")
    return df
