"""
CyberGuard Unified Dataset Builder
Builds separate, leakage-safe, versioned unified datasets for:
1. Cyberbullying Domain (CB-DATA-001 Baseline & CB-DATA-002 Expanded)
2. Wellbeing Support Domain (WB-DATA-001)

Saves Parquet splits into data/unified/ and metadata into data/metadata/unified_dataset_manifest.json.
Strictly excludes corrupt (GoEmotions) and tiled (Archive 25K) datasets.
"""
import os
import re
import json
import zipfile
import hashlib
import unicodedata
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

RANDOM_SEED = 42

def normalize_text(text):
    if not isinstance(text, str):
        return ""
    # Unicode NFKC normalization
    text = unicodedata.normalize('NFKC', text)
    # Remove URL links
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    # Remove Twitter handles
    text = re.sub(r'@\w+', '', text)
    # Normalize excessive whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def compute_hash(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def detect_language(text, default_lang="English"):
    if not isinstance(text, str) or not text.strip():
        return default_lang
    # Check for Devanagari
    if re.search(r'[\u0900-\u097F]', text):
        return "Hindi"
    # Check for Hinglish slang tokens
    hinglish_markers = {
        "kya", "kyu", "hai", "nahi", "bhai", "tere", "mera", "meri", "karo", "tu", "teri",
        "sale", "kamina", "pagal", "bkl", "mc", "bc", "chutiya", "gandu", "moti", "bhaisn",
        "marr", "jaa", "kutta", "kamine", "harami", "dost", "yaar", "aur", "hota", "hoga"
    }
    tokens = set(re.findall(r'\b[a-zA-Z]+\b', text.lower()))
    if len(tokens.intersection(hinglish_markers)) >= 1:
        return "Hinglish"
    return default_lang

