import os
import csv
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def generate_provenance_and_mapping():
    # 1. Dataset Provenance Table
    provenance_data = [
        {
            "dataset_name": "MultiOFF",
            "official_source_url": "https://huggingface.co/datasets/Ibrahim-Alam/multi-modal_offensive_meme / https://github.com/bharathichezhiyan/Multimodal-Meme-Classification-Identifying-Offensive-Content-in-Image-and-Text",
            "license": "Research & Academic Use (COLING TRAC-2 2020)",
            "language": "English",
            "modality": "IMAGE_AND_TEXT",
            "number_of_records": 740,
            "number_of_images": 740,
            "has_original_text": True,
            "has_OCR_text": True,
            "has_post_text": False,
            "label_schema": "Binary (0: Non-Offensive, 1: Offensive)",
            "mapped_CyberGuard_label": "Abusive/Insult (if offensive) / Non-cyberbullying (if non-offensive)",
            "source_type": "Meme/Image-Text Dataset (U.S. 2016 Election Memes)",
            "download_timestamp": "2026-09-25T15:20:00Z",
            "local_file_path": "data/external/multioff/",
            "usable_for_training": True,
            "reason_if_not_used": "N/A - Fully Verified and Ingested with 740 Real Images"
        },
        {
            "dataset_name": "Facebook_Hateful_Memes",
            "official_source_url": "https://huggingface.co/datasets/neuralcatcher/hateful_memes / https://ai.meta.com/tools/hatefulmemes/",
            "license": "Meta AI Research Use Agreement (NeurIPS 2020)",
            "language": "English",
            "modality": "IMAGE_AND_TEXT",
            "number_of_records": 500,
            "number_of_images": 150,
            "has_original_text": True,
            "has_OCR_text": True,
            "has_post_text": False,
            "label_schema": "Binary (0: Not-Hateful, 1: Hateful)",
            "mapped_CyberGuard_label": "Abusive/Insult (Hateful) / Non-cyberbullying (Not-Hateful)",
            "source_type": "Meme/Image-Text Dataset (Facebook Multimodal Hate Speech Benchmark)",
            "download_timestamp": "2026-09-25T15:21:00Z",
            "local_file_path": "data/external/hateful_memes/",
            "usable_for_training": True,
            "reason_if_not_used": "N/A - Ingested Dev Split (500 records, 150 Real Images on Disk)"
        },
        {
            "dataset_name": "M3_Multimodal_Meme",
            "official_source_url": "https://github.com/mira-ai-lab/M3",
            "license": "MIT License / Academic Open Access (ArXiv 2404.14818)",
            "language": "English, Chinese (Weibo), Mixed",
            "modality": "IMAGE_AND_TEXT",
            "number_of_records": 526,
            "number_of_images": 150,
            "has_original_text": True,
            "has_OCR_text": True,
            "has_post_text": True,
            "label_schema": "Fine-Grained (label: hate/normal, categories: none, racism, sexism, religion, politics)",
            "mapped_CyberGuard_label": "Religion-based, Gender-based, Ethnicity-based, Abusive/Insult, Non-cyberbullying",
            "source_type": "Meme & Social-Media Post Dataset (Twitter/X & 4chan)",
            "download_timestamp": "2026-09-25T15:21:30Z",
            "local_file_path": "data/external/m3/",
            "usable_for_training": True,
            "reason_if_not_used": "N/A - Ingested Twitter Split (526 records, 150 Real Images on Disk)"
        },
        {
            "dataset_name": "Zenodo_Toxic_Memes",
            "official_source_url": "https://zenodo.org/records/8306439",
            "license": "Creative Commons Attribution 4.0 International",
            "language": "Russian (Cyrillic)",
            "modality": "IMAGE_AND_TEXT",
            "number_of_records": 1998,
            "number_of_images": 0,
            "has_original_text": True,
            "has_OCR_text": False,
            "has_post_text": False,
            "label_schema": "Binary (0: Non-Toxic, 1: Toxic)",
            "mapped_CyberGuard_label": "UNMAPPED / AUXILIARY",
            "source_type": "Meme/Image-Text Dataset",
            "download_timestamp": "2026-09-25T15:21:40Z",
            "local_file_path": "data/external/zenodo_toxic_memes/labels.csv",
            "usable_for_training": False,
            "reason_if_not_used": "Monolingual Russian/Cyrillic text. CyberGuard target scope is English, Hindi, and Hinglish. Cataloged as AUXILIARY."
        },
        {
            "dataset_name": "CyberDTD",
            "official_source_url": "https://doi.org/10.1007/978-3-031-77893-3 (ACLING 2025)",
            "license": "Restricted Academic Publication (Author Approval Required)",
            "language": "Tunisian Arabic Dialect (Arabizi / Arabic script)",
            "modality": "IMAGE_AND_TEXT",
            "number_of_records": 0,
            "number_of_images": 0,
            "has_original_text": True,
            "has_OCR_text": False,
            "has_post_text": True,
            "label_schema": "Multi-class Cyberbullying (Tunisian Dialect)",
            "mapped_CyberGuard_label": "UNMAPPED / AUXILIARY",
            "source_type": "Social Media Screenshot Dataset (Tunisian Dialect)",
            "download_timestamp": "2026-09-25T15:18:00Z (Queried)",
            "local_file_path": "N/A",
            "usable_for_training": False,
            "reason_if_not_used": "Not hosted on public open repositories (HuggingFace/Zenodo/GitHub); restricted to formal academic institutional request. Dialect out of target scope (Tunisian vs Hindi/Hinglish/English)."
        },
        {
            "dataset_name": "Public_Chat_Screenshots",
            "official_source_url": "N/A (Industry-wide Legal & Privacy Restrictions: GDPR / COPPA / Meta Terms)",
            "license": "Restricted Privacy / User Protection",
            "language": "English / Multilingual",
            "modality": "IMAGE_AND_TEXT",
            "number_of_records": 0,
            "number_of_images": 0,
            "has_original_text": False,
            "has_OCR_text": False,
            "has_post_text": False,
            "label_schema": "N/A",
            "mapped_CyberGuard_label": "N/A",
            "source_type": "Chat Screenshot Dataset",
            "download_timestamp": "2026-09-25T15:20:00Z (Investigated)",
            "local_file_path": "N/A",
            "usable_for_training": False,
            "reason_if_not_used": "No public open repository exists for private chat screenshots due to strict GDPR/privacy legal barriers. Evaluated via realistic synthetic/representative chat screenshots in OCR Benchmark."
        },
        {
            "dataset_name": "Synthetic_CyberGuard",
            "official_source_url": "scripts/generate_rich_dataset.py",
            "license": "Internal Project Benchmark",
            "language": "English, Hindi, Hinglish",
            "modality": "TEXT_ONLY",
            "number_of_records": 2036,
            "number_of_images": 0,
            "has_original_text": True,
            "has_OCR_text": False,
            "has_post_text": False,
            "label_schema": "10 Unified Classes (Age, Gender, Religion, Ethnicity, Appearance, Mockery, Abusive, Threat, Harassment, Non-cyberbullying)",
            "mapped_CyberGuard_label": "Direct 1:1 Identity Mapping",
            "source_type": "Synthetic Linguistic Benchmark",
            "download_timestamp": "2026-09-24T22:06:00Z",
            "local_file_path": "data/raw/cyberbullying_multilingual_raw.csv",
            "usable_for_training": True,
            "reason_if_not_used": "N/A - Maintained as separate baseline source (SOURCE = SYNTHETIC_CYBERGUARD)"
        }
    ]

    df_prov = pd.DataFrame(provenance_data)
    prov_file = BASE_DIR / "dataset_provenance.csv"
    df_prov.to_csv(prov_file, index=False)
    print(f"-> Generated {prov_file} ({len(df_prov)} datasets cataloged)")

    # 2. Multimodal Explicit Label Mapping Table
    label_mappings = [
        # MultiOFF Mappings
        {"source_label": "1", "source_dataset": "MultiOFF", "CyberGuard_label": "Abusive/Insult", "mapping_confidence": 0.85, "mapping_reason": "Offensive meme content directly aligns with Abusive/Insult taxonomy"},
        {"source_label": "0", "source_dataset": "MultiOFF", "CyberGuard_label": "Non-cyberbullying", "mapping_confidence": 0.95, "mapping_reason": "Non-offensive meme content maps to benign baseline"},
        
        # Meta Hateful Memes Mappings
        {"source_label": "1", "source_dataset": "Facebook_Hateful_Memes", "CyberGuard_label": "Abusive/Insult", "mapping_confidence": 0.85, "mapping_reason": "Multimodal hate speech maps to Abusive/Insult / Hostility"},
        {"source_label": "0", "source_dataset": "Facebook_Hateful_Memes", "CyberGuard_label": "Non-cyberbullying", "mapping_confidence": 0.95, "mapping_reason": "Benign / non-hateful meme maps to clean baseline"},
        
        # M3 Fine-Grained Mappings
        {"source_label": "racism", "source_dataset": "M3", "CyberGuard_label": "Ethnicity-based", "mapping_confidence": 0.95, "mapping_reason": "Racial hate memes directly map to Ethnicity-based cyberbullying"},
        {"source_label": "sexism", "source_dataset": "M3", "CyberGuard_label": "Gender-based", "mapping_confidence": 0.95, "mapping_reason": "Sexism and misogynistic hate memes directly map to Gender-based cyberbullying"},
        {"source_label": "religion", "source_dataset": "M3", "CyberGuard_label": "Religion-based", "mapping_confidence": 0.95, "mapping_reason": "Religious hate speech memes directly map to Religion-based cyberbullying"},
        {"source_label": "hate", "source_dataset": "M3", "CyberGuard_label": "Abusive/Insult", "mapping_confidence": 0.85, "mapping_reason": "General hate label without subcategory maps to Abusive/Insult"},
        {"source_label": "normal", "source_dataset": "M3", "CyberGuard_label": "Non-cyberbullying", "mapping_confidence": 0.95, "mapping_reason": "Normal / benign social media post maps to clean baseline"},
        {"source_label": "none", "source_dataset": "M3", "CyberGuard_label": "Non-cyberbullying", "mapping_confidence": 0.95, "mapping_reason": "Category 'none' indicates absence of hate speech"},
        {"source_label": "politics", "source_dataset": "M3", "CyberGuard_label": "UNMAPPED / AUXILIARY", "mapping_confidence": 0.00, "mapping_reason": "General political satire without personal targeting is out-of-taxonomy; marked UNMAPPED"},
        
        # Zenodo Toxic Memes Mappings
        {"source_label": "1", "source_dataset": "Zenodo_Toxic_Memes", "CyberGuard_label": "UNMAPPED / AUXILIARY", "mapping_confidence": 0.00, "mapping_reason": "Russian/Cyrillic text. Monolingual Russian out of project target scope (EN, HI, Hinglish)"},
        {"source_label": "0", "source_dataset": "Zenodo_Toxic_Memes", "CyberGuard_label": "UNMAPPED / AUXILIARY", "mapping_confidence": 0.00, "mapping_reason": "Russian/Cyrillic text. Out of project target scope"}
    ]
    
    df_map = pd.DataFrame(label_mappings)
    map_file = BASE_DIR / "data" / "metadata" / "multimodal_label_mapping.csv"
    map_file.parent.mkdir(parents=True, exist_ok=True)
    df_map.to_csv(map_file, index=False)
    print(f"-> Generated {map_file} ({len(df_map)} mapping rules defined)")

if __name__ == "__main__":
    generate_provenance_and_mapping()
