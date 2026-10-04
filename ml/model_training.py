"""
SHG Model Training Pipeline
==============================
Trains multiple ML models, performs hyperparameter tuning,
builds an ensemble, and saves the best model.

Usage:
    python model_training.py
"""

import os
import sys
import time
import warnings
import numpy as np
import pandas as pd
import joblib

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import (
    RandomForestClassifier, GradientBoostingClassifier,
    AdaBoostClassifier, ExtraTreesClassifier, VotingClassifier
)
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold
from sklearn.preprocessing import LabelEncoder

warnings.filterwarnings('ignore')

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (
    DATASET_PATH, SAVED_MODELS_DIR, EVALUATION_DIR,
    BEST_MODEL_PATH, TARGET_COLUMN, DROP_COLUMNS,
    CATEGORICAL_COLUMNS, MODEL_METADATA_PATH
)
from ml.data_preprocessing import (
    load_data, handle_missing_values, remove_outliers,
    encode_categoricals, drop_unnecessary_columns,
    get_train_test_split, create_scaler, save_preprocessor
)
from ml.feature_engineering import (
    apply_feature_engineering, select_features
)
from ml.model_evaluation import (
    evaluate_model, plot_confusion_matrix, plot_roc_curves,
    plot_feature_importance, generate_classification_report,
    plot_model_comparison, analyze_shap_values, generate_full_report
)

# Try to import XGBoost
try:
    from xgboost import XGBClassifier
    HAS_XGBOOST = True
    print("XGBoost available.")
except ImportError:
    HAS_XGBOOST = False
    print("XGBoost not available. Using sklearn GradientBoosting instead.")


# ── Model Definitions ──────────────────────────────────────────────────────

def get_models(label_encoder) -> dict:
    """
    Define all candidate models.
    
    Returns:
        Dict of {model_name: model_instance}.
    """
    models = {
        "Logistic Regression": LogisticRegression(
            max_iter=1000, random_state=42,
            solver='lbfgs', C=1.0
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=200, max_depth=20, min_samples_split=5,
            min_samples_leaf=2, random_state=42, n_jobs=-1
        ),
        "Decision Tree": DecisionTreeClassifier(
            max_depth=15, min_samples_split=10, random_state=42
        ),
        "KNN": KNeighborsClassifier(
            n_neighbors=7, weights='distance', n_jobs=-1
        ),
        "SVM": SVC(
            kernel='rbf', C=10, gamma='scale',
            probability=True, random_state=42
        ),
        "AdaBoost": AdaBoostClassifier(
            n_estimators=150, learning_rate=0.1, random_state=42
        ),
        "Extra Trees": ExtraTreesClassifier(
            n_estimators=200, max_depth=20, min_samples_split=5,
            random_state=42, n_jobs=-1
        ),
    }
    
    if HAS_XGBOOST:
        models["XGBoost"] = XGBClassifier(
            n_estimators=200, max_depth=8, learning_rate=0.1,
            subsample=0.8, colsample_bytree=0.8,
            random_state=42, eval_metric='mlogloss'
        )
    else:
        models["Gradient Boosting"] = GradientBoostingClassifier(
            n_estimators=200, max_depth=6, learning_rate=0.1,
            subsample=0.8, random_state=42
        )
    
    return models


def get_hyperparam_grids() -> dict:
    """
    Define hyperparameter search spaces for top models.
    """
    grids = {
        "Random Forest": {
            "n_estimators": [100, 200, 300, 500],
            "max_depth": [10, 15, 20, 25, None],
            "min_samples_split": [2, 5, 10],
            "min_samples_leaf": [1, 2, 4],
            "max_features": ["sqrt", "log2", 0.5],
        },
        "Extra Trees": {
            "n_estimators": [100, 200, 300, 500],
            "max_depth": [10, 15, 20, 25, None],
            "min_samples_split": [2, 5, 10],
            "min_samples_leaf": [1, 2, 4],
        },
    }
    
    if HAS_XGBOOST:
        grids["XGBoost"] = {
            "n_estimators": [100, 200, 300, 500],
            "max_depth": [4, 6, 8, 10, 12],
            "learning_rate": [0.01, 0.05, 0.1, 0.2],
            "subsample": [0.7, 0.8, 0.9, 1.0],
            "colsample_bytree": [0.7, 0.8, 0.9, 1.0],
            "min_child_weight": [1, 3, 5],
            "gamma": [0, 0.1, 0.2],
        }
    else:
        grids["Gradient Boosting"] = {
            "n_estimators": [100, 200, 300],
            "max_depth": [4, 6, 8, 10],
            "learning_rate": [0.01, 0.05, 0.1, 0.2],
            "subsample": [0.7, 0.8, 0.9, 1.0],
            "min_samples_split": [2, 5, 10],
        }
    
    return grids


