# CyberGuard Machine Learning Training & Artifact Audit (Initial State)

**Audit Date:** 2026-09-24T20:51:00+05:30  
**Auditor:** Lead AI/ML Auditor  
**System Evaluated:** CyberGuard Multilingual Cyberbullying Detection System  
**Verdict:** **DEFICIENT / PARTIALLY IMPLEMENTED (FAILED AUDIT)**  
The existing system relies on a synthetic 216-sample seed prototype dataset, yielding ~15% test accuracy on raw model outputs, which was masked during inference by heuristic keyword-matching rules in `ml/inference/pipeline.py`. A genuinely robust, production-trained cyberbullying model does NOT currently exist on disk.

---

## 1. Datasets Actually Present on Disk

| Dataset Identifier | Actual Filename on Disk | Absolute / Relative Path | Actual Record Count | Source & Provenance | Disk Size |
|---|---|---|---|---|---|
| `cyberbullying_multilingual` | `cyberbullying_multilingual_raw.csv` | `data/raw/cyberbullying_multilingual_raw.csv` | **216 records** | Synthetic seed expansion (36 unique base statements × 6 modifier prefixes) | 26,043 bytes |
| `support_wellbeing` | `support_wellbeing_raw.csv` | `data/raw/support_wellbeing_raw.csv` | **200 records** | Synthetic seed expansion (8 unique statements × 25 repetitions) | 15,827 bytes |
| `unified_dataset` | `unified_dataset.csv` | `data/unified/unified_dataset.csv` | **216 records** | Preprocessed output of `cyberbullying_multilingual_raw.csv` | 51,873 bytes |
| `DAIC-WOZ` | N/A | N/A | **0 records** | **NOT IMPLEMENTED / EXCLUDED** (Restricted clinical dataset) | 0 bytes |

---

## 2. Actual Dataset Label Distribution

### Raw Cyberbullying Dataset (`data/raw/cyberbullying_multilingual_raw.csv` - 216 records)
* **Non-cyberbullying:** 54 records (25.0%)
* **Abusive/Insult:** 18 records (8.3%)
* **Appearance-based:** 18 records (8.3%)
* **Threat/Intimidation:** 18 records (8.3%)
* **Religion-based:** 18 records (8.3%)
* **Ethnicity-based:** 18 records (8.3%)
* **Gender-based:** 18 records (8.3%)
* **Age-based:** 18 records (8.3%)
* **Mockery/Defamation:** 18 records (8.3%)
* **Personal Harassment:** 18 records (8.3%)

**Language Breakdown (Declared vs Detected):**
* **English:** 72 records declared (92 detected by langdetect)
* **Hindi (Devanagari):** 72 records declared (72 detected)
* **Hinglish (Roman Script):** 72 records declared (52 detected as Hinglish/code-mixed)

---

## 3. Actual Train / Validation / Test Split

* **Split Strategy:** Stratified 80/20 train/test split (no separate validation split).
* **Train Samples:** **160 samples** (average 16 samples per class).
* **Test Samples:** **40 samples** (average 4 samples per class).
* **Validation Split:** **NOT IMPLEMENTED** (no separate validation set or k-fold CV log on disk).

---

## 4. Actual Preprocessing Pipeline

* **Script:** `ml/preprocessing/normalizer.py`
* **Operations Executed:**
  - URL removal (`https?://\S+|www\.\S+`)
  - Mention normalization (`@username` -> `@user`)
  - Contraction expansion (`don't` -> `do not`, etc.)
  - Hindi Devanagari character preservation (`\u0900-\u097F`)
  - Obfuscation character collapse (`f***` -> `f`, repeated character deduplication)
  - Lowercasing and whitespace normalization
* **Status:** **IMPLEMENTED** (Preprocessing code functions correctly).

---

## 5. Actual Embedding Model

