import os
import sys
import io
import csv
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from backend.app.ocr.ocr_engine import get_ocr_engine

BENCHMARK_DIR = BASE_DIR / "data" / "ocr_benchmark"
IMG_DIR = BENCHMARK_DIR / "images"
IMG_DIR.mkdir(parents=True, exist_ok=True)

def levenshtein_distance(s1: str, s2: str) -> int:
    """Compute character-level Levenshtein edit distance."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def calculate_cer(reference: str, hypothesis: str) -> float:
    """Character Error Rate = edit_distance(ref, hyp) / len(ref)"""
    ref_clean = reference.strip()
    hyp_clean = hypothesis.strip()
    if not ref_clean:
        return 0.0 if not hyp_clean else 1.0
    dist = levenshtein_distance(ref_clean, hyp_clean)
    return round(float(dist) / float(len(ref_clean)), 4)

def calculate_wer(reference: str, hypothesis: str) -> float:
    """Word Error Rate = edit_distance(ref_words, hyp_words) / len(ref_words)"""
    ref_words = reference.strip().split()
    hyp_words = hypothesis.strip().split()
    if not ref_words:
        return 0.0 if not hyp_words else 1.0
    dist = levenshtein_distance(" ".join(ref_words), " ".join(hyp_words))
    # Approximate WER by token comparison
    diff = sum(1 for w in hyp_words if w not in ref_words) + abs(len(ref_words) - len(hyp_words))
    return round(min(1.0, float(diff) / float(len(ref_words))), 4)

# Benchmark test definitions with realistic visual parameters
BENCHMARK_CASES = [
    {
        "case_id": "OCR-01",
        "name": "WhatsApp Light Mode — English Threat",
        "ground_truth": "I know where you live. Watch your back.",
        "bg_color": (255, 255, 255),
        "text_color": (15, 20, 25),
        "bubble_color": (220, 248, 198), # WhatsApp incoming bubble green
        "platform": "WhatsApp (Light)",
        "language": "English",
        "dimensions": (720, 180),
        "header": "Alex User • 10:42 PM",
        "is_dark": False,
        "blur": False
    },
    {
        "case_id": "OCR-02",
        "name": "WhatsApp Dark Mode — Hinglish Colloquial Threat",
        "ground_truth": "moti bhaisn marr jaa tu jaake",
        "bg_color": (18, 27, 34),        # WhatsApp dark background
        "text_color": (233, 237, 239),
        "bubble_color": (32, 44, 51),     # WhatsApp dark bubble
        "platform": "WhatsApp (Dark)",
        "language": "Hinglish",
        "dimensions": (720, 180),
        "header": "Unknown • 11:15 PM",
        "is_dark": True,
        "blur": False
    },
    {
        "case_id": "OCR-03",
        "name": "Instagram Dark Mode — Devanagari Hindi Threat",
        "ground_truth": "घर से बाहर निकल, तुझे जान से मार दूंगा आज।",
        "bg_color": (0, 0, 0),            # Instagram black
        "text_color": (245, 245, 245),
        "bubble_color": (38, 38, 38),
        "platform": "Instagram (Dark)",
        "language": "Hindi (Devanagari)",
        "dimensions": (720, 180),
        "header": "@troll_account22 • 2h ago",
        "is_dark": True,
        "blur": False
    },
    {
        "case_id": "OCR-04",
        "name": "YouTube Light Mode — Hinglish Insult",
        "ground_truth": "tu chutiya hai aur rahega hamesha",
        "bg_color": (249, 249, 249),      # YouTube light background
        "text_color": (15, 15, 15),
        "bubble_color": (255, 255, 255),
        "platform": "YouTube (Light)",
        "language": "Hinglish",
        "dimensions": (720, 180),
        "header": "User9817 • 14 minutes ago",
        "is_dark": False,
        "blur": False
    },
    {
        "case_id": "OCR-05",
        "name": "X / Twitter Dark Mode — Explicit Threat",
        "ground_truth": "I will rape you and destroy your life",
        "bg_color": (0, 0, 0),            # Twitter AMOLED dark
        "text_color": (231, 233, 234),
        "bubble_color": (22, 24, 28),
        "platform": "X/Twitter (Dark)",
        "language": "English",
        "dimensions": (720, 180),
        "header": "Anonymous @stalker_01 • 5m",
        "is_dark": True,
        "blur": False
    },
    {
        "case_id": "OCR-06",
        "name": "Multi-Message Harassment — Consecutive Bubbles",
        "ground_truth": "Hey answer me. Why are you ignoring my DMs? We will leak your private photos.",
        "bg_color": (15, 23, 42),
        "text_color": (241, 245, 249),
        "bubble_color": (30, 41, 59),
        "platform": "Chat Multi-Message",
        "language": "English",
        "dimensions": (720, 240),
        "header": "Targeted Harasser • 3 messages",
        "is_dark": True,
        "blur": False
    },
    {
        "case_id": "OCR-07",
        "name": "Low-Resolution / Small Font — Abusive Comment",
        "ground_truth": "You disgusting scum, everyone here despises you",
        "bg_color": (240, 242, 245),
        "text_color": (50, 50, 50),
        "bubble_color": (255, 255, 255),
        "platform": "Facebook (Light)",
        "language": "English",
        "dimensions": (480, 120),          # Small resolution
        "header": "Comment • 1h",
        "is_dark": False,
        "blur": False
    },
    {
        "case_id": "OCR-08",
        "name": "Mixed Hindi-English Code-Switched Comment",
        "ground_truth": "Saale idiot, tera address mil gaya hai mujhe",
        "bg_color": (20, 24, 30),
        "text_color": (225, 230, 240),
        "bubble_color": (35, 42, 54),
        "platform": "Telegram (Dark)",
        "language": "Hinglish",
        "dimensions": (720, 180),
        "header": "Forwarded message • 18:30",
        "is_dark": True,
        "blur": False
    },
    {
        "case_id": "OCR-09",
        "name": "Slightly Blurred / Noisy Screenshot",
        "ground_truth": "I will track your IP and destroy your family",
        "bg_color": (245, 245, 250),
        "text_color": (30, 30, 35),
        "bubble_color": (255, 255, 255),
        "platform": "Recompressed Screenshot",
        "language": "English",
        "dimensions": (720, 180),
        "header": "Discord Message • Today at 4:15 PM",
        "is_dark": False,
        "blur": True
    },
    {
        "case_id": "OCR-10",
        "name": "Clean Benign Conversational Screenshot",
        "ground_truth": "Thank you so much for explaining the code, really helpful project!",
        "bg_color": (255, 255, 255),
        "text_color": (20, 20, 20),
        "bubble_color": (240, 245, 255),
        "platform": "Slack (Light)",
        "language": "English",
        "dimensions": (720, 180),
        "header": "Colleague • 09:30 AM",
        "is_dark": False,
        "blur": False
    }
]

def render_screenshot(case: dict) -> Path:
    w, h = case["dimensions"]
    img = Image.new("RGB", (w, h), color=case["bg_color"])
    d = ImageDraw.Draw(img)

    # Draw simulated UI card/bubble
    bubble_x0, bubble_y0 = 30, 25
    bubble_x1, bubble_y1 = w - 30, h - 25
    d.rounded_rectangle([bubble_x0, bubble_y0, bubble_x1, bubble_y1], radius=12, fill=case["bubble_color"])

    # Draw header (sender + timestamp)
    header_color = (130, 140, 150) if case["is_dark"] else (100, 110, 120)
    d.text((bubble_x0 + 20, bubble_y0 + 15), case["header"], fill=header_color)

    # Draw main message text
    d.text((bubble_x0 + 20, bubble_y0 + 45), case["ground_truth"], fill=case["text_color"])

    if case["blur"]:
        img = img.filter(ImageFilter.GaussianBlur(radius=0.8))

    filename = f"{case['case_id']}.png"
    out_path = IMG_DIR / filename
    img.save(out_path, format="PNG")
    return out_path

def run_benchmark():
    print("=== CyberGuard Empirical OCR Benchmark Suite ===")
    print(f"Evaluating {len(BENCHMARK_CASES)} representative platform screenshots...\n")

    engine = get_ocr_engine()
    print(f"Active OCR Engine Backend: {engine.backend}\n")

    results = []

    for case in BENCHMARK_CASES:
        img_path = render_screenshot(case)
        with open(img_path, "rb") as f:
            img_bytes = f.read()

        ocr_meta = engine.extract_with_metadata(img_bytes, filename=img_path.name)
        extracted = ocr_meta["extracted_text"]
        conf = ocr_meta["confidence"]

        # Calculate metrics
        cer = calculate_cer(case["ground_truth"], extracted)
        wer = calculate_wer(case["ground_truth"], extracted)

        status = "PASSED" if cer <= 0.35 else "PARTIAL" if cer <= 0.60 else "FAILED"

        results.append({
            "case_id": case["case_id"],
            "platform": case["platform"],
            "language": case["language"],
            "ground_truth": case["ground_truth"],
            "extracted_text": extracted,
            "ocr_confidence": conf,
            "character_error_rate": cer,
            "word_error_rate": wer,
            "status": status,
            "image_path": str(img_path)
        })

        print(f"[{case['case_id']}] {case['platform']} ({case['language']})")
        print(f"  Ground Truth: \"{case['ground_truth']}\"")
        print(f"  Extracted:    \"{extracted}\"")
        print(f"  Conf: {conf * 100:.2f}% | CER: {cer:.4f} | WER: {wer:.4f} | Status: {status}")
        print("-" * 70)

    # Save to CSV
    csv_file = BENCHMARK_DIR / "ocr_benchmark_results.csv"
    keys = results[0].keys()
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)

    avg_cer = np.mean([r["character_error_rate"] for r in results])
    avg_wer = np.mean([r["word_error_rate"] for r in results])
    avg_conf = np.mean([r["ocr_confidence"] for r in results])
    pass_count = sum(1 for r in results if r["status"] == "PASSED")

    print(f"\n-> Saved benchmark results to {csv_file}")
    print(f"Summary: {pass_count}/{len(results)} Passed | Mean CER: {avg_cer:.4f} | Mean WER: {avg_wer:.4f} | Mean Conf: {avg_conf * 100:.2f}%")

if __name__ == "__main__":
    run_benchmark()
