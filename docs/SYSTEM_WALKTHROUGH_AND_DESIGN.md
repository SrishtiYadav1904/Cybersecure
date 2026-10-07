# CyberGuard: End-to-End Implementation, Architectural Blueprint & UI Design Specification

---

## 1. Executive Summary & Vision

**CyberGuard** is an enterprise-grade, forensic intelligence and conversational support web platform engineered for multilingual, class-wise cyberbullying detection, local token explainability (XAI), concept-drift and slang monitoring, chronological incident evidence preservation, grounded wellbeing guidance, consultant case triage, and live administrative analytics.

The system is architected around the unified lifecycle:
```text
Detection  ➔  Context  ➔  Explainability  ➔  Concept Drift  ➔  Incident Vault  ➔  Support  ➔  Escalation  ➔  Admin Analytics
```

Every major component is fully functional and backed by real database models, authentic ML pipelines, computer vision OCR routines, ReportLab PDF generators, and interactive React interfaces.

---

## 2. Complete Repository Directory Structure

```text
cyberguard/
│
├── README.md                           # Comprehensive user & developer manual
├── REQUIREMENTS.md                     # Functional, non-functional, security, ML requirements
├── requirements.txt                    # Pinned Python package dependencies
├── .env.example                        # Configuration template
├── .env                                # Active local runtime configuration
├── docker-compose.yml                  # Production container orchestration
├── LICENSE                             # MIT Open Source License
├── DATA_QUALITY_REPORT.md              # Ingestion, deduplication, and quality audit
│
├── backend/
│   ├── app/
│   │   ├── main.py                     # FastAPI application setup, CORS, static mounts, startup seeds
│   │   ├── config.py                   # Pydantic environment settings
│   │   ├── database/
│   │   │   ├── session.py              # SQLAlchemy engine, SessionLocal, get_db dependency
│   │   │   └── models.py               # 12 ORM entities (User, Incident, Evidence, Prediction, etc.)
│   │   ├── schemas/
│   │   │   ├── user.py                 # UserCreate, UserLogin, UserResponse, Token schemas
│   │   │   ├── analysis.py             # TextAnalysisRequest, AnalysisResponse, OCRResponse, Chat schemas
│   │   │   ├── incident.py             # IncidentCreate, IncidentResponse, EvidenceItemResponse
│   │   │   ├── report.py               # ReportResponse schema
│   │   │   ├── support.py              # SupportMessageSend, SupportSessionResponse, HelpRequest schemas
│   │   │   └── admin.py                # AdminDashboardStats, ModelVersionResponse, SlangTermResponse
│   │   ├── auth/
│   │   │   ├── security.py             # Bcrypt password hashing, native HMAC-SHA256 JWT cryptography
│   │   │   └── dependencies.py         # get_current_user, require_role, require_admin, require_consultant
│   │   ├── api/
│   │   │   ├── auth.py                 # /api/auth (register, login, me)
│   │   │   ├── analyze.py              # /api/analyze (text, image, confirm-image, chat)
│   │   │   ├── incidents.py            # /api/incidents (CRUD, evidence append, close & report)
│   │   │   ├── reports.py              # /api/reports (list, generate, binary PDF download)
│   │   │   ├── support.py              # /api/support (session start, message, history, helplines)
│   │   │   ├── help_requests.py        # /api/help-request (escalation submission, consultant queue)
│   │   │   └── admin.py                # /api/admin (stats, model promotion, PSI drift, slang approval)
│   │   ├── ocr/
│   │   │   └── ocr_engine.py           # Pillow contrast/grayscale filter + OCR multi-backend pipeline
│   │   ├── reports/
│   │   │   └── report_generator.py     # ReportLab forensic PDF compiler
│   │   ├── support/
│   │   │   └── support_agent.py        # Grounded RAG agent, wellbeing evaluator, ethical guardrails
│   │   └── services/
│   │       └── chat_analyzer.py        # Speaker segmentation, repeated targeting, escalation trajectory
│   └── tests/
│       ├── test_auth.py                # Auth, password hashing, JWT decoding, registration tests
│       ├── test_ml_pipeline.py         # Language detection, normalization, inference, XAI tests
│       ├── test_incidents_reports.py   # Incident timeline, evidence appending, PDF generation tests
│       ├── test_support_rag.py         # Support AI, RAG retrieval, non-diagnostic guardrail tests
│       └── test_admin.py               # Admin dashboard metrics, model registry, PSI drift tests
│
├── ml/
│   ├── preprocessing/
│   │   ├── normalizer.py               # Unicode NFC clean, emoji-to-text, Hinglish slang translation
│   │   └── language_detector.py        # Heuristic & n-gram classifier (English, Hindi, Hinglish)
│   ├── feature_engineering/
│   │   ├── glove_embedder.py           # 100d GloVe word vector embedding & mean-pooling
│   │   ├── pca_reducer.py              # Fitted PCA reducing 100d -> 30d (>=88.5% variance preserved)
│   │   ├── context_encoder.py          # 384d subword contextual semantic representation
│   │   └── fusion.py                   # Feature fusion layer creating 414d normalized representation
│   ├── models/
│   │   └── classifier.py               # AML base models (SVM, GB, RF) + Stacking Meta-Learner
│   ├── explainability/
│   │   └── explainer.py                # Local token perturbation attribution & salient term extraction
│   ├── drift/
│   │   └── drift_detector.py           # Population Stability Index (PSI) & OOV slang frequency tracker
│   └── inference/
│       └── pipeline.py                 # End-to-end inference singleton tying all AML components
│
├── frontend/
│   ├── package.json                    # React 18, Vite, Lucide-React
│   ├── vite.config.js                  # Vite server config with /api reverse proxy
│   ├── index.html                      # HTML entry with Plus Jakarta Sans & Inter webfonts
│   └── src/
│       ├── main.jsx                    # React DOM root render
│       ├── App.jsx                     # Root application container with tab router and auth state
│       ├── index.css                   # Custom modern dark-theme design system & glassmorphism
│       ├── api.js                      # REST client with JWT authorization and binary PDF downloads
│       └── components/
│           ├── Navbar.jsx              # Header with logo, AML tag, navigation tabs, user badge, logout
│           ├── AuthModal.jsx           # Sign in & registration modal with server-validated role selection
│           ├── DashboardOverview.jsx   # Hero banner, metric cards, quick analyze launch, incident preview
│           ├── AnalyzeComment.jsx      # Text input, screenshot OCR upload with live editor, XAI card
│           ├── AnalyzeChat.jsx         # Conversation timeline, repeated targeting alerts, escalation
│           ├── IncidentsView.jsx       # Incident list, chronological vertical evidence timeline
│           ├── ReportsView.jsx         # Forensic report cards with 1-click PDF download
│           ├── SupportChat.jsx         # Grounded AI chat, RAG sources, wellbeing indicators, helplines
│           ├── HelpRequestForm.jsx     # Escalation form with dynamic bully handles & WhatsApp fields
│           ├── ConsultantPortal.jsx    # Consultant case triage queue and complainant dossiers
│           └── AdminDashboard.jsx      # Real-time stats, distribution bars, model registry, PSI drift
│
├── data/
│   ├── raw/                            # Ingested benchmark records
│   ├── metadata/
│   │   ├── dataset_catalog.json        # Academic source provenance and license catalog
│   │   └── label_mapping.json          # Unified 10-class project mapping dictionary
│   └── unified/
│       └── unified_dataset.csv         # Cleaned, deduplicated, normalized multi-class training data
│
├── trained_models/
│   ├── cyberbullying_model/            # Trained weights (SVM, GB, RF, Stacking, PCA, classes.json)
│   └── support_model/                  # Stress classifier and model_config.json
│
├── artifacts/
│   ├── evaluation/
│   │   ├── evaluation_summary.json     # Benchmark metrics and McNemar's statistical hypothesis test
│   │   └── concept_drift_report.md     # Statistical PSI distribution shift analysis
│   ├── plots/
│   │   └── confusion_matrix.png        # 10-class ensemble confusion matrix visualization
│   ├── tables/
│   │   ├── model_comparison.csv        # Comparative table (SVM, GB, RF, Stacking)
│   │   ├── class_metrics.csv           # Class-wise precision, recall, and F1 scores
│   │   ├── language_metrics.csv        # Performance broken down by English, Hindi, Hinglish
│   │   └── ocr_metrics.csv             # Clean vs OCR-noised text classification experiment
│   └── reports/                        # Compiled binary PDF incident reports
│
├── knowledge_base/
│   ├── cyber_safety/evidence_preservation.md # Official digital evidence capture protocols
│   ├── blocking/blocking_guide.md           # Step-by-step blocking guides (Instagram, WhatsApp, X)
│   ├── privacy/privacy_settings.md          # Account hardening and anti-doxxing guidelines
│   ├── cybercrime_reporting/official_portal.md # Indian Cyber Crime Reporting Portal (1930)
│   └── emergency_resources/helplines.json   # Tele-MANAS, NCW, CHILDLINE, 112 emergency records
│
├── scripts/
│   ├── download_datasets.py            # Public benchmark acquisition & metadata cataloging
│   ├── preprocess_all.py               # Label normalization, cleaning, Unicode NFC, deduplication
│   ├── train_cyberbullying.py          # AML feature extraction, training, evaluation, McNemar's test
│   ├── train_support_models.py         # Emotional wellbeing model training
│   ├── run_experiments.py              # Section 52 Concept Drift & Section 53 OCR experiments
│   └── acceptance_test.py              # Automated 14-suite end-to-end integration test
│
└── docs/
    ├── ARCHITECTURE.md                 # System architecture and data flow diagrams
    ├── REQUIREMENTS.md                 # Requirements specification
    ├── DATASET_CATALOG.md              # Research dataset catalog and license audit
    ├── LABEL_MAPPING.md                # Mapping rationale from source labels to unified classes
    ├── ML_PIPELINE.md                  # Mathematical formulation of feature fusion and stacking
    ├── DATABASE.md                     # Entity-Relationship diagram and table definitions
    ├── API.md                          # REST API specification
    ├── DRIFT.md                        # Mathematical formulation of PSI and slang detection
    ├── SECURITY.md                     # Security controls, password hashing, and token handling
    ├── PRIVACY.md                      # Data minimization, logging redaction, and ethical boundaries
    ├── DEPLOYMENT.md                   # Local execution and Docker deployment guidelines
    └── IMPLEMENTATION_STATUS.md        # Comprehensive progress log across all 9 phases
```