# ── Training Pipeline ──────────────────────────────────────────────────────

def train_all_models(X_train, X_test, y_train, y_test, feature_names) -> dict:
    """
    Train all candidate models and evaluate them.
    
    Returns:
        Dict of {model_name: {'model': model, 'metrics': metrics, 'time': time}}.
    """
    # Encode target labels
    le_target = LabelEncoder()
    y_train_enc = le_target.fit_transform(y_train)
    y_test_enc = le_target.transform(y_test)
    
    models = get_models(le_target)
    results = {}
    
    print("\n" + "=" * 70)
    print("TRAINING ALL MODELS")
    print("=" * 70)
    
    for name, model in models.items():
        print(f"\n  Training: {name}...", end=" ", flush=True)
        start = time.time()
        
        try:
            model.fit(X_train, y_train_enc)
            elapsed = time.time() - start
            
            metrics = evaluate_model(model, X_test, y_test_enc)
            results[name] = {
                "model": model,
                "metrics": metrics,
                "time": round(elapsed, 2)
            }
            
            print(f"Done ({elapsed:.1f}s) | Accuracy: {metrics['accuracy']}% | F1: {metrics['f1_macro']}%")
        except Exception as e:
            print(f"FAILED: {e}")
    
    return results, le_target


def tune_top_models(X_train, y_train_enc, results: dict, top_n: int = 3) -> dict:
    """
    Perform hyperparameter tuning on the top N models.
    
    Args:
        X_train: Training features.
        y_train_enc: Encoded training labels.
        results: Results from train_all_models.
        top_n: Number of top models to tune.
    
    Returns:
        Updated results dict with tuned models.
    """
    # Rank models by F1 score
    ranked = sorted(
        results.items(),
        key=lambda x: x[1]["metrics"]["f1_macro"],
        reverse=True
    )
    
    grids = get_hyperparam_grids()
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    print("\n" + "=" * 70)
    print(f"HYPERPARAMETER TUNING (Top {top_n} Models)")
    print("=" * 70)
    
    tuned_results = {}
    
    for name, data in ranked[:top_n]:
        if name not in grids:
            print(f"\n  {name}: No hyperparameter grid defined, keeping default.")
            tuned_results[name] = data
            continue
        
        print(f"\n  Tuning: {name}...")
        start = time.time()
        
        search = RandomizedSearchCV(
            estimator=data["model"],
            param_distributions=grids[name],
            n_iter=30,
            cv=cv,
            scoring='f1_macro',
            random_state=42,
            n_jobs=-1,
            verbose=0
        )
        
        search.fit(X_train, y_train_enc)
        elapsed = time.time() - start
        
        print(f"    Best CV F1: {search.best_score_ * 100:.2f}%")
        print(f"    Best params: {search.best_params_}")
        print(f"    Time: {elapsed:.1f}s")
        
        tuned_results[name] = {
            "model": search.best_estimator_,
            "metrics": data["metrics"],  # Will be re-evaluated
            "time": round(elapsed, 2),
            "best_params": search.best_params_,
            "cv_score": round(search.best_score_ * 100, 2)
        }
    
    return tuned_results


