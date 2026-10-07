# CYBERGUARD — COMPREHENSIVE DATASET CATALOG

**Version:** 2.0 (Post-Audit Expansion)
**Generated:** 2026-09-25T17:25:00Z
**Standard:** Non-Destructive Preservation, Strict Two-Domain Separation, Verifiable Provenance

---

## CYBERBULLYING DATASETS

### CyberbullyX-63K (`DS-CB-01`)
- **Dataset Version:** `CyberbullyX-63K-v1`
- **Local Path:** `C:\Users\vivek\Documents\aml\cyberbullying_dataset\CyberbullyX-63K.xlsx`
- **Source URL:** https://github.com/CyberBullyX / Twitter Stream API
- **Source Type:** `REAL_EXTERNAL`
- **Access Type / License:** `PUBLIC_ACADEMIC` / Research & Educational Use Only
- **Languages:** Hindi, English, Hinglish
- **Modality:** `TEXT_ONLY`
- **Record Count:** 63,145
- **Pipeline Status:** `AVAILABLE` (Training: `STAGED_FOR_EXPANDED_TRAINING`)
- **Original Labels:** 0, 1
- **Quality & Usability:** Clean real Twitter posts from June 2020 onwards; 60.7% Hindi/Hinglish, 39.1% English. Excellent linguistic diversity.

### Kaggle Cyberbullying Tweets (Wang et al.) (`DS-CB-02`)
- **Dataset Version:** `Kaggle-CB-Tweets-v1`
- **Local Path:** `C:\Users\vivek\Documents\aml\cyberbullying_dataset\kaggledataset.zip::cyberbullying_tweets.csv`
- **Source URL:** https://www.kaggle.com/datasets/andrewmvd/cyberbullying-classification
- **Source Type:** `REAL_EXTERNAL`
- **Access Type / License:** `OPEN_PUBLIC` / CC0: Public Domain
- **Languages:** English
- **Modality:** `TEXT_ONLY`
- **Record Count:** 47,692
- **Pipeline Status:** `AVAILABLE` (Training: `STAGED_FOR_EXPANDED_TRAINING`)
- **Original Labels:** religion, age, gender, ethnicity, not_cyberbullying, other_cyberbullying
- **Quality & Usability:** Balanced 6-class distribution (~7,950 records per class). 1,701 natural retweets to be deduplicated.

### Hinglish Codemixed Cyberbullying (Paper 4989) (`DS-CB-03`)
- **Dataset Version:** `Hinglish-Codemixed-18K-v1`
- **Local Path:** `C:\Users\vivek\Documents\aml\cyberbullying_dataset\final_dataset_hinglish.csv`
- **Source URL:** Academic Paper: Cyberbullying Detection in a Multi-classification Codemixed Dataset (4989-10831-1-PB.pdf)
- **Source Type:** `REAL_EXTERNAL`
- **Access Type / License:** `PUBLIC_ACADEMIC` / Research Open Access
- **Languages:** Hinglish, English
- **Modality:** `TEXT_ONLY`
- **Record Count:** 18,148
- **Pipeline Status:** `AVAILABLE` (Training: `STAGED_FOR_EXPANDED_TRAINING`)
- **Original Labels:** -1, 0
- **Quality & Usability:** 17,065 unique comments capturing genuine Indian social media slang, abusive lexicon, and code-mixing.

### Jigsaw Toxic Comment Classification Challenge (Train) (`DS-CB-04`)
- **Dataset Version:** `Jigsaw-Toxic-Train-v1`
- **Local Path:** `C:\Users\vivek\Documents\aml\cyberbullying_dataset\archive (1).zip::train.csv`
- **Source URL:** https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge
- **Source Type:** `REAL_EXTERNAL`
- **Access Type / License:** `OPEN_PUBLIC` / CC0: Public Domain
- **Languages:** English
- **Modality:** `TEXT_ONLY`
- **Record Count:** 159,571
- **Pipeline Status:** `AUXILIARY` (Training: `STAGED_FOR_AUXILIARY_FEATURE_EXPANSION`)
- **Original Labels:** toxic, severe_toxic, obscene, threat, insult, identity_hate
- **Quality & Usability:** Benchmark scale (159,571 comments). Threat (478) and Insult (7,877) directly align with CyberGuard Threat/Intimidation and Abusive/Insult classes.

