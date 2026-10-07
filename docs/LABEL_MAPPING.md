# CYBERGUARD — LABEL NORMALIZATION & MAPPING DOCUMENTATION

**Document Version:** 2.0  
**Generated:** 2026-09-25T17:35:00Z  
**Standard:** Strict Domain Isolation, No Medical Diagnostics, Provenance Justification

---

## 1. CORE ARCHITECTURAL PRINCIPLE

CyberGuard strictly decouples **Cyberbullying Detection** from **Wellbeing Support Intelligence**. Under no circumstances are mental health conditions (such as depression, anxiety, or suicide) treated as labels inside the cyberbullying classifier, nor are cyberbullying categories merged into psychiatric taxonomies.

```text
                 CYBERGUARD ARCHITECTURE
                            |
           ┌────────────────┴────────────────┐
           |                                 |
           ↓                                 ↓
CYBERBULLYING DATA DOMAIN          WELLBEING DATA DOMAIN
(Age, Gender, Religion,            (Crisis Indicator, Stress,
 Ethnicity, Threat, Insult,         Distress, Coping Support)
 Appearance, Mockery, Harassment)            |
           |                                 ↓
           ↓                          SUPPORT MODELS
  CYBERBULLYING MODEL                        |
           |                                 ↓
           ↓                        RAG SUPPORT ENGINE
  EXPLAINABILITY (SHAP/LIME)        + SAFETY TRIAGE
           |                        (Helpline 14416 / 1930)
           └────────────────┬────────────────┘
                            ↓
                INTEGRATED INCIDENT REPORT
```

---

## 2. CYBERGUARD TARGET TAXONOMIES

### A. Cyberbullying Taxonomy (10 Classes)
1. **`Age-based`**: Harassment targeting minors, students, or elderly persons.
2. **`Gender-based`**: Misogyny, sexism, gender-based disparagement, or harassment.
3. **`Religion-based`**: Attacks against religious beliefs, practices, or faith communities.
4. **`Ethnicity-based`**: Racial slurs, xenophobic attacks, caste-based or ethnic abuse.
5. **`Appearance-based`**: Body shaming, facial insults, appearance-directed humiliation.
6. **`Mockery/Defamation`**: Belittling, ridicule, public shaming, character defamation.
7. **`Abusive/Insult`**: Profanities, vulgar slang, cursing (including Hindi/Hinglish *gaaliyan*).
8. **`Threat/Intimidation`**: Threats of physical violence, extortion, stalking, or bodily harm.
9. **`Personal Harassment`**: Persistent direct hostility, harassment, or interpersonal bullying.
10. **`Non-cyberbullying`**: Benign conversation, non-toxic discourse, neutral discussion.

### B. Wellbeing Support Taxonomy (3 Signals)
1. **Crisis Risk Indicator**:
   - `CRISIS_ESCALATION`: High-risk distress ideation triggering emergency hotline modal (Tele-MANAS 14416 / Cybercrime 1930).
   - `DEPRESSIVE_DISTRESS`: Deep emotional fatigue, hopelessness, or emotional pain requiring supportive RAG conversation.
   - `STANDARD_WELLBEING`: Balanced, neutral emotional state.
2. **Stress Level**: `LOW`, `MODERATE`, `HIGH`, `SEVERE`.
3. **Loss of Self (LoST) Cognitive Distortion**:
   - `LOSS_OF_SELF_DETECTED`: Self-worth erosion following online humiliation.
   - `NORMAL_AFFECT`: Intact self-concept.

> **CRITICAL POLICY:** Wellbeing outputs are presented as **support signals / triage indicators**, NEVER as clinical psychiatric or medical diagnoses.

---

## 3. MAPPING TYPES

| Mapping Type | Definition | Confidence Threshold | Action |
| :--- | :--- | :--- | :--- |
| **`DIRECT`** | 1-to-1 semantic and legal equivalence | 0.95 – 1.00 | Retain mapped label directly |
| **`SAFE_MERGE`** | Semantic subset with verifiable empirical alignment | 0.80 – 0.94 | Merge into broader target class with documentation |
| **`AUXILIARY`** | Multi-class or partial overlap feature | 0.60 – 0.79 | Use as secondary signal / feature expansion |
| **`UNMAPPED`** | Out-of-scope taxonomy | 0.00 – 0.59 | Quarantine from primary training pool |
| **`EXCLUDED`** | Defective, corrupted, or severely tiled data | 0.00 | Strictly excluded from training and evaluation |

---

## 4. COMPREHENSIVE DATASET MAPPING MATRIX

### Cyberbullying Corpora

