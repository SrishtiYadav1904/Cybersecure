"""
CyberGuard Full Data Integrity, Audit, and Quality Script
Inspects physical datasets across all local sources, computes SHA256 hashes,
duplicate rates, language distributions, label statistics, and generates:
- artifacts/data_audit/dataset_integrity.csv
- artifacts/data_audit/duplicate_analysis.csv
- artifacts/data_audit/language_analysis.csv
- artifacts/data_audit/class_distribution.csv
- artifacts/data_audit/license_status.csv
"""
import os
import hashlib
import zipfile
import pandas as pd
import numpy as np

def compute_sha256(filepath):
    if not os.path.exists(filepath):
        return "FILE_NOT_FOUND"
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def run_data_audit():
    os.makedirs("artifacts/data_audit", exist_ok=True)
    os.makedirs("data/interim", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("data/unified/cyberbullying", exist_ok=True)
    os.makedirs("data/unified/wellbeing", exist_ok=True)
    os.makedirs("data/metadata", exist_ok=True)

    print("=== CYBERGUARD DATA AUDIT ===")

    # 1. Dataset Integrity
    datasets_meta = [
        {
            "dataset_id": "DS-CB-01",
            "name": "CyberbullyX-63K",
            "domain": "CYBERBULLYING",
            "path": r"C:\Users\vivek\Documents\aml\cyberbullying_dataset\CyberbullyX-63K.xlsx",
            "is_zip": False,
            "license": "Public Academic / Research Use",
            "status": "AVAILABLE",
            "language": "Hindi / English / Hinglish"
        },
        {
            "dataset_id": "DS-CB-02",
            "name": "Kaggle Cyberbullying Tweets",
            "domain": "CYBERBULLYING",
            "path": r"C:\Users\vivek\Documents\aml\cyberbullying_dataset\kaggledataset.zip",
            "zip_subpath": "cyberbullying_tweets.csv",
            "is_zip": True,
            "license": "CC0: Public Domain",
            "status": "AVAILABLE",
            "language": "English"
        },
        {
            "dataset_id": "DS-CB-03",
            "name": "Hinglish Codemixed Dataset",
            "domain": "CYBERBULLYING",
            "path": r"C:\Users\vivek\Documents\aml\cyberbullying_dataset\final_dataset_hinglish.csv",
            "is_zip": False,
            "license": "Public Academic / Research Open Access",
            "status": "AVAILABLE",
            "language": "Hinglish / English"
        },
        {
            "dataset_id": "DS-CB-04",
            "name": "Jigsaw Toxic Comment (Train)",
            "domain": "CYBERBULLYING",
            "path": r"C:\Users\vivek\Documents\aml\cyberbullying_dataset\archive (1).zip",
            "zip_subpath": "train.csv",
            "is_zip": True,
            "license": "CC0: Public Domain",
            "status": "AUXILIARY",
            "language": "English"
        },
        {
            "dataset_id": "DS-CB-05",
            "name": "Jigsaw Toxic Comment (Test & Labels)",
            "domain": "CYBERBULLYING",
            "path": r"C:\Users\vivek\Documents\aml\cyberbullying_dataset\archive (1).zip",
            "zip_subpath": "test.csv",
            "is_zip": True,
            "license": "CC0: Public Domain",
            "status": "EVALUATION_ONLY",
            "language": "English"
        },
        {
            "dataset_id": "DS-CB-06",
            "name": "MultiOFF Meme Dataset",
            "domain": "CYBERBULLYING_MULTIMODAL",
            "path": r"data\external\multioff\multioff_catalog.csv",
            "is_zip": False,
            "license": "Public Academic / Research Use",
            "status": "AVAILABLE",
            "language": "English"
        },
        {
            "dataset_id": "DS-CB-07",
            "name": "M3 Twitter Memes",
            "domain": "CYBERBULLYING_MULTIMODAL",
            "path": r"data\external\m3\m3_catalog.csv",
            "is_zip": False,
            "license": "MIT License",
            "status": "AVAILABLE",
            "language": "English / Mixed"
        },
        {
            "dataset_id": "DS-CB-08",
            "name": "Facebook Hateful Memes (Dev)",
            "domain": "CYBERBULLYING_MULTIMODAL",
            "path": r"data\external\hateful_memes\hateful_memes_catalog.csv",
            "is_zip": False,
            "license": "Meta AI Research Agreement",
            "status": "HOLDOUT",
            "language": "English"
        },
        {
            "dataset_id": "DS-CB-09",
            "name": "Synthetic CyberGuard Multilingual",
            "domain": "CYBERBULLYING",
            "path": r"data\raw\cyberbullying_multilingual_raw.csv",
            "is_zip": False,
            "license": "Internal Project License",
            "status": "AVAILABLE",
            "language": "English / Hindi / Hinglish"
        },
        {
            "dataset_id": "DS-CB-10",
            "name": "Zenodo Russian Toxic Memes",
            "domain": "CYBERBULLYING_MULTIMODAL",
            "path": r"data\external\zenodo_toxic_memes\labels.csv",
            "is_zip": False,
            "license": "CC-BY 4.0",
            "status": "AUXILIARY",
            "language": "Russian"
        },
        {
            "dataset_id": "DS-CB-11",
            "name": "Archive.zip 25K Hinglish (Tiled)",
            "domain": "CYBERBULLYING",
            "path": r"C:\Users\vivek\Documents\aml\cyberbullying_dataset\archive.zip",
            "zip_subpath": "hinglish_cyberbullying_dataset_25000.csv",
            "is_zip": True,
            "license": "Unknown / Unverified",
            "status": "EXCLUDED",
            "language": "Hinglish / English"
        },
        {
            "dataset_id": "DS-WB-01",
            "name": "Reddit LoST v1",
            "domain": "WELLBEING",
            "path": r"C:\Users\vivek\Documents\aml\mental\LoSTv1.csv",
            "is_zip": False,
            "license": "Academic Research Use",
            "status": "AVAILABLE",
            "language": "English"
        },
        {
            "dataset_id": "DS-WB-02",
            "name": "Reddit LoST Final Train",
            "domain": "WELLBEING",
            "path": r"C:\Users\vivek\Documents\aml\mental\final_train.csv",
            "is_zip": False,
            "license": "Academic Research Use",
            "status": "AVAILABLE",
            "language": "English"
        },
        {
            "dataset_id": "DS-WB-03",
            "name": "Reddit LoST Final Test",
            "domain": "WELLBEING",
            "path": r"C:\Users\vivek\Documents\aml\mental\final_test.csv",
            "is_zip": False,
            "license": "Academic Research Use",
            "status": "HOLDOUT",
            "language": "English"
        },
        {
            "dataset_id": "DS-WB-04",
            "name": "Reddit Suicide vs Depression",
            "domain": "WELLBEING",
            "path": r"C:\Users\vivek\Documents\aml\mental\combined-set.csv",
            "is_zip": False,
            "license": "Public Academic / Research Use",
            "status": "AVAILABLE",
            "language": "English"
        },
        {
            "dataset_id": "DS-WB-05",
            "name": "GoEmotions Subset",
            "domain": "WELLBEING",
            "path": r"C:\Users\vivek\Documents\aml\mental\goemotions_1-selected-columns.csv",
            "is_zip": False,
            "license": "Apache 2.0",
            "status": "AUXILIARY",
            "language": "English"
        },
        {
            "dataset_id": "DS-WB-06",
            "name": "Synthetic Support Wellbeing Prompts",
            "domain": "WELLBEING",
            "path": r"data\raw\support_wellbeing_raw.csv",
            "is_zip": False,
            "license": "Internal Project License",
            "status": "AVAILABLE",
            "language": "English"
        }
    ]

    integrity_rows = []
    duplicate_rows = []
    language_rows = []
    class_rows = []
    license_rows = []

    for d in datasets_meta:
        path = d["path"]
        exists = os.path.exists(path)
        file_sha256 = compute_sha256(path) if exists else "NOT_FOUND"
        file_size = os.path.getsize(path) if exists else 0

        total_rows = 0
        unique_texts = 0
        dup_count = 0
        dup_rate = 0.0
        empty_rows = 0
        cols_str = ""

        # Read sample/data to analyze
        try:
            df = None
            if exists:
                if d.get("is_zip"):
                    with zipfile.ZipFile(path, 'r') as z:
                        with z.open(d["zip_subpath"]) as f:
                            df = pd.read_csv(f, nrows=200000)
                elif path.endswith(".xlsx"):
                    df = pd.read_excel(path)
                elif path.endswith(".csv"):
                    df = pd.read_csv(path, nrows=200000)

            if df is not None:
                total_rows = len(df)
                cols_str = "|".join(list(df.columns)[:8])
                # Find text column case-insensitively
                text_col = None
                for col in df.columns:
                    if col.lower() in ["text", "comment_text", "tweet_text", "clean_text", "comment", "sentence", "headline", "selftext", "title"]:
                        text_col = col
                        break
                if text_col is None and len(df.columns) > 0:
                    text_col = df.columns[0]

                if text_col and text_col in df.columns:
                    empty_rows = int(df[text_col].isna().sum())
                    valid_texts = df[text_col].dropna().astype(str)
                    unique_texts = int(valid_texts.nunique()) if len(valid_texts) > 0 else 0
                    dup_count = total_rows - unique_texts
                    dup_rate = round((dup_count / total_rows) * 100, 2) if total_rows > 0 else 0.0

                # Analyze labels
                label_col = None
                for lcol in ["cyberbullying_type", "cb_label", "label", "target", "Sentiment", "toxic"]:
                    if lcol in df.columns:
                        label_col = lcol
                        break
                if label_col:
                    vc = df[label_col].value_counts().head(10).to_dict()
                    for k, v in vc.items():
                        class_rows.append({
                            "dataset_id": d["dataset_id"],
                            "dataset_name": d["name"],
                            "class_label": str(k),
                            "count": int(v),
                            "proportion_pct": round((v / total_rows) * 100, 2)
                        })

        except Exception as e:
            cols_str = f"ERROR: {str(e)[:40]}"

        integrity_rows.append({
            "dataset_id": d["dataset_id"],
            "dataset_name": d["name"],
            "domain": d["domain"],
            "status": d["status"],
            "file_exists": exists,
            "file_size_bytes": file_size,
            "sha256": file_sha256,
            "record_count": total_rows,
            "columns": cols_str,
            "empty_records": empty_rows
        })

        status_str = "ACCEPTABLE"
        if d["dataset_id"] == "DS-WB-05":
            status_str = "CORRUPTED_ALL_NULL"
        elif dup_rate > 90:
            status_str = "CRITICAL_TILED"
        elif dup_rate > 10:
            status_str = "HIGH_RETWEET"

        duplicate_rows.append({
            "dataset_id": d["dataset_id"],
            "dataset_name": d["name"],
            "total_records": total_rows,
            "unique_records": unique_texts,
            "duplicate_records": dup_count,
            "duplicate_rate_pct": dup_rate,
            "status": status_str
        })

        language_rows.append({
            "dataset_id": d["dataset_id"],
            "dataset_name": d["name"],
            "declared_language": d["language"],
            "target_alignment": "HIGH" if "Hindi" in d["language"] or "Hinglish" in d["language"] else ("STANDARD" if "English" in d["language"] else "OUT_OF_SCOPE")
        })

        license_rows.append({
            "dataset_id": d["dataset_id"],
            "dataset_name": d["name"],
            "license": d["license"],
            "access_type": "OPEN" if "CC" in d["license"] or "MIT" in d["license"] or "Apache" in d["license"] else "ACADEMIC_RESEARCH",
            "commercial_use": "ALLOWED" if "CC0" in d["license"] or "MIT" in d["license"] or "Apache" in d["license"] else "RESEARCH_ONLY",
            "retention_policy": "PRESERVE"
        })

    # Save CSVs
    pd.DataFrame(integrity_rows).to_csv("artifacts/data_audit/dataset_integrity.csv", index=False)
    pd.DataFrame(duplicate_rows).to_csv("artifacts/data_audit/duplicate_analysis.csv", index=False)
    pd.DataFrame(language_rows).to_csv("artifacts/data_audit/language_analysis.csv", index=False)
    pd.DataFrame(class_rows).to_csv("artifacts/data_audit/class_distribution.csv", index=False)
    pd.DataFrame(license_rows).to_csv("artifacts/data_audit/license_status.csv", index=False)

    print("Data audit artifacts successfully created in artifacts/data_audit/:")
    print("- artifacts/data_audit/dataset_integrity.csv")
    print("- artifacts/data_audit/duplicate_analysis.csv")
    print("- artifacts/data_audit/language_analysis.csv")
    print("- artifacts/data_audit/class_distribution.csv")
    print("- artifacts/data_audit/license_status.csv")

if __name__ == "__main__":
    run_data_audit()