* **File:** `ml/feature_engineering/glove_embedder.py`
* **Status:** **SIMULATED / NOT GENUINELY TRAINED**
* **Finding:** Rather than loading authentic 6-billion token pre-trained GloVe embeddings (`glove.6B.100d.txt`), the class initializes a hardcoded 40-word seed dictionary and generates random standard-normal vectors (`np.random.randn(len(seed_words), 100)`) with seed `42`. Out-of-vocabulary words are mapped via a deterministic PRNG hash (`hash(word) % 1000000`). It does NOT represent real word semantic geometry.

---

## 6. Actual Contextual Semantic Encoder

* **File:** `ml/feature_engineering/context_encoder.py`
* **Status:** **FALLBACK HASHING / NOT PRE-TRAINED TRANSFORMER**
* **Finding:** Offline environment lacks downloaded weights for `roberta-base`. The class catches the `ImportError`/`OSError` and falls back to `_deterministic_context_vector`, which hashes unigrams, bigrams, and character trigrams into a 384-dimensional vector. While mathematically deterministic, it is not a trained neural language model.

---

## 7. Actual PCA Dimensionality Reduction

* **File:** `ml/feature_engineering/pca_reducer.py`
* **Saved Artifact:** `trained_models/cyberbullying_model/pca_model.joblib` (13,695 bytes)
* **Metadata:** `trained_models/cyberbullying_model/pca_metadata.json` (916 bytes)
* **Input Dimension:** 100d (from GloVeEmbedder)
* **Output Dimension:** 30d
* **Fitted Status:** **FITTED on 160 synthetic training samples**.
* **Variance Explained:** 0.6179 (61.8% cumulative variance across 30 components).

---

## 8. Actual Classifier Fitting & Ensemble Fitting

* **File:** `ml/models/classifier.py`
* **Saved Artifacts:**
  - `svm_model.joblib` (40,477 bytes) — CalibratedClassifierCV over SGDClassifier (`modified_huber`)
  - `gradient_boost_model.joblib` (272,008 bytes) — GradientBoostingClassifier (n_estimators=25, max_depth=3)
  - `random_forest_model.joblib` (143,705 bytes) — RandomForestClassifier (n_estimators=30, max_depth=6)
  - `stacking_ensemble.joblib` (913,763 bytes) — StackingClassifier with LogisticRegression meta-learner
  - `classes.json` (566 bytes) — 10 target classes
* **Training Date/Time:** `2026-09-24 20:17:06`
* **Exact Command Used:**
  ```powershell
  python scripts/train_cyberbullying.py --mode fast
  ```
* **Fitted Status:** **FITTED, BUT SEVERELY UNDERFITTED DUE TO INSUFFICIENT DATA (160 samples)**.

---

## 9. Actual Evaluation Metrics on Disk

Extracted directly from `artifacts/evaluation/evaluation_summary.json` and `artifacts/tables/model_comparison.csv`:

| Model Architecture | Accuracy | Macro F1 | Weighted F1 | Precision | Recall |
|---|---|---|---|---|---|
| Support Vector Machine (SVM) | **0.1500** (15.0%) | **0.2000** | 0.1500 | 0.2000 | 0.2000 |
| Gradient Boosting (GB) | **0.1500** (15.0%) | **0.2000** | 0.1500 | 0.2000 | 0.2000 |
| Random Forest (RF) | **0.1500** (15.0%) | **0.2000** | 0.1500 | 0.2000 | 0.2000 |
| **CyberGuard Stacking Ensemble** | **0.1500** (15.0%) | **0.2000** | 0.1500 | 0.2000 | 0.2000 |

* **McNemar's Test Statistic:** `0.0000`, p-value = `1.0000` (no statistically significant difference between base models and ensemble because sample size is tiny).

---

## 10. The Critical Flaw: Heuristic Rule Overrides in Inference

In `ml/inference/pipeline.py` (lines 98–142), the inference engine circumvented the model's actual output:

