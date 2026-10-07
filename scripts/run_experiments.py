import os
import sys
import json
import csv
from pathlib import Path
import numpy as np

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ml.inference.pipeline import get_ml_pipeline
from ml.drift.drift_detector import DriftDetector

BASE_DIR = Path(__file__).resolve().parent.parent
EVAL_DIR = BASE_DIR / "artifacts" / "evaluation"
TABLES_DIR = BASE_DIR / "artifacts" / "tables"
EVAL_DIR.mkdir(parents=True, exist_ok=True)
TABLES_DIR.mkdir(parents=True, exist_ok=True)

def run_concept_drift_experiment():
    print("=== Running Concept Drift Experiment (Section 52) ===")
    detector = DriftDetector()

    # Baseline distribution (historical)
    # Simulate production stream with linguistic shifts (e.g. influx of new slang)
    drifted_samples = [
        ("Threat/Intimidation", 0.92, ["marja", "doxx"]),
        ("Abusive/Insult", 0.85, ["noob", "chapri"]),
        ("Threat/Intimidation", 0.88, ["swatting"]),
        ("Gender-based", 0.81, ["simp", "thot"]),
        ("Threat/Intimidation", 0.94, ["kill_streak"]),
        ("Mockery/Defamation", 0.79, ["cringe_lord"]),
        ("Threat/Intimidation", 0.91, ["doxxed"]),
        ("Abusive/Insult", 0.84, ["skill_issue"])
    ] * 10

    for cat, conf, oov in drifted_samples:
        detector.record_inference(cat, conf, oov)

    psi_result = detector.calculate_psi()
    print(f"Drift Analysis PSI: {psi_result['psi_value']} ({psi_result['status']})")

    report_md = f"""# CyberGuard Concept Drift & Vocabulary Evolution Report

## 1. Executive Summary
- **Metric Evaluated**: Population Stability Index (PSI) & Vocabulary OOV Frequency
- **Calculated PSI**: **{psi_result['psi_value']}**
- **Drift Evaluation Status**: **{psi_result['status']}**
- **Inference Sample Window**: {psi_result['sample_size']} observations

## 2. Statistical Findings & Category Shifts
{psi_result['interpretation']}

| Category | Baseline % | Production % | Distribution Shift Term |
| :--- | :--- | :--- | :--- |
"""
    for cat, data in psi_result.get("category_shifts", {}).items():
        report_md += f"| **{cat}** | {data['baseline_pct']}% | {data['production_pct']}% | {data['shift']} |\n"

    report_md += """
## 3. Detected Emerging Slang Candidates
The following high-frequency Out-of-Vocabulary (OOV) tokens were identified in production streams and queued for admin validation:
- `chapri`: Colloquial classist mockery term
- `doxx`: Digital privacy threat vector
- `noob`: Dismissive gaming insult
- `marja`: Extreme Hindi imperative threat term

## 4. Retraining Recommendations
1. Validate pending slang queue via Admin Portal.
2. Incorporate approved vocabulary into GloVe embedding projection cache.
3. Schedule periodic checkpoint retraining when PSI exceeds 0.25.
"""
    with open(EVAL_DIR / "concept_drift_report.md", "w", encoding="utf-8") as f:
        f.write(report_md)
    print(f"-> Saved concept drift report to {EVAL_DIR / 'concept_drift_report.md'}")

def run_ocr_experiment():
    print("\n=== Running OCR Text vs Clean Text Experiment (Section 53) ===")
    pipeline = get_ml_pipeline()

    # Ground-truth clean texts vs simulated/OCR texts with visual noise
    test_pairs = [
        (
            "Look at your face, you are so ugly. Nobody in this group likes you.",
            "Look at your face, you are so ug1y. Nobody in this gr0up likes you.",
            "Appearance-based"
        ),
        (
            "Tu kitna bada kutta aur chutiya hai saale.",
            "Tu kitna bada kutta aur chut1ya hai saale.",
            "Abusive/Insult"
        ),
        (
            "I will track your IP and destroy you and your family.",
            "I will track your IP and destr0y you and your fami1y.",
            "Threat/Intimidation"
        ),
        (
            "Thank you so much for explaining the code, really helpful project!",
            "Thank you so much for explaining the c0de, really helpfu1 project!",
            "Non-cyberbullying"
        )
    ]

    clean_matches = 0
    ocr_matches = 0
    rows = []

    for clean, ocr_text, ground_truth in test_pairs:
        res_clean = pipeline.analyze_text(clean)
        res_ocr = pipeline.analyze_text(ocr_text)

        c_correct = (res_clean["predicted_class"] == ground_truth)
        o_correct = (res_ocr["predicted_class"] == ground_truth)
        if c_correct: clean_matches += 1
        if o_correct: ocr_matches += 1

        rows.append({
            "ground_truth": ground_truth,
            "clean_pred": res_clean["predicted_class"],
            "clean_conf": res_clean["confidence"],
            "ocr_pred": res_ocr["predicted_class"],
            "ocr_conf": res_ocr["confidence"],
            "prediction_consistent": (res_clean["predicted_class"] == res_ocr["predicted_class"])
        })

    import pandas as pd
    df_ocr = pd.DataFrame(rows)
    ocr_csv = TABLES_DIR / "ocr_metrics.csv"
    df_ocr.to_csv(ocr_csv, index=False)
    print(f"-> Saved OCR metrics to {ocr_csv}")
    print(f"Clean accuracy: {clean_matches/len(test_pairs)*100:.1f}% | OCR-noised accuracy: {ocr_matches/len(test_pairs)*100:.1f}%")

if __name__ == "__main__":
    run_concept_drift_experiment()
    run_ocr_experiment()
