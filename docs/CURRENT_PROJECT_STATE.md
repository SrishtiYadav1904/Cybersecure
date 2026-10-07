# CYBERGUARD — CURRENT PROJECT STATE AUDIT & RECONCILIATION

**Audit Timestamp:** 2026-09-25T17:20:00Z  
**Phase:** Phase 0 Baseline Reconciliation  
**Lead Roles:** AI/ML Engineer, Data Engineer, Backend Engineer, Technical Architect  
**Compliance Standard:** Mandatory Source Verification, Zero-Fabrication Integrity, Non-Destructive Preservation  

---

## 1. Executive System Overview

CyberGuard is an end-to-end, multilingual, explainable cyberbullying detection and AI-assisted wellbeing support system targeting **English, Hindi (Devanagari), and Hinglish (Code-Mixed Romanized Hindi)**.

The system is organized into modular tiers:
```text
Screenshot / Text / Chat
        ↓
RapidOCR (DBNet + SVTR ONNX Engine)
        ↓
Language Detection & Normalization (Slang/Phonetics)
        ↓
Feature Engineering (GloVe 100d -> PCA 30d + Contextual 384d = 414d Text)
        ↓
Visual Encoder (Quadrant Color 64d + Gradients 32d + DCT 32d = 128d Visual)
        ↓
Multimodal Gated Feature Fusion (542d)
        ↓
AML Stacking Ensemble (Calibrated SVM + Gradient Boosting + Random Forest -> Meta-LogReg)
        ↓
10-Class Cyberbullying Classification + Token Explainability + Severity Triage
        ↓
Support Engine (Emotion/Stress Signals + Grounded RAG + Safety Rules + Hotline Triage)
        ↓
Incident Management & Forensic PDF Generation
        ↓
Admin Analytics & Concept Drift Monitoring
```

---

## 2. Reconciliation of September 25 Dataset Audit with Physical Files

The September 25 audit reported baseline inventory figures across three source locations. We have independently reconciled every physical file on disk:

### Summary of Physical Records
* **Discovered Records on Disk:** **514,754 records** across 20 distinct files/archives.
* **External Real Records:** **487,648 records** (484,884 text + 2,764 multimodal).
* **Synthetic Records:** **27,106 records** (2,036 multilingual baseline + 70 support prompts + 25,000 tiled variants).
* **Excluded Synthetic Tiling:** `archive.zip::hinglish_cyberbullying_dataset_25000.csv` (25,000 rows generated from **only 40 unique template sentences repeated ~1,000 times each**). Formally quarantined and excluded from all model training.

### Inventory Reconciliation Table

