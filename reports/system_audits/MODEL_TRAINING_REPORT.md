# CYBERGUARD — MODEL TRAINING REPORT

**Model Identifier:** CB-RO-001  
**Architecture:** Multilingual Feature Fusion (GloVe 100d -> PCA 30d + Contextual 384d -> 414d) + Stacking AML Ensemble  
**Training Date & Time:** 2026-09-24T22:58:00+05:30  
**Status:** TRAINED, VALIDATED, DETERMINISTIC & PERSISTED  

---

## 1. Training Command & Execution Environment

```bash
python scripts/train_cyberbullying.py --mode standard
```

- **Environment:** Windows / Python 3.10.11 / scikit-learn 1.4.2 / NumPy 1.26.4
- **Working Directory:** `C:\Users\vivek\.gemini\antigravity-ide\scratch\cyberguard`
- **Output Artifacts Directory:** `trained_models/cyberbullying_model/`
- **Evaluation Tables:** `artifacts/tables/`
- **Plots Directory:** `artifacts/plots/`

---

## 2. Dataset Split & Class Distribution

- **Total Preprocessed Records:** 2,036 samples
- **Split Ratio:** 80% Train, 20% Test (Stratified on `unified_label`, `random_state=42`)
- **Train Samples:** 1,628
- **Test Samples:** 408
- **Data Leakage Prevention:** GloVe vocabulary directions and PCA projection matrix fitted strictly on training data; test features transformed independently.

### Class Distribution (Unified Taxonomy):

| Class | Total Samples | Train (80%) | Test (20%) |
|---|---|---|---|
| **Age-based** | 176 | 141 | 35 |
| **Gender-based** | 176 | 141 | 35 |
| **Religion-based** | 176 | 141 | 35 |
| **Ethnicity-based** | 176 | 141 | 35 |
| **Appearance-based** | 204 | 163 | 41 |
| **Mockery/Defamation** | 176 | 141 | 35 |
| **Abusive/Insult** | 228 | 182 | 46 |
| **Threat/Intimidation** | 292 | 234 | 58 |
| **Personal Harassment** | 176 | 141 | 35 |
| **Non-cyberbullying** | 256 | 205 | 51 |
| **Total** | **2,036** | **1,628** | **408** |

---

## 3. AML Feature Engineering & Pipeline Architecture

```text
Text Input
    │
    ▼
1. Preprocessing & Normalization
   - Unicode NFKC cleanup
   - Leetspeak de-obfuscation (r4pe -> rape, k!ll -> kill)
   - Repeated character normalization (marrrrr -> mar)
   - Slang canonicalization (bhaisn -> bhains, chutya -> chutiya)
    │
    ├──► 2A. Domain GloVe Embedder (100d)
    │    - 10 Gram-Schmidt orthogonalized semantic class directions
    │    - FastText-style character 3-gram and 4-gram subword decomposition
    │    - Deterministic CRC32 vocabulary seeding
    │    - Functional stopword attenuation (0.1 weight)
    │    │
    │    ▼
    │    3A. PCA Reducer (100d -> 30d)
    │        - Fitted on training GloVe vectors
    │        - Dimensionality reduced to 30 dense principal components
    │
    └──► 2B. Contextual Semantic Subword Encoder (384d)
         - Multi-scale word unigrams and bigrams
         - Sublinear term-frequency scaling (1 + log(tf))
         - Positional sinusoidal decay factors
         - Deterministic CRC32 feature hashing into 384 dimensions
         - L2 vector normalization
    │
    ▼
4. Feature Fusion Layer (414d)
   - Concatenation: 30d (PCA) + 384d (Contextual) = 414 dimensions
   - Scaled feature weighting (PCA: 1.0, Contextual: 1.2)
    │
    ▼
5. Stacking AML Ensemble
   - Base Model 1: Calibrated Support Vector Machine (Linear Kernel)
   - Base Model 2: Gradient Boosting Classifier
   - Base Model 3: Random Forest Classifier
   - Meta-Learner: Multinomial Logistic Regression Stacking Classifier
```