### Jigsaw Toxic Comment Classification Challenge (Test & Labels) (`DS-CB-05`)
- **Dataset Version:** `Jigsaw-Toxic-Test-v1`
- **Local Path:** `C:\Users\vivek\Documents\aml\cyberbullying_dataset\archive (1).zip::test.csv & test_labels.csv`
- **Source URL:** https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge
- **Source Type:** `REAL_EXTERNAL`
- **Access Type / License:** `OPEN_PUBLIC` / CC0: Public Domain
- **Languages:** English
- **Modality:** `TEXT_ONLY`
- **Record Count:** 153,164
- **Pipeline Status:** `EVALUATION_ONLY` (Training: `EXCLUDED_FROM_TRAINING`)
- **Original Labels:** toxic, severe_toxic, obscene, threat, insult, identity_hate
- **Quality & Usability:** Official Kaggle competition holdout (63,978 scored labels, 89,186 masked).

### MultiOFF Multimodal Meme Benchmark (`DS-CB-06`)
- **Dataset Version:** `MultiOFF-v1`
- **Local Path:** `data\external\multioff\multioff_catalog.csv`
- **Source URL:** https://huggingface.co/datasets/Ibrahim-Alam/multi-modal_offensive_meme / COLING TRAC-2 2020
- **Source Type:** `REAL_EXTERNAL`
- **Access Type / License:** `PUBLIC_ACADEMIC` / Research & Academic Use (TRAC-2 / COLING 2020)
- **Languages:** English
- **Modality:** `IMAGE_AND_TEXT`
- **Record Count:** 740
- **Pipeline Status:** `AVAILABLE` (Training: `TRAINED_IN_CB_MM_001`)
- **Original Labels:** 0, 1
- **Quality & Usability:** 740 real image files verified on disk in data/external/multioff/images/ with corresponding OCR text.

### M3 Twitter Multimodal Memes (`DS-CB-07`)
- **Dataset Version:** `M3-Twitter-v1`
- **Local Path:** `data\external\m3\m3_catalog.csv`
- **Source URL:** https://github.com/mira-ai-lab/M3 (ArXiv 2404.14818)
- **Source Type:** `REAL_EXTERNAL`
- **Access Type / License:** `OPEN_PUBLIC` / MIT License
- **Languages:** English, Mixed
- **Modality:** `IMAGE_AND_TEXT`
- **Record Count:** 526
- **Pipeline Status:** `AVAILABLE` (Training: `TRAINED_IN_CB_MM_001`)
- **Original Labels:** normal, hate, racism, sexism, religion
- **Quality & Usability:** 150 physical images on disk in data/external/m3/img/; 376 text records.

### Facebook Hateful Memes (Dev Split) (`DS-CB-08`)
- **Dataset Version:** `Facebook-Hateful-Memes-Dev-v1`
- **Local Path:** `data\external\hateful_memes\hateful_memes_catalog.csv`
- **Source URL:** https://huggingface.co/datasets/neuralcatcher/hateful_memes / Meta AI NeurIPS 2020
- **Source Type:** `REAL_EXTERNAL`
- **Access Type / License:** `RESTRICTED_RESEARCH` / Meta AI Research Agreement
- **Languages:** English
- **Modality:** `IMAGE_AND_TEXT`
- **Record Count:** 500
- **Pipeline Status:** `HOLDOUT` (Training: `EXCLUDED_FROM_TRAINING`)
- **Original Labels:** 0, 1
- **Quality & Usability:** 150 physical images on disk in data/external/hateful_memes/img/. Rigorously isolated from all training pools.

### Synthetic CyberGuard Multilingual Baseline (`DS-CB-09`)
- **Dataset Version:** `Synthetic-CyberGuard-v1`
- **Local Path:** `data\raw\cyberbullying_multilingual_raw.csv`
- **Source URL:** Internal CyberGuard Dataset Generator (scripts/generate_rich_dataset.py)
- **Source Type:** `CYBERGUARD_SYNTHETIC`
- **Access Type / License:** `INTERNAL` / Internal Project License
- **Languages:** English, Hindi, Hinglish
- **Modality:** `TEXT_ONLY`
- **Record Count:** 2,036
- **Pipeline Status:** `AVAILABLE` (Training: `TRAINED_AS_BASELINE`)
- **Original Labels:** Age-based, Gender-based, Religion-based, Ethnicity-based, Appearance-based, Mockery/Defamation, Abusive/Insult, Threat/Intimidation, Personal Harassment, Non-cyberbullying
- **Quality & Usability:** Controlled benchmark preserving coverage across all 10 CyberGuard classes in English, Hindi, and Hinglish.

