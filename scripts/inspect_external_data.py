import urllib.request
import ssl
import csv
import io
import sys
import json

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def inspect_zenodo():
    print("=== Checking Zenodo 8306439 (Multimodal Toxic Memes Detection Dataset) ===")
    url = "https://zenodo.org/records/8306439/files/labels.csv"
    req = urllib.request.Request(url, headers={'User-Agent': 'CyberGuard-Auditor/1.0'})
    try:
        with urllib.request.urlopen(req, context=ctx) as r:
            lines = [r.readline().decode('utf-8', errors='ignore') for _ in range(5)]
            print("Headers & Sample rows:")
            for l in lines:
                print(" ", l.strip())
    except Exception as e:
        print("Error fetching Zenodo labels:", e)

def inspect_huggingface():
    print("\n=== Checking Hugging Face Hateful Memes Dataset ===")
    # Check neuralcatcher/hateful_memes or limjiayi/hateful_memes_expanded
    url = "https://huggingface.co/api/datasets/neuralcatcher/hateful_memes"
    req = urllib.request.Request(url, headers={'User-Agent': 'CyberGuard-Auditor/1.0'})
    try:
        with urllib.request.urlopen(req, context=ctx) as r:
            data = json.loads(r.read().decode('utf-8'))
            print("Repo:", data.get('id'))
            print("Downloads:", data.get('downloads'))
            print("Tags:", data.get('tags'))
            print("Description:", str(data.get('description'))[:200])
    except Exception as e:
        print("Error:", e)

def inspect_multioff_hf():
    print("\n=== Checking Hugging Face Multi-modal Offensive Meme ===")
    url = "https://huggingface.co/api/datasets/Ibrahim-Alam/multi-modal_offensive_meme"
    req = urllib.request.Request(url, headers={'User-Agent': 'CyberGuard-Auditor/1.0'})
    try:
        with urllib.request.urlopen(req, context=ctx) as r:
            data = json.loads(r.read().decode('utf-8'))
            print("Repo:", data.get('id'))
            print("Tags:", data.get('tags'))
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    inspect_zenodo()
    inspect_huggingface()
    inspect_multioff_hf()