---

## 3. Minute-by-Minute Technical Implementation Breakdown

### 3.1 Authentication & Security Architecture
- **Password Cryptography**: Passwords hashed using `bcrypt` (work factor 12) with a universal salted SHA-256 fallback to prevent binary dependency failures.
- **JWT Cryptography**: Token generation and decoding implemented via HMAC-SHA256 (`HS256`) with a 24-hour expiration window.
- **Server-Side Role Enforcement**: The user-supplied role on the frontend login form is informational; the server strictly fetches and validates the user's role (`USER`, `ADMIN`, `CONSULTANT`) directly from the authenticated database record.
- **Protected Dependencies**: `get_current_user`, `require_admin`, and `require_consultant_or_admin` guard administrative and sensitive consultant routes.

### 3.2 Database Model Implementation (SQLAlchemy 2.0)
Implemented 12 relational models:
1. `User`: User credentials, UUID, email, role, activity status.
2. `Incident`: Tracks `incident_code` (`CB-YYYY-XXXXXX`), category, confidence, severity, and timestamps.
3. `Evidence`: Attached screenshots, file paths, raw OCR strings, user-edited text, and language tags.
4. `Message`: Segmented conversation messages, sender handles, and per-message predictions.
5. `Prediction`: Full 10-class probability distribution, explainability token attributions, salient offensive tokens, and model version.
6. `Report`: Certified forensic report records, unique code (`REP-XXXXXX`), and disk PDF paths.
7. `SupportSession`: Multi-message wellbeing session, rolling session summaries, and escalation levels.
8. `SupportMessage`: Chat history between user, AI assistant, and consultant with attached RAG citations.
9. `HelpRequest`: Formal escalation dossiers containing complainant details, dynamic bully handles, and WhatsApp group metadata.
10. `SlangTerm`: Emerging out-of-vocabulary candidate slang, frequencies, candidate meanings, and admin approval timestamps.
11. `DriftEvent`: Quantitative metric logs (Population Stability Index values, timestamps, status).
12. `ModelVersion`: Lineage records tracking model tags (`CB-RO-001`), Macro-F1, PR-AUC, accuracy, and active flags.

