import urllib.request
import json
import ssl
from pathlib import Path

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'CyberGuard-Research/1.0'})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
            return json.loads(r.read().decode('utf-8'))
    except Exception as e:
        return {"error": str(e)}

def investigate():
    print("=== 1. Investigating MultiOFF GitHub Repository ===")
    url = "https://api.github.com/repos/bharathichezhiyan/Multimodal-Meme-Classification-Identifying-Offensive-Content-in-Image-and-Text/contents"
    data = fetch_json(url)
    if isinstance(data, list):
        for item in data:
            print(f"- {item['name']} ({item['type']}, size={item.get('size', 0)})")
    else:
        print("GitHub error:", data)

    print("\n=== 2. Investigating Hugging Face for Hateful Memes / Multimodal Toxicity ===")
    hf_queries = [
        "https://huggingface.co/api/datasets?search=hateful_memes&limit=5",
        "https://huggingface.co/api/datasets?search=multimodal+offensive&limit=5",
        "https://huggingface.co/api/datasets?search=cyberbullying&limit=5",
        "https://huggingface.co/api/datasets?search=toxic+memes&limit=5"
    ]
    for hf_url in hf_queries:
        print(f"\nQuery: {hf_url}")
        res = fetch_json(hf_url)
        if isinstance(res, list):
            for d in res[:4]:
                print(f"  * {d.get('id')} | Downloads: {d.get('downloads', 0)} | Tags: {d.get('tags', [])[:4]}")
        else:
            print("  Error:", res)

    print("\n=== 3. Investigating Zenodo for Multimodal Toxic Memes ===")
    zenodo_url = "https://zenodo.org/api/records?q=multimodal+toxic+memes&size=5"
    z_data = fetch_json(zenodo_url)
    if "hits" in z_data and "hits" in z_data["hits"]:
        for hit in z_data["hits"]["hits"]:
            meta = hit.get("metadata", {})
            print(f"  * Title: {meta.get('title')} | DOI: {hit.get('doi')} | ID: {hit.get('id')}")
            for f in hit.get("files", [])[:3]:
                print(f"    - File: {f.get('key')} ({f.get('size', 0)} bytes)")
    else:
        print("Zenodo error:", z_data)

if __name__ == "__main__":
    investigate()