| Dataset Identifier | Physical File Path | Format | Physical Records | External / Synthetic | Current Pipeline Role |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`CyberbullyX-63K`** | `C:\Users\vivek\Documents\aml\cyberbullying_dataset\CyberbullyX-63K.xlsx` | Excel | 63,145 | Real External | **Staged for Expansion** (38k Hindi, 24k English) |
| **`Kaggle CB Tweets`** | `C:\Users\vivek\Documents\aml\cyberbullying_dataset\kaggledataset.zip` | Zip (CSV) | 47,692 | Real External | **Staged for Expansion** (Direct 5-class match) |
| **`Hinglish 18K (Paper 4989)`** | `C:\Users\vivek\Documents\aml\cyberbullying_dataset\final_dataset_hinglish.csv` | CSV | 18,148 | Real External | **Staged for Expansion** (17k unique Hinglish insults) |
| **`Jigsaw Toxicity (Train)`** | `C:\Users\vivek\Documents\aml\cyberbullying_dataset\archive (1).zip` | Zip (CSV) | 159,571 | Real External | **Staged for Expansion** (Multi-label toxicity/threat) |
| **`Jigsaw Toxicity (Test)`** | `C:\Users\vivek\Documents\aml\cyberbullying_dataset\archive (1).zip` | Zip (CSV) | 153,164 | Real External | **Evaluation Holdout** |
| **`MultiOFF Memes`** | `data/external/multioff/multioff_catalog.csv` | CSV + Images | 740 (740 imgs) | Real External | **Active in Production** (`CB-MM-001`) |
| **`M3 Twitter Memes`** | `data/external/m3/m3_catalog.csv` | CSV + Images | 526 (150 imgs) | Real External | **Active in Production** (`CB-MM-001`) |
| **`Facebook Hateful Memes`** | `data/external/hateful_memes/hateful_memes_catalog.csv` | CSV + Images | 500 (150 imgs) | Real External | **Strict Real-World External Holdout (Set B)** |
| **`Zenodo Toxic Memes`** | `data/external/zenodo_toxic_memes/labels.csv` | CSV | 1,998 | Real External | **Auxiliary Only** (Russian/Cyrillic out-of-scope) |
| **`Synthetic CyberGuard`** | `data/raw/cyberbullying_multilingual_raw.csv` | CSV | 2,036 | Synthetic | **Active Baseline** (`CB-RO-001` / `CB-MM-001`) |
| **`Synthetic Support Prompts`** | `data/raw/support_wellbeing_raw.csv` | CSV | 70 | Synthetic | **Active Support Baseline** |
| **`Reddit LoST v1`** | `C:\Users\vivek\Documents\aml\mental\LoSTv1.csv` | CSV | 3,251 | Real External | **Staged for Wellbeing Support Model** |
| **`Reddit LoST Train Split`** | `C:\Users\vivek\Documents\aml\mental\final_train.csv` | CSV | 1,739 | Real External | **Staged for Wellbeing Support Model** |
| **`Reddit LoST Test Split`** | `C:\Users\vivek\Documents\aml\mental\final_test.csv` | CSV | 435 | Real External | **Staged for Wellbeing Support Evaluation** |
| **`Reddit Suicide vs Depression`**| `C:\Users\vivek\Documents\aml\mental\combined-set.csv` | CSV | 1,895 | Real External | **Staged for Emergency Crisis Escalation Model** |
| **`GoEmotions Subset`** | `C:\Users\vivek\Documents\aml\mental\goemotions_1-selected-columns.csv` | CSV | 21,039 | Real External | **Staged for Affective / Empathetic Support RAG** |
| **`Sample Data 1 (Reddit)`** | `C:\Users\vivek\Documents\aml\mental\sample_data_1.xlsx` | Excel | 96 | Real External | **Unit Test Sample** |
| **`Sample Data 2 (Twitter)`** | `C:\Users\vivek\Documents\aml\mental\sample_data_2.xlsx` | Excel | 96 | Real External | **Unit Test Sample** |
| **`PolEval 2019`** | N/A (Referenced in literature) | N/A | 0 | External Ref. | **NOT FOUND LOCALLY** (Polish out-of-scope) |
| **`archive.zip::hinglish_25k`** | `C:\Users\vivek\Documents\aml\cyberbullying_dataset\archive.zip` | Zip (CSV) | 25,000 | Synthetic Tiled | **QUARANTINED / EXCLUDED** (40 templates tiled) |

---

## 3. Existing Models & Training Artifacts

The repository currently maintains three model directories in `trained_models/`:

### A. Cyberbullying Baseline Model (`trained_models/cyberbullying_model/`)
* **Model Version:** `CB-RO-001` / `CB-MM-001`
* **Artifacts on Disk:**
  - `stacking_ensemble.joblib` (5.25 MB): Fused StackingClassifier (LinearSGD, GradientBoosting, RandomForest -> LogisticRegression).
  - `gradient_boost_model.joblib` (920 KB)
  - `random_forest_model.joblib` (1.63 MB)
  - `svm_model.joblib` (75 KB)
  - `pca_model.joblib` (13.7 KB)
  - `classes.json`: 10 unified classes.
* **Input Features:** 542 dimensions (414d text + 128d visual, supports zero-gating for `TEXT_ONLY` and `IMAGE_ONLY`).
* **Current Training Data:** Ingested pool of 3,284 unique records (2,036 synthetic baseline + 740 MultiOFF + 508 M3 Twitter).

### B. Multimodal Model Sandbox (`trained_models/multimodal_model/`)
* Identical checkpoint mirror of the multimodal stacking ensemble with full ablation metadata.

### C. Support Baseline Model (`trained_models/support_model/`)
* **Artifacts on Disk:**
  - `stress_classifier.joblib` (1.2 MB): SGD/SVM classifier predicting stress severity (`LOW`, `MODERATE`, `HIGH`, `SEVERE`).
  - `model_config.json`: Feature and threshold configurations.
* **Current Training Data:** 70 synthetic stress prompts in `data/raw/support_wellbeing_raw.csv`.

---

## 4. Existing Backend APIs (`backend/app/api/`)

The FastAPI application provides 7 comprehensive API routers:

1. **Authentication (`api/auth.py`):**
   - `POST /api/auth/register`, `POST /api/auth/token`, `GET /api/auth/me`.
   - JWT tokens, bcrypt password hashing, RBAC (`USER`, `CONSULTANT`, `ADMIN`).
