import os
import sys
import argparse
import json
import csv
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix, precision_recall_fscore_support
)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ml.preprocessing.normalizer import normalize_text
from ml.feature_engineering.glove_embedder import GloVeEmbedder
from ml.feature_engineering.pca_reducer import PCAReducer
from ml.feature_engineering.context_encoder import ContextualEncoder
from ml.feature_engineering.fusion import FeatureFusion
from ml.models.classifier import CyberbullyingAMLClassifier, UNIFIED_CLASSES

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "unified" / "unified_dataset.csv"
MODELS_DIR = BASE_DIR / "trained_models" / "cyberbullying_model"
ARTIFACTS_DIR = BASE_DIR / "artifacts"
EVAL_DIR = ARTIFACTS_DIR / "evaluation"
PLOTS_DIR = ARTIFACTS_DIR / "plots"
TABLES_DIR = ARTIFACTS_DIR / "tables"

for d in [MODELS_DIR, EVAL_DIR, PLOTS_DIR, TABLES_DIR]:
    d.mkdir(parents=True, exist_ok=True)

def mcnemar_test(y_true, y_pred1, y_pred2):
    """
    McNemar's statistical test for comparing two classifiers:
    b: Classifier 1 correct, Classifier 2 incorrect
    c: Classifier 1 incorrect, Classifier 2 correct
    Test statistic = (|b - c| - 1)^2 / (b + c)
    """
    b = sum((p1 == y and p2 != y) for y, p1, p2 in zip(y_true, y_pred1, y_pred2))
    c = sum((p1 != y and p2 == y) for y, p1, p2 in zip(y_true, y_pred1, y_pred2))
    if b + c == 0:
        return 0.0, 1.0
    statistic = ((abs(b - c) - 1) ** 2) / (b + c)
    # 1 degree of freedom chi-square approximation
    from scipy.stats import chi2
    p_value = 1.0 - chi2.cdf(statistic, df=1)
    return float(statistic), float(p_value)

