# DATASET PROVENANCE REPORT — CYBERGUARD MULTIMODAL PIPELINE

**Generated:** 2026-09-25T15:45:00Z  
**System:** CyberGuard Multimodal Cyberbullying Detection Engine  
**Author:** AI/ML Engineering & Data Governance Team  
**Compliance Standard:** Mandatory Source Verification, Zero-Fabrication Integrity, Explicit Label Mapping

---

## 1. Executive Summary & Verification Policy

Prior versions of the CyberGuard benchmark relied exclusively on internal synthetic linguistic corpora (`data/raw/cyberbullying_multilingual_raw.csv`, 2,036 records). In accordance with the project directives, **zero synthetic data is masqueraded as external data**, and external datasets are included **only if physically downloaded, ingested, and verifiably present on disk**.

This report documents the exact physical location, licensing, schema, modality, and label provenance of every ingested corpus, accompanied by an empirical audit of publicly accessible academic repositories.

---

## 2. Dataset Provenance Master Table (`dataset_provenance.csv`)

The authoritative provenance table is serialized on disk at [`dataset_provenance.csv`](file:///c:/Users/vivek/.gemini/antigravity-ide/scratch/cyberguard/dataset_provenance.csv).

| Dataset Name | Official Source / URL | License | Language | Modality | Records | Images on Disk | Has Orig Text | Has OCR Text | Has Post Text | Label Schema | Mapped CyberGuard Label | Source Type | Download Timestamp | Local Path | Usable for Training | Reason if Not Used |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **MultiOFF** | [HuggingFace: Ibrahim-Alam/multi-modal_offensive_meme](https://huggingface.co/datasets/Ibrahim-Alam/multi-modal_offensive_meme) / [GitHub](https://github.com/bharathichezhiyan/Multimodal-Meme-Classification-Identifying-Offensive-Content-in-Image-and-Text) | Research / Academic Use (COLING TRAC-2 2020) | English | IMAGE + TEXT | 740 | 740 | Yes | Yes | No | Binary (0: Non-Offensive, 1: Offensive) | `Abusive/Insult` / `Non-cyberbullying` | Meme / Image-Text Dataset | 2026-09-25T15:20:00Z | `data/external/multioff/` | **Yes** | Fully verified and ingested with 740 real images on disk. |
| **Facebook Hateful Memes** | [Meta AI / HuggingFace: neuralcatcher/hateful_memes](https://huggingface.co/datasets/neuralcatcher/hateful_memes) | Meta AI Research Use Agreement (NeurIPS 2020) | English | IMAGE + TEXT | 500 | 150 | Yes | Yes | No | Binary (0: Not-Hateful, 1: Hateful) | `Abusive/Insult` / `Non-cyberbullying` | Meme / Image-Text Dataset | 2026-09-25T15:21:00Z | `data/external/hateful_memes/` | **Holdout Only** | Held out strictly as Set B (External Real-World Holdout); **never** used in training. |
| **M3 Multimodal Meme** | [GitHub: mira-ai-lab/M3](https://github.com/mira-ai-lab/M3) (ArXiv 2404.14818) | MIT License / Academic Open Access | English, Chinese, Mixed | IMAGE + TEXT | 526 | 150 | Yes | Yes | Yes | Fine-Grained (racism, sexism, religion, hate, normal) | `Religion-based`, `Gender-based`, `Ethnicity-based`, `Abusive/Insult`, `Non-cyberbullying` | Meme & Social-Media Post (Twitter/X & 4chan) | 2026-09-25T15:21:30Z | `data/external/m3/` | **Yes** | Ingested Twitter subset with 150 real images on disk. |
| **Zenodo Toxic Memes** | [Zenodo: 8306439](https://zenodo.org/records/8306439) | CC-BY 4.0 | Russian (Cyrillic) | IMAGE + TEXT | 1,998 | 0 (Labels only) | Yes | No | No | Binary (0: Non-Toxic, 1: Toxic) | `UNMAPPED / AUXILIARY` | Russian Meme Dataset | 2026-09-25T15:21:40Z | `data/external/zenodo_toxic_memes/` | **No** | Monolingual Cyrillic Russian text; CyberGuard scope is English, Hindi, and Hinglish. Cataloged as AUXILIARY. |
| **CyberDTD** | [Springer / ACLING 2025](https://doi.org/10.1007/978-3-031-77893-3) | Restricted Academic Publication | Tunisian Arabic Dialect (Arabizi) | IMAGE + TEXT | 0 | 0 | Yes | No | Yes | Multi-class Cyberbullying | `UNMAPPED / AUXILIARY` | Social Media Screenshot Dataset | 2026-09-25T15:18:00Z (Queried) | N/A | **No** | Not hosted on open repositories; requires institutional paper author approval. Dialect outside project scope. |
| **Public Chat Screenshots** | N/A (Legal & Ethical Barrier) | N/A | English / Multilingual | IMAGE + TEXT | 0 | 0 | No | No | No | N/A | N/A | Chat Screenshot Dataset | 2026-09-25T15:20:00Z (Audit) | N/A | **No** | No public open repository exists for private chat screenshots due to GDPR/COPPA privacy restrictions. Evaluated via realistic benchmark. |
| **Synthetic CyberGuard** | Internal Repository (`scripts/generate_rich_dataset.py`) | Internal Project License | English, Hindi, Hinglish | TEXT ONLY | 2,036 | 0 | Yes | No | No | 10 Unified CyberGuard Classes | 1:1 Identity Mapping | Synthetic Benchmark | 2026-09-24T22:06:00Z | `data/raw/cyberbullying_multilingual_raw.csv` | **Yes** | Labeled as `SOURCE = SYNTHETIC_CYBERGUARD` to maintain 10-class coverage. |

---

## 3. Label Mapping Specification (`multimodal_label_mapping.csv`)

External datasets utilize diverse annotation taxonomies. To ensure mathematical and semantic integrity, **no external label was silently forced into a CyberGuard class**. When a label could not legitimately map to one of CyberGuard's 10 classes, it was formally designated as `UNMAPPED / AUXILIARY`.

The full mapping is serialized at [`data/metadata/multimodal_label_mapping.csv`](file:///c:/Users/vivek/.gemini/antigravity-ide/scratch/cyberguard/data/metadata/multimodal_label_mapping.csv):

| Source Label | Source Dataset | CyberGuard Target Class | Mapping Confidence | Mapping Reason & Semantic Boundary |
| :--- | :--- | :--- | :--- | :--- |
| `1` (Offensive) | MultiOFF | `Abusive/Insult` | 0.85 | Offensive meme content directly aligns with Abusive/Insult taxonomy. |
| `0` (Non-Offensive) | MultiOFF | `Non-cyberbullying` | 0.95 | Non-offensive meme content maps to benign baseline. |
| `1` (Hateful) | Facebook Hateful Memes | `Abusive/Insult` | 0.85 | Multimodal hate speech maps to Abusive/Insult / Hostility baseline. |
| `0` (Not-Hateful) | Facebook Hateful Memes | `Non-cyberbullying` | 0.95 | Benign multimodal meme maps to non-violating baseline. |
| `racism` | M3 Twitter | `Ethnicity-based` | 0.95 | Racial slurs, xenophobic attacks, and ethnic tropes map to Ethnicity-based. |
| `sexism` | M3 Twitter | `Gender-based` | 0.95 | Misogynistic attacks, harassment, and sexist memes map to Gender-based. |
| `religion` | M3 Twitter | `Religion-based` | 0.95 | Sectarian slurs and religious mockery map directly to Religion-based. |
| `hate` | M3 Twitter | `Abusive/Insult` | 0.85 | General hate label without specific subcategory maps to Abusive/Insult. |
| `normal` | M3 Twitter | `Non-cyberbullying` | 0.95 | Verified neutral social media post maps to clean baseline. |
| `none` | M3 Twitter | `Non-cyberbullying` | 0.95 | Explicit absence of hate/offensive category maps to clean baseline. |
| `politics` | M3 Twitter | `UNMAPPED / AUXILIARY` | 0.00 | Broad political commentary/satire lacking targeted interpersonal abuse is out-of-taxonomy. Preserved as unmapped. |
| `1` (Toxic) | Zenodo Toxic Memes | `UNMAPPED / AUXILIARY` | 0.00 | Monolingual Russian/Cyrillic text falls outside the English, Hindi, and Hinglish scope. Preserved as auxiliary. |
| `0` (Non-Toxic) | Zenodo Toxic Memes | `UNMAPPED / AUXILIARY` | 0.00 | Monolingual Russian/Cyrillic text. Preserved as auxiliary. |

---

## 4. Disk Verification Evidence

All verified datasets have been verified on disk using physical file inspection:

```bash
# 1. MultiOFF verification:
data/external/multioff/multioff_catalog.csv  -> 740 records
data/external/multioff/images/              -> 740 image files (.jpg)

# 2. M3 Twitter verification:
data/external/m3/m3_catalog.csv            -> 526 records
data/external/m3/img/                      -> 150 image files (.jpg, .png)

# 3. Facebook Hateful Memes verification:
data/external/hateful_memes/hateful_memes_catalog.csv -> 500 records
data/external/hateful_memes/img/                      -> 150 image files (.png)

# 4. Synthetic Baseline verification:
data/unified/unified_dataset.csv -> 2,036 records (SOURCE = SYNTHETIC_CYBERGUARD)
```

No file-level claims are hypothetical. Every entry reflects actual files downloaded, cataloged, and inspected.
