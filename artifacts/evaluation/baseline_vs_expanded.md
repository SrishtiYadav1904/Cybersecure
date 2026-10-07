# CYBERGUARD — BASELINE VS. EXPANDED MODEL EVALUATION REPORT

**Generated:** 2026-09-25T18:00:00Z  
**Research Standard:** Empirical AML Comparative Verification

---

## 1. EXECUTIVE SUMMARY & EXPERIMENT RESULTS

We evaluated the performance of CyberGuard's Stacking Ensemble when trained on:
1. **Experiment A (Baseline `CB-BASE-001`):** Trained strictly on `CB-DATA-001` (Synthetic Multilingual Baseline, 1,628 training samples).
2. **Experiment B (Expanded `CB-EXP-002`):** Trained on `CB-DATA-002` (Expanded verified real social corpora combining Kaggle Tweets, Hinglish Codemixed, CyberbullyX Hindi stream, Jigsaw threat cases, and Synthetic baseline — 22,497 training samples).

### Primary Comparison Table

| Metric | Baseline (`CB-BASE-001`) | Expanded (`CB-EXP-002`) | Absolute Delta | Relative Gain |
| :--- | :--- | :--- | :--- | :--- |
| **Training Samples** | 1,628 | 22,497 | +20,869 | +1,281% |
| **Accuracy** | 0.9706 | 0.7553 | -0.2153 | -22.18% |
| **Macro-F1** | 0.9711 | 0.7081 | -0.2630 | -27.08% |
| **Weighted-F1** | 0.9705 | 0.7569 | -0.2136 | -22.01% |
| **PR-AUC (Macro)** | 0.9968 | 0.7718 | -0.2250 | -22.57% |
| **ROC-AUC (Macro)** | 0.9996 | 0.9523 | -0.0473 | -4.73% |

---

## 2. MULTI-MODEL AML COMPARISON TABLE (EXPANDED DATASET)

| Model Architecture | Accuracy | Macro-F1 | Weighted-F1 | Precision | Recall | Training Time (s) | Inference (ms/sample) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **SVM** | 0.7148 | 0.7320 | 0.7069 | 0.7680 | 0.7141 | 8.7s | 0.00ms |
| **XGBoost** | 0.7480 | 0.7301 | 0.7435 | 0.8330 | 0.6808 | 16.83s | 0.01ms |
| **LightGBM** | 0.7603 | 0.7079 | 0.7569 | 0.7559 | 0.6786 | 14.16s | 0.03ms |
| **CatBoost** | 0.6518 | 0.4541 | 0.6291 | 0.5148 | 0.4474 | 42.36s | 0.00ms |
| **CyberGuard Stacking Ensemble** | 0.7553 | 0.7081 | 0.7569 | 0.7539 | 0.6760 | 44.0s | 0.04ms |

---

## 3. MULTILINGUAL GENERALIZATION ANALYSIS

| Language | Test Samples | Accuracy | Macro-F1 | Weighted-F1 |
| :--- | :--- | :--- | :--- | :--- |
| **English** | 3143 | 0.7579 | 0.6311 | 0.7715 |
| **Hindi** | 462 | 0.7229 | 0.6134 | 0.7219 |
| **Hinglish** | 1217 | 0.7609 | 0.6206 | 0.7757 |

---

## 4. CROSS-DATASET GENERALIZATION

| Source Dataset | Test Samples | Accuracy | Macro-F1 |
| :--- | :--- | :--- | :--- |
| **Hinglish-Codemixed-18K-v1** | 786 | 0.7532 | 0.1963 |
| **Kaggle-CB-Tweets-v1** | 3042 | 0.7686 | 0.5158 |
| **Synthetic-CyberGuard-v1** | 306 | 0.6307 | 0.6291 |
| **CyberbullyX-63K-v1** | 668 | 0.7740 | 0.1967 |
| **Jigsaw-Toxic-Train-v1** | 20 | 0.1000 | 0.0455 |

---

## 5. LEAKAGE CONTROLS AND METHODOLOGY

1. **Exact-Match Text Deduplication:** Text hashing across all sources eliminated redundant samples before data partitioning.
2. **Quarantine of Mechanically Tiled Data:** `archive.zip` (40 sentences repeated 25,000 times) was permanently excluded from both training and evaluation pools.
3. **Partition Independence:** Train (70%), Validation (15%), and Test (15%) splits were partitioned by text hash to prevent overlapping n-grams or target leakage.
4. **External Holdout:** 4,516 real external records were isolated and never seen during training or validation hyperparameter tuning.

Generated plot artifacts:
- `artifacts/plots/confusion_matrix.png`
- `artifacts/plots/roc_curve.png`
- `artifacts/plots/precision_recall_curve.png`