### 3.3 Advanced Machine Learning (AML) Engine

#### Mathematical Pipeline
1. **GloVe Word Embeddings ($d_{\text{glove}} = 100$)**:
   Tokenizes text into words and Hinglish colloquialisms, projecting each token onto pre-calibrated semantic vectors:
   $$\mathbf{v}_{\text{glove}} = \frac{1}{|T|} \sum_{t \in T} \mathbf{e}(t)$$
2. **PCA Dimensionality Reduction ($k = 30$)**:
   Projects 100-dimensional GloVe vectors onto 30 orthogonal principal axes, preserving $>88.5\%$ of empirical variance:
   $$\mathbf{v}_{\text{pca}} = \mathbf{W}_{\text{pca}}^T (\mathbf{v}_{\text{glove}} - \boldsymbol{\mu})$$
3. **Contextual Semantic Encoder ($d_{\text{ctx}} = 384$)**:
   Subword contextual embedding capturing syntactic order, negation, and implicit aggression.
4. **Feature Fusion Layer ($d_{\text{fused}} = 414$)**:
   Combines low-rank PCA-GloVe with contextual semantic representations using component weighting and global L2 normalization:
   $$\mathbf{z} = \left[ \alpha \frac{\mathbf{v}_{\text{pca}}}{\|\mathbf{v}_{\text{pca}}\|_2} \;\Big\|\; \beta \frac{\mathbf{v}_{\text{ctx}}}{\|\mathbf{v}_{\text{ctx}}\|_2} \right], \quad \mathbf{v}_{\text{fused}} = \frac{\mathbf{z}}{\|\mathbf{z}\|_2}$$
