# MENTAL & WELLBEING DATASET ANALYSIS — READ-ONLY AUDIT

**Audit Date:** 2026-09-25T16:26:00Z  
**Target Directory:** `C:\Users\vivek\Documents\aml\mental`  
**Compliance Standard:** Ethical Medical AI Separation, No Diagnostic Mapping, Strict Support-Only Scope  

---

## 1. Ethical Governance & Core Architecture Rules

In strict compliance with Prompt Section 11:
1. **NO CYBERBULLYING $\rightarrow$ MENTAL ILLNESS MAPPING:** Being targeted by cyberbullying is an external event of harassment, NOT an internal psychiatric diagnosis. Cyberbullying victims must never be labeled or assumed to have a mental disorder.
2. **NO CLINICAL OR MEDICAL DIAGNOSIS:** None of these datasets or models may produce medical, psychiatric, or clinical diagnoses (e.g., "Major Depressive Disorder", "Clinical Suicidality").
3. **SUPPORT / ESCALATION ONLY:** Mental and wellbeing datasets are strictly isolated from the main cyberbullying classifier. They are evaluated exclusively for:
   - AI wellbeing grounded conversational support (empathy, safety escalation).
   - Emergency consultant escalation triggers (National Cybercrime Portal 1930, Tele-MANAS 14416).
   - Stress / coping guidance in the user wellness portal.

---

## 2. File-by-File Inventory of Source A (`C:\Users\vivek\Documents\aml\mental`)

| Filename | Format | Size | Total Records | Columns | Primary Labels | Task & Construct Measured |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`LoSTv1.csv`** | CSV | 1,963,797 B | 3,251 | `text`, `self` | Binary `self`: `0.0` (78.1%), `1.0` (21.8%) | **Loss of Self Theory (LoST):** Self-harm / psychological detachment expressed in Reddit posts. |
| **`final_train.csv`** | CSV | 1,129,697 B | 1,739 | `text`, `self`, `Trigger`, `LoST`, `Consequences` | Binary `self` + Spans (`Trigger`, `LoST`, `Consequences`) | **Cognitive Attribution Mining:** Span-level extraction of stress triggers, loss of self expressions, and consequences. |
| **`final_test.csv`** | CSV | 279,977 B | 435 | `text`, `self`, `Trigger`, `LoST`, `Consequences` | Binary `self` + Spans | **Evaluation Holdout:** Companion test set for cognitive span extraction. |
| **`combined-set.csv`** | CSV | 4,085,313 B | 1,895 | `title`, `selftext`, `is_suicide`, `megatext_clean` | Binary `is_suicide`: `1` (51.7%), `0` (48.3%) | **Distress Crisis Discrimination:** Distinguishes acute crisis posts (`r/SuicideWatch`) from chronic depressive posts (`r/depression`). |
| **`goemotions_1-selected-columns.csv`** | CSV | 210,486 B | 21,039 | `text`, `id`, `subreddit`, `admiration` | Emotion indicators (`admiration`, `unclear`) | **Affective Emotion Lexicon:** Google GoEmotions fine-grained emotion detection on Reddit comments. |
| **`sample_data_1.xlsx`** | Excel | 8,727 B | 96 | `title`, `usertext`, `y` | Binary `y`: `1` (48), `0` (48) | **Distress Sample:** Small Reddit mental health sample benchmark. |
| **`sample_data_2.xlsx`** | Excel | 8,349 B | 96 | `tweets`, `y` | Binary `y`: `1` (48), `0` (48) | **Distress Sample:** Small Twitter distress expression sample benchmark. |

---

## 3. Detailed Dataset Profiles

### A. LoST Suite (`LoSTv1.csv`, `final_train.csv`, `final_test.csv`)
* **Task:** Cognitive and linguistic modeling of "Loss of Self" (LoST) — psychological distress where an individual perceives complete loss of agency, worth, or identity.
* **Population:** Anonymous Reddit users participating in mental health and support subreddits (`r/depression`, `r/selfharm`, `r/mentalhealth`).
* **Language:** English (informal, narrative, first-person confessionals).
* **Modality:** TEXT ONLY.
* **Appropriateness for CyberGuard:**
  - **Main Cyberbullying Model:** **STRICTLY PROHIBITED.** The text represents self-reflective confessions, not interpersonal attacks or insults.
  - **Wellbeing Support Module:** **HIGH VALUE.** The annotated spans (`Trigger`, `LoST`, `Consequences`) provide grounded knowledge for empathetic response framing, helping the AI recognize when a user expresses acute self-blame following a bullying incident.

### B. Reddit Suicide vs. Depression (`combined-set.csv`)
* **Task:** Binary classification between acute suicidal ideation (`is_suicide = 1`, scraped from `r/SuicideWatch`) and non-acute depressive rumination (`is_suicide = 0`, scraped from `r/depression`).
* **Population:** Anonymous Reddit posters.
* **Language:** English long-form posts (mean length: 948 characters).
* **Appropriateness for CyberGuard:**
  - **Main Cyberbullying Model:** **STRICTLY PROHIBITED.**
  - **Emergency Safety Guardrails:** **HIGH VALUE.** Can be used as a standalone safety classifier to trigger the emergency hotline modal (Tele-MANAS, 14416, Vandrevala Foundation) if a distressed victim expresses imminent self-harm in the user support portal.

### C. Google GoEmotions Subset (`goemotions_1-selected-columns.csv`)
* **Task:** Fine-grained emotion labeling across 27 emotion categories.
* **Population:** Reddit comment participants.
* **Language:** English conversational text.
* **Appropriateness for CyberGuard:**
  - Useful as an auxiliary feature extractor for sentiment/affective modeling in empathetic dialogue generation.

---

## 4. Usability Classification Matrix

| Dataset | Core Cyberbullying Classification | AI Wellbeing Support RAG | Emergency Safety Escalation | Recommendation |
| :--- | :--- | :--- | :--- | :--- |
| `LoSTv1.csv` | **DO NOT USE** | **YES (Auxiliary)** | **YES (Auxiliary)** | AUXILIARY: Support Knowledge Base |
| `final_train.csv` | **DO NOT USE** | **YES (High Value)** | **YES (Span Grounding)** | AUXILIARY: Cognitive Span Grounding |
| `final_test.csv` | **DO NOT USE** | **YES (Evaluation)** | **YES (Evaluation)** | EVALUATION: Support Evaluation Set |
| `combined-set.csv` | **DO NOT USE** | **NO** | **YES (Critical Safety)** | AUXILIARY: Emergency Crisis Trigger |
| `goemotions_1.csv` | **DO NOT USE** | **YES (Affective Tone)** | **NO** | AUXILIARY: Empathetic Tone Tuner |
| `sample_data_1.xlsx`| **DO NOT USE** | **YES (Small Sample)** | **NO** | AUXILIARY: Unit Testing |
| `sample_data_2.xlsx`| **DO NOT USE** | **YES (Small Sample)** | **NO** | AUXILIARY: Unit Testing |
