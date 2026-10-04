"""
SHG Data Preprocessing Module
==============================
Handles data cleaning, missing value imputation, encoding,
and train/test splitting for the SHG performance prediction pipeline.
"""

import os
import sys
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (
    DATASET_PATH, DROP_COLUMNS, CATEGORICAL_COLUMNS,
    TARGET_COLUMN, SAVED_MODELS_DIR
)


def load_data(filepath: str = DATASET_PATH) -> pd.DataFrame:
    """
    Load the SHG dataset from CSV.
    
    Args:
        filepath: Path to the CSV file.
    
    Returns:
        Loaded DataFrame.
    """
    print(f"Loading data from: {filepath}")
    df = pd.read_csv(filepath)
    print(f"  Shape: {df.shape}")
    print(f"  Columns: {len(df.columns)}")
    print(f"  Target distribution:\n{df[TARGET_COLUMN].value_counts()}")
    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Impute missing values using median for numeric and mode for categorical.
    
    Args:
        df: Input DataFrame with potential missing values.
    
    Returns:
        DataFrame with missing values imputed.
    """
    df = df.copy()
    missing_before = df.isnull().sum().sum()
    
    # Numeric columns — median imputation
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df[col].isnull().any():
            median_val = df[col].median()
            df[col].fillna(median_val, inplace=True)
    
    # Categorical columns — mode imputation
    cat_cols = df.select_dtypes(include=['object']).columns
    for col in cat_cols:
        if df[col].isnull().any():
            mode_val = df[col].mode()[0] if not df[col].mode().empty else "Unknown"
            df[col].fillna(mode_val, inplace=True)
    
    missing_after = df.isnull().sum().sum()
    print(f"  Missing values: {missing_before} -> {missing_after}")
    return df


def remove_outliers(df: pd.DataFrame, columns: list = None, iqr_factor: float = 3.0) -> pd.DataFrame:
    """
    Cap outliers using IQR method (winsorization). Does NOT remove rows,
    instead caps values at the IQR boundaries to preserve data.
    
    Args:
        df: Input DataFrame.
        columns: Columns to check for outliers. If None, uses all numeric.
        iqr_factor: IQR multiplier for boundary calculation.
    
    Returns:
        DataFrame with outliers capped.
    """
    df = df.copy()
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Exclude target score and binary columns
    exclude = [TARGET_COLUMN, "performance_score"]
    columns = [c for c in columns if c not in exclude and df[c].nunique() > 2]
    
    outlier_count = 0
    for col in columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - iqr_factor * IQR
        upper = Q3 + iqr_factor * IQR
        
        outliers = ((df[col] < lower) | (df[col] > upper)).sum()
        outlier_count += outliers
        
        df[col] = df[col].clip(lower=lower, upper=upper)
    
    print(f"  Outliers capped: {outlier_count} values across {len(columns)} columns")
    return df


def encode_categoricals(df: pd.DataFrame, fit: bool = True,
                        encoders: dict = None) -> tuple:
    """
    Label encode categorical features for ML training.
    
    Args:
        df: Input DataFrame.
        fit: If True, fit new encoders. If False, use provided encoders.
        encoders: Pre-fitted encoders (used during prediction).
    
    Returns:
        Tuple of (encoded DataFrame, dict of fitted encoders).
    """
    df = df.copy()
    if encoders is None:
        encoders = {}
    
    cat_cols = [c for c in CATEGORICAL_COLUMNS if c in df.columns]
    
    for col in cat_cols:
        if fit:
            le = LabelEncoder()
            # Add 'Unknown' to handle unseen categories during prediction
            unique_vals = list(df[col].unique()) + ["Unknown"]
            le.fit(unique_vals)
            encoders[col] = le
        else:
            le = encoders.get(col)
            if le is None:
                continue
            # Handle unseen categories
            df[col] = df[col].apply(
                lambda x: x if x in le.classes_ else "Unknown"
            )
        
        df[col] = le.transform(df[col])
    
    print(f"  Encoded {len(cat_cols)} categorical columns")
    return df, encoders


def drop_unnecessary_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drop non-predictive columns (IDs, names, dates).
    Also drops performance_score to prevent data leakage.
    
    Args:
        df: Input DataFrame.
    
    Returns:
        DataFrame with unnecessary columns dropped.
    """
    cols_to_drop = [c for c in DROP_COLUMNS + ["performance_score"] if c in df.columns]
    df = df.drop(columns=cols_to_drop, errors='ignore')
    print(f"  Dropped columns: {cols_to_drop}")
    return df


