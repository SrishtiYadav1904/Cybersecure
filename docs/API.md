# CyberGuard REST API Reference

CyberGuard exposes a standard FastAPI OpenAPI/Swagger specification at `/docs` and `/redoc`.

---

## 1. Authentication & Users
- `POST /api/auth/register`: Register new account (`email`, `username`, `password`, `full_name`, `role`).
- `POST /api/auth/login`: Authenticate credentials and receive JWT bearer token.
- `GET /api/users/me`: Return authenticated profile and permissions.
- `PUT /api/users/me`: Update profile information.

---

## 2. Ingestion & Analysis
- `POST /api/analyze/text`: Classify direct text string.
  - **Body**: `{"text": "...", "incident_id": "optional-uuid"}`
  - **Returns**: `predicted_class`, `confidence`, `probabilities`, `detected_language`, `explanation`, `important_tokens`, `model_version`.
- `POST /api/analyze/image`: Upload screenshot (`.png`, `.jpg`, etc.) for OCR extraction.
  - **Form Data**: `file` (image file), `incident_id` (optional).
  - **Returns**: `extracted_text`, `language`, `confidence`.
- `POST /api/analyze/chat`: Segment and analyze multi-message chat transcript/screenshot.
  - **Returns**: Message array with individual predictions + aggregated context findings (repeated targeting, escalation count, coordination score).

---

## 3. Incident Management & Evidence
- `POST /api/incidents`: Initialize or continue an incident (`title`, `platform`).
- `GET /api/incidents`: List incidents for current user (or all if Admin/Consultant).
- `GET /api/incidents/{id}`: Detailed incident view with timeline, all evidence pieces, predictions.
- `POST /api/incidents/{id}/evidence`: Append new evidence to active incident.
- `POST /api/incidents/{id}/close`: Conclude evidence collection and trigger report generation.

---

## 4. Reports
- `POST /api/reports/generate/{incident_id}`: Compiles comprehensive incident report into a PDF artifact.
- `GET /api/reports`: List all generated reports for current user.
- `GET /api/reports/{id}/download`: Download actual PDF file.

---

## 5. Grounded AI Support & RAG
- `POST /api/support/start`: Initialize or resume support conversation with session context.
- `POST /api/support/message`: Send user message; performs intent detection + RAG search + safety response + wellbeing indicator update.
- `GET /api/support/history`: Retrieve past support sessions and summaries.
- `GET /api/support/resources`: Retrieve active emergency and official cyber safety helplines.

---

## 6. Help Request & Escalation
- `POST /api/help-request`: Submit formal help escalation (`name`, `age`, `email`, `phone`, `platform`, `bully_accounts`, `whatsapp_info`).
- `GET /api/help-request/cases`: Consultant view of escalated cases.

---

## 7. Admin & MLOps
- `GET /api/admin/dashboard`: Aggregate statistics (counts, class distribution, language split, platform distribution).
- `GET /api/admin/models`: List registered model versions and evaluation metrics.
- `POST /api/admin/models/{version}/promote`: Promote candidate model to production.
- `GET /api/admin/drift`: Current PSI, KS-test, and vocabulary distribution drift logs.
- `GET /api/admin/slang`: List pending slang terms.
- `POST /api/admin/slang/{id}/approve`: Approve slang term into training vocabulary.
