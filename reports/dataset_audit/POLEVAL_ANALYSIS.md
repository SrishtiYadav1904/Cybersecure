# POLEVAL 2019 DATASET AUDIT & ANALYSIS

**Audit Date:** 2026-09-25T16:25:00Z  
**Project:** CyberGuard Multilingual Cyberbullying Detection Engine  
**Audit Type:** Read-Only Verification & Research Attribution  
**Status:** Physically Verified on Local Filesystem  

---

## 1. Official Verification Statement

In strict compliance with Prompt Section 3, following an exhaustive recursive audit across all supplied local directories:

> **"PolEval 2019 referenced in project but dataset files were not found in the supplied local directories."**

---

## 2. Research Reference & BibTeX Citation

The referenced research work is:

* **Authors:** Ptaszynski, Michal; Pieciukiewicz, Agata; Dybała, Paweł.
* **Title:** *"Results of the PolEval 2019 Shared Task 6: First Dataset and Open Shared Task for Automatic Cyberbullying Detection in Polish Twitter"*
* **Venue:** Proceedings of the PolEval 2019 Workshop, Institute of Computer Science, Polish Academy of Sciences, page 89, 2019.

### Official BibTeX
```bibtex
@article{ptaszynski2019results,
  title={Results of the PolEval 2019 Shared Task 6: First Dataset and Open Shared Task for Automatic Cyberbullying Detection in Polish Twitter},
  author={Ptaszynski, Michal and Pieciukiewicz, Agata and Dyba{\l}a, Pawe{\l}},
  journal={Proceedings of the PolEval 2019 Workshop},
  publisher={Institute of Computer Science, Polish Academy of Sciences},
  pages={89},
  year={2019}
}
```

---

## 3. Local Directory Audit Findings

The audit performed recursive path-matching, content-searching, and archive inspection across:
1. `C:\Users\vivek\Documents\aml\mental` (0 occurrences of PolEval / Ptaszynski)
2. `C:\Users\vivek\Documents\aml\cyberbullying_dataset` (0 occurrences of PolEval / Ptaszynski)
3. `c:\Users\vivek\.gemini\antigravity-ide\scratch\cyberguard` (0 occurrences in raw/external corpora)

### Summary of Physical Evidence
* **Downloaded Status:** `NO`
* **Local Files Present:** `NONE`
* **Archives Containing PolEval:** `NONE`
* **Automated Download Action Taken:** `NONE` (Explicitly blocked per read-only guidelines).

---

## 4. Technical Analysis & Task Characteristics

Although not present locally, PolEval 2019 Shared Task 6 is well-documented in NLP literature:

1. **Target Language:** Polish (Polski).
2. **Platform & Modality:** Polish Twitter text (text-only, tweets scraped during 2018–2019).
3. **Task Decomposition:**
   - **Subtask 6.1:** Binary Cyberbullying Detection:
     - Class `0`: Non-harmful / Non-cyberbullying tweets.
     - Class `1`: Cyberbullying / Harmful tweets.
   - **Subtask 6.2:** Fine-Grained Harm Evaluation:
     - Class `0`: Non-harmful.
     - Class `1`: Cyberbullying / Public attacks.
     - Class `2`: Hate speech (targeted at minorities / protected groups).

---

## 5. Potential Relevance & Usability for CyberGuard

| Dimension | Evaluation for CyberGuard |
| :--- | :--- |
| **Language Compatibility** | **NOT COMPATIBLE.** The dataset is 100% Polish. CyberGuard's core operational languages are English, Devanagari Hindi, and Romanized Hinglish. |
| **Modality Compatibility** | **TEXT ONLY.** Does not support screenshot OCR or multimodal visual feature fusion. |
| **Label Mapping** | **PARTIAL.** Binary subtask 6.1 maps only to `Abusive/Insult` and `Non-cyberbullying`. It does not support CyberGuard's 10-class fine-grained taxonomy (Age, Religion, Ethnicity, Appearance, etc.). |
| **Recommendation** | **NOT SUITABLE for core training.** If ever ingested in the future, it should serve strictly as a multilingual auxiliary or transfer-learning benchmark, not for primary CyberGuard inference. |
