import os
import io
import sys
import json
import ssl
import urllib.request
from pathlib import Path
import pyarrow.parquet as pq
import pandas as pd
from PIL import Image

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

BASE_DIR = Path(__file__).resolve().parent.parent
EXTERNAL_DIR = BASE_DIR / "data" / "external"
MULTIOFF_DIR = EXTERNAL_DIR / "multioff"
HATEFUL_MEMES_DIR = EXTERNAL_DIR / "hateful_memes"
M3_DIR = EXTERNAL_DIR / "m3"
ZENODO_DIR = EXTERNAL_DIR / "zenodo_toxic_memes"

for d in [MULTIOFF_DIR / "images", HATEFUL_MEMES_DIR / "img", M3_DIR / "img", ZENODO_DIR]:
    d.mkdir(parents=True, exist_ok=True)

def download_file(url, out_path, chunk_size=65536):
    req = urllib.request.Request(url, headers={'User-Agent': 'CyberGuard-Auditor/1.0'})
    with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
        with open(out_path, 'wb') as f:
            while True:
                chunk = resp.read(chunk_size)
                if not chunk:
                    break
                f.write(chunk)

def ingest_multioff():
    print("\n--- 1. Ingesting Real MultiOFF Dataset ---")
    splits = ["train", "validation", "test"]
    base_hf = "https://huggingface.co/datasets/Ibrahim-Alam/multi-modal_offensive_meme/resolve/main/data"
    
    all_records = []
    for split in splits:
        parquet_file = MULTIOFF_DIR / f"{split}.parquet"
        url = f"{base_hf}/{split}-00000-of-00001.parquet"
        print(f"Downloading MultiOFF {split} split...")
        download_file(url, parquet_file)
        
        table = pq.read_table(parquet_file)
        df = table.to_pandas()
        print(f"Loaded {len(df)} samples from {split}.parquet")
        
        for idx, row in df.iterrows():
            img_dict = row["image"]
            img_bytes = img_dict["bytes"] if isinstance(img_dict, dict) and "bytes" in img_dict else None
            
            img_filename = f"multioff_{split}_{idx}.jpg"
            img_disk_path = MULTIOFF_DIR / "images" / img_filename
            
            if img_bytes:
                try:
                    img = Image.open(io.BytesIO(img_bytes))
                    if img.mode not in ("RGB", "L"):
                        img = img.convert("RGB")
                    img.save(img_disk_path, "JPEG", quality=90)
                except Exception as e:
                    pass
            
            all_records.append({
                "sample_id": f"multioff_{split}_{idx}",
                "dataset_name": "MultiOFF",
                "split": split,
                "image_filename": img_filename,
                "local_image_path": str(img_disk_path),
                "text": str(row.get("text", "")).strip(),
                "source_label": int(row.get("label", 0)),
                "source_label_name": "Offensive" if int(row.get("label", 0)) == 1 else "Non-Offensive",
                "language": "English",
                "modality": "IMAGE_AND_TEXT"
            })
            
    df_multioff = pd.DataFrame(all_records)
    csv_out = MULTIOFF_DIR / "multioff_catalog.csv"
    df_multioff.to_csv(csv_out, index=False)
    print(f"Saved {len(df_multioff)} verified MultiOFF records to {csv_out}")
    print(f"Saved images to {MULTIOFF_DIR / 'images'}")
    return df_multioff