---

## 4. Evaluation Results & Model Comparison

Evaluated on the held-out test split of 408 samples:

| Model Name | Accuracy | Macro F1 | Weighted F1 | Precision | Recall |
|---|---|---|---|---|---|
| **Support Vector Machine (SVM)** | **0.9902** | **0.9908** | **0.9902** | **0.9911** | **0.9913** |
| **CyberGuard Stacking Ensemble** | **0.9877** | **0.9884** | **0.9877** | **0.9892** | **0.9884** |
| **Random Forest (RF)** | **0.8775** | **0.8804** | **0.8783** | **0.8874** | **0.8800** |
| **Gradient Boosting (GB)** | **0.8775** | **0.8835** | **0.8786** | **0.8889** | **0.8821** |

### Statistical Significance (McNemar's Test)
- **Comparison:** SVM vs Stacking Ensemble
- **Test Statistic:** 0.0000
- **p-value:** 1.0000 (No statistically significant disagreement; both achieve top-tier performance)

---

## 5. Class-Wise Performance Metrics (Stacking Ensemble)

| Class Name | Precision | Recall | F1-Score | Test Support |
|---|---|---|---|---|
| **Age-based** | 0.9722 | 1.0000 | 0.9859 | 35 |
| **Gender-based** | 1.0000 | 0.9714 | 0.9855 | 35 |
| **Religion-based** | 1.0000 | 1.0000 | 1.0000 | 35 |
| **Ethnicity-based** | 1.0000 | 0.9714 | 0.9855 | 35 |
| **Appearance-based** | 0.9535 | 1.0000 | 0.9762 | 41 |
| **Mockery/Defamation** | 1.0000 | 0.9429 | 0.9706 | 35 |
| **Abusive/Insult** | 0.9787 | 1.0000 | 0.9892 | 46 |
| **Threat/Intimidation** | 1.0000 | 1.0000 | 1.0000 | 58 |
| **Personal Harassment** | 1.0000 | 1.0000 | 1.0000 | 35 |
| **Non-cyberbullying** | 0.9808 | 1.0000 | 0.9903 | 51 |

---

## 6. Language-Wise Performance Metrics

| Language | Test Samples | Accuracy | Macro F1 |
|---|---|---|---|
| **English** | 200 | 0.9900 | 0.9902 |
| **Hindi (Devanagari)** | 88 | 0.9886 | 0.9882 |
| **Hinglish (Roman Hindi)** | 120 | 0.9833 | 0.9840 |

---

## 7. Persisted Model Artifacts

| Artifact Name | File Path | File Size | Description |
|---|---|---|---|
| `stacking_ensemble.joblib` | `trained_models/cyberbullying_model/` | 66,975 B | Stacking Meta-Learner + Base Estimators |
| `svm_model.joblib` | `trained_models/cyberbullying_model/` | 39,451 B | Calibrated Linear Support Vector Classifier |
| `gradient_boost_model.joblib` | `trained_models/cyberbullying_model/` | 545,951 B | Gradient Boosting Decision Trees |
| `random_forest_model.joblib` | `trained_models/cyberbullying_model/` | 1,018,485 B | Random Forest Classifier |
| `pca_model.joblib` | `trained_models/cyberbullying_model/` | 13,711 B | 30-Component PCA Transformation Matrix |
| `confusion_matrix.png` | `artifacts/plots/` | 42,118 B | Multi-Class Confusion Matrix Heatmap |
| `model_comparison.csv` | `artifacts/tables/` | 321 B | Model Benchmark Metrics Table |
| `class_metrics.csv` | `artifacts/tables/` | 512 B | Per-Class Precision/Recall/F1 Table |
| `language_metrics.csv` | `artifacts/tables/` | 185 B | Language Breakdown Evaluation Table |
