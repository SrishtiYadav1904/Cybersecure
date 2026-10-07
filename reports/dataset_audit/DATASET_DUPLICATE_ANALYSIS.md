# DATASET DUPLICATE & OVERLAP ANALYSIS — READ-ONLY AUDIT

**Audit Date:** 2026-09-25T16:28:00Z  
**Project:** CyberGuard Multilingual Cyberbullying Detection Engine  
**Audit Scope:** Intra-Dataset Redundancy, Cross-Dataset Overlaps, Synthetic Tiling, Perceptual Hashing  
**Action:** READ-ONLY DISCOVERY (Zero files modified, deleted, or merged)  

---

## 1. Executive Summary of Duplication Findings

Our empirical audit identified three distinct duplication profiles across the audited corpora:

1. **Catastrophic Synthetic Tiling:** In `archive.zip` (`hinglish_cyberbullying_dataset_25000.csv`), an extreme duplication rate of **99.84%** was discovered: exactly **40 unique sentences were duplicated across 25,000 rows**.
2. **Natural Retweet/Repetition in Social Media:** Datasets collected from Twitter (`cyberbullying_tweets.csv`, `CyberbullyX-63K.xlsx`) contain natural duplicate rates between **0.68% and 3.57%**, reflecting viral retweets, bot quotes, and standard conversational replies.
3. **Cross-Corpus Independence:** The internally synthesized CyberGuard baseline (`cyberbullying_multilingual_raw.csv`, 2,036 rows) has **0 text overlaps** with Kaggle Tweets, CyberbullyX, or the Hinglish codemixed corpora, proving that synthetic samples were not plagiarized from external benchmarks.

---

## 2. Intra-Dataset Exact Duplication Table

| Dataset Identifier | File Format | Total Records | Unique Texts | Exact Duplicate Count | Duplicate Percentage | Primary Nature of Duplication |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`archive.zip::hinglish_25k`** | Zipped CSV | 25,000 | **40** | **24,960** | **99.84%** | **MECHANICAL TILING:** 40 template sentences duplicated ~1,000 times each. |
| **`kaggledataset.zip::tweets`** | Zipped CSV | 47,692 | 45,991 | **1,701** | **3.57%** | **TWITTER RE-TWEETS:** Viral bullying copypastas and broadcast quotes. |
| **`final_dataset_hinglish.csv`**| CSV | 18,148 | 17,065 | **1,083** | **5.97%** | **YOUTUBE/TWITTER ECHOES:** Repeated insults in comment threads (`carry ki maa ki chut`). |
| **`CyberbullyX-63K.xlsx`** | Excel | 63,145 | 62,713 | **432** | **0.68%** | **MINIMAL DUPLICATION:** Highly clean unique tweet stream. |
| **`Jigsaw train.csv`** | Zipped CSV | 159,571 | 159,571 | **0** | **0.00%** | **UNIQUE WIKIPEDIA EDITS:** Each comment corresponds to a distinct talk page revision. |
| **`MultiOFF Memes`** | CSV + Images | 740 | 738 | **2** | **0.27%** | **MEME TEMPLATES:** Minor duplicate caption texts across image variants. |
| **`M3 Twitter Memes`** | CSV + Images | 526 | 508 | **18** | **3.42%** | **VIRAL POST RESHARES:** Same meme graphic shared with identical captions. |
| **`Facebook Hateful Memes`** | CSV + Images | 500 | 500 | **0** | **0.00%** | **CURATED BENCHMARK:** Unique multimodal pairs. |
| **`Synthetic CyberGuard`** | CSV | 2,036 | 2,036 | **0** | **0.00%** | **CONTROLLED GENERATION:** Distinct synthesized sentences. |
| **`Reddit LoST v1`** | CSV | 3,251 | 3,212 | **39** | **1.20%** | **CROSS-POSTS:** Reddit users posting identical distress narratives to multiple subreddits. |

---

## 3. The `archive.zip` 40-Sentence Tiling Breakdown

To provide transparent evidence of the mechanical generation in `archive.zip::hinglish_cyberbullying_dataset_25000.csv`:

| Rank | Sentence Text | Frequency in Dataset | Original Label | Language | Nature |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `"Nice effort, proud of you."` | 1,046 | `0` | English | Positive Template |
| 2 | `"Tujhe sharam nahi aati?"` | 1,045 | `1` | Hinglish | Insult Template |
| 3 | `"You're awesome!"` | 1,034 | `0` | English | Positive Template |
| 4 | `"Bakwas band kar."` | 1,032 | `1` | Hinglish | Insult Template |
| 5 | `"Kamaal kar diya bhai!"` | 1,032 | `0` | Hinglish | Positive Template |
| 6 | `"Itna irritating koi kaise ho sakta hai?"` | 1,019 | `1` | Hinglish | Insult Template |
| 7 | `"You're such a loser yaar."` | 1,016 | `1` | Hinglish | Insult Template |
| 8 | `"Thanks for your support yaar."` | 1,010 | `0` | Hinglish | Positive Template |
| 9 | `"Tum jaise logon se baat nahi karte."` | 996 | `1` | Hinglish | Insult Template |
| 10 | `"Bas kar nautanki, dimag kharab kar diya."`| 994 | `1` | Hinglish | Insult Template |
| 11 | `"Tu pagal ho gaya hai kya?"` | 993 | `1` | Hinglish | Insult Template |
| 12 | `"Teri aukaat kya hai samjhta hai?"` | 992 | `1` | Hinglish | Insult Template |
| 13 | `"Good job, well done!"` | 992 | `0` | English | Positive Template |
| 14 | `"Tum bahut accha kaam karte ho."` | 989 | `0` | Hinglish | Positive Template |
| 15 | `"You're one of the kindest souls I know."` | 983 | `0` | English | Positive Template |

**Audit Recommendation:** This dataset is **NOT SUITABLE** for training or evaluation. If ingested, it would drastically overfit on these 40 trivial sentences and ruin real-world generalization.

---

## 4. Cross-Dataset Overlap & Plagiarism Analysis

We computed set intersections of normalized text strings across all major datasets:

| Comparison Pair | Dataset A Unique Texts | Dataset B Unique Texts | Overlapping Texts | Overlap % | Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Synthetic CyberGuard vs. Kaggle Tweets** | 2,036 | 45,991 | **0** | 0.00% | Completely Independent |
| **Synthetic CyberGuard vs. CyberbullyX-63K** | 2,036 | 62,713 | **0** | 0.00% | Completely Independent |
| **Synthetic CyberGuard vs. Hinglish 18K** | 2,036 | 17,065 | **0** | 0.00% | Completely Independent |
| **CyberbullyX-63K vs. Hinglish 18K** | 62,713 | 17,065 | **1** (`"shut up"`) | <0.001% | Independent Corpora |
| **Kaggle Tweets vs. CyberbullyX-63K** | 45,991 | 62,713 | **1** (`"hello"`) | <0.001% | Independent Corpora |

**Conclusion:** The available datasets are genuine, distinct collections. There is zero evidence of cross-corpus contamination or circular copying.

---

## 5. Multimodal Perceptual Hash (`dHash`) Duplicate Analysis

For the multimodal image datasets:
* **MultiOFF:** 740 images analyzed. 735 unique 64-bit difference hashes (`dHash`). Found 5 template duplicate pairs (e.g., Donald Trump debate still used with slightly different text overlays).
* **M3 Twitter:** 150 images on disk analyzed. 147 unique hashes (3 duplicate meme templates).
* **Facebook Hateful Memes:** 150 images on disk analyzed. 150 unique hashes (0 duplicate images).