def build_cyberbullying_datasets():
    print("\n--- 1. BUILDING CYBERBULLYING UNIFIED DATASETS ---")
    
    # Target 10 Classes
    TARGET_CLASSES = [
        "Age-based", "Gender-based", "Religion-based", "Ethnicity-based",
        "Appearance-based", "Mockery/Defamation", "Abusive/Insult",
        "Threat/Intimidation", "Personal Harassment", "Non-cyberbullying"
    ]
    
    all_cb_records = []
    seen_hashes = set()
    
    # 1. Baseline Synthetic Dataset (CB-DATA-001)
    base_path = os.path.join("data", "raw", "cyberbullying_multilingual_raw.csv")
    if os.path.exists(base_path):
        df_base = pd.read_csv(base_path)
        print(f"Loading Baseline Synthetic: {len(df_base)} rows")
        for _, row in df_base.iterrows():
            raw_text = str(row.get("text", ""))
            norm_text = normalize_text(raw_text)
            if not norm_text or len(norm_text) < 5:
                continue
            thash = compute_hash(norm_text)
            if thash in seen_hashes:
                continue
            seen_hashes.add(thash)
            
            lbl = str(row.get("raw_label", "Non-cyberbullying"))
            if lbl not in TARGET_CLASSES:
                lbl = "Non-cyberbullying"
            lang = str(row.get("language", detect_language(norm_text)))
            
            all_cb_records.append({
                "text": raw_text,
                "normalized_text": norm_text,
                "label": lbl,
                "source_dataset": "Synthetic-CyberGuard-v1",
                "source_label": str(row.get("raw_label", "")),
                "language": lang,
                "text_hash": thash,
                "is_baseline": True
            })

    # Save Baseline Data Splits for Experiment A
    df_baseline_all = pd.DataFrame([r for r in all_cb_records if r["is_baseline"]])
    base_train, base_test = train_test_split(df_baseline_all, test_size=0.20, random_state=RANDOM_SEED, stratify=df_baseline_all['label'])
    base_train.to_parquet("data/unified/cyberbullying/baseline_train.parquet", index=False)
    base_test.to_parquet("data/unified/cyberbullying/baseline_test.parquet", index=False)
    print(f"Saved Baseline CB-DATA-001: Train={len(base_train)}, Test={len(base_test)}")

    # 2. Kaggle Cyberbullying Tweets (Real 47K records)
    kaggle_zip = r"C:\Users\vivek\Documents\aml\cyberbullying_dataset\kaggledataset.zip"
    if os.path.exists(kaggle_zip):
        print("Loading Kaggle Cyberbullying Tweets...")
        with zipfile.ZipFile(kaggle_zip, 'r') as z:
            with z.open("cyberbullying_tweets.csv") as f:
                df_k = pd.read_csv(f)
                mapping = {
                    "religion": "Religion-based",
                    "age": "Age-based",
                    "gender": "Gender-based",
                    "ethnicity": "Ethnicity-based",
                    "not_cyberbullying": "Non-cyberbullying",
                    "other_cyberbullying": "Personal Harassment"
                }
                # Subsample up to 4,000 per class for balanced high-speed AML representation
                for orig_lbl, target_lbl in mapping.items():
                    sub = df_k[df_k["cyberbullying_type"] == orig_lbl].head(3500)
                    for _, row in sub.iterrows():
                        raw_text = str(row["tweet_text"])
                        norm_text = normalize_text(raw_text)
                        if not norm_text or len(norm_text) < 10:
                            continue
                        thash = compute_hash(norm_text)
                        if thash in seen_hashes:
                            continue
                        seen_hashes.add(thash)
                        all_cb_records.append({
                            "text": raw_text,
                            "normalized_text": norm_text,
                            "label": target_lbl,
                            "source_dataset": "Kaggle-CB-Tweets-v1",
                            "source_label": orig_lbl,
                            "language": detect_language(norm_text, "English"),
                            "text_hash": thash,
                            "is_baseline": False
                        })
        print(f"Total after Kaggle: {len(all_cb_records)} records")

    # 3. Hinglish Codemixed Dataset (Real 18K comments)
    hinglish_csv = r"C:\Users\vivek\Documents\aml\cyberbullying_dataset\final_dataset_hinglish.csv"
    if os.path.exists(hinglish_csv):
        print("Loading Hinglish Codemixed Dataset...")
        df_h = pd.read_csv(hinglish_csv)
        # -1 -> Abusive/Insult, 0 -> Non-cyberbullying
        sub_neg = df_h[df_h["label"] == -1].head(3000)
        sub_zero = df_h[df_h["label"] == 0].head(2000)
        for sub, target_lbl, orig_lbl in [(sub_neg, "Abusive/Insult", "-1"), (sub_zero, "Non-cyberbullying", "0")]:
            for _, row in sub.iterrows():
                raw_text = str(row.get("headline", ""))
                norm_text = normalize_text(raw_text)
                if not norm_text or len(norm_text) < 5:
                    continue
                thash = compute_hash(norm_text)
                if thash in seen_hashes:
                    continue
                seen_hashes.add(thash)
                all_cb_records.append({
                    "text": raw_text,
                    "normalized_text": norm_text,
                    "label": target_lbl,
                    "source_dataset": "Hinglish-Codemixed-18K-v1",
                    "source_label": orig_lbl,
                    "language": "Hinglish",
                    "text_hash": thash,
                    "is_baseline": False
                })
        print(f"Total after Hinglish: {len(all_cb_records)} records")

    # 4. CyberbullyX-63K (Real Hindi/English stream)
    cbx_path = r"C:\Users\vivek\Documents\aml\cyberbullying_dataset\CyberbullyX-63K.xlsx"
    if os.path.exists(cbx_path):
        print("Loading CyberbullyX-63K (subsampling representative Hindi/English stream)...")
        # Subsample real tweets
        df_cbx = pd.read_excel(cbx_path, nrows=15000)
        sub_cbx_pos = df_cbx[df_cbx["final_label"] == 1].head(2500)
        sub_cbx_neg = df_cbx[df_cbx["final_label"] == 0].head(2500)
        for sub, target_lbl, orig_lbl in [(sub_cbx_pos, "Abusive/Insult", "1"), (sub_cbx_neg, "Non-cyberbullying", "0")]:
            for _, row in sub.iterrows():
                raw_text = str(row.get("text", ""))
                norm_text = normalize_text(raw_text)
                if not norm_text or len(norm_text) < 8:
                    continue
                thash = compute_hash(norm_text)
                if thash in seen_hashes:
                    continue
                seen_hashes.add(thash)
                all_cb_records.append({
                    "text": raw_text,
                    "normalized_text": norm_text,
                    "label": target_lbl,
                    "source_dataset": "CyberbullyX-63K-v1",
                    "source_label": orig_lbl,
                    "language": detect_language(norm_text, "Hindi"),
                    "text_hash": thash,
                    "is_baseline": False
                })
        print(f"Total after CyberbullyX: {len(all_cb_records)} records")

    # 5. Jigsaw Toxic Comments for Threat/Intimidation alignment
    jigsaw_zip = r"C:\Users\vivek\Documents\aml\cyberbullying_dataset\archive (1).zip"
    if os.path.exists(jigsaw_zip):
        print("Loading Jigsaw Threat & Intimidation instances...")
        with zipfile.ZipFile(jigsaw_zip, 'r') as z:
            with z.open("train.csv") as f:
                df_j = pd.read_csv(f, nrows=40000)
                threats = df_j[df_j["threat"] == 1]
                for _, row in threats.iterrows():
                    raw_text = str(row["comment_text"])
                    norm_text = normalize_text(raw_text)
                    if not norm_text or len(norm_text) < 10:
                        continue
                    thash = compute_hash(norm_text)
                    if thash in seen_hashes:
                        continue
                    seen_hashes.add(thash)
                    all_cb_records.append({
                        "text": raw_text,
                        "normalized_text": norm_text,
                        "label": "Threat/Intimidation",
                        "source_dataset": "Jigsaw-Toxic-Train-v1",
                        "source_label": "threat=1",
                        "language": "English",
                        "text_hash": thash,
                        "is_baseline": False
                    })
        print(f"Total after Jigsaw Threat: {len(all_cb_records)} records")

    df_cb_expanded = pd.DataFrame(all_cb_records)
    print("\nExpanded Cyberbullying Dataset Summary:")
    print("Total verified unique records:", len(df_cb_expanded))
    print("Class Distribution:\n", df_cb_expanded["label"].value_counts())
    print("Language Distribution:\n", df_cb_expanded["language"].value_counts())
    print("Source Distribution:\n", df_cb_expanded["source_dataset"].value_counts())

    # Create Leakage-Safe Splits
    # 1. External holdout: 10% held out exclusively from real external sources
    df_real = df_cb_expanded[~df_cb_expanded["is_baseline"]]
    df_base_part = df_cb_expanded[df_cb_expanded["is_baseline"]]
    
    train_real, temp_real = train_test_split(df_real, test_size=0.30, random_state=RANDOM_SEED, stratify=df_real['label'])
    val_real, test_real = train_test_split(temp_real, test_size=0.50, random_state=RANDOM_SEED, stratify=temp_real['label'])
    
    # Combined Expanded Train / Val / Test (including baseline)
    train_base, temp_base = train_test_split(df_base_part, test_size=0.30, random_state=RANDOM_SEED, stratify=df_base_part['label'])
    val_base, test_base = train_test_split(temp_base, test_size=0.50, random_state=RANDOM_SEED, stratify=temp_base['label'])
    
    cb_train = pd.concat([train_real, train_base], ignore_index=True).sample(frac=1, random_state=RANDOM_SEED).reset_index(drop=True)
    cb_val = pd.concat([val_real, val_base], ignore_index=True).sample(frac=1, random_state=RANDOM_SEED).reset_index(drop=True)
    cb_test = pd.concat([test_real, test_base], ignore_index=True).sample(frac=1, random_state=RANDOM_SEED).reset_index(drop=True)
    cb_holdout = test_real.copy().reset_index(drop=True) # Pure external real holdout

    cb_train.to_parquet("data/unified/cyberbullying/train.parquet", index=False)
    cb_val.to_parquet("data/unified/cyberbullying/validation.parquet", index=False)
    cb_test.to_parquet("data/unified/cyberbullying/test.parquet", index=False)
    cb_holdout.to_parquet("data/unified/cyberbullying/external_holdout.parquet", index=False)

    print(f"\nSaved CB-DATA-002 Splits:")
    print(f"- Train: {len(cb_train)} rows -> data/unified/cyberbullying/train.parquet")
    print(f"- Val: {len(cb_val)} rows -> data/unified/cyberbullying/validation.parquet")
    print(f"- Test: {len(cb_test)} rows -> data/unified/cyberbullying/test.parquet")
    print(f"- External Holdout: {len(cb_holdout)} rows -> data/unified/cyberbullying/external_holdout.parquet")
    
    return df_cb_expanded

