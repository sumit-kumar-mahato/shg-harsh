"""
SHG Model Evaluation Module
=============================
Comprehensive evaluation of ML models with visualizations,
confusion matrices, ROC curves, feature importance, and SHAP analysis.
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix, roc_curve, auc
)
from sklearn.preprocessing import label_binarize


def evaluate_model(model, X_test, y_test) -> dict:
    """
    Compute comprehensive evaluation metrics for a trained model.
    
    Args:
        model: Trained classifier.
        X_test: Test feature matrix.
        y_test: True test labels.
    
    Returns:
        Dict with accuracy, precision, recall, f1, and per-class metrics.
    """
    y_pred = model.predict(X_test)
    
    results = {
        "accuracy": round(accuracy_score(y_test, y_pred) * 100, 2),
        "precision_macro": round(precision_score(y_test, y_pred, average='macro', zero_division=0) * 100, 2),
        "recall_macro": round(recall_score(y_test, y_pred, average='macro', zero_division=0) * 100, 2),
        "f1_macro": round(f1_score(y_test, y_pred, average='macro', zero_division=0) * 100, 2),
        "precision_weighted": round(precision_score(y_test, y_pred, average='weighted', zero_division=0) * 100, 2),
        "recall_weighted": round(recall_score(y_test, y_pred, average='weighted', zero_division=0) * 100, 2),
        "f1_weighted": round(f1_score(y_test, y_pred, average='weighted', zero_division=0) * 100, 2),
    }
    
    return results


def plot_confusion_matrix(y_true, y_pred, classes, save_path: str = None):
    """
    Plot and save a confusion matrix heatmap.
    """
    cm = confusion_matrix(y_true, y_pred, labels=classes)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(
        cm, annot=True, fmt='d', cmap='Blues',
        xticklabels=classes, yticklabels=classes,
        ax=ax, linewidths=0.5
    )
    ax.set_xlabel('Predicted Label', fontsize=12)
    ax.set_ylabel('True Label', fontsize=12)
    ax.set_title('Confusion Matrix — SHG Performance Prediction', fontsize=14)
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"  Confusion matrix saved to: {save_path}")
    plt.close(fig)
    
    return cm


def plot_roc_curves(model, X_test, y_test, classes, save_path: str = None):
    """
    Plot multi-class ROC curves (One-vs-Rest).
    """
    try:
        y_prob = model.predict_proba(X_test)
    except AttributeError:
        print("  Model does not support predict_proba. Skipping ROC curves.")
        return
    
    # Binarize labels
    y_bin = label_binarize(y_test, classes=classes)
    n_classes = len(classes)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    colors = ['#2196F3', '#FF9800', '#4CAF50']
    
    for i in range(n_classes):
        fpr, tpr, _ = roc_curve(y_bin[:, i], y_prob[:, i])
        roc_auc = auc(fpr, tpr)
        ax.plot(fpr, tpr, color=colors[i % len(colors)], lw=2,
                label=f'{classes[i]} (AUC = {roc_auc:.3f})')
    
    ax.plot([0, 1], [0, 1], 'k--', lw=1, alpha=0.5)
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel('False Positive Rate', fontsize=12)
    ax.set_ylabel('True Positive Rate', fontsize=12)
    ax.set_title('Multi-Class ROC Curves — SHG Performance', fontsize=14)
    ax.legend(loc='lower right', fontsize=11)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"  ROC curves saved to: {save_path}")
    plt.close(fig)


def plot_feature_importance(model, feature_names, top_n: int = 20,
                            save_path: str = None):
    """
    Plot horizontal bar chart of top feature importances.
    """
    try:
        importances = model.feature_importances_
    except AttributeError:
        try:
            importances = np.abs(model.coef_[0])
        except (AttributeError, IndexError):
            print("  Cannot extract feature importance from this model.")
            return None
    
    feat_imp = pd.Series(importances, index=feature_names).sort_values(ascending=True)
    feat_imp = feat_imp.tail(top_n)
    
    fig, ax = plt.subplots(figsize=(10, max(8, top_n * 0.4)))
    colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(feat_imp)))
    feat_imp.plot(kind='barh', ax=ax, color=colors)
    ax.set_xlabel('Importance Score', fontsize=12)
    ax.set_title(f'Top {top_n} Feature Importances', fontsize=14)
    ax.grid(True, axis='x', alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"  Feature importance plot saved to: {save_path}")
    plt.close(fig)
    
    return feat_imp


def generate_classification_report(y_true, y_pred, save_path: str = None) -> str:
    """
    Generate and optionally save a full classification report.
    """
    report = classification_report(y_true, y_pred, zero_division=0)
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'w') as f:
            f.write("SHG Performance Prediction — Classification Report\n")
            f.write("=" * 60 + "\n\n")
            f.write(report)
        print(f"  Classification report saved to: {save_path}")
    
    return report


def plot_model_comparison(results_dict: dict, save_path: str = None):
    """
    Plot bar chart comparing multiple models on key metrics.
    
    Args:
        results_dict: {model_name: {metric_name: value, ...}, ...}
    """
    metrics = ["accuracy", "precision_macro", "recall_macro", "f1_macro"]
    metric_labels = ["Accuracy", "Precision", "Recall", "F1-Score"]
    
    model_names = list(results_dict.keys())
    x = np.arange(len(model_names))
    width = 0.20
    
    fig, ax = plt.subplots(figsize=(14, 7))
    colors = ['#2196F3', '#FF9800', '#4CAF50', '#9C27B0']
    
    for i, (metric, label) in enumerate(zip(metrics, metric_labels)):
        values = [results_dict[m].get(metric, 0) for m in model_names]
        ax.bar(x + i * width, values, width, label=label, color=colors[i], alpha=0.85)
    
    ax.set_xlabel('Model', fontsize=12)
    ax.set_ylabel('Score (%)', fontsize=12)
    ax.set_title('Model Comparison — SHG Performance Prediction', fontsize=14)
    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(model_names, rotation=30, ha='right')
    ax.legend(fontsize=10)
    ax.set_ylim(0, 105)
    ax.grid(True, axis='y', alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"  Model comparison plot saved to: {save_path}")
    plt.close(fig)


def analyze_shap_values(model, X_test, feature_names, save_path: str = None):
    """
    Generate SHAP summary plot for model explainability.
    Handles gracefully if SHAP is not installed.
    """
    try:
        import shap
        
        print("  Computing SHAP values (this may take a moment)...")
        
        # Use TreeExplainer for tree-based models, KernelExplainer for others
        try:
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X_test[:200])
        except Exception:
            # Fallback to KernelExplainer with sampling
            background = shap.sample(X_test, 50)
            explainer = shap.KernelExplainer(model.predict_proba, background)
            shap_values = explainer.shap_values(X_test[:100])
        
        fig = plt.figure(figsize=(12, 8))
        if isinstance(shap_values, list):
            shap.summary_plot(shap_values[0], X_test[:200],
                              feature_names=feature_names, show=False)
        else:
            shap.summary_plot(shap_values, X_test[:200],
                              feature_names=feature_names, show=False)
        
        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"  SHAP plot saved to: {save_path}")
        plt.close()
        
    except ImportError:
        print("  SHAP not installed. Skipping SHAP analysis.")
        print("  Install with: pip install shap")
    except Exception as e:
        print(f"  SHAP analysis failed: {e}")


def generate_full_report(model, X_test, y_test, feature_names,
                         output_dir: str, model_name: str = "Best Model"):
    """
    Run all evaluation steps and save everything to output_dir.
    
    Args:
        model: Trained model.
        X_test: Test features.
        y_test: True labels.
        feature_names: List of feature names.
        output_dir: Directory to save all outputs.
        model_name: Name of the model for reporting.
    """
    os.makedirs(output_dir, exist_ok=True)
    classes = sorted(np.unique(y_test))
    y_pred = model.predict(X_test)
    
    print(f"\n{'='*60}")
    print(f"FULL EVALUATION REPORT — {model_name}")
    print(f"{'='*60}")
    
    # 1. Metrics
    print("\n[1] Computing metrics...")
    metrics = evaluate_model(model, X_test, y_test)
    for k, v in metrics.items():
        print(f"    {k}: {v}%")
    
    # 2. Classification report
    print("\n[2] Classification report...")
    report = generate_classification_report(
        y_test, y_pred,
        save_path=os.path.join(output_dir, "classification_report.txt")
    )
    print(report)
    
    # 3. Confusion matrix
    print("\n[3] Confusion matrix...")
    plot_confusion_matrix(
        y_test, y_pred, classes,
        save_path=os.path.join(output_dir, "confusion_matrix.png")
    )
    
    # 4. ROC curves
    print("\n[4] ROC curves...")
    plot_roc_curves(
        model, X_test, y_test, classes,
        save_path=os.path.join(output_dir, "roc_curves.png")
    )
    
    # 5. Feature importance
    print("\n[5] Feature importance...")
    plot_feature_importance(
        model, feature_names, top_n=25,
        save_path=os.path.join(output_dir, "feature_importance.png")
    )
    
    # 6. SHAP values
    print("\n[6] SHAP analysis...")
    analyze_shap_values(
        model, X_test, feature_names,
        save_path=os.path.join(output_dir, "shap_summary.png")
    )
    
    # 7. Save metrics to JSON-like text
    metrics_path = os.path.join(output_dir, "metrics_summary.txt")
    with open(metrics_path, 'w') as f:
        f.write(f"Model: {model_name}\n")
        f.write("=" * 40 + "\n")
        for k, v in metrics.items():
            f.write(f"{k}: {v}%\n")
    
    print(f"\n All evaluation artifacts saved to: {output_dir}")
    return metrics
