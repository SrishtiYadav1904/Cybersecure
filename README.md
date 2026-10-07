# CyberGuard — Multilingual Explainable Cyberbullying Detection and Support System

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10+-brightgreen.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-teal.svg)](https://fastapi.tiangolo.com)
[![Frontend: React](https://img.shields.io/badge/Frontend-React_18-indigo.svg)](https://react.dev)
[![Architecture: AML](https://img.shields.io/badge/AML-PCA_GloVe_%2B_Contextual_%2B_Stacking-purple.svg)](docs/ML_PIPELINE.md)
[![Model Version: CB-EXP-002](https://img.shields.io/badge/Model_Version-CB--EXP--002-success.svg)](data/metadata/model_registry.json)
[![Support Version: SUP-001](https://img.shields.io/badge/Support_Model-SUP--001-orange.svg)](data/metadata/model_registry.json)

CyberGuard is an end-to-end, dynamic production web application and forensic intelligence platform for multilingual, class-wise cyberbullying detection, local token explainability (XAI), concept-drift and slang monitoring, incident timeline preservation, grounded AI wellbeing support, consultant escalation triage, and real-time administrative analytics.

> **Moving to another computer?** Use the setup steps below. Activate the project virtual environment before launching `run.py`; the launcher uses the Python interpreter that starts it.

## Quick Setup (Windows PowerShell)

### Prerequisites

- 64-bit Python 3.13 (the CB-EXP-003 model was trained with Python 3.13.9).
- Node.js 22 LTS/current and npm (Node.js 22.20.0 was used for verification).
- Git, or a copy of the complete project folder.

### 1. Copy the project

Copy the project folder to the other computer. Keep the trained model directory `trained_models/cyberbullying/CB-EXP-003/`; it contains the classifier and PCA artifacts required for inference. The prebuilt model means the external raw training datasets are not required just to run the application.

Do not copy a virtual environment or `frontend/node_modules` from another computer. Do not share a real `.env`, `cyberguard.db`, or `uploads/` folder if they contain secrets or personal evidence. The recipient should create their own `.env` and database.

### 2. Create and activate a virtual environment

Open PowerShell in the project root (the folder containing `run.py`) and run:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -c "import sys; print(sys.executable)"
```

The printed Python path should end in `cyberguard\\.venv\\Scripts\\python.exe`. If PowerShell blocks activation in this terminal, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, then activate again. This only changes policy for the current PowerShell process.

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
npm --prefix frontend install
```

The Python requirements include FastAPI/Uvicorn, the pinned CB-EXP-003 ML libraries, OpenCV, Parquet support, and Pydantic email validation. Screenshot OCR uses optional engines; for the recommended RapidOCR engine, also run:

```powershell
python -m pip install rapidocr-onnxruntime
```

### 4. Configure local settings

Create a local environment file from the example, then edit it before sharing or using beyond a local demo:

```powershell
Copy-Item .env.example .env
```

Set a private random `SECRET_KEY` and change the seeded admin password in `.env`. Never send `.env` to another person or commit it to source control. The demo credentials printed by the launcher are not appropriate for a deployed system.

### 5. Start CyberGuard

With `(.venv)` shown in the PowerShell prompt, run:

```powershell
python run.py
```

The launcher starts both services. Open:

- Frontend: <http://127.0.0.1:5173>
- Backend API docs: <http://127.0.0.1:8000/docs>

On startup, confirm the backend log says it loaded `trained_models\\cyberbullying\\CB-EXP-003`. If it prints an Anaconda or global Python path, stop the process and activate `.venv` before running the launcher.

Press Ctrl+C in the launcher terminal to stop both services.

### Run services in separate terminals (alternative)

Activate `.venv` in the backend terminal, then run:

```powershell
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

In a second terminal, from the project root:

```powershell
npm --prefix frontend run dev
```

### Verify setup

With `.venv` active, check core imports:

```powershell
python -c "import fastapi, uvicorn, sklearn, xgboost, lightgbm, catboost, cv2, pyarrow, email_validator; print('Python dependencies OK')"
```

Run backend tests with:

```powershell
python -m pytest backend/tests/ -v
```

If tests fail during collection with `ModuleNotFoundError`, confirm `.venv` is active and install requirements using `python -m pip install -r requirements.txt`.

### macOS / Linux quick setup

Install Python 3.13, Node.js 22, and npm first. From the project root:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
npm --prefix frontend install
cp .env.example .env
python run.py
```

Change the example secret and admin password in `.env`. Keep the terminal running while using the app; Ctrl+C stops the launcher.

---

## 1. System Vision & Architecture

CyberGuard addresses online toxicity across text, screenshot uploads, and group conversations through a unified multi-stage intelligence pipeline with **strict decoupling between Cyberbullying Detection and Wellbeing Support Intelligence**:

```text
Screenshot / Text / Chat
        ↓
RapidOCR (Deep Learning Text Detection & Recognition)
        ↓
Multilingual Language & Code-Mixing Detection (EN / HI / Hinglish)
        ↓
Unicode Normalization & Slang Token Filtering
        ↓
Feature Fusion: GloVe (100d) -> PCA (30d) + Contextual Semantic (384d) -> Fusion (414d)
        ↓
AML Stacking Ensemble (SVM + XGBoost + LightGBM + CatBoost -> Meta-Logistic Regression)
        ↓
Class-Wise Probabilities (10 CyberGuard Taxonomy Categories)
        ↓
Explainable AI (XAI) Attribution & Salient Offensive Tokens
        ↓
Incident Vault & Chronological Evidence Timeline
        ↓
Dual Wellbeing Path:
  ├── Grounded RAG Support Engine (Official Procedural Guides & Emergency Hotlines)
  ├── SUP-001 Wellbeing Intelligence (Crisis Triage, LoST Distress, Stress Calibration)
  └── Safety Triage (Tele-MANAS 14416 / National Cybercrime Portal 1930 Modal)
```

---

## 2. Core Functional Modules

### 2.1 Multilingual & Class-Wise Detection

- **Languages**: English, Hindi (Devanagari script), and Hinglish (Romanized Hindi code-mixed).
- **10-Class Cyberbullying Taxonomy**:
  1. `Age-based`
  2. `Gender-based`
  3. `Religion-based`
  4. `Ethnicity-based`
  5. `Appearance-based`
  6. `Mockery/Defamation`
  7. `Abusive/Insult`
  8. `Threat/Intimidation`
  9. `Personal Harassment`
  10. `Non-cyberbullying`

### 2.2 Advanced Machine Learning (AML) Engine

- **GloVe Embeddings**: 100-dimensional dense semantic word vectors trained on category prototypes and Devanagari roots.
- **Principal Component Analysis (PCA)**: Low-rank dimensionality reduction from 100d down to 30d, preserving principal semantic variance.
- **Contextual Semantic Encoder**: High-capacity 384-dimensional representation capturing subword morphology, character 3-5 grams, and positional decay.
- **Feature Fusion Matrix**: Concatenation and L2 normalization yielding a unified 414-dimensional feature vector.
- **Stacking Ensemble**:
  - Calibrated Support Vector Machine (`SGDClassifier` with modified Huber loss)
  - Extreme Gradient Boosting (`XGBClassifier`)
  - Lightweight Gradient Boosting (`LGBMClassifier`)
  - Categorical Boosting (`CatBoostClassifier`)
  - Meta-Learner: Calibrated `LogisticRegression` meta-estimator.

### 2.3 Strict Domain Separation & Wellbeing Support (`SUP-001`)

- **Ethical Boundary**: Wellbeing models strictly provide **risk-aware support signals and crisis triage triggers**, NEVER clinical or psychiatric diagnoses.
- **Crisis Triage Model**: CatBoost trained on `Reddit-Crisis-Triage-v1` (1,888 samples) distinguishing acute crisis (`CRISIS_ESCALATION` triggering Tele-MANAS 14416 / 1930) from depressive rumination (`DEPRESSIVE_DISTRESS`).
- **Cognitive Distortion Model**: LightGBM trained on `Reddit-LoST-v1` (3,245 samples) identifying Loss of Self and self-worth erosion following online harassment.
- **Stress Severity Calibrator**: Calibrated classification into `LOW`, `MODERATE`, `HIGH`, `SEVERE`.

---

## 3. Data Architecture & Provenance

CyberGuard enforces a strict three-layer data architecture:

```text
data/
├── raw/            # Original unmodified datasets
├── interim/        # Temporary extraction and staging
├── processed/      # Deduplicated, normalized, and hashed records
├── unified/        # Leakage-safe model-ready Parquet partitions
│   ├── cyberbullying/ (train, validation, test, external_holdout)
│   └── wellbeing/     (train, validation, test, external_holdout)
└── metadata/       # Registries, label mappings, and manifests
```

### Verified External Datasets on Disk

- **`CyberbullyX-63K` (`DS-CB-01`):** 63,145 real social posts (60.7% Hindi/Hinglish, 39.1% English).
- **`Kaggle Cyberbullying Tweets` (`DS-CB-02`):** 47,692 real tweets across 6 balanced classes.
- **`Hinglish Codemixed Dataset` (`DS-CB-03`):** 18,148 real Roman Hindi comments.
- **`Jigsaw Toxic Comment Challenge` (`DS-CB-04`):** 159,571 comments (threat instances extracted).
- **`Reddit Suicide vs Depression` (`DS-WB-04`):** 1,895 posts for crisis triage.
- **`Reddit LoST Suite` (`DS-WB-01`):** 3,251 posts for cognitive distress analysis.
- **`MultiOFF` & `M3 Twitter Memes`:** Real multimodal benchmark memes.

### Quarantined & Barred Datasets

- **`Archive.zip 25K Hinglish` (`DS-CB-11`):** CRITICAL FLAW: Exactly 40 unique template sentences repeated 25,000 times (99.84% duplicate rate). Strictly excluded from all training.
- **`GoEmotions Subset` (`DS-WB-05`):** Disk file `goemotions_1-selected-columns.csv` contains 100% NaN entries (0 valid text entries). Excluded with documented audit finding.

---

## 4. Empirical Evaluation Results

### Baseline (`CB-BASE-001`) vs. Expanded (`CB-EXP-002`)

| Metric                | Baseline (`CB-BASE-001`)                | Expanded (`CB-EXP-002` - PRODUCTION)       |
| :-------------------- | :-------------------------------------- | :----------------------------------------- |
| **Training Corpus**   | `CB-DATA-001` (1,628 synthetic samples) | `CB-DATA-002` (22,497 real social samples) |
| **Accuracy**          | 0.9706                                  | **0.7553**                                 |
| **Macro-F1**          | 0.9711                                  | **0.7081**                                 |
| **Weighted-F1**       | 0.9705                                  | **0.7569**                                 |
| **PR-AUC (Macro)**    | 0.9968                                  | **0.7718**                                 |
| **ROC-AUC (Macro)**   | 0.9996                                  | **0.9523**                                 |
| **English Accuracy**  | 0.9710                                  | **0.7579**                                 |
| **Hindi Accuracy**    | 0.9680                                  | **0.7229**                                 |
| **Hinglish Accuracy** | 0.9720                                  | **0.7609**                                 |

_Key Scientific Insight:_ While synthetic toy benchmarks produce high metric values due to template homogeneity, the expanded real-world model demonstrates genuine, robust generalization across noisy, messy social media discourse in English, Hindi, and Hinglish with an empirical ROC-AUC of 0.9523.

---

## 5. Verification & Acceptance Testing

Run the automated 12-subsystem acceptance test suite:

```bash
python scripts/master_system_acceptance_test.py
```

Output:

```text
==============================================================
   ALL 12 SUBSYSTEM ACCEPTANCE TESTS PASSED WITH 100% SUCCESS
==============================================================
```

---

## 6. Official Resources & Emergency Contacts

CyberGuard maintains official, verified Indian emergency and reporting contacts:

- **Tele-MANAS (Ministry of Health & Family Welfare):** `14416` (24x7 Toll-Free)
- **National Cyber Crime Reporting Portal (I4C / MHA):** `1930` / [cybercrime.gov.in](https://cybercrime.gov.in)
- **KIRAN Mental Health Helpline:** `1800-599-0019`
- **National Commission for Women (NCW) Cyber Cell:** `7827170170`
- **Childline India:** `1098`
- **Vandrevala Foundation:** `+91 9999 666 555`

---

## 7. Documentation Directory

- [`docs/CURRENT_PROJECT_STATE.md`](docs/CURRENT_PROJECT_STATE.md) — Comprehensive repository & physical file reconciliation
- [`docs/DATASET_CATALOG.md`](docs/DATASET_CATALOG.md) — Exhaustive dataset registry & licensing catalog
- [`docs/LABEL_MAPPING.md`](docs/LABEL_MAPPING.md) — Taxonomy normalization & domain isolation specification
- [`docs/DRIFT.md`](docs/DRIFT.md) — Concept drift, PSI, KS tests, and dynamic slang lifecycle
- [`docs/IMPLEMENTATION_STATUS.md`](docs/IMPLEMENTATION_STATUS.md) — Complete phase-by-phase implementation ledger
- [`artifacts/evaluation/baseline_vs_expanded.md`](artifacts/evaluation/baseline_vs_expanded.md) — Dual-model empirical comparison report
