# CyberGuard — System Requirements Document

## 1. Functional Requirements (FR)

### FR-1: Multilingual Ingestion & Preprocessing
- **FR-1.1**: Direct text input accepting single comments, forum snippets, or pasted chats.
- **FR-1.2**: Image upload (`.png`, `.jpg`, `.jpeg`, `.webp`) with validation and dimension checking.
- **FR-1.3**: OCR text extraction with user-editable review interface before inference.
- **FR-1.4**: Automated language identification for English, Hindi (Devanagari), and Hinglish (Roman Hindi/code-mixed).
- **FR-1.5**: Text normalization pipeline (repeated characters, emoji handling, case folding, Hindi diacritic normalization).

### FR-2: Class-Wise Cyberbullying Classification
- **FR-2.1**: Multi-category taxonomy: `Age-based`, `Gender-based`, `Religion-based`, `Ethnicity-based`, `Appearance-based`, `Mockery/Defamation`, `Abusive/Insult`, `Threat/Intimidation`, `Personal Harassment`, and `Non-cyberbullying`.
- **FR-2.2**: Probability distribution across all categories with confidence thresholds.
- **FR-2.3**: Multi-label support when content violates multiple taxonomy axes simultaneously.

### FR-3: Advanced ML Architecture (AML)
- **FR-3.1**: GloVe word vector representation combined with PCA dimensionality reduction.
- **FR-3.2**: Contextual semantic embeddings (RoBERTa / transformer sentence encoder).
- **FR-3.3**: Feature fusion matrix combining low-rank GloVe and contextual transformer representations.
- **FR-3.4**: Ensemble classifier comparison (SVM, XGBoost, LightGBM, CatBoost, Stacking Classifier).

### FR-4: Explainable AI (XAI)
- **FR-4.1**: Local feature importance attributing predictions to specific tokens/phrases.
- **FR-4.2**: Human-readable explanations clarifying *why* terms contributed to the designated category.
- **FR-4.3**: Model version metadata attached to every generated explanation.

### FR-5: Conversational & Chat Context Analysis
- **FR-5.1**: Message segmentation extracting sender, timestamp, and payload.
- **FR-5.2**: Repeated targeting detection identifying escalation and multiple abusive messages from single or coordinated actors.
- **FR-5.3**: Neutral, non-legal terminology in assessments ("Repeated harmful-language pattern detected").

### FR-6: Incident Management Workflow
- **FR-6.1**: Unique incident identification (`CB-YYYY-XXXXXX`).
- **FR-6.2**: Multi-evidence accumulation timeline under a single incident.
- **FR-6.3**: User tri-choice prompt post-analysis: `CONTINUE` (add evidence), `STOP` (generate report), `SEEK HELP` (open support request).

### FR-7: Incident Report Generation
- **FR-7.1**: Real, downloadable PDF compilation containing incident timeline, extracted OCR, detected classes, confidence scores, explainability highlights, and recommended safety actions.

### FR-8: Support AI & Grounded RAG Knowledge Base
- **FR-8.1**: Factual, safety-focused conversational guidance (blocking, reporting, digital footprint protection, evidence preservation).
- **FR-8.2**: Retrieval-Augmented Generation (RAG) anchored to official platform safety guides and statutory helplines.
- **FR-8.3**: Strict ethical boundary: No mental health or psychiatric diagnosis under any circumstance.
- **FR-8.4**: Dynamic emergency escalation for acute risk signals.
- **FR-8.5**: Session-based memory with daily follow-up tracking and wellbeing indicators.

### FR-9: Concept Drift & Slang Monitoring
- **FR-9.1**: Out-of-vocabulary and emerging slang detection from live inference streams.
- **FR-9.2**: Quantitative drift metric calculations (Population Stability Index, KS-test, prediction distribution shifts).
- **FR-9.3**: Admin vocabulary review queue with approval workflows for retraining pipelines.

### FR-10: Roles & Administration
- **FR-10.1**: Role-based access control supporting `USER`, `ADMIN`, and extensible for `CONSULTANT`.
- **FR-10.2**: Secure authentication via bcrypt password hashing and JWT bearer tokens.
- **FR-10.3**: Comprehensive admin portal displaying aggregate metrics, category breakdowns, drift scores, and model promotion controls.

### FR-11: Three-Layer Data Architecture & Strict Domain Decoupling
- **FR-11.1**: Strict preservation of raw data in `data/raw/` with zero in-place destruction or loss.
- **FR-11.2**: 3-layer data lifecycle: `data/raw/` -> `data/interim/` -> `data/processed/` -> `data/unified/`.
- **FR-11.3**: Cryptographic integrity tracking with SHA-256 hashes recorded in `data/metadata/dataset_versions.json`.
- **FR-11.4**: Absolute decoupling between Cyberbullying and Wellbeing support intelligence; zero diagnostic medical claims.
- **FR-11.5**: Mechanical duplicate quarantine: bar tiled corpora (`Archive.zip 25K`) and corrupt files (`GoEmotions All-Null`).

### FR-12: Dual-Model Training & Empirical Comparative Evaluation
- **FR-12.1**: Baseline training experiment (`CB-BASE-001`) on baseline corpus (`CB-DATA-001`).
- **FR-12.2**: Expanded training experiment (`CB-EXP-002`) on multi-source verified corpus (`CB-DATA-002`).
- **FR-12.3**: Independent holdout evaluation on 4,516 unexposed real social records.
- **FR-12.4**: Multi-model comparison reporting Accuracy, Macro-F1, Weighted-F1, Precision, Recall, PR-AUC, and ROC-AUC for SVM, XGBoost, LightGBM, CatBoost, and Stacking.
- **FR-12.5**: Dedicated wellbeing support model family (`SUP-001`) with multi-task evaluation for crisis triage, cognitive distress, and stress calibration.

---

## 2. Non-Functional Requirements (NFR)
- **NFR-1 (Performance)**: Inference latency < 350ms for text input on CPU; OCR pipeline < 2.5s.
- **NFR-2 (Scalability)**: Stateless REST API containerizable via Docker and orchestratable with horizontal scaling.
- **NFR-3 (Reliability)**: Fault-tolerant fallbacks for optional ML runtimes; persistence in relational storage.
- **NFR-4 (Usability)**: Intuitive, accessible UI with responsive layout, clear status indicators, and zero jargon in user-facing guidance.

---

## 3. Security & Privacy Requirements
- **SEC-1**: Passwords hashed with bcrypt (cost factor >= 12).
- **SEC-2**: All API endpoints protected with role-verified JWT signatures.
- **SEC-3**: Input validation and file-type verification (magic bytes & MIME checking).
- **PRIV-1**: Zero permanent logging of raw credentials or full private chat transcripts in application logs.
- **PRIV-2**: User-initiated evidence redaction and incident deletion capability.

---

## 4. Hardware & Software Requirements
- **Python**: 3.10+
- **Node.js**: 18.0+
- **Database**: SQLite (local development) / PostgreSQL 15+ (production)
- **Memory**: Minimum 4GB RAM (8GB+ recommended for full transformer pipelines)
- **Storage**: Minimum 2GB free disk space for models, embeddings, and artifacts