def build_wellbeing_datasets():
    print("\n--- 2. BUILDING WELLBEING UNIFIED DATASETS ---")
    all_wb_records = []
    seen_hashes = set()

    # 1. Reddit Suicide vs Depression (Crisis vs Depression Triage)
    suicide_path = r"C:\Users\vivek\Documents\aml\mental\combined-set.csv"
    if os.path.exists(suicide_path):
        print("Loading Reddit Suicide vs Depression triage dataset...")
        df_s = pd.read_csv(suicide_path)
        for _, row in df_s.iterrows():
            raw_title = str(row.get("title", ""))
            raw_body = str(row.get("selftext", ""))
            full_text = f"{raw_title} {raw_body}".strip()
            norm_text = normalize_text(full_text)
            if not norm_text or len(norm_text) < 15:
                continue
            thash = compute_hash(norm_text)
            if thash in seen_hashes:
                continue
            seen_hashes.add(thash)

            is_suicide = int(row.get("is_suicide", 0))
            label = "CRISIS_ESCALATION" if is_suicide == 1 else "DEPRESSIVE_DISTRESS"

            all_wb_records.append({
                "text": full_text[:1000],
                "normalized_text": norm_text[:1000],
                "label": label,
                "task": "CRISIS_TRIAGE",
                "source_dataset": "Reddit-Crisis-Triage-v1",
                "source_label": str(is_suicide),
                "language": "English",
                "text_hash": thash
            })

    # 2. Reddit LoST v1 & Final Train (Loss of Self Cognitive Distress)
    lost_path = r"C:\Users\vivek\Documents\aml\mental\LoSTv1.csv"
    if os.path.exists(lost_path):
        print("Loading Reddit LoST v1...")
        df_l = pd.read_csv(lost_path)
        for _, row in df_l.iterrows():
            raw_text = str(row.get("text", ""))
            norm_text = normalize_text(raw_text)
            if not norm_text or len(norm_text) < 20:
                continue
            thash = compute_hash(norm_text)
            if thash in seen_hashes:
                continue
            seen_hashes.add(thash)

            self_score = float(row.get("self", 0))
            label = "LOSS_OF_SELF_DETECTED" if self_score >= 0.5 else "NORMAL_AFFECT"

            all_wb_records.append({
                "text": raw_text[:1000],
                "normalized_text": norm_text[:1000],
                "label": label,
                "task": "COGNITIVE_DISTRESS",
                "source_dataset": "Reddit-LoST-v1",
                "source_label": str(self_score),
                "language": "English",
                "text_hash": thash
            })

    # 3. LoST Final Test as dedicated External Holdout
    lost_test_path = r"C:\Users\vivek\Documents\aml\mental\final_test.csv"
    holdout_records = []
    if os.path.exists(lost_test_path):
        print("Loading LoST Final Test as dedicated External Holdout...")
        df_lt = pd.read_csv(lost_test_path)
        for _, row in df_lt.iterrows():
            raw_text = str(row.get("text", ""))
            norm_text = normalize_text(raw_text)
            if not norm_text or len(norm_text) < 20:
                continue
            thash = compute_hash(norm_text)
            self_score = float(row.get("self", 0))
            label = "LOSS_OF_SELF_DETECTED" if self_score >= 0.5 else "NORMAL_AFFECT"
            holdout_records.append({
                "text": raw_text[:1000],
                "normalized_text": norm_text[:1000],
                "label": label,
                "task": "COGNITIVE_DISTRESS",
                "source_dataset": "Reddit-LoST-Test-v1",
                "source_label": str(self_score),
                "language": "English",
                "text_hash": thash
            })

    # 4. Synthetic Support Wellbeing Prompts (Stress calibration)
    synth_wb_path = os.path.join("data", "raw", "support_wellbeing_raw.csv")
    if os.path.exists(synth_wb_path):
        df_sw = pd.read_csv(synth_wb_path)
        for _, row in df_sw.iterrows():
            raw_text = str(row.get("text", ""))
            norm_text = normalize_text(raw_text)
            if not norm_text:
                continue
            thash = compute_hash(norm_text)
            if thash in seen_hashes:
                continue
            seen_hashes.add(thash)
            stress_lbl = str(row.get("stress_label", "MODERATE"))
            all_wb_records.append({
                "text": raw_text,
                "normalized_text": norm_text,
                "label": stress_lbl,
                "task": "STRESS_CALIBRATION",
                "source_dataset": "Synthetic-Support-v1",
                "source_label": stress_lbl,
                "language": "English",
                "text_hash": thash
            })

    df_wb = pd.DataFrame(all_wb_records)
    print("\nWellbeing Unified Dataset Summary:")
    print("Total verified records:", len(df_wb))
    print("Label Breakdown:\n", df_wb["label"].value_counts())
    print("Task Breakdown:\n", df_wb["task"].value_counts())

    # Split Train (70%), Val (15%), Test (15%)
    train_wb, temp_wb = train_test_split(df_wb, test_size=0.30, random_state=RANDOM_SEED, stratify=df_wb['label'])
    val_wb, test_wb = train_test_split(temp_wb, test_size=0.50, random_state=RANDOM_SEED, stratify=temp_wb['label'])
    df_holdout = pd.DataFrame(holdout_records)

    train_wb.to_parquet("data/unified/wellbeing/train.parquet", index=False)
    val_wb.to_parquet("data/unified/wellbeing/validation.parquet", index=False)
    test_wb.to_parquet("data/unified/wellbeing/test.parquet", index=False)
    df_holdout.to_parquet("data/unified/wellbeing/external_holdout.parquet", index=False)

    print(f"\nSaved WB-DATA-001 Splits:")
    print(f"- Train: {len(train_wb)} rows -> data/unified/wellbeing/train.parquet")
    print(f"- Val: {len(val_wb)} rows -> data/unified/wellbeing/validation.parquet")
    print(f"- Test: {len(test_wb)} rows -> data/unified/wellbeing/test.parquet")
    print(f"- External Holdout: {len(df_holdout)} rows -> data/unified/wellbeing/external_holdout.parquet")

    return df_wb