def ingest_m3():
    print("\n--- 2. Ingesting Real M3 (Multi-platform, Multilingual Meme) Dataset ---")
    url_twitter = "https://raw.githubusercontent.com/mira-ai-lab/M3/main/dataset/CHEM_twitter.json"
    json_path = M3_DIR / "CHEM_twitter.json"
    print("Downloading M3 CHEM_twitter.json from GitHub...")
    download_file(url_twitter, json_path)
    
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    print(f"Loaded {len(data)} items from M3 Twitter split.")
    
    m3_records = []
    # Download first 150 real images from GitHub
    base_img_url = "https://raw.githubusercontent.com/mira-ai-lab/M3/main/dataset/img"
    downloaded_imgs = 0
    
    for idx, item in enumerate(data):
        img_name = item.get("img", "")
        img_disk_path = M3_DIR / "img" / img_name
        
        has_img = False
        if downloaded_imgs < 150 and img_name:
            try:
                img_url = f"{base_img_url}/{img_name}"
                download_file(img_url, img_disk_path)
                has_img = os.path.exists(img_disk_path)
                if has_img:
                    downloaded_imgs += 1
            except Exception:
                has_img = False
        else:
            has_img = os.path.exists(img_disk_path)
            
        m3_records.append({
            "sample_id": f"m3_twitter_{idx}",
            "dataset_name": "M3",
            "split": "twitter",
            "image_filename": img_name,
            "local_image_path": str(img_disk_path) if has_img else "",
            "has_image_on_disk": has_img,
            "text": str(item.get("img_text", "")).strip(),
            "post_text": str(item.get("post_text", "")).strip(),
            "source_label": item.get("label", "normal"),
            "category": ",".join(item.get("category", [])),
            "reason": item.get("reason", ""),
            "language": "English",
            "modality": "IMAGE_AND_TEXT" if has_img else "TEXT_ONLY"
        })
        
    df_m3 = pd.DataFrame(m3_records)
    csv_out = M3_DIR / "m3_catalog.csv"
    df_m3.to_csv(csv_out, index=False)
    print(f"Saved {len(df_m3)} M3 records ({downloaded_imgs} images downloaded) to {csv_out}")
    return df_m3

def ingest_hateful_memes():
    print("\n--- 3. Ingesting Real Facebook / Meta Hateful Memes Dataset ---")
    url_dev = "https://huggingface.co/datasets/neuralcatcher/hateful_memes/raw/main/dev_seen.jsonl"
    jsonl_path = HATEFUL_MEMES_DIR / "dev_seen.jsonl"
    print("Downloading Facebook Hateful Memes dev_seen.jsonl...")
    download_file(url_dev, jsonl_path)
    
    records = []
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line.strip()))
                
    print(f"Loaded {len(records)} samples from Hateful Memes dev split.")
    
    # Download first 150 real images from Hugging Face
    base_hf_img = "https://huggingface.co/datasets/neuralcatcher/hateful_memes/resolve/main"
    downloaded_imgs = 0
    hm_records = []
    
    for idx, item in enumerate(records):
        img_rel = item.get("img", "")
        img_name = os.path.basename(img_rel)
        img_disk_path = HATEFUL_MEMES_DIR / "img" / img_name
        
        has_img = False
        if downloaded_imgs < 150 and img_rel:
            try:
                img_url = f"{base_hf_img}/{img_rel}"
                download_file(img_url, img_disk_path)
                has_img = os.path.exists(img_disk_path)
                if has_img:
                    downloaded_imgs += 1
            except Exception:
                has_img = False
        else:
            has_img = os.path.exists(img_disk_path)
            
        hm_records.append({
            "sample_id": f"hateful_memes_dev_{item.get('id', idx)}",
            "dataset_name": "Meta_Hateful_Memes",
            "split": "dev_seen",
            "image_filename": img_name,
            "local_image_path": str(img_disk_path) if has_img else "",
            "has_image_on_disk": has_img,
            "text": str(item.get("text", "")).strip(),
            "source_label": int(item.get("label", 0)),
            "source_label_name": "Hateful" if int(item.get("label", 0)) == 1 else "Non-Hateful",
            "language": "English",
            "modality": "IMAGE_AND_TEXT" if has_img else "TEXT_ONLY"
        })
        
    df_hm = pd.DataFrame(hm_records)
    csv_out = HATEFUL_MEMES_DIR / "hateful_memes_catalog.csv"
    df_hm.to_csv(csv_out, index=False)
    print(f"Saved {len(df_hm)} Hateful Memes records ({downloaded_imgs} images downloaded) to {csv_out}")
    return df_hm

def ingest_zenodo():
    print("\n--- 4. Ingesting Zenodo Multimodal Toxic Memes Dataset ---")
    url_labels = "https://zenodo.org/records/8306439/files/labels.csv"
    csv_path = ZENODO_DIR / "labels.csv"
    print("Downloading Zenodo 8306439 labels.csv...")
    download_file(url_labels, csv_path)
    
    df_zenodo = pd.read_csv(csv_path)
    print(f"Loaded {len(df_zenodo)} records from Zenodo labels.csv (Language: Russian/Cyrillic).")
    return df_zenodo

if __name__ == "__main__":
    df_mo = ingest_multioff()
    df_m3 = ingest_m3()
    df_hm = ingest_hateful_memes()
    df_z = ingest_zenodo()
    print("\n=== Dataset Ingestion Completed Successfully! ===")