2. **Analysis & Detection (`api/analyze.py`):**
   - `POST /api/analyze/text`: Direct comment classification with GloVe/PCA/RoBERTa/Stacking and XAI.
   - `POST /api/analyze/image`: Multi-stage OCR upload; returns extracted text and confidence for user review.
   - `POST /api/analyze/confirm-image`: Multimodal classification combining user-verified text and 128d visual embeddings.
   - `POST /api/analyze/chat`: Conversation-level harassment analysis (identifying targeted victims and aggressors).
3. **Incidents Management (`api/incidents.py`):**
   - `GET /api/incidents`, `POST /api/incidents`, `GET /api/incidents/{id}`, `PATCH /api/incidents/{id}/status`.
4. **Forensic Reports (`api/reports.py`):**
   - `POST /api/reports/generate/{incident_id}`: Compiles cryptographic SHA-256 evidence chain and generates ReportLab PDF.
   - `GET /api/reports/download/{id}`.
5. **Support & Wellbeing (`api/support.py`):**
   - `POST /api/support/message`: Grounded RAG wellbeing assistant, emergency hotline triggers, and session memory.
6. **Consultant Help Requests (`api/help_requests.py`):**
   - `POST /api/help-requests`: Secure case referral for victim escalation.
7. **Admin Monitoring & Analytics (`api/admin.py`):**
   - `GET /api/admin/metrics`, `GET /api/admin/drift`, `GET /api/admin/slang`, `POST /api/admin/slang/{id}/approve`.

---

## 5. Existing Database Schema (`cyberguard.db`)

SQLite database managed via SQLAlchemy (`backend/app/database/models.py`):
* `users`
* `incidents`
* `evidence`
* `messages`
* `predictions`
* `reports`
* `support_sessions`
* `support_messages`
* `help_requests`
* `slang_terms`
* `drift_events`
* `resources`
* `model_versions`

---

## 6. Existing Frontend Features (`frontend/src/`)

React + Vite dynamic dashboard:
* **User Portal:** Comment analyzer, screenshot upload modal with OCR preview/edit, chat timeline analyzer, incident case log, support chat with empathetic RAG, and helpline directory.
* **Consultant Portal:** Case triage queue, severity indicators, evidence timeline, victim assistance notes.
* **Admin Portal:** Drift metrics charts, slang approval queue, model version selector, system health metrics.

---

## 7. Known Issues & Gaps Addressed by This Extension

1. **Unexploited External Cyberbullying Corpora:** Over 288,000 real records (`CyberbullyX-63K`, `cyberbullying_tweets.csv`, `final_dataset_hinglish.csv`, Jigsaw) are present on the local filesystem in `C:\Users\vivek\Documents\aml\cyberbullying_dataset` but have not yet been integrated into the versioned CyberGuard training pipeline.
2. **Support Intelligence Gap:** The support model in `trained_models/support_model/` was trained on only 70 synthetic prompts, while rich external corpora (`LoSTv1.csv`, `combined-set.csv`, `goemotions`) exist in `C:\Users\vivek\Documents\aml\mental` waiting to be leveraged for stress, distress, and empathetic support signals.
3. **Dual-Model Separation:** Need to formally decouple the Cyberbullying model family (`trained_models/cyberbullying/`) from the Wellbeing support model family (`trained_models/support/`) to maintain strict medical/ethical boundaries.
4. **Comparative Baseline vs. Expanded Evaluation:** Must run a rigorous head-to-head evaluation (`CB-BASE-001` vs. `CB-EXP-002`) to empirically measure whether expanding with external data improves real-world generalization across English, Hindi, and Hinglish.

---

## 8. Recommended Next Steps (Phased Execution)

1. **Phase 1:** Build the comprehensive `docs/DATASET_CATALOG.md` and `data/metadata/dataset_registry.json`.
2. **Phase 2 & 3:** Ingest and stage verified datasets into `data/raw/` and `data/interim/`, establishing the 3-layer data architecture.
3. **Phase 4 & 5:** Formalize `label_mapping.json`, `docs/LABEL_MAPPING.md`, and versioned dataset manifests (`CB-DATA-001`, `CB-DATA-002`, `WB-DATA-001`).
4. **Phase 6:** Construct model-ready Parquet partitions in `data/unified/cyberbullying/` and `data/unified/wellbeing/`.
5. **Phase 7 & 8:** Train `CB-BASE-001` (Baseline) and `CB-EXP-002` (Expanded) models with full AML stacking pipelines.
6. **Phase 9:** Generate empirical `baseline_vs_expanded.md` evaluation report.
7. **Phase 10:** Train and evaluate the separate `SUP-001` Wellbeing Support model.
8. **Phase 11-14:** Wire models to FastAPI endpoints, verify database tracking, test end-to-end, and update all system documentation.