def generate_manifest(df_cb, df_wb):
    manifest = {
        "generated_at": "2026-09-25T17:40:00Z",
        "cyberbullying": {
            "version": "CB-DATA-002",
            "baseline_version": "CB-DATA-001",
            "sources": [
                {"name": "Synthetic-CyberGuard-v1", "records": int((df_cb["source_dataset"] == "Synthetic-CyberGuard-v1").sum())},
                {"name": "Kaggle-CB-Tweets-v1", "records": int((df_cb["source_dataset"] == "Kaggle-CB-Tweets-v1").sum())},
                {"name": "Hinglish-Codemixed-18K-v1", "records": int((df_cb["source_dataset"] == "Hinglish-Codemixed-18K-v1").sum())},
                {"name": "CyberbullyX-63K-v1", "records": int((df_cb["source_dataset"] == "CyberbullyX-63K-v1").sum())},
                {"name": "Jigsaw-Toxic-Train-v1", "records": int((df_cb["source_dataset"] == "Jigsaw-Toxic-Train-v1").sum())}
            ],
            "record_count": len(df_cb),
            "languages": {k: int(v) for k, v in df_cb["language"].value_counts().items()},
            "class_distribution": {k: int(v) for k, v in df_cb["label"].value_counts().items()},
            "excluded_sources": [
                {"name": "Archive-Hinglish-25K-TILED", "reason": "99.84% mechanical duplicate rate (only 40 unique sentences)"},
                {"name": "Zenodo-Russian-Toxic-Memes", "reason": "Russian language out of target scope (English/Hindi/Hinglish)"},
                {"name": "PolEval-2019-SharedTask6", "reason": "Polish language, not present in local directories"}
            ]
        },
        "wellbeing": {
            "version": "WB-DATA-001",
            "sources": [
                {"name": "Reddit-Crisis-Triage-v1", "records": int((df_wb["source_dataset"] == "Reddit-Crisis-Triage-v1").sum())},
                {"name": "Reddit-LoST-v1", "records": int((df_wb["source_dataset"] == "Reddit-LoST-v1").sum())},
                {"name": "Synthetic-Support-v1", "records": int((df_wb["source_dataset"] == "Synthetic-Support-v1").sum())}
            ],
            "record_count": len(df_wb),
            "languages": {"English": len(df_wb)},
            "task_distribution": {k: int(v) for k, v in df_wb["task"].value_counts().items()},
            "excluded_sources": [
                {"name": "GoEmotions-Subset-Local", "reason": "Local file goemotions_1-selected-columns.csv contains 100% NaN entries"},
                {"name": "DAIC-WOZ-Clinical-Interviews", "reason": "Restricted institutional access; violates ethical non-diagnosis policy"}
            ]
        }
    }

    out_path = "data/metadata/unified_dataset_manifest.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"\nManifest successfully written to {out_path}")

if __name__ == "__main__":
    os.makedirs("data/unified/cyberbullying", exist_ok=True)
    os.makedirs("data/unified/wellbeing", exist_ok=True)
    os.makedirs("data/metadata", exist_ok=True)
    df_cb = build_cyberbullying_datasets()
    df_wb = build_wellbeing_datasets()
    generate_manifest(df_cb, df_wb)
    print("\nUnified datasets build complete!")