def build_ensemble(tuned_results: dict, X_train, y_train_enc) -> VotingClassifier:
    """
    Build a soft-voting ensemble from the top tuned models.
    """
    estimators = [(name, data["model"]) for name, data in tuned_results.items()]
    
    # Ensure all models support predict_proba
    valid_estimators = []
    for name, model in estimators:
        if hasattr(model, 'predict_proba'):
            valid_estimators.append((name, model))
        else:
            print(f"  Skipping {name} in ensemble (no predict_proba)")
    
    if len(valid_estimators) < 2:
        print("  Not enough models for ensemble. Using best single model.")
        return None
    
    print(f"\n  Building ensemble with: {[n for n, _ in valid_estimators]}")
    ensemble = VotingClassifier(
        estimators=valid_estimators,
        voting='soft',
        n_jobs=-1
    )
    ensemble.fit(X_train, y_train_enc)
    
    return ensemble


# ── Main Pipeline ──────────────────────────────────────────────────────────

def run_training_pipeline():
    """
    Execute the complete training pipeline:
    1. Load and preprocess data
    2. Engineer features
    3. Train multiple models
    4. Tune top models
    5. Build ensemble
    6. Evaluate and save best model
    """
    print("\n" + "=" * 70)
    print("SHG PERFORMANCE PREDICTION — MODEL TRAINING PIPELINE")
    print("=" * 70)
    
    # ── Step 1: Load data ───────────────────────────────────────────────
    print("\n[Step 1/8] Loading data...")
    df = load_data(DATASET_PATH)
    
    # ── Step 2: Handle missing values ───────────────────────────────────
    print("\n[Step 2/8] Handling missing values...")
    df = handle_missing_values(df)
    
    # ── Step 3: Feature engineering (before encoding) ───────────────────
    print("\n[Step 3/8] Feature engineering...")
    # Drop only ID columns first, keep categoricals for FE
    df = df.drop(columns=[c for c in DROP_COLUMNS if c in df.columns], errors='ignore')
    
    # Remove performance_score (data leakage)
    if "performance_score" in df.columns:
        df = df.drop(columns=["performance_score"])
    
    df = apply_feature_engineering(df)
    
    # ── Step 4: Encode categoricals ─────────────────────────────────────
    print("\n[Step 4/8] Encoding categoricals...")
    y = df[TARGET_COLUMN]
    X = df.drop(columns=[TARGET_COLUMN])
    X, encoders = encode_categoricals(X, fit=True)
    
    # ── Step 5: Remove outliers ─────────────────────────────────────────
    print("\n[Step 5/8] Capping outliers...")
    X = remove_outliers(X)
    
    # ── Step 6: Split and scale ─────────────────────────────────────────
    print("\n[Step 6/8] Splitting and scaling data...")
    X_train, X_test, y_train, y_test = get_train_test_split(X, y)
    
    scaler, X_train_scaled = create_scaler(X_train)
    X_test_scaled = pd.DataFrame(
        scaler.transform(X_test),
        columns=X_test.columns,
        index=X_test.index
    )
    
    feature_list = list(X_train.columns)
    
    # Save preprocessing artifacts
    save_preprocessor(scaler, encoders, feature_list)
    
    # Feature selection analysis
    print("\n[Feature Analysis] Ranking features by importance...")
    select_features(X_train_scaled, y_train, method='importance')
    
    # ── Step 7: Train models ────────────────────────────────────────────
    print("\n[Step 7/8] Training models...")
    results, le_target = train_all_models(
        X_train_scaled, X_test_scaled, y_train, y_test, feature_list
    )
    
    # Encode targets for tuning
    y_train_enc = le_target.transform(y_train)
    y_test_enc = le_target.transform(y_test)
    
    # Print comparison table
    print("\n" + "=" * 70)
    print("MODEL COMPARISON TABLE")
    print("=" * 70)
    print(f"{'Model':<25s} {'Accuracy':>10s} {'Precision':>10s} {'Recall':>10s} {'F1-Score':>10s} {'Time(s)':>8s}")
    print("-" * 73)
    
    for name, data in sorted(results.items(),
                              key=lambda x: x[1]["metrics"]["f1_macro"],
                              reverse=True):
        m = data["metrics"]
        print(f"{name:<25s} {m['accuracy']:>9.2f}% {m['precision_macro']:>9.2f}% "
              f"{m['recall_macro']:>9.2f}% {m['f1_macro']:>9.2f}% {data['time']:>7.1f}")
    
    # ── Tune top 3 models ──────────────────────────────────────────────
    # Get top 3 models that have tuning grids
    ranked = sorted(results.items(), key=lambda x: x[1]["metrics"]["f1_macro"], reverse=True)
    tunable = {n: d for n, d in ranked if n in get_hyperparam_grids()}
    top_tunable = dict(list(tunable.items())[:3])
    
    if top_tunable:
        tuned = tune_top_models(X_train_scaled, y_train_enc, top_tunable, top_n=3)
        
        # Re-evaluate tuned models
        for name, data in tuned.items():
            metrics = evaluate_model(data["model"], X_test_scaled, y_test_enc)
            tuned[name]["metrics"] = metrics
            results[f"{name} (Tuned)"] = data
        
        # Build ensemble
        print("\n[Ensemble] Building voting ensemble...")
        ensemble = build_ensemble(tuned, X_train_scaled, y_train_enc)
        
        if ensemble is not None:
            ensemble_metrics = evaluate_model(ensemble, X_test_scaled, y_test_enc)
            results["Ensemble (Top 3)"] = {
                "model": ensemble,
                "metrics": ensemble_metrics,
                "time": 0
            }
            print(f"  Ensemble Accuracy: {ensemble_metrics['accuracy']}% | F1: {ensemble_metrics['f1_macro']}%")
    
    # ── Step 8: Select and save best model ──────────────────────────────
    print("\n[Step 8/8] Selecting and saving best model...")
    
    # Pick the best model by F1 macro
    best_name = max(results.items(), key=lambda x: x[1]["metrics"]["f1_macro"])[0]
    best_model = results[best_name]["model"]
    best_metrics = results[best_name]["metrics"]
    
    print(f"\n  BEST MODEL: {best_name}")
    print(f"  Accuracy:  {best_metrics['accuracy']}%")
    print(f"  F1-Score:  {best_metrics['f1_macro']}%")
    print(f"  Precision: {best_metrics['precision_macro']}%")
    print(f"  Recall:    {best_metrics['recall_macro']}%")
    
    # Save model
    os.makedirs(SAVED_MODELS_DIR, exist_ok=True)
    joblib.dump(best_model, BEST_MODEL_PATH)
    joblib.dump(le_target, os.path.join(SAVED_MODELS_DIR, "target_encoder.joblib"))
    
    # Save metadata
    metadata = {
        "model_name": best_name,
        "metrics": best_metrics,
        "feature_count": len(feature_list),
        "training_samples": len(X_train),
        "test_samples": len(X_test),
        "classes": list(le_target.classes_),
    }
    joblib.dump(metadata, MODEL_METADATA_PATH)
    
    print(f"\n  Model saved to: {BEST_MODEL_PATH}")
    
    # ── Generate evaluation report ──────────────────────────────────────
    print("\n[Evaluation] Generating full evaluation report...")
    os.makedirs(EVALUATION_DIR, exist_ok=True)
    
    # Evaluation report for best model
    generate_full_report(
        best_model, X_test_scaled, y_test_enc,
        feature_list, EVALUATION_DIR, model_name=best_name
    )
    
    # Model comparison plot
    all_metrics = {n: d["metrics"] for n, d in results.items()}
    plot_model_comparison(
        all_metrics,
        save_path=os.path.join(EVALUATION_DIR, "model_comparison.png")
    )
    
    print("\n" + "=" * 70)
    print("TRAINING PIPELINE COMPLETE")
    print("=" * 70)
    print(f"  Best model: {best_name}")
    print(f"  Accuracy:   {best_metrics['accuracy']}%")
    print(f"  F1-Score:   {best_metrics['f1_macro']}%")
    print(f"  Saved to:   {SAVED_MODELS_DIR}")
    print(f"  Eval:       {EVALUATION_DIR}")
    
    return best_model, best_metrics


if __name__ == "__main__":
    model, metrics = run_training_pipeline()
