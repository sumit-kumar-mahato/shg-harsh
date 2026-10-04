"""
SHG Synthetic Dataset Generator
================================
Generates a realistic synthetic dataset of 5000+ Self Help Groups (SHGs) in India
for ML classification (High/Medium/Low Performance).

Features: 50+ columns covering demographics, finances, governance, training,
enterprise, digital adoption, and federation details.
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Seed for reproducibility
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)

NUM_SHGS = 5000

# ── Reference Data ──────────────────────────────────────────────────────────

STATES_DISTRICTS = {
    "Uttar Pradesh": ["Lucknow", "Varanasi", "Agra", "Prayagraj", "Kanpur", "Gorakhpur", "Jhansi", "Bareilly"],
    "Bihar": ["Patna", "Gaya", "Muzaffarpur", "Bhagalpur", "Darbhanga", "Purnia", "Begusarai"],
    "Madhya Pradesh": ["Bhopal", "Indore", "Jabalpur", "Gwalior", "Ujjain", "Sagar", "Rewa"],
    "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Ajmer", "Kota", "Bikaner", "Alwar"],
    "Jharkhand": ["Ranchi", "Jamshedpur", "Dhanbad", "Bokaro", "Hazaribagh", "Deoghar"],
    "Odisha": ["Bhubaneswar", "Cuttack", "Berhampur", "Sambalpur", "Rourkela", "Balasore"],
    "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur", "Tirupati", "Nellore", "Kurnool", "Kakinada"],
    "Telangana": ["Hyderabad", "Warangal", "Karimnagar", "Nizamabad", "Khammam", "Mahbubnagar"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem", "Erode", "Tirunelveli"],
    "Karnataka": ["Bengaluru", "Mysuru", "Hubli-Dharwad", "Mangaluru", "Belagavi", "Kalaburagi"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad", "Solapur", "Kolhapur"],
    "West Bengal": ["Kolkata", "Howrah", "Siliguri", "Durgapur", "Asansol", "Bardhaman"],
    "Assam": ["Guwahati", "Silchar", "Dibrugarh", "Jorhat", "Nagaon"],
    "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur", "Kollam"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar"],
}

STATE_WEIGHTS = [0.12, 0.10, 0.08, 0.07, 0.07, 0.07, 0.08, 0.06, 0.07, 0.06, 0.06, 0.06, 0.04, 0.03, 0.03]
STATES = list(STATES_DISTRICTS.keys())

SHG_NAME_PREFIXES = [
    "Lakshmi", "Shakti", "Durga", "Saraswati", "Asha", "Nari", "Mahila", "Pragati",
    "Ujjwal", "Swayam", "Saheli", "Jyoti", "Kiran", "Rani", "Deepika", "Chandni",
    "Parvati", "Sita", "Ganga", "Radha", "Meera", "Savitri", "Annapurna", "Vaishali",
    "Kamla", "Sunita", "Geeta", "Mamta", "Nirmala", "Pushpa", "Tulsi", "Kavita",
    "Sangini", "Sahyog", "Ekta", "Samridhi", "Unnati", "Vikas", "Jagriti", "Chetna"
]

SHG_NAME_SUFFIXES = [
    "Mahila SHG", "Women SHG", "Self Help Group", "Mahila Mandal",
    "Swayam Sahayata Samuh", "Bachat Gat", "Mahila Samuh",
    "Livelihood Group", "Empowerment Group", "Development SHG"
]

BANK_NAMES = ["SBI", "PNB", "Bank of Baroda", "Canara Bank", "IOB",
              "Union Bank", "Central Bank", "UCO Bank", "IDBI Bank",
              "District Cooperative Bank", "Gramin Bank"]

ENTERPRISE_TYPES = ["Agriculture", "Dairy", "Handicrafts", "Tailoring",
                    "Food Processing", "Retail", "Services", "None"]

TRAINING_ORGS = ["NRLM", "NGO", "Bank", "Government", "None"]

CATEGORIES = ["SC", "ST", "OBC", "General", "Minority"]
CATEGORY_WEIGHTS = [0.20, 0.15, 0.35, 0.20, 0.10]

BLOCKS = [
    "Block-I", "Block-II", "Block-III", "Block-IV", "Block-V",
    "North Block", "South Block", "East Block", "West Block", "Central Block"
]


# ── Helper Functions ────────────────────────────────────────────────────────

def generate_shg_name(idx: int) -> str:
    """Generate a realistic SHG name."""
    prefix = random.choice(SHG_NAME_PREFIXES)
    suffix = random.choice(SHG_NAME_SUFFIXES)
    return f"{prefix} {suffix}"


def generate_formation_date() -> datetime:
    """Generate a random formation date between 2005 and 2024."""
    start = datetime(2005, 1, 1)
    end = datetime(2024, 6, 30)
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))


def clamp(value, min_val, max_val):
    """Clamp a value between min and max."""
    return max(min_val, min(max_val, value))


# ── Main Generation Function ───────────────────────────────────────────────

def generate_shg_record(idx: int) -> dict:
    """
    Generate a single SHG record with 50+ correlated features.
    
    The function creates realistic correlations between features:
    - Older groups tend to have more savings and bank linkages
    - Better governance correlates with higher financial performance
    - Training received correlates with enterprise activity
    - Digital adoption correlates with younger/urban groups
    """
    record = {}
    
    # ── Basic Demographics ──────────────────────────────────────────────
    record["shg_id"] = f"SHG_{idx:04d}"
    record["shg_name"] = generate_shg_name(idx)
    
    state = np.random.choice(STATES, p=STATE_WEIGHTS)
    record["state"] = state
    record["district"] = random.choice(STATES_DISTRICTS[state])
    record["block"] = random.choice(BLOCKS)
    
    formation_date = generate_formation_date()
    record["formation_date"] = formation_date.strftime("%Y-%m-%d")
    group_age = (datetime(2025, 1, 1) - formation_date).days / 365.25
    record["group_age_years"] = round(group_age, 1)
    
    # Group size and retention — older groups have slightly better retention
    group_size = random.randint(10, 20)
    record["group_size"] = group_size
    
    age_factor = min(group_age / 15, 1.0)  # Normalize age 0-1
    retention_base = 0.60 + 0.30 * age_factor + np.random.normal(0, 0.08)
    retention_rate = clamp(retention_base, 0.50, 1.0)
    active_members = max(int(group_size * retention_rate), 5)
    record["active_members"] = min(active_members, group_size)
    record["member_retention_rate"] = round(record["active_members"] / group_size, 3)
    
    record["is_women_shg"] = random.random() < 0.85
    record["is_tribal_shg"] = random.random() < 0.15
    record["category"] = np.random.choice(CATEGORIES, p=CATEGORY_WEIGHTS)
    
    # ── Governance Quality (latent variable) ────────────────────────────
    # This drives many correlated features
    governance_quality = clamp(np.random.beta(2.5, 2.0) + 0.10 * age_factor, 0, 1)
    
    # ── Meeting & Governance ────────────────────────────────────────────
    meetings_base = int(governance_quality * 12 + np.random.normal(0, 1.5))
    record["meetings_held_last_year"] = clamp(meetings_base, 0, 12)
    
    attendance_base = governance_quality * 100 + np.random.normal(0, 10)
    record["meeting_attendance_pct"] = round(clamp(attendance_base, 40, 100), 1)
    
    record["minutes_recorded"] = random.random() < (0.3 + 0.6 * governance_quality)
    
    books_score = governance_quality + np.random.normal(0, 0.1)
    if books_score > 0.75:
        record["books_maintained"] = "Excellent"
    elif books_score > 0.50:
        record["books_maintained"] = "Good"
    elif books_score > 0.25:
        record["books_maintained"] = "Average"
    else:
        record["books_maintained"] = "Poor"
    
    record["audit_completed"] = random.random() < (0.2 + 0.7 * governance_quality)
    
    if record["audit_completed"]:
        audit_score = governance_quality + np.random.normal(0, 0.1)
        if audit_score > 0.70:
            record["audit_grade"] = "A"
        elif audit_score > 0.50:
            record["audit_grade"] = "B"
        elif audit_score > 0.30:
            record["audit_grade"] = "C"
        else:
            record["audit_grade"] = "D"
    else:
        record["audit_grade"] = "Not Audited"
    
    record["has_elected_leaders"] = random.random() < (0.4 + 0.5 * governance_quality)
    record["leadership_rotation"] = random.random() < (0.3 + 0.4 * governance_quality)
    
    # ── Financial Metrics ───────────────────────────────────────────────
    # Monthly savings — correlated with governance and age
    savings_multiplier = 1.0 + 0.5 * governance_quality + 0.3 * age_factor
    monthly_savings_per_member = clamp(
        int(np.random.lognormal(4.5, 0.6) * savings_multiplier / 10) * 10,
        50, 500
    )
    record["monthly_savings_per_member"] = monthly_savings_per_member
    record["total_monthly_savings"] = monthly_savings_per_member * record["active_members"]
    
    # Cumulative savings — based on age and monthly rate
    months_active = int(group_age * 12)
    savings_regularity = clamp(governance_quality * 0.9 + np.random.normal(0.05, 0.08), 0.50, 1.0)
    record["savings_regularity_pct"] = round(savings_regularity * 100, 1)
    
    cumulative_savings = int(
        record["total_monthly_savings"] * months_active * savings_regularity * np.random.uniform(0.7, 1.1)
    )
    record["cumulative_savings"] = max(cumulative_savings, record["total_monthly_savings"])
    
    # Internal lending
    record["internal_lending_amount"] = int(record["cumulative_savings"] * np.random.uniform(0.5, 1.5))
    
    # Interest earned
    record["interest_earned"] = int(record["internal_lending_amount"] * np.random.uniform(0.05, 0.20))
    
    # Corpus fund
    record["corpus_fund"] = record["cumulative_savings"] + record["interest_earned"]
    
    # External loans — older and better-governed groups get bigger loans
    loan_probability = 0.3 + 0.5 * age_factor + 0.2 * governance_quality
    has_external_loan = random.random() < clamp(loan_probability, 0, 0.95)
    
    if has_external_loan:
        max_loan = min(record["cumulative_savings"] * np.random.uniform(2, 8), 500000)
        record["external_loan_amount"] = int(clamp(max_loan, 10000, 500000))
        record["number_of_loans_taken"] = random.randint(1, max(min(int(group_age), 10), 1))
    else:
        record["external_loan_amount"] = 0
        record["number_of_loans_taken"] = 0
    
    # Repayment rate — correlated with governance
    if record["external_loan_amount"] > 0:
        repayment_base = governance_quality * 80 + np.random.normal(15, 10)
        record["repayment_rate_pct"] = round(clamp(repayment_base, 30, 100), 1)
        outstanding_pct = clamp(1 - (record["repayment_rate_pct"] / 100) + np.random.normal(0, 0.1), 0, 0.8)
        record["loan_outstanding"] = int(record["external_loan_amount"] * outstanding_pct)
    else:
        record["repayment_rate_pct"] = round(clamp(np.random.normal(85, 10), 60, 100), 1)
        record["loan_outstanding"] = 0
    
    record["loan_demand_met_pct"] = round(clamp(
        50 + 40 * governance_quality + np.random.normal(0, 8), 30, 100
    ), 1)
    
    record["npa_status"] = record["repayment_rate_pct"] < 60
    
    record["average_loan_size"] = (
        int(record["external_loan_amount"] / record["number_of_loans_taken"])
        if record["number_of_loans_taken"] > 0 else 0
    )
    
    record["bank_account_balance"] = int(clamp(
        record["corpus_fund"] * np.random.uniform(0.05, 0.40), 500, 200000
    ))
    
    # ── Bank Linkage ────────────────────────────────────────────────────
    bank_link_prob = 0.3 + 0.4 * age_factor + 0.2 * governance_quality
    record["bank_linked"] = random.random() < clamp(bank_link_prob, 0.2, 0.95)
    
    if record["bank_linked"]:
        record["bank_name"] = random.choice(BANK_NAMES)
        link_year = formation_date.year + random.randint(0, max(int(group_age), 1))
        record["bank_linkage_year"] = min(link_year, 2024)
        credit_amount = int(record["cumulative_savings"] * np.random.uniform(1.5, 6.0))
        record["credit_linkage_amount"] = clamp(credit_amount, 0, 1000000)
        record["number_of_credit_linkages"] = random.randint(1, min(int(group_age / 2) + 1, 5))
        record["savings_bank_account"] = True
    else:
        record["bank_name"] = "None"
        record["bank_linkage_year"] = 0
        record["credit_linkage_amount"] = 0
        record["number_of_credit_linkages"] = 0
        record["savings_bank_account"] = random.random() < 0.3
    
    # ── Training & Capacity ─────────────────────────────────────────────
    training_factor = governance_quality * 0.6 + age_factor * 0.3
    
    record["financial_literacy_training"] = random.random() < (0.2 + 0.6 * training_factor)
    record["skill_training_received"] = random.random() < (0.15 + 0.5 * training_factor)
    record["enterprise_training"] = random.random() < (0.10 + 0.4 * training_factor)
    
    num_trainings = sum([
        record["financial_literacy_training"],
        record["skill_training_received"],
        record["enterprise_training"]
    ])
    record["number_of_trainings"] = num_trainings + random.randint(0, max(int(training_factor * 7), 0))
    record["number_of_trainings"] = clamp(record["number_of_trainings"], 0, 10)
    
    if record["number_of_trainings"] > 0:
        record["training_organization"] = np.random.choice(
            ["NRLM", "NGO", "Bank", "Government"],
            p=[0.35, 0.30, 0.20, 0.15]
        )
    else:
        record["training_organization"] = "None"
    
    # ── Livelihood & Enterprise ─────────────────────────────────────────
    enterprise_prob = 0.15 + 0.4 * training_factor + 0.2 * (record["skill_training_received"])
    record["has_micro_enterprise"] = random.random() < clamp(enterprise_prob, 0.1, 0.7)
    
    if record["has_micro_enterprise"]:
        # Weight enterprise types by region
        if state in ["Tamil Nadu", "Karnataka", "Kerala", "Andhra Pradesh", "Telangana"]:
            weights = [0.15, 0.15, 0.20, 0.20, 0.15, 0.10, 0.05, 0.00]
        elif state in ["Rajasthan", "Gujarat", "Madhya Pradesh"]:
            weights = [0.20, 0.10, 0.25, 0.15, 0.10, 0.10, 0.10, 0.00]
        else:
            weights = [0.20, 0.15, 0.15, 0.15, 0.15, 0.10, 0.10, 0.00]
        
        record["enterprise_type"] = np.random.choice(
            ENTERPRISE_TYPES, p=weights
        )
        income_base = np.random.lognormal(8.5, 1.0)
        record["monthly_enterprise_income"] = int(clamp(income_base, 1000, 50000))
        record["enterprise_age_months"] = random.randint(3, min(int(group_age * 12), 120))
        record["market_linkage"] = random.random() < (0.2 + 0.4 * governance_quality)
    else:
        record["enterprise_type"] = "None"
        record["monthly_enterprise_income"] = 0
        record["enterprise_age_months"] = 0
        record["market_linkage"] = False
    
    record["number_of_income_sources"] = 1 + (
        int(record["has_micro_enterprise"]) +
        random.randint(0, 2) +
        int(record["skill_training_received"])
    )
    record["number_of_income_sources"] = clamp(record["number_of_income_sources"], 1, 5)
    
    # ── Digital Adoption ────────────────────────────────────────────────
    # Younger groups and southern states tend to be more digitally savvy
    digital_base = 0.2 + 0.3 * (1 - age_factor)  # Newer groups more digital
    if state in ["Tamil Nadu", "Karnataka", "Kerala", "Telangana", "Maharashtra"]:
        digital_base += 0.15
    
    record["has_digital_payment"] = random.random() < clamp(digital_base + 0.1, 0, 0.8)
    record["uses_mobile_banking"] = random.random() < clamp(digital_base, 0, 0.7)
    record["has_whatsapp_group"] = random.random() < clamp(digital_base + 0.2, 0, 0.9)
    record["uses_social_media_marketing"] = random.random() < clamp(digital_base - 0.1, 0, 0.4)
    
    digital_score = (
        2 * record["has_digital_payment"] +
        2 * record["uses_mobile_banking"] +
        1.5 * record["has_whatsapp_group"] +
        2.5 * record["uses_social_media_marketing"] +
        np.random.normal(1, 0.8)
    )
    record["digital_literacy_score"] = round(clamp(digital_score, 0, 10), 1)
    
    # ── Federation & Network ────────────────────────────────────────────
    record["is_federated"] = random.random() < (0.2 + 0.4 * age_factor)
    if record["is_federated"]:
        record["federation_level"] = np.random.choice(
            ["Primary", "Cluster", "Block"], p=[0.5, 0.3, 0.2]
        )
    else:
        record["federation_level"] = "None"
    
    record["connected_to_nrlm"] = random.random() < (0.3 + 0.4 * governance_quality)
    
    if record["connected_to_nrlm"]:
        grade_score = governance_quality + np.random.normal(0, 0.1)
        if grade_score > 0.65:
            record["nrlm_grade"] = "A"
        elif grade_score > 0.40:
            record["nrlm_grade"] = "B"
        else:
            record["nrlm_grade"] = "C"
    else:
        record["nrlm_grade"] = "Not Graded"
    
    return record


# ── Performance Scoring ─────────────────────────────────────────────────────

def compute_performance_score(record: dict) -> float:
    """
    Compute a weighted performance score (0-100) for an SHG.
    
    Weight breakdown:
        - repayment_rate_pct:       20%
        - meeting_attendance_pct:   15%
        - savings_regularity_pct:   12%
        - member_retention_rate:    10%
        - books_maintained:          8%
        - has_micro_enterprise:      8%
        - bank_linked:               5%
        - financial_literacy:        5%
        - number_of_trainings:       5%
        - digital_literacy_score:    4%
        - enterprise_income:         4%
        - audit_grade:               4%
    """
    score = 0.0
    
    # Repayment rate (20%)
    score += (record["repayment_rate_pct"] / 100) * 20
    
    # Meeting attendance (15%)
    score += (record["meeting_attendance_pct"] / 100) * 15
    
    # Savings regularity (12%)
    score += (record["savings_regularity_pct"] / 100) * 12
    
    # Member retention (10%)
    score += record["member_retention_rate"] * 10
    
    # Books maintained (8%)
    books_map = {"Excellent": 1.0, "Good": 0.75, "Average": 0.45, "Poor": 0.15}
    score += books_map.get(record["books_maintained"], 0.3) * 8
    
    # Has micro enterprise (8%)
    score += (1.0 if record["has_micro_enterprise"] else 0.0) * 8
    
    # Bank linked (5%)
    score += (1.0 if record["bank_linked"] else 0.0) * 5
    
    # Financial literacy training (5%)
    score += (1.0 if record["financial_literacy_training"] else 0.0) * 5
    
    # Number of trainings (5%) — normalized to 0-1
    score += min(record["number_of_trainings"] / 8.0, 1.0) * 5
    
    # Digital literacy score (4%) — normalized 0-10 -> 0-1
    score += (record["digital_literacy_score"] / 10.0) * 4
    
    # Enterprise income (4%) — normalized with log transform
    if record["monthly_enterprise_income"] > 0:
        income_norm = min(np.log1p(record["monthly_enterprise_income"]) / np.log1p(50000), 1.0)
    else:
        income_norm = 0.0
    score += income_norm * 4
    
    # Audit grade (4%)
    audit_map = {"A": 1.0, "B": 0.70, "C": 0.40, "D": 0.15, "Not Audited": 0.10}
    score += audit_map.get(record["audit_grade"], 0.1) * 4
    
    # Add slight noise to prevent perfect separability
    noise = np.random.normal(0, 3)
    score = clamp(score + noise, 0, 100)
    
    return round(score, 2)


def classify_performance(score: float) -> str:
    """Classify SHG performance based on score."""
    if score >= 70:
        return "High Performance"
    elif score >= 45:
        return "Medium Performance"
    else:
        return "Low Performance"


# ── Introduce Missing Values ───────────────────────────────────────────────

def add_missing_values(df: pd.DataFrame, missing_rate: float = 0.03) -> pd.DataFrame:
    """
    Introduce realistic missing values (2-5%) in selected columns.
    Never add missing values to the target or key ID columns.
    """
    columns_with_missing = [
        "bank_linkage_year", "credit_linkage_amount", "enterprise_age_months",
        "monthly_enterprise_income", "audit_grade", "training_organization",
        "digital_literacy_score", "nrlm_grade", "bank_account_balance"
    ]
    
    df_out = df.copy()
    for col in columns_with_missing:
        if col in df_out.columns:
            mask = np.random.random(len(df_out)) < missing_rate
            df_out.loc[mask, col] = np.nan
    
    return df_out


# ── Main Generator ──────────────────────────────────────────────────────────

def generate_dataset(num_shgs: int = NUM_SHGS) -> pd.DataFrame:
    """
    Generate the full SHG dataset with performance labels.
    
    Args:
        num_shgs: Number of SHG records to generate.
        
    Returns:
        pd.DataFrame with all features and performance labels.
    """
    print(f"Generating {num_shgs} SHG records...")
    
    records = []
    for i in range(1, num_shgs + 1):
        record = generate_shg_record(i)
        record["performance_score"] = compute_performance_score(record)
        record["performance_category"] = classify_performance(record["performance_score"])
        records.append(record)
        
        if i % 1000 == 0:
            print(f"  Generated {i}/{num_shgs} records...")
    
    df = pd.DataFrame(records)
    
    # Convert boolean columns to int for ML compatibility
    bool_cols = df.select_dtypes(include=['bool']).columns
    for col in bool_cols:
        df[col] = df[col].astype(int)
    
    # Add missing values
    df = add_missing_values(df)
    
    return df


# ── Entry Point ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Generate dataset
    df = generate_dataset(NUM_SHGS)
    
    # Create output directory
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")
    os.makedirs(output_dir, exist_ok=True)
    
    # Save to CSV
    output_path = os.path.join(output_dir, "shg_performance_dataset.csv")
    df.to_csv(output_path, index=False)
    print(f"\nDataset saved to: {output_path}")
    
    # Summary statistics
    print(f"\n{'='*60}")
    print("DATASET SUMMARY")
    print(f"{'='*60}")
    print(f"Shape: {df.shape}")
    print(f"Columns: {len(df.columns)}")
    print(f"\nPerformance Distribution:")
    print(df["performance_category"].value_counts())
    print(f"\nPerformance Score Stats:")
    print(df["performance_score"].describe())
    print(f"\nMissing Values:")
    missing = df.isnull().sum()
    print(missing[missing > 0])
    print(f"\nSample Records (first 3):")
    print(df.head(3).T)
    print(f"\nStates Distribution:")
    print(df["state"].value_counts())