### Zenodo Multimodal Toxic Memes (`DS-CB-10`)
- **Dataset Version:** `Zenodo-Toxic-Memes-v1`
- **Local Path:** `data\external\zenodo_toxic_memes\labels.csv`
- **Source URL:** https://zenodo.org/records/8306439
- **Source Type:** `REAL_EXTERNAL`
- **Access Type / License:** `OPEN_PUBLIC` / CC-BY 4.0
- **Languages:** Russian
- **Modality:** `IMAGE_AND_TEXT`
- **Record Count:** 1,998
- **Pipeline Status:** `AUXILIARY` (Training: `EXCLUDED_LANGUAGE_OUT_OF_SCOPE`)
- **Original Labels:** 0, 1
- **Quality & Usability:** Russian Cyrillic text. Monolingual Russian is outside the current target scope (English, Hindi, Hinglish).

### Archive.zip Hinglish 25K (40 Tiled Templates) (`DS-CB-11`)
- **Dataset Version:** `Archive-Hinglish-25K-TILED-INVALID`
- **Local Path:** `C:\Users\vivek\Documents\aml\cyberbullying_dataset\archive.zip::hinglish_cyberbullying_dataset_25000.csv`
- **Source URL:** Unverified Kaggle upload in archive.zip
- **Source Type:** `CYBERGUARD_SYNTHETIC_TILED`
- **Access Type / License:** `UNVERIFIED` / UNKNOWN / UNVERIFIED
- **Languages:** Hinglish, English
- **Modality:** `TEXT_ONLY`
- **Record Count:** 25,000
- **Pipeline Status:** `EXCLUDED` (Training: `STRICTLY_PROHIBITED_FROM_TRAINING`)
- **Original Labels:** 0, 1
- **Quality & Usability:** CRITICAL FLAW: Exactly 40 unique template sentences repeated 25,000 times (1,000x each). Guaranteed severe leakage and overfitting.

### OffensEval / OLID (Zampieri et al.) (`DS-NEW-01`)
- **Dataset Version:** `OLID-2019-v1`
- **Local Path:** `EXTERNAL_PUBLIC_REPOSITORY`
- **Source URL:** https://huggingface.co/datasets/tasksource/olid / SemEval-2019 Task 6
- **Source Type:** `REAL_EXTERNAL`
- **Access Type / License:** `OPEN_PUBLIC` / Research & Educational Use Only
- **Languages:** English
- **Modality:** `TEXT_ONLY`
- **Record Count:** 14,100
- **Pipeline Status:** `AVAILABLE` (Training: `CANDIDATE_FOR_FUTURE_EXPANSION`)
- **Original Labels:** OFF, NOT, TIN, UNT, IND, GRP, OTH
- **Quality & Usability:** Classic SemEval gold standard. Label 'IND' (individual targeted) directly corresponds to Personal Harassment.

### HateXplain (Mathew et al.) (`DS-NEW-02`)
- **Dataset Version:** `HateXplain-v1`
- **Local Path:** `EXTERNAL_PUBLIC_REPOSITORY`
- **Source URL:** https://github.com/hate-alert/HateXplain / AAAI 2021
- **Source Type:** `REAL_EXTERNAL`
- **Access Type / License:** `OPEN_PUBLIC` / MIT License
- **Languages:** English
- **Modality:** `TEXT_ONLY`
- **Record Count:** 20,148
- **Pipeline Status:** `AVAILABLE` (Training: `CANDIDATE_FOR_EXPLAINABILITY_BENCHMARK`)
- **Original Labels:** hate, offensive, normal
- **Quality & Usability:** Contains word-level rationale annotations (highlighted toxic spans) ideal for evaluating XAI attribution.