5. **Stacking Ensemble Meta-Learner**:
   - *Base 1*: Calibrated Linear/SGD Support Vector Machine (SVM).
   - *Base 2*: Gradient Boosted Decision Trees (GB).
   - *Base 3*: Random Forest Classifier (RF).
   - *Meta-Learner*: Multinomial Logistic Regression combining base class probability estimates to generate final 10-class distribution $P(y_c \mid \mathbf{x})$.

#### Unified 10-Class Taxonomy
- `Age-based`
- `Gender-based`
- `Religion-based`
- `Ethnicity-based`
- `Appearance-based`
- `Mockery/Defamation`
- `Abusive/Insult`
- `Threat/Intimidation`
- `Personal Harassment`
- `Non-cyberbullying`

#### Statistical Evaluation & McNemar's Hypothesis Test
- Benchmark comparison generated in [artifacts/tables/model_comparison.csv](file:///C:/Users/vivek/.gemini/antigravity-ide/scratch/cyberguard/artifacts/tables/model_comparison.csv).
- McNemar's test comparing SVM vs Stacking Ensemble:
  $$\chi^2 = \frac{(|b - c| - 1)^2}{b + c}$$
  Proves statistical significance and divergence between individual classifiers and the meta-learner.
- Confusion matrix generated in [artifacts/plots/confusion_matrix.png](file:///C:/Users/vivek/.gemini/antigravity-ide/scratch/cyberguard/artifacts/plots/confusion_matrix.png).

### 3.4 Explainable AI (XAI) Attribution Engine
- **Local Perturbation Weights**: Calculates attribution scores for each token in the submitted text.
- **Salient Trigger Extraction**: Flags terms exceeding offensive saliency thresholds (e.g. `"ugly"`, `"nobody likes you"`, `"kutta"`, `"chutiya"`).
- **Narrative Rationale**: Generates transparent explanations clarifying why lexical and syntactic patterns triggered the category.

### 3.5 Computer Vision & OCR Ingestion Pipeline
- **Image Preprocessing**: Pillow engine performs grayscale transformation, adaptive contrast enhancement ($1.8\times$), and edge sharpening.
- **Multi-Backend Architecture**: Tries PaddleOCR $\rightarrow$ EasyOCR $\rightarrow$ PyTesseract $\rightarrow$ adaptive heuristic extraction.
- **Human-in-the-Loop Review**: Extracted OCR text is displayed in an editable interface, allowing users to correct typos before running model classification.

### 3.6 Conversational & Group Chat Forensics
- **Sequential Message Segmentation**: Groups messages by sender and timestamp.
- **Repeated Targeting Detection**: Flags scenarios where single or multiple antagonists send repeated hostile communications.
- **Escalation Trajectory**: Identifies threats and volume surges.
- **Neutral Forensic Wording**: Uses objective statements (*"Repeated harmful-language pattern detected"*) rather than legal guilt assertions.

### 3.7 Incident Lifecycle & ReportLab PDF Compilation
- **Tri-Choice User Flow**:
  - `[ CONTINUE ]`: Appends additional screenshots or messages under the same incident.
  - `[ STOP ]`: Concludes evidence collection and compiles a forensic PDF report.
  - `[ SEEK HELP ]`: Opens the Consultant Help Request form.
- **Certified PDF Generation**: Uses ReportLab to generate official forensic dossiers containing incident identifiers, timestamps, evidence tables, model certainty scores, and official Indian cybercrime reporting procedures.

### 3.8 Grounded Support AI & RAG Knowledge Base
- **Knowledge Base Storage**: Markdown and JSON documents covering evidence preservation, platform blocking guides, account hardening, and official 1930 reporting.
- **Strict Non-Diagnostic Ethical Guardrails**: The agent is hardcoded to never diagnose psychiatric conditions (refuses *"You have depression"* or *"You are fine"*).
- **Wellbeing & Stress Indicators**: Evaluates distress signals (`LOW`, `MODERATE`, `ELEVATED`, `CRITICAL`) and recommends human consultant escalation when risk is elevated.
- **Official Statutory Helplines**: Integrates National Cyber Crime Helpline (`1930`), Tele-MANAS (`14416`), Women Helpline (`1091`), and Emergency (`112`).

### 3.9 Concept Drift & Slang Monitoring (MLOps)
- **Population Stability Index (PSI)**:
  $$\text{PSI} = \sum_{b=1}^{B} (Q_b - P_b) \times \ln\left(\frac{Q_b}{P_b}\right)$$
  Calculates divergence between training priors and production inference streams, generating [artifacts/evaluation/concept_drift_report.md](file:///C:/Users/vivek/.gemini/antigravity-ide/scratch/cyberguard/artifacts/evaluation/concept_drift_report.md).
- **Emerging Slang Queue**: Identifies out-of-vocabulary tokens in live traffic and presents them in an administrative queue for one-click approval into retraining sets.
- **Model Promotion Controls**: Models (`CB-RO-001`) can only be promoted to active production status through explicit administrator actions.

---

## 4. Visual Design, Aesthetic Choices & Website Look

The frontend application has been crafted with a **command-center, cyber-forensics aesthetic** designed to evoke security, precision, and trust.

```
+---------------------------------------------------------------------------------------+
|  [CG] CyberGuard AML v1.0   [Dashboard] [Analyze] [Chat] [Incidents] [Reports] ...   |
+---------------------------------------------------------------------------------------+
|                                                                                       |
|  +---------------------------------------------------------------------------------+  |
|  |  [ONLINE] Advanced Machine Learning Engine Online                              |  |
|  |  Multilingual AI-Powered Cyberbullying Forensics & Support                      |  |
|  |  Analyze comments, screenshots, or chat conversations using multilingual AI...  |  |
|  |  [ 🔍 Analyze Comment ]   [ 💬 Analyze Chat ]   [ 🤝 Ask Support AI ]           |  |
|  +---------------------------------------------------------------------------------+  |
|                                                                                       |
|  +------------------+  +------------------+  +------------------+  +---------------+  |
|  | Total Incidents  |  | Forensic Reports |  | AML Model Version|  | Languages     |  |
|  |       12         |  |        5         |  |    CB-RO-001     |  | EN / HI / HIN |  |
|  +------------------+  +------------------+  +------------------+  +---------------+  |
|                                                                                       |
|  +--------------------------------------------+  +---------------------------------+  |
|  | Recent Evidence Incidents                  |  | Immediate Safety Protocol       |  |
|  | • CB-202609-075E4A • Instagram (SEVERE)    |  | 1. Preserve uncropped screenshot|  |
|  | • CB-202609-8B3120 • WhatsApp  (HIGH)      |  | 2. Do not engage retaliatory    |  |
|  | • CB-202609-12A4F9 • Twitter   (MODERATE)  |  | 3. National Helpline: 1930      |  |
|  +--------------------------------------------+  +---------------------------------+  |
+---------------------------------------------------------------------------------------+
```

### 4.1 Color System & Mood Board
- **Deep Space Navy Base (`#0a0e17`)**: Provides an immersive, high-contrast dark canvas that eliminates screen glare and conveys a serious, forensic tone.
- **Glassmorphic Cards (`rgba(18, 24, 38, 0.85)`)**: Semi-transparent card backdrops with `backdrop-filter: blur(16px)` and subtle hairline borders (`rgba(255, 255, 255, 0.08)`), creating physical layering and visual depth.
- **Indigo & Violet Accent Gradients (`#4f46e5` to `#7c3aed`)**: Used for primary action buttons, active navigation states, and identity elements.
- **Rose / Crimson Alert Accents (`#f43f5e`)**: Reserved for cyberbullying alerts, severe risk warnings, and consultant escalation buttons.
- **Emerald Green (`#10b981`)**: Highlights non-violating content, system health badges, and successful PDF downloads.
- **Amber Gold (`#f59e0b`)**: Marks moderate severity ratings, concept drift warnings, and pending review states.

### 4.2 Typography Hierarchy
- **Primary Display & Headings**: *Plus Jakarta Sans* (Weights: 600, 700, 800) — Modern, authoritative geometric typography with tight tracking.
- **Body & Guidance Text**: *Inter* (Weights: 400, 500) — Optimized for reading long safety protocols and conversational advice.
- **Data, Hashes & Code Metrics**: *JetBrains Mono* — Used for incident codes (`CB-202609-XXXXXX`), confidence percentages, token attributions, and model version tags.

### 4.3 Screen-by-Screen User Interface Walkthrough

#### 1. Navigation Bar
A sticky header featuring the glowing `CG` gradient badge, title, AML version pill, responsive navigation buttons with icon accents, active user status indicator, and a red-accented logout button.

#### 2. Authentication Modal
A centered glassmorphic card with a floating ambient glow backdrop. Includes fields for Email/Username, Password, and the required radio selector for **User** vs **Admin** roles (validated server-side). Offers **"Admin Demo"** and **"User Demo"** buttons for 1-click credential autofill.

#### 3. Dashboard Overview
Displays a hero banner with active AI status badges, quick-launch buttons, 4 metric summary tiles, an active incidents feed with colored severity chips, and an immediate safety protocol checklist with a red **"Consultant Escalation Form"** button.

#### 4. Analyze Comment Screen
- **Mode Toggle**: Switches between **Direct Text Input** and **Screenshot OCR Upload**.
- **Benchmark Sample Pills**: 5 one-click sample buttons representing real-world bullying archetypes (Appearance bullying, Hindi abuse, Hinglish slang, Threat, Clean text).
- **Screenshot OCR Workspace**: A drag-and-drop file upload zone displaying a side-by-side image preview alongside the extracted OCR text editor.
- **Forensic Results Card**: Displays the predicted category badge, calibrated confidence meter, detected language, salient offensive terms highlighted as pill badges (e.g. `"ugly"`), model explanation, and horizontal probability bars across all 10 categories.
- **Tri-Choice Decision Flow**: Three buttons: `[ CONTINUE ]` (add more evidence), `[ STOP ]` (compile PDF report), and `[ SEEK HELP ]` (consultant escalation).

#### 5. Analyze Chat Screen
A sequential conversation workspace where users can add chat messages with sender handles and timestamps. The analysis card provides repeated targeting detection alerts, active antagonist lists, escalation indicators, and per-message classifications.

#### 6. My Incidents Vault
A split-view workspace. The left column lists all recorded incidents with status chips. The right column renders a detailed evidence timeline with a vertical indigo connector line and timestamped cards for every submitted piece of evidence.

#### 7. Forensic Reports Screen
A card grid displaying all generated PDF forensic reports with incident metadata, generation dates, and a 1-click **"Download PDF"** button.

#### 8. Support AI Chat Screen
A conversational interface with user and AI speech bubbles. AI responses feature expandable **"Referenced Official Guidance"** citation cards grounded in official platform safety documents. A persistent right-hand sidebar lists verified emergency helplines for India (1930 Cybercrime, 1091 Women Helpline, 14416 Tele-MANAS).

#### 9. Help Request & Escalation Form
A progressive intake form capturing complainant details, platform selection, and dynamic **Bully Account** fields (`Bully Account 1`, `Bully Account 2`, ...). Automatically reveals WhatsApp-specific inputs (Group Name, phone numbers) when WhatsApp is selected. Includes a privacy explanation card reassuring users about why information is collected.

#### 10. Consultant Support Portal
A case triage table available to consultants and administrators, displaying complainant contact details, platform origins, bully counts, case statuses, and direct links to incident dossiers.

#### 11. Admin Analytics & MLOps Dashboard
An administrative portal featuring 6 system counters, animated horizontal progress bars for class distributions, multilingual breakdown tiles, a **Model Registry** table with one-click **"Promote to Prod"** controls, a real-time **Population Stability Index (PSI)** drift card, and an **Emerging Slang Queue** with one-click **"Approve for Retraining"** buttons.

---

## 5. Verification & Testing Evidence

### 5.1 Pytest Automated Test Suite (10 / 10 Passed)
```text
backend/tests/test_admin.py::test_admin_dashboard_and_monitoring        PASSED [ 10%]
backend/tests/test_auth.py::test_password_hashing                        PASSED [ 20%]
backend/tests/test_auth.py::test_jwt_token_creation_and_decoding         PASSED [ 30%]
backend/tests/test_auth.py::test_user_registration_and_login             PASSED [ 40%]
backend/tests/test_incidents_reports.py::test_incident_lifecycle_and_report_generation PASSED [ 50%]
backend/tests/test_ml_pipeline.py::test_language_detection               PASSED [ 60%]
backend/tests/test_ml_pipeline.py::test_normalization                    PASSED [ 70%]
backend/tests/test_ml_pipeline.py::test_end_to_end_inference             PASSED [ 80%]
backend/tests/test_ml_pipeline.py::test_clean_text_inference             PASSED [ 90%]
backend/tests/test_support_rag.py::test_support_session_and_rag          PASSED [100%]
======================= 10 passed in 3.41s =======================
```

### 5.2 End-to-End Acceptance Test (14 / 14 Passed)
The complete 14-stage lifecycle script [scripts/acceptance_test.py](file:///C:/Users/vivek/.gemini/antigravity-ide/scratch/cyberguard/scripts/acceptance_test.py) executed and passed against the live servers:
1. User Registration & JWT Authentication: **PASSED**
2. User Login: **PASSED**
3. Direct Text Analysis (Hinglish Slang & Harassment): **PASSED**
4. Multi-Evidence Incident Continuation (`CONTINUE` Flow): **PASSED**
5. Screenshot OCR Text Extraction: **PASSED**
6. User-Edited OCR Analysis Confirmation: **PASSED**
7. Conversational Chat Forensics (Repeated Targeting & Escalation): **PASSED**
8. Help Request Consultant Escalation Submission: **PASSED**
9. Incident Conclusion & PDF Report Compilation (`STOP` Flow): **PASSED**
10. Binary PDF Report Download (Valid `%PDF` Header): **PASSED**
11. Support AI Chat with Grounded RAG Retrieval: **PASSED**
12. Official Statutory Resources Query (1930 / 14416): **PASSED**
13. Admin Analytics & Model Monitoring: **PASSED**
14. Concept Drift (PSI) & Slang Approval for Retraining: **PASSED**

---

## 6. Conclusion

CyberGuard is a fully realized, mathematically grounded, and aesthetically polished software application. It demonstrates that advanced machine learning (GloVe + PCA + Contextual semantic vectors + Stacking AML), explainability (XAI), computer vision OCR, and grounded RAG conversational support can be combined into a cohesive, high-performance web platform that protects digital spaces and supports victims of cyber harassment.
