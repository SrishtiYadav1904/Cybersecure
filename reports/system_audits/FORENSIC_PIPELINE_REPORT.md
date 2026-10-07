# CYBERGUARD — FORENSIC PIPELINE & EVIDENCE PROVENANCE REPORT

**Date:** 2026-09-24T23:45:00+05:30  
**Standard:** NIST FIPS 180-4 Cryptographic Hash Standard & ISO/IEC 27037 Digital Evidence Handling  
**Lead Forensic Engineer:** Lead Forensic Systems Architect  

---

## 1. Defining True Forensic Evidence vs Cosmetic Claims

In previous iterations, the term "forensic" was used as branding without underlying cryptographic provenance. The repaired CyberGuard platform enforces strict digital evidence standards:

1. **Cryptographic Immutability:** Every uploaded screenshot or chat export receives a SHA-256 cryptographic digest calculated at the moment of intake (`hashlib.sha256(content).hexdigest()`).
2. **Immutable Provenance:** The raw binary file is stored securely in `uploads/evidence/` with an immutable file path and timestamp.
3. **Dual OCR Preservation:** The original raw OCR transcription is permanently preserved in `extracted_text`. If a user corrects transcription errors, edits are recorded in a separate `user_corrected_text` field without overwriting the original evidence record.
4. **Chain of Custody:** Every stage of the evidence lifecycle (Intake -> OCR Extraction -> Human Review -> AML Model Classification -> Incident Inclusion -> Report Generation) is logged with UTC timestamps, user IDs, and digital signatures.

---

## 2. Complete Forensic Evidence Metadata Schema

Each piece of evidence attached to an incident captures the following attributes:

```json
{
  "evidence_id": "EV-20260924-8842",
  "incident_id": 14,
  "original_filename": "harassment_comment_screenshot.png",
  "file_type": "image/png",
  "file_size_bytes": 348210,
  "upload_timestamp_utc": "2026-09-24T18:14:22Z",
  "sha256_hash": "a8f5c381d89b19d28e754efb56d35e1656b823e20bfd7515d978a3c89b740523",
  "ocr_engine": "Tesseract-OCR v5.3.3",
  "ocr_raw_text": "moti bhaisn marr jaa",
  "user_corrected_text": null,
  "extracted_language": "Hinglish (HI-Latn)",
  "model_version": "CB-RO-001",
  "model_predicted_class": "Threat/Intimidation",
  "model_confidence": 0.9949,
  "severity_level": "SEVERE",
  "evidence_sequence_number": 1,
  "custody_status": "LOCKED_IN_INCIDENT"
}
```

---

## 3. OCR Extraction & Chat Analysis Pipeline

```text
Evidence Screenshot Upload
    │
    ▼
1. Cryptographic Intake
   - Compute SHA-256 hash of binary stream
   - Store in uploads/evidence/{evidence_id}_{hash[:8]}.png
    │
    ▼
2. Tesseract OCR Engine (backend/app/evidence/ocr.py)
   - Preprocessing: Grayscale conversion, adaptive thresholding, noise removal
   - Raw character extraction + confidence calculation
   - Save to database field: `extracted_text`
    │
    ▼
3. Provenance-Preserving Review
   - User reviews extracted text
   - Optional corrections saved to `user_corrected_text`
   - Original `extracted_text` is NEVER overwritten
    │
    ▼
4. Dual-Level Chat Analysis
   ┌───────────────────────────────────┬───────────────────────────────────┐
   │      Message-Level Analysis       │     Conversation-Level Pattern    │
   ├───────────────────────────────────┼───────────────────────────────────┤
   │ • Individual sentence classification│ • Message frequency & bursts      │
   │ • Salient toxic token attribution │ • Escalation over time            │
   │ • Exact confidence per bubble     │ • Repeated targeting indicators   │
   │ • Categorical tag (e.g. Threat)   │ • Incident severity synthesis     │
   └───────────────────────────────────┴───────────────────────────────────┘
```

---

## 4. Tamper-Evident Report Generation (`report_generator.py`)

The forensic report generator outputs legal-grade PDF dossiers:
- **Header:** Formal investigative metadata, Incident ID, Reporting Officer / User, Generation Timestamp.
- **Executive Summary:** Overall severity, incident status, primary classification, highest confidence.
- **Evidence Table:** Original filename, file size, SHA-256 digest, OCR extraction timestamp, and model version.
- **Chain of Custody Log:** Complete audit trail of all custody transfers and modifications.
- **Official Investigator Seal:** FIPS 180-4 cryptographic seal verification block and formal signature lines for cybercrime reporting.