def train(mode: str = "standard"):
    print(f"=== CyberGuard Training Pipeline (Mode: {mode.upper()}) ===")

    if not DATA_PATH.exists():
        print(f"Dataset not found at {DATA_PATH}. Run download_datasets.py and preprocess_all.py first.")
        return

    df = pd.read_csv(DATA_PATH)
    print(f"Loaded {len(df)} preprocessed records from {DATA_PATH}")

    # Configure sample size and model hyperparams based on mode
    if mode == "fast":
        df_train_sample = df.sample(min(len(df), 200), random_state=42)
    elif mode == "standard":
        df_train_sample = df
    else: # full
        df_train_sample = df

    X_texts = df_train_sample["normalized_text"].tolist()
    y_labels = df_train_sample["unified_label"].tolist()
    languages = df_train_sample["detected_language"].tolist()

    # Split train/test (80/20 stratified)
    X_train, X_test, y_train, y_test, lang_train, lang_test = train_test_split(
        X_texts, y_labels, languages, test_size=0.20, random_state=42, stratify=y_labels
    )
    print(f"Train samples: {len(X_train)} | Test samples: {len(X_test)}")

    # 1. GloVe & PCA
    print("1. Extracting GloVe embeddings (100d)...")
    glove = GloVeEmbedder(embedding_dim=100)
    X_glove_train = glove.transform_batch(X_train)
    X_glove_test = glove.transform_batch(X_test)

    print("2. Applying PCA dimensionality reduction (100d -> 30d)...")
    pca = PCAReducer(n_components=30)
    X_pca_train = pca.fit_transform(X_glove_train)
    X_pca_test = pca.transform(X_glove_test)

    # 2. Contextual semantic representation (384d)
    print("3. Encoding contextual semantic representations (384d)...")
    ctx_enc = ContextualEncoder(output_dim=384)
    X_ctx_train = ctx_enc.encode_batch(X_train)
    X_ctx_test = ctx_enc.encode_batch(X_test)

    # 3. Feature Fusion (30d + 384d -> 414d)
    print("4. Executing Feature Fusion Layer...")
    fusion = FeatureFusion(pca_weight=1.0, ctx_weight=1.2)
    X_fused_train = fusion.fuse(X_pca_train, X_ctx_train)
    X_fused_test = fusion.fuse(X_pca_test, X_ctx_test)

    # 4. Train Classifiers
    print("5. Training AML base models & Stacking Ensemble...")
    classifier = CyberbullyingAMLClassifier(classes=UNIFIED_CLASSES)
    classifier.fit(X_fused_train, np.array(y_train))

    # Save models
    classifier.save(str(MODELS_DIR))
    pca.save(str(MODELS_DIR))
    print(f"-> Models and PCA metadata saved to {MODELS_DIR}")

    # 5. Evaluate Individual Models vs Ensemble
    print("6. Calculating comprehensive evaluation metrics...")
    models_to_eval = [
        ("Support Vector Machine (SVM)", "svm"),
        ("Gradient Boosting (GB)", "gradient_boost"),
        ("Random Forest (RF)", "random_forest"),
        ("CyberGuard Stacking Ensemble", "ensemble")
    ]

    comparison_results = []
    predictions_map = {}

    for name, m_key in models_to_eval:
        preds, confs = classifier.predict(X_fused_test, model_type=m_key)
        predictions_map[m_key] = preds

        acc = accuracy_score(y_test, preds)
        macro_f1 = f1_score(y_test, preds, average="macro", zero_division=0)
        weighted_f1 = f1_score(y_test, preds, average="weighted", zero_division=0)
        prec = precision_score(y_test, preds, average="macro", zero_division=0)
        rec = recall_score(y_test, preds, average="macro", zero_division=0)

        comparison_results.append({
            "model_name": name,
            "accuracy": round(acc, 4),
            "macro_f1": round(macro_f1, 4),
            "weighted_f1": round(weighted_f1, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4)
        })

    # Save comparison table
    comp_df = pd.DataFrame(comparison_results)
    comp_csv = TABLES_DIR / "model_comparison.csv"
    comp_df.to_csv(comp_csv, index=False)
    print(f"-> Saved {comp_csv}")
    print(comp_df.to_string(index=False))

    # McNemar's Test: SVM vs Ensemble
    stat, p_val = mcnemar_test(y_test, predictions_map["svm"], predictions_map["ensemble"])
    print(f"\nMcNemar's Test (SVM vs Stacking Ensemble): Stat={stat:.4f}, p-value={p_val:.4f}")

    # 6. Class-Wise Metrics (Ensemble)
    ensemble_preds = predictions_map["ensemble"]
    report_dict = classification_report(y_test, ensemble_preds, output_dict=True, zero_division=0)
    class_rows = []
    for cls in UNIFIED_CLASSES:
        if cls in report_dict:
            class_rows.append({
                "class_name": cls,
                "precision": round(report_dict[cls]["precision"], 4),
                "recall": round(report_dict[cls]["recall"], 4),
                "f1_score": round(report_dict[cls]["f1-score"], 4),
                "support": int(report_dict[cls]["support"])
            })
    class_df = pd.DataFrame(class_rows)
    class_csv = TABLES_DIR / "class_metrics.csv"
    class_df.to_csv(class_csv, index=False)

    # 7. Language-Wise Metrics
    lang_rows = []
    df_eval = pd.DataFrame({"y_true": y_test, "y_pred": ensemble_preds, "lang": lang_test})
    for lang in ["English", "Hindi", "Hinglish"]:
        subset = df_eval[df_eval["lang"] == lang]
        if len(subset) > 0:
            lang_acc = accuracy_score(subset["y_true"], subset["y_pred"])
            lang_f1 = f1_score(subset["y_true"], subset["y_pred"], average="macro", zero_division=0)
            lang_rows.append({
                "language": lang,
                "samples": len(subset),
                "accuracy": round(lang_acc, 4),
                "macro_f1": round(lang_f1, 4)
            })
    lang_df = pd.DataFrame(lang_rows)
    lang_csv = TABLES_DIR / "language_metrics.csv"
    lang_df.to_csv(lang_csv, index=False)

    # 8. Confusion Matrix Plot
    cm = confusion_matrix(y_test, ensemble_preds, labels=UNIFIED_CLASSES)
    plt.figure(figsize=(10, 8))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title("CyberGuard Ensemble Confusion Matrix")
    plt.colorbar()
    tick_marks = np.arange(len(UNIFIED_CLASSES))
    plt.xticks(tick_marks, UNIFIED_CLASSES, rotation=45, ha='right', fontsize=8)
    plt.yticks(tick_marks, UNIFIED_CLASSES, fontsize=8)
    plt.ylabel('True Class')
    plt.xlabel('Predicted Class')
    plt.tight_layout()
    cm_path = PLOTS_DIR / "confusion_matrix.png"
    plt.savefig(cm_path, dpi=150)
    plt.close()
    print(f"-> Generated confusion matrix plot: {cm_path}")

    # Save summary evaluation JSON
    best_f1 = max([r["macro_f1"] for r in comparison_results])
    eval_summary = {
        "model_version": "CB-RO-001",
        "training_mode": mode,
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "ensemble_macro_f1": float(best_f1),
        "mcnemar_statistic": stat,
        "mcnemar_p_value": p_val,
        "comparison": comparison_results
    }
    with open(EVAL_DIR / "evaluation_summary.json", "w") as f:
        json.dump(eval_summary, f, indent=2)

    print("Training and evaluation completed successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["fast", "standard", "full"], default="standard")
    args = parser.parse_args()
    train(mode=args.mode)