def get_train_test_split(X: pd.DataFrame, y: pd.Series,
                         test_size: float = 0.2, random_state: int = 42) -> tuple:
    """
    Perform stratified train-test split.
    
    Args:
        X: Feature matrix.
        y: Target vector.
        test_size: Proportion for test set.
        random_state: Random seed.
    
    Returns:
        Tuple of (X_train, X_test, y_train, y_test).
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state,
        stratify=y
    )
    print(f"  Train: {X_train.shape}, Test: {X_test.shape}")
    print(f"  Train distribution:\n{y_train.value_counts()}")
    print(f"  Test distribution:\n{y_test.value_counts()}")
    return X_train, X_test, y_train, y_test


def create_scaler(X_train: pd.DataFrame) -> tuple:
    """
    Create and fit a StandardScaler on training data.
    
    Args:
        X_train: Training feature matrix.
    
    Returns:
        Tuple of (fitted scaler, scaled X_train).
    """
    scaler = StandardScaler()
    X_train_scaled = pd.DataFrame(
        scaler.fit_transform(X_train),
        columns=X_train.columns,
        index=X_train.index
    )
    return scaler, X_train_scaled


def save_preprocessor(scaler, encoders, feature_list, save_dir: str = SAVED_MODELS_DIR):
    """
    Save preprocessing artifacts for deployment.
    
    Args:
        scaler: Fitted StandardScaler.
        encoders: Dict of fitted LabelEncoders.
        feature_list: List of feature column names.
        save_dir: Directory to save artifacts.
    """
    os.makedirs(save_dir, exist_ok=True)
    
    joblib.dump(scaler, os.path.join(save_dir, "scaler.joblib"))
    joblib.dump(encoders, os.path.join(save_dir, "label_encoders.joblib"))
    joblib.dump(feature_list, os.path.join(save_dir, "feature_list.joblib"))
    
    print(f"  Preprocessing artifacts saved to: {save_dir}")


def run_full_preprocessing(filepath: str = DATASET_PATH) -> tuple:
    """
    Run the complete preprocessing pipeline.
    
    Args:
        filepath: Path to the raw dataset CSV.
    
    Returns:
        Tuple of (X_train, X_test, y_train, y_test, scaler, encoders, feature_list).
    """
    print("\n" + "=" * 60)
    print("DATA PREPROCESSING PIPELINE")
    print("=" * 60)
    
    # Step 1: Load data
    print("\n[Step 1] Loading data...")
    df = load_data(filepath)
    
    # Step 2: Handle missing values
    print("\n[Step 2] Handling missing values...")
    df = handle_missing_values(df)
    
    # Step 3: Drop unnecessary columns
    print("\n[Step 3] Dropping non-predictive columns...")
    df = drop_unnecessary_columns(df)
    
    # Step 4: Remove outliers
    print("\n[Step 4] Capping outliers...")
    df = remove_outliers(df)
    
    # Step 5: Separate features and target
    print("\n[Step 5] Separating features and target...")
    y = df[TARGET_COLUMN]
    X = df.drop(columns=[TARGET_COLUMN])
    
    # Step 6: Encode categoricals
    print("\n[Step 6] Encoding categorical features...")
    X, encoders = encode_categoricals(X, fit=True)
    
    # Step 7: Train-test split
    print("\n[Step 7] Splitting data...")
    X_train, X_test, y_train, y_test = get_train_test_split(X, y)
    
    # Step 8: Scale features
    print("\n[Step 8] Scaling features...")
    scaler, X_train_scaled = create_scaler(X_train)
    X_test_scaled = pd.DataFrame(
        scaler.transform(X_test),
        columns=X_test.columns,
        index=X_test.index
    )
    
    feature_list = list(X_train.columns)
    
    # Step 9: Save preprocessor
    print("\n[Step 9] Saving preprocessing artifacts...")
    save_preprocessor(scaler, encoders, feature_list)
    
    print(f"\nPreprocessing complete. Features: {len(feature_list)}")
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler, encoders, feature_list


if __name__ == "__main__":
    X_train, X_test, y_train, y_test, scaler, encoders, features = run_full_preprocessing()
    print(f"\nFinal feature count: {len(features)}")
    print(f"Features: {features}")
