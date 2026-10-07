# CyberGuard System Architecture

## 1. High-Level Architecture Overview

CyberGuard is designed as an end-to-end, multi-tier platform combining advanced machine learning, explainable AI, computer vision OCR, structured incident management, and grounded conversational support.

```
+-------------------------------------------------------------------------+
|                              Frontend UI                                |
|    (React / Modern Single-Page Dashboard / Responsive Glassmorphism)    |
+------------------------------------+------------------------------------+
                                     |  HTTPS / REST / JSON
                                     v
+------------------------------------+------------------------------------+
|                         FastAPI Application                             |
|  +--------------------+---------------------+------------------------+  |
|  |   Auth & RBAC      |   Incident Service  |    Reporting Service   |  |
|  | (JWT, Bcrypt, Role)| (Timeline, Evidence)|     (ReportLab PDF)    |  |
|  +--------------------+---------------------+------------------------+  |
|  |     OCR Engine     |   Support AI Engine | Drift & Slang Service  |  |
|  | (Image Preproc/OCR)| (RAG, Session Memory|(PSI, Term Aggregation) |  |
|  +--------------------+---------------------+------------------------+  |
+------------------------------------+------------------------------------+
                                     |
             +-----------------------+-----------------------+
             v                                               v
+----------------------------+             +-------------------------------+
|      Relational Database   |             |       AML Inference Engine    |
|   (PostgreSQL / SQLite)    |             |  1. Language Identification   |
| - Users & Roles            |             |  2. Slang & Preprocessing     |
| - Incidents & Evidence     |             |  3. GloVe (100d) -> PCA (30d) |
| - Messages & Predictions   |             |  4. RoBERTa Context Vectors   |
| - Reports & Sessions       |             |  5. Feature Fusion Matrix     |
| - Slang Terms & Drift Logs |             |  6. Stacking Ensemble Classif |
| - Model Versions           |             |  7. Token-Level Attribution   |
+----------------------------+             +-------------------------------+
                                                             |
                                           +-----------------+-------------+
                                           v                               v
                             +--------------------------+    +-----------------------+
                             |   RAG Knowledge Base     |    |   Artifacts Storage   |
                             | - Official Cyber Safety  |    | - Evaluation Metrics  |
                             | - Platform Block Guides  |    | - PDF Reports         |
                             | - Emergency Helplines    |    | - Model Snapshots     |
                             +--------------------------+    +-----------------------+
```

---

## 2. Advanced Machine Learning (AML) Pipeline

### 2.1 Text Ingestion & Language Identification
1. **Raw Text / OCR Text Extraction**: User pastes message or uploads screenshot.
2. **Text Normalization**:
   - Case folding, regex cleanup for excessive punctuation and repeated characters.
   - De-emojification converting glyphs to semantic text tokens.
   - Hinglish token mapping and Devanagari Unicode normalization.
3. **Language Detection**:
   - Heuristic Devanagari script detection (`[\u0900-\u097F]`).
   - Romanized Hindi (Hinglish) pattern scoring against common romanized function words (`tu`, `kya`, `bhai`, `tera`, `gaya`, `wala`, `nahi`).
   - Standard English token frequency checking.

### 2.2 Feature Engineering & Fusion
- **GloVe Embeddings**: Static word vectors capturing broad semantic associations.
- **PCA Dimensionality Reduction**: Principal Component Analysis reduces 100d GloVe vectors to a compact 30d dense representation, capturing max variance while filtering noise.
- **RoBERTa Contextual Embeddings**: Context-sensitive sentence representation capturing syntax, intent, and subtle connotations.
- **Concatenated Feature Fusion**:
  $$\mathbf{z} = [\mathbf{v}_{\text{PCA-GloVe}} \,\|\, \mathbf{v}_{\text{RoBERTa}}]$$
  This dual-representation balances broad vocabulary coverage with contextual nuance.

### 2.3 Ensemble Classification
- Base classifiers:
  - **Support Vector Machine (Linear & RBF Kernels)**: Strong margin separation in dense fused space.
  - **XGBoost / LightGBM / Gradient Boosting**: Robust non-linear decision trees handling skewed feature distributions.
  - **Meta-Classifier (Stacking / Soft-Voting)**: Calibrates base probabilities to yield final multi-class scores.