### PolEval 2019 Shared Task 6 (`DS-NEW-05`)
- **Dataset Version:** `PolEval-2019-UNAVAILABLE`
- **Local Path:** `NOT_FOUND_IN_LOCAL_DIRECTORIES`
- **Source URL:** Ptaszynski et al., PolEval 2019 Workshop
- **Source Type:** `REAL_EXTERNAL`
- **Access Type / License:** `OPEN_PUBLIC` / Open Research Evaluation (PolEval 2019)
- **Languages:** Polish
- **Modality:** `TEXT_ONLY`
- **Record Count:** 0
- **Pipeline Status:** `UNAVAILABLE` (Training: `EXCLUDED_NOT_FOUND_LOCALLY`)
- **Original Labels:** 0, 1, harmful, attack, non_harmful
- **Quality & Usability:** Not found in supplied local directories. Polish language is out-of-scope for CyberGuard's English/Hindi/Hinglish focus.

## WELLBEING DATASETS

### Reddit LoST v1 (Loss of Self Theory) (`DS-WB-01`)
- **Dataset Version:** `Reddit-LoST-v1`
- **Local Path:** `C:\Users\vivek\Documents\aml\mental\LoSTv1.csv`
- **Source URL:** Academic Research: Modeling Loss of Self in Mental Health Communities
- **Source Type:** `REAL_EXTERNAL`
- **Access Type / License:** `PUBLIC_ACADEMIC` / Academic Research Use Only
- **Languages:** English
- **Modality:** `TEXT_ONLY`
- **Record Count:** 3,251
- **Pipeline Status:** `AVAILABLE` (Training: `STAGED_FOR_SUPPORT_MODEL_TRAINING`)
- **Original Labels:** 0.0, 1.0
- **Quality & Usability:** Narrative confessional text (mean length 892 chars). Ideal for training empathetic distress detection.

### Reddit LoST Final Train (Cognitive Spans) (`DS-WB-02`)
- **Dataset Version:** `Reddit-LoST-Train-v1`
- **Local Path:** `C:\Users\vivek\Documents\aml\mental\final_train.csv`
- **Source URL:** Academic Research: LoST Cognitive Attribution
- **Source Type:** `REAL_EXTERNAL`
- **Access Type / License:** `PUBLIC_ACADEMIC` / Academic Research Use Only
- **Languages:** English
- **Modality:** `TEXT_ONLY`
- **Record Count:** 1,739
- **Pipeline Status:** `AVAILABLE` (Training: `STAGED_FOR_SUPPORT_MODEL_TRAINING`)
- **Original Labels:** 0, 1
- **Quality & Usability:** High-value annotated spans for grounding AI wellbeing responses in victim trigger analysis.

### Reddit LoST Final Test (Cognitive Spans) (`DS-WB-03`)
- **Dataset Version:** `Reddit-LoST-Test-v1`
- **Local Path:** `C:\Users\vivek\Documents\aml\mental\final_test.csv`
- **Source URL:** Academic Research: LoST Cognitive Attribution
- **Source Type:** `REAL_EXTERNAL`
- **Access Type / License:** `PUBLIC_ACADEMIC` / Academic Research Use Only
- **Languages:** English
- **Modality:** `TEXT_ONLY`
- **Record Count:** 435
- **Pipeline Status:** `HOLDOUT` (Training: `EXCLUDED_FROM_TRAINING`)
- **Original Labels:** 0, 1
- **Quality & Usability:** Official benchmark holdout split for the LoST study.

### Reddit Suicide vs. Depression (`DS-WB-04`)
- **Dataset Version:** `Reddit-Crisis-Triage-v1`
- **Local Path:** `C:\Users\vivek\Documents\aml\mental\combined-set.csv`
- **Source URL:** Reddit API Scrape / SuicideWatch & depression Subreddits
- **Source Type:** `REAL_EXTERNAL`
- **Access Type / License:** `PUBLIC_ACADEMIC` / Research & Educational Use Only
- **Languages:** English
- **Modality:** `TEXT_ONLY`
- **Record Count:** 1,895
- **Pipeline Status:** `AVAILABLE` (Training: `STAGED_FOR_CRISIS_ESCALATION_TRAINING`)
- **Original Labels:** 0, 1
- **Quality & Usability:** Crucial for safety triage: triggers hotline modal (Tele-MANAS 14416 / 1930) when acute crisis is detected in support chat.

