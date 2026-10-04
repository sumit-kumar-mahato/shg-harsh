# ==============================================================================
# SHG Performance Platform - Configuration
# ==============================================================================

import os

# Project root directory
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Data paths
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
DATASET_PATH = os.path.join(RAW_DATA_DIR, "shg_performance_dataset.csv")

# ML paths
ML_DIR = os.path.join(PROJECT_ROOT, "ml")
SAVED_MODELS_DIR = os.path.join(ML_DIR, "saved_models")
EVALUATION_DIR = os.path.join(ML_DIR, "evaluation_results")

# Model filenames
BEST_MODEL_PATH = os.path.join(SAVED_MODELS_DIR, "best_model.joblib")
SCALER_PATH = os.path.join(SAVED_MODELS_DIR, "scaler.joblib")
LABEL_ENCODERS_PATH = os.path.join(SAVED_MODELS_DIR, "label_encoders.joblib")
FEATURE_LIST_PATH = os.path.join(SAVED_MODELS_DIR, "feature_list.joblib")
MODEL_METADATA_PATH = os.path.join(SAVED_MODELS_DIR, "model_metadata.joblib")

# Target column
TARGET_COLUMN = "performance_category"
PERFORMANCE_CLASSES = ["High Performance", "Medium Performance", "Low Performance"]

# Columns to drop during ML training (non-predictive)
DROP_COLUMNS = ["shg_id", "shg_name", "block", "formation_date"]

# Categorical columns for encoding
CATEGORICAL_COLUMNS = [
    "state", "district", "category", "bank_name", "enterprise_type",
    "audit_grade", "books_maintained", "federation_level", "nrlm_grade",
    "training_organization"
]

# Numeric columns that need scaling
BOOLEAN_COLUMNS = [
    "is_women_shg", "is_tribal_shg", "bank_linked", "minutes_recorded",
    "audit_completed", "has_elected_leaders", "leadership_rotation",
    "financial_literacy_training", "skill_training_received",
    "enterprise_training", "has_micro_enterprise", "market_linkage",
    "has_digital_payment", "uses_mobile_banking", "has_whatsapp_group",
    "uses_social_media_marketing", "is_federated", "connected_to_nrlm",
    "savings_bank_account"
]

# Dataset generation settings
NUM_SHGS = 5000
RANDOM_SEED = 42

# Performance thresholds
HIGH_PERFORMANCE_THRESHOLD = 70
LOW_PERFORMANCE_THRESHOLD = 45

# Indian states with weights for data generation
STATES_WEIGHTS = {
    "Uttar Pradesh": 0.12, "Bihar": 0.10, "Madhya Pradesh": 0.08,
    "Rajasthan": 0.07, "Jharkhand": 0.07, "Odisha": 0.07,
    "Andhra Pradesh": 0.08, "Telangana": 0.06, "Tamil Nadu": 0.07,
    "Karnataka": 0.06, "Maharashtra": 0.06, "West Bengal": 0.06,
    "Assam": 0.04, "Kerala": 0.03, "Gujarat": 0.03
}