| Dataset | Original Label | Definition | CyberGuard Target Class | Type | Conf. | Empirical Justification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Kaggle CB Tweets** | `religion` | Religious attacks | `Religion-based` | `DIRECT` | 1.00 | Exact 1:1 match across 7,998 samples. |
| **Kaggle CB Tweets** | `age` | Ageist harassment | `Age-based` | `DIRECT` | 1.00 | Exact 1:1 match across 7,992 samples. |
| **Kaggle CB Tweets** | `gender` | Sexist/misogynistic tweets | `Gender-based` | `DIRECT` | 1.00 | Exact 1:1 match across 7,973 samples. |
| **Kaggle CB Tweets** | `ethnicity` | Racial/ethnic slurs | `Ethnicity-based` | `DIRECT` | 1.00 | Exact 1:1 match across 7,961 samples. |
| **Kaggle CB Tweets** | `not_cyberbullying` | Benign tweets | `Non-cyberbullying` | `DIRECT` | 1.00 | Exact 1:1 match across 7,945 samples. |
| **Kaggle CB Tweets** | `other_cyberbullying` | General hostility | `Personal Harassment` | `SAFE_MERGE` | 0.85 | Manual inspection shows interpersonal harassment not fitting identity tags. |
| **CyberbullyX-63K** | `0` | Clean Hindi/EN tweet | `Non-cyberbullying` | `DIRECT` | 0.95 | Verified benign tweet stream. |
| **CyberbullyX-63K** | `1` | Harmful Hindi/EN tweet | `Abusive/Insult` | `SAFE_MERGE` | 0.80 | Lexical audit shows >75% insults, cursing, and derogatory expressions. |
| **Hinglish 18K** | `0` | Clean Hinglish text | `Non-cyberbullying` | `DIRECT` | 0.95 | Clean conversational Roman Hindi/English. |
| **Hinglish 18K** | `-1` | Vulgar/abusive Hinglish | `Abusive/Insult` | `SAFE_MERGE` | 0.90 | High density of Hindi curse words (*gaaliyan*) and vulgar slang. |
| **Jigsaw Train** | `threat` | Threats of violence | `Threat/Intimidation` | `DIRECT` | 0.95 | Direct alignment with intimidation/threat class. |
| **Jigsaw Train** | `insult` | Name-calling/insults | `Abusive/Insult` | `DIRECT` | 0.95 | Direct alignment with verbal abuse/insult class. |
| **Jigsaw Train** | `identity_hate` | Hate speech | `Ethnicity-based` | `AUXILIARY` | 0.70 | Kept auxiliary to prevent blurring religion/gender. |
| **MultiOFF Memes** | `0` (Non-offensive) | Benign meme | `Non-cyberbullying` | `DIRECT` | 0.95 | Multimodal benign baseline. |
| **MultiOFF Memes** | `1` (Offensive) | Offensive meme | `Abusive/Insult` | `SAFE_MERGE` | 0.85 | Multimodal offensive baseline. |
| **Synthetic Baseline**| 10 Native Classes | Target classes | `NATIVE_IDENTITY` | `DIRECT` | 1.00 | Created natively for CyberGuard taxonomy. |
| **Archive.zip 25K** | `0, 1` | 40 tiled sentences | `EXCLUDED` | `EXCLUDED` | 0.00 | 99.84% duplicate rate causes severe leakage. |

### Wellbeing Corpora

| Dataset | Original Label | Definition | CyberGuard Target Signal | Type | Conf. | Empirical Justification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Reddit Suicide/Dep**| `1` (`r/SuicideWatch`)| Acute crisis ideation | `CRISIS_ESCALATION` | `DIRECT` | 0.98 | Activates emergency hotline modal (14416 / 1930). |
| **Reddit Suicide/Dep**| `0` (`r/depression`) | Depressive rumination | `DEPRESSIVE_DISTRESS`| `DIRECT` | 0.95 | Empathetic wellbeing dialogue & consultant triage. |
| **Reddit LoST v1** | `1` | Loss of Self distortion| `LOSS_OF_SELF_DETECTED`| `DIRECT` | 0.95 | Cognitive reframing and grounding in support assistant. |
| **Reddit LoST v1** | `0` | Normal affect | `NORMAL_AFFECT` | `DIRECT` | 0.95 | Standard baseline conversation. |
| **Synthetic Prompts** | `LOW..SEVERE` | Stress scale | `NATIVE_IDENTITY` | `DIRECT` | 1.00 | Native stress severity calibration. |
| **GoEmotions** | All columns | Corrupt file (all NaN) | `EXCLUDED_CORRUPT` | `EXCLUDED` | 0.00 | Disk file contains zero non-null entries. |

---

## 5. SUMMARY OF LEAKAGE CONTROLS

1. **Partition Isolation:** Training and holdout partitions are split by unique text hash; no identical or near-duplicate texts can appear across both train and test.
2. **Exclusion of Tiled Artifacts:** `archive.zip` (40 sentences repeated 25,000 times) is strictly barred from all training data pipelines.
3. **Multimodal Split Protection:** Multimodal datasets (`MultiOFF`, `M3`, `Facebook Hateful Memes`) retain their official splits, with Facebook Hateful Memes strictly held out.