### GoEmotions Affective Emotion Subset (`DS-WB-05`)
- **Dataset Version:** `GoEmotions-Subset-v1`
- **Local Path:** `C:\Users\vivek\Documents\aml\mental\goemotions_1-selected-columns.csv`
- **Source URL:** https://github.com/google-research/google-research/tree/master/goemotions
- **Source Type:** `REAL_EXTERNAL`
- **Access Type / License:** `OPEN_PUBLIC` / Apache 2.0
- **Languages:** English
- **Modality:** `TEXT_ONLY`
- **Record Count:** 21,039
- **Pipeline Status:** `AUXILIARY` (Training: `STAGED_FOR_RAG_EMPATHY_ALIGNMENT`)
- **Original Labels:** admiration, example_very_unclear
- **Quality & Usability:** Google Research benchmark for emotional sentiment alignment in support conversations.

### Synthetic Support Wellbeing Prompts (`DS-WB-06`)
- **Dataset Version:** `Synthetic-Support-v1`
- **Local Path:** `data\raw\support_wellbeing_raw.csv`
- **Source URL:** Internal CyberGuard Wellbeing Calibration
- **Source Type:** `CYBERGUARD_SYNTHETIC`
- **Access Type / License:** `INTERNAL` / Internal Project License
- **Languages:** English
- **Modality:** `TEXT_ONLY`
- **Record Count:** 70
- **Pipeline Status:** `AVAILABLE` (Training: `TRAINED_AS_BASELINE`)
- **Original Labels:** LOW, MODERATE, HIGH, SEVERE
- **Quality & Usability:** Minimal baseline prompt set for stress severity classifier.

### Dreaddit (Turcan & McKeown) (`DS-NEW-03`)
- **Dataset Version:** `Dreaddit-v1`
- **Local Path:** `EXTERNAL_PUBLIC_REPOSITORY`
- **Source URL:** https://github.com/elena-orlova/dreaddit / EMNLP 2019
- **Source Type:** `REAL_EXTERNAL`
- **Access Type / License:** `OPEN_PUBLIC` / Academic Research Use
- **Languages:** English
- **Modality:** `TEXT_ONLY`
- **Record Count:** 3,553
- **Pipeline Status:** `AVAILABLE` (Training: `CANDIDATE_FOR_STRESS_EXPANSION`)
- **Original Labels:** 0, 1
- **Quality & Usability:** Gold-standard academic benchmark for social media stress detection.

### DAIC-WOZ (Distress Analysis Interview Corpus) (`DS-NEW-04`)
- **Dataset Version:** `DAIC-WOZ-RESTRICTED`
- **Local Path:** `RESTRICTED_USC_ICT_REPOSITORY`
- **Source URL:** https://dcapswoz.ict.usc.edu/
- **Source Type:** `REAL_EXTERNAL`
- **Access Type / License:** `RESTRICTED` / Restricted Institutional Research Agreement
- **Languages:** English
- **Modality:** `AUDIO_AND_TRANSCRIPT`
- **Record Count:** 189
- **Pipeline Status:** `RESTRICTED` (Training: `EXCLUDED_RESTRICTED_ACCESS`)
- **Original Labels:** PHQ-8 Score, Depression, PTSD
- **Quality & Usability:** Clinical diagnostic interviews. Excluded due to ethical non-diagnosis policy and restricted institutional licensing.

## EXCLUDED & QUARANTINED DATASETS

### Archive.zip Hinglish 25K (40 Tiled Templates) (`DS-CB-11`)
- **Local Path:** `C:\Users\vivek\Documents\aml\cyberbullying_dataset\archive.zip::hinglish_cyberbullying_dataset_25000.csv`
- **Reason for Exclusion:** CRITICAL FLAW: Exactly 40 unique template sentences repeated 25,000 times (1,000x each). Guaranteed severe leakage and overfitting.
- **Directive:** Strictly excluded from all training and evaluation pools.

## RESTRICTED / UNAVAILABLE DATASETS

### DAIC-WOZ (Distress Analysis Interview Corpus) (`DS-NEW-04`)
- **Status:** `RESTRICTED`
- **License / Access Note:** Requires formal USC-ICT institutional data use agreement.
- **Policy:** CyberGuard does not bypass institutional or legal access controls.

### PolEval 2019 Shared Task 6 (`DS-NEW-05`)
- **Status:** `UNAVAILABLE`
- **License / Access Note:** Open research evaluation.
- **Policy:** CyberGuard does not bypass institutional or legal access controls.