### 2.4 Explainable AI (XAI)
- Token attribution assigns importance scores to input tokens based on their contribution to the predicted class score.
- Generates human-interpretable justifications and extracts the critical offensive trigger words.

---

## 3. Incident Management & Context Analysis
- Multi-evidence collection under unique incident identifiers (`CB-YYYY-XXXXXX`).
- Sequential conversation timeline analysis:
  - Grouping messages by sender.
  - Tracking escalation over time.
  - Detecting repeated harassment patterns and multi-party harassment indicators.

---

## 4. Support AI & Grounded RAG Knowledge Base
- **Knowledge Base Directories**:
  - `knowledge_base/cyber_safety/`: General digital hygiene and evidence retention.
  - `knowledge_base/privacy/`: Social media account lock down procedures.
  - `knowledge_base/blocking/`: Step-by-step blocking guides for Instagram, WhatsApp, Twitter/X, Discord.
  - `knowledge_base/platform_guides/`: Platform reporting mechanisms.
  - `knowledge_base/cybercrime_reporting/`: Official Indian Cyber Crime Reporting Portal (`cybercrime.gov.in`, 1930).
  - `knowledge_base/emergency_resources/`: Statutory crisis numbers (Women Helpline 1091, Tele-MANAS 14416).
- **Session Memory**:
  - Multi-session continuity without token overflow through structured summaries.
  - Daily follow-up wellbeing indicator tracking.

---

## 5. Concept Drift & Vocabulary Evolution
- Live monitoring of Out-of-Vocabulary (OOV) tokens.
- Slang candidate extraction with frequency counters.
- **Population Stability Index (PSI)** and prediction distribution divergence tracking.
- Human-in-the-loop admin validation workflow before retraining.

---

## 6. Strict Two-Domain Data and Model Decoupling

CyberGuard permanently maintains two independent model families operating across isolated data layers:

```text
                    CYBERGUARD DATA LAYER
                           |
          ┌────────────────┴────────────────┐
          |                                 |
          ↓                                 ↓
 CYBERBULLYING DATA DOMAIN            WELLBEING DATA DOMAIN
 (Kaggle Tweets, CyberbullyX,         (Reddit Suicide vs Depression,
  Hinglish 18K, Jigsaw Threat,         Reddit LoST Cognitive Spans,
  Multimodal Memes, Synthetic)         Synthetic Stress Prompts)
          |                                 |
 ┌────────┼────────┐                 ┌──────┼──────┐
 |        |        |                 |      |      |
Text    Hindi    Multimodal       Emotion Stress Distress
 |        |        |                 |      |      |
 └────────┴────────┘                 └──────┴──────┘
          |                                 |
          ↓                                 ↓
 CYBERBULLYING MODEL FAMILY           SUPPORT MODEL FAMILY
 (CB-EXP-002 Production Stacking)     (SUP-001 Crisis & LoST Models)
          |                                 |
          ↓                                 ↓
 Explainability (XAI Attribution)     Safety Rules & Hotline Triage
          |                                 |
          └──────────────┬──────────────────┘
                         ↓
                    SUPPORT ENGINE
                         |
                         ↓
                       RAG
                         |
                         ↓
                 HUMAN ESCALATION
```

### Key Decoupling Principles:
1. **Taxonomy Independence:** Psychiatric and medical categories (such as depression, suicidal ideation, anxiety) are never treated as labels inside the cyberbullying classifier, nor are cyberbullying categories merged into clinical diagnoses.
2. **Ethical Non-Diagnostic Boundary:** Wellbeing outputs are explicitly presented as **support signals, distress indicators, and crisis triage triggers**, NEVER as clinical psychiatric diagnoses.
3. **Safety Escalation:** Acute crisis ideation triggers an immediate emergency modal displaying verified national hotlines: **Tele-MANAS (14416)** and **National Cyber Crime Helpline (1930)**.
