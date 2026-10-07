# EXTERNAL DATA USAGE AUDIT — CLAIMED VS. PHYSICAL EVIDENCE

**Audit Date:** 2026-09-25T16:27:00Z  
**Project:** CyberGuard Multilingual Cyberbullying Detection Engine  
**Objective:** Independent Verification of Claimed vs. Physically Present Datasets  
**Compliance Standard:** Mandatory Source Verification, Zero-Fabrication Integrity  

---

## 1. Executive Summary & Verification Matrix

Prior project reports and scripts referenced a series of public benchmark datasets. In accordance with Prompt Sections 4 and 15, we distinguish between:
* **CLAIMED:** Mentioned in codebase, comments, or documentation.
* **PHYSICALLY PRESENT:** Verified files existing on disk.
* **ACTUALLY LOADED:** Read by data loader scripts.
* **ACTUALLY USED FOR TRAINING:** Contributed samples to the fitted `.joblib` model weights.
* **VERIFIED SAMPLE COUNT:** Exact physical record count.

| Dataset Name | Claimed in Project? | Physically Present? | Actually Loaded? | Used for Training? | Verified Sample Count | Verified Physical Location | Status & Discrepancy Note |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **CyberbullyX-63K** | YES | **YES** | NO | NO | 63,145 rows | `C:\Users\vivek\Documents\aml\cyberbullying_dataset\CyberbullyX-63K.xlsx` | **VERIFIED ON DISK.** Not previously ingested into `scratch/cyberguard`. High-value primary candidate. |
| **Kaggle Cyberbullying Tweets** | YES | **YES** | NO | NO | 47,692 rows | `C:\Users\vivek\Documents\aml\cyberbullying_dataset\kaggledataset.zip::cyberbullying_tweets.csv` | **VERIFIED ON DISK (ZIP).** Never extracted or trained in previous pipeline. Direct 5-class match. |
| **Jigsaw Toxic Comments** | YES | **YES** | NO | NO | 159,571 train / 153,164 test | `C:\Users\vivek\Documents\aml\cyberbullying_dataset\archive (1).zip` | **VERIFIED ON DISK (ZIP).** Never extracted or trained in previous pipeline. |
| **Hinglish Codemixed (Paper 4989)**| YES | **YES** | NO | NO | 18,148 rows | `C:\Users\vivek\Documents\aml\cyberbullying_dataset\final_dataset_hinglish.csv` | **VERIFIED ON DISK.** Real Hinglish comments; never trained in previous pipeline. |
| **Archive.zip Hinglish (25K)** | YES | **YES** | NO | NO | 25,000 rows (40 unique) | `C:\Users\vivek\Documents\aml\cyberbullying_dataset\archive.zip` | **SYNTHETIC / TILED.** 40 template sentences repeated 25,000 times. Excluded from training. |
| **MultiOFF TRAC-2** | YES | **YES** | **YES** | **YES** | 740 records / 740 images | `data\external\multioff\` | **VERIFIED & TRAINED.** Ingested with 740 physical images; trained in `CB-MM-001`. |
| **M3 Twitter Memes** | YES | **YES** | **YES** | **YES** | 526 records / 150 images | `data\external\m3\` | **VERIFIED & TRAINED.** Ingested with 150 physical images; trained in `CB-MM-001`. |
| **Facebook Hateful Memes** | YES | **YES** | **YES** | **NO (Holdout Only)**| 500 records / 150 images | `data\external\hateful_memes\` | **VERIFIED AS HOLDOUT.** Ingested with 150 physical images; evaluated strictly as Set B holdout. |
| **Zenodo Toxic Memes** | YES | **YES** | NO | NO | 1,998 records (Labels only) | `data\external\zenodo_toxic_memes\labels.csv` | **CATALOGED AS AUXILIARY.** Russian Cyrillic out of target scope. |
| **Synthetic CyberGuard Baseline**| YES | **YES** | **YES** | **YES** | 2,036 records | `data\raw\cyberbullying_multilingual_raw.csv` | **VERIFIED SYNTHETIC.** Internally generated baseline; trained in `CB-MM-001`. |
| **MC-Hinglish** | **YES (CLAIMED)** | **NO** | NO | NO | 0 | None found on disk | **CLAIMED BUT NOT PRESENT.** No physical folder or file named `MC-Hinglish` exists on disk. |
| **HASOC** | **YES (CLAIMED)** | **NO** | NO | NO | 0 | None found on disk | **CLAIMED BUT NOT PRESENT.** Referenced in documentation; no physical files found. |
| **CyberDTD** | **YES (CLAIMED)** | **NO** | NO | NO | 0 | Springer ACLING 2025 (Restricted) | **NOT PRESENT.** Restricted academic paper; Tunisian Arabic out-of-scope. |
| **PolEval 2019** | **YES (CLAIMED)** | **NO** | NO | NO | 0 | PolEval 2019 Workshop (Polish) | **NOT PRESENT.** Zero physical files in local directories. Polish out-of-scope. |

---

## 2. Discrepancy & Provenance Investigation

### 1. The "MC-Hinglish" and "HASOC" Discrepancy
* **Claim:** Historical project proposals stated that CyberGuard would incorporate MC-Hinglish and HASOC (Hate Speech and Offensive Content in Indo-European Languages).
* **Physical Reality:** Neither dataset was physically downloaded into the workspace.
* **Finding:** Previous models claimed to be trained on multilingual data were actually trained **exclusively on the 2,036 internally generated synthetic sentences** in `data/raw/cyberbullying_multilingual_raw.csv`.

### 2. Discovered Treasure in `C:\Users\vivek\Documents\aml\cyberbullying_dataset`
* **Finding:** While not yet integrated into the `scratch/cyberguard` codebase, **massive, high-quality, genuine external datasets are physically available** on the user's system:
  1. `CyberbullyX-63K.xlsx` (63,145 real Hindi/English tweets)
  2. `cyberbullying_tweets.csv` inside `kaggledataset.zip` (47,692 real labeled tweets across Religion, Age, Gender, Ethnicity)
  3. `final_dataset_hinglish.csv` (18,148 real codemixed Hinglish comments)
  4. `train.csv` inside `archive (1).zip` (159,571 Jigsaw toxicity comments)
* **Status:** These datasets represent **over 288,000 real external records** awaiting formal human review before ingestion.

### 3. The `archive.zip` Synthetic Tiling Revelation
* **Finding:** `archive.zip` contains `hinglish_cyberbullying_dataset_25000.csv` (25,000 rows).
* **Audit Result:** Empirical text deduplication revealed that **only 40 unique sentences exist** in the entire 25,000 rows. Each sentence was mechanically repeated ~1,000 times.
* **Decision:** Tagged as `CYBERGUARD-GENERATED SYNTHETIC / TILED` and marked **NOT SUITABLE** for training.