```python
# Discovered in ml/inference/pipeline.py:
if any(w in lower_text for w in ["ugly", "fat", "pig", "face", "shame", "body"]):
    idx = self.classifier.class_to_idx.get("Appearance-based", 4)
    probs[idx] = max(probs[idx], 0.78)
elif any(w in lower_text for w in ["bitch", "slut", "whore", "randi", "girl", "woman"]):
    idx = self.classifier.class_to_idx.get("Gender-based", 1)
    probs[idx] = max(probs[idx], 0.82)
...
if not has_abusive_token:
    predicted_class = "Non-cyberbullying"
    probs[idx_non] = max(probs[idx_non], 0.85)
```

**Audit Assessment:** The actual machine learning model failed to generalize (15% accuracy), and the inference pipeline used hardcoded keyword overrides to fake high-confidence classifications. **This violates core requirements and must be completely removed.**

---

## 11. Component Implementation Status Matrix

| Component | Status | Evidence / Notes |
|---|---|---|
| Raw Cyberbullying Dataset | **DEFICIENT** | Only 216 synthetic rows present on disk. |
| Raw Support Wellbeing Dataset | **DEFICIENT** | Only 200 synthetic rows present on disk. |
| Text Preprocessing Pipeline | **IMPLEMENTED** | `ml/preprocessing/normalizer.py` properly strips URLs, normalizes mentions, handles Devanagari. |
| GloVe Word Vector Embedder | **SIMULATED** | Seed dictionary with random Gaussian vectors; not real GloVe 6B corpus. |
| Contextual Semantic Encoder | **FALLBACK** | Subword n-gram hashing fallback used in lieu of loaded transformer weights. |
| PCA Dimensionality Reducer | **IMPLEMENTED** | Scikit-learn PCA fitted to 30 components on synthetic training split. |
| Feature Fusion Layer | **IMPLEMENTED** | Concatenates 30d PCA + 384d context vector -> 414d feature representation. |
| AML Classifier Suite | **FITTED (DEGRADED)** | Models exist on disk but achieved only 15% accuracy due to 160-sample training size. |
| Stacking Ensemble | **FITTED (DEGRADED)** | Meta-learner exists but mirrors the 15% base accuracy. |
| True Model Inference | **NOT IMPLEMENTED** | Masked by keyword heuristic overrides in `ml/inference/pipeline.py`. |
| Server-Side RBAC | **PARTIALLY IMPLEMENTED** | Route guards exist in `dependencies.py` but need audit against all endpoints. |
| Forensic PDF Reporting | **DEFICIENT** | Missing cryptographic file hashes, full OCR dumps, and provenance validation. |

---

## 12. Corrective Action Plan

1. **Purge Heuristic Overrides:** Delete lines 98–142 in `ml/inference/pipeline.py` so that all classifications, probability vectors, and confidences stem purely from the trained model's `predict_proba`.
2. **Ingest Substantial Multilingual Dataset:** Expand dataset from 216 rows to 1,200+ rich, authentic samples covering all 10 unified classes across English, Hindi (Devanagari), and Hinglish (Roman script), including nuanced slang, slurs, threats, mockery, and genuine non-abusive communication.
3. **Upgrade Feature Representations:** Enhance `GloVeEmbedder` with an authentic 500+ token domain vocabulary and `ContextualEncoder` with multi-scale subword n-gram TF-IDF frequency representations.
4. **Re-Train & Evaluate Classifiers:** Fit SVM, Random Forest, Gradient Boosting, and Stacking Ensemble on the full dataset with a genuine stratified split; evaluate metrics and save actual model artifacts.
5. **Mandatory 30+ Case Benchmark:** Execute the required benchmark script logging input text, predicted class, probability distribution, confidence, and model version.
6. **Enforce Strict RBAC & Forensic Provenance:** Verify 403 Forbidden enforcement on user roles and embed SHA-256 evidence hashes in reports.
