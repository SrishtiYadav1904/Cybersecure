# CyberGuard Database Schema Specification

CyberGuard uses SQLAlchemy 2.0 with PostgreSQL in production and SQLite in development.

## 1. Entity-Relationship Model

```
+---------------+        1:N       +-------------------+        1:N       +----------------------+
|     users     | ---------------- |     incidents     | ---------------- |       evidence       |
+---------------+                  +-------------------+                  +----------------------+
| id (PK)       |                  | id (PK)           |                  | id (PK)              |
| email (UQ)    |                  | incident_code(UQ) |                  | incident_id (FK)     |
| username (UQ) |                  | user_id (FK)      |                  | evidence_type        |
| password_hash |                  | status            |                  | file_path            |
| role          |                  | primary_category  |                  | ocr_text             |
| full_name     |                  | confidence        |                  | edited_text          |
| created_at    |                  | severity          |                  | detected_language    |
+---------------+                  | created_at        |                  | created_at           |
                                   +-------------------+                  +----------------------+
                                             |                                       |
                                             | 1:N                                   | 1:N
                                             v                                       v
                                   +-------------------+                  +----------------------+
                                   |      reports      |                  |     predictions      |
                                   +-------------------+                  +----------------------+
                                   | id (PK)           |                  | id (PK)              |
                                   | incident_id (FK)  |                  | evidence_id (FK)     |
                                   | report_code (UQ)  |                  | predicted_class      |
                                   | pdf_path          |                  | confidence           |
                                   | summary_json      |                  | probabilities_json   |
                                   | generated_at      |                  | explainability_json  |
                                   +-------------------+                  | model_version        |
                                                                          +----------------------+

+----------------------+        1:N       +----------------------+
|   support_sessions   | ---------------- |   support_messages   |
+----------------------+                  +----------------------+
| id (PK)              |                  | id (PK)              |
| user_id (FK)         |                  | session_id (FK)      |
| incident_id (FK,opt) |                  | sender (user/ai/con) |
| session_summary      |                  | content              |
| wellbeing_indicators |                  | rag_sources_json     |
| escalation_level     |                  | created_at           |
| created_at           |                  +----------------------+
+----------------------+

+----------------------+     +----------------------+     +----------------------+
|     help_requests    |     |      slang_terms     |     |     drift_events     |
+----------------------+     +----------------------+     +----------------------+
| id (PK)              |     | id (PK)              |     | id (PK)              |
| incident_id (FK)     |     | term                 |     | metric_name (PSI/KS) |
| user_id (FK)         |     | language             |     | metric_value         |
| platform             |     | candidate_meaning    |     | drift_status         |
| bully_accounts_json  |     | frequency            |     | affected_classes     |
| whatsapp_details     |     | status (pending/app) |     | sample_size          |
| status               |     | first_seen           |     | timestamp            |
| created_at           |     | approved_at          |     +----------------------+
+----------------------+     +----------------------+
```

---

## 2. Table Specifications
- **users**: Stores authenticated identities, role permissions (`USER`, `ADMIN`, `CONSULTANT`), and profile data.
- **incidents**: Aggregates incident timeline, status (`ACTIVE`, `PENDING_REVIEW`, `RESOLVED`, `REPORTED`), and category.
- **evidence**: Stores artifacts uploaded by the user, raw OCR output, user-corrected text, and metadata.
- **predictions**: Records class probabilities, token attribution arrays, and model provenance (`model_version`).
- **reports**: Tracks compiled PDF artifacts saved to disk and metadata summaries.
- **support_sessions** & **support_messages**: Implements grounded conversational memory with summary rollups.
- **help_requests**: Stores consultant escalation data including dynamic bully usernames and platform handles.
- **slang_terms**: Out-of-vocabulary terms and candidate slang for admin validation.
- **drift_events**: Logs statistical divergence measurements over time.
- **resources**: Configurable national and regional helplines (e.g. 1930 Cybercrime, 1091 Women Helpline).
- **model_versions**: Tracks model lineage, training dates, evaluation metrics (Macro-F1, PR-AUC), and active flag.
