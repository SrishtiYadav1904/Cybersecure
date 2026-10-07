# CYBERGUARD — DATASET & DATA QUALITY REPORT

**Date:** 2026-09-24T23:35:00+05:30  
**Scope:** Dataset Acquisition, Cataloging, Label Mapping, Preprocessing, and Quality Verification  

---

## 1. Inventory of Datasets on Disk

| Dataset Identifier | File Path | Records | Format | Languages | Status |
|---|---|---|---|---|---|
| **Cyberbullying Multilingual Raw** | `data/raw/cyberbullying_multilingual_raw.csv` | 2,036 | CSV | EN, HI, HI-Latn | **AVAILABLE** |
| **Unified Training Dataset** | `data/unified/unified_dataset.csv` | 2,036 | CSV | EN, HI, HI-Latn | **PROCESSED & READY** |
| **Support & Wellbeing Raw** | `data/raw/support_wellbeing_raw.csv` | 70 | CSV | EN | **AVAILABLE** |
| **Dataset Catalog & Metadata** | `data/metadata/dataset_catalog.json` | 3 entries | JSON | N/A | **DOCUMENTED** |
| **Label Mapping Metadata** | `data/metadata/label_mapping.json` | 21 entries | JSON | N/A | **DOCUMENTED** |

---

## 2. Dataset Taxonomies & Explicit Label Mapping

Raw cyberbullying datasets historically exhibit incompatible taxonomy naming schemes (e.g. `insult` vs `abusive`, `threat` vs `intimidation`, `not_cyberbullying` vs `neutral`). CyberGuard implements an explicit normalization mapping layer:

```json
{
  "abusive": "Abusive/Insult",
  "insult": "Abusive/Insult",
  "abusive/insult": "Abusive/Insult",
  "appearance": "Appearance-based",
  "appearance-based": "Appearance-based",
  "threat": "Threat/Intimidation",
  "threat/intimidation": "Threat/Intimidation",
  "ethnicity": "Ethnicity-based",
  "ethnicity-based": "Ethnicity-based",
  "religion": "Religion-based",
  "religion-based": "Religion-based",
  "gender": "Gender-based",
  "gender-based": "Gender-based",
  "age": "Age-based",
  "age-based": "Age-based",
  "mockery": "Mockery/Defamation",
  "mockery/defamation": "Mockery/Defamation",
  "personal harassment": "Personal Harassment",
  "harassment": "Personal Harassment",
  "not_cyberbullying": "Non-cyberbullying",
  "non-cyberbullying": "Non-cyberbullying",
  "neutral": "Non-cyberbullying"
}
```

---

## 3. Class & Language Distribution

### Unified Class Breakdown:
- **Age-based:** 176 records (8.64%)
- **Gender-based:** 176 records (8.64%)
- **Religion-based:** 176 records (8.64%)
- **Ethnicity-based:** 176 records (8.64%)
- **Appearance-based:** 204 records (10.02%)
- **Mockery/Defamation:** 176 records (8.64%)
- **Abusive/Insult:** 228 records (11.20%)
- **Threat/Intimidation:** 292 records (14.34%)
- **Personal Harassment:** 176 records (8.64%)
- **Non-cyberbullying:** 256 records (12.57%)
- **Total:** **2,036 records** (100.0%)

### Language Representation:
- **English:** 1,012 records (49.71%)
- **Hindi (Devanagari):** 436 records (21.41%)
- **Hinglish (Roman Hindi):** 588 records (28.88%)

---

## 4. Data Quality & Cleansing Audit

Executed via `scripts/preprocess_all.py`:
1. **Missing Values:**
   - Raw records with null or empty text: 0
   - Null labels: 0
2. **Unicode & Normalization:**
   - Devanagari punctuation standardized (dandas `।`, `॥` stripped from word boundaries).
   - Emojis converted to canonical text descriptions (e.g. `😡` -> `:angry_face:`).
   - Leetspeak obfuscations normalized (`r4pe` -> `rape`, `k!ll` -> `kill`, `b!tch` -> `bitch`).
   - Slang canonicalized (`marr` -> `mar`, `bhaisn` -> `bhains`, `chutya` -> `chutiya`, `bsdk` -> `bhosdike`).
3. **Deduplication:**
   - Normalized text deduplication verified. Zero duplicate records in unified training split.

---

## 5. Ethical Compliance Regarding Restricted Data

- **DAIC-WOZ Corpus:** The DAIC-WOZ clinical distress corpus requires formal human-subjects institutional agreements. In compliance with strict research ethics, this data was NOT fabricated, mocked, or scraped illegally. It is officially cataloged as `RESTRICTED` in `data/metadata/dataset_catalog.json`.
- **Support System:** Grounded wellbeing guidance uses open-access, non-clinical wellbeing datasets (Dreaddit / GoEmotions) for ethical emotional grounding and non-diagnostic crisis triage.
