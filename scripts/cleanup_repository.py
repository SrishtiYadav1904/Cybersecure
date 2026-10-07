import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 1. Ensure reports/system_audits directory exists
system_audits_dir = ROOT / "reports" / "system_audits"
system_audits_dir.mkdir(parents=True, exist_ok=True)

# 2. Files to move to reports/system_audits
reports_to_archive = [
    "AUDIT_REPORT.md",
    "DATASET_REPORT.md",
    "DATA_QUALITY_REPORT.md",
    "DATASET_PROVENANCE_REPORT.md",
    "FORENSIC_PIPELINE_REPORT.md",
    "IMPLEMENTATION_STATUS.md",
    "INFERENCE_BENCHMARK.md",
    "INFERENCE_TEST_REPORT.md",
    "MODEL_AUDIT.md",
    "MODEL_TRAINING_REPORT.md",
    "MULTIMODAL_DATASET_REPORT.md",
    "MULTIMODAL_MODEL_REPORT.md",
    "OCR_EVALUATION_REPORT.md",
    "SECURITY_RBAC_REPORT.md",
    "TRAINING_AUDIT.md",
    "UI_AUDIT.md",
    "UI_REVIEW_REPORT.md"
]

for filename in reports_to_archive:
    src = ROOT / filename
    if src.exists():
        dst = system_audits_dir / filename
        shutil.move(str(src), str(dst))
        print(f"Moved {filename} -> reports/system_audits/")

# 3. Duplicate reports to delete (already in reports/dataset_audit/)
duplicates_to_remove = [
    "DATASET_AUDIT_REPORT.md",
    "DATASET_CLASS_DISTRIBUTION.csv",
    "DATASET_DUPLICATE_ANALYSIS.md",
    "DATASET_INVENTORY.csv",
    "DATASET_LANGUAGE_DISTRIBUTION.csv",
    "DATASET_LEAKAGE_ANALYSIS.md",
    "DATASET_MODALITY_ANALYSIS.csv",
    "dataset_provenance.csv",
    "EXTERNAL_DATA_USAGE_AUDIT.md",
    "MENTAL_DATASET_ANALYSIS.md",
    "POLEVAL_ANALYSIS.md"
]

for filename in duplicates_to_remove:
    p = ROOT / filename
    if p.exists():
        p.unlink()
        print(f"Removed duplicate file: {filename}")

# 4. Remove unnecessary temporary folders
temp_dirs = [
    ROOT / "catboost_info",
    ROOT / "scratch",
    ROOT / ".pytest_cache"
]

for td in temp_dirs:
    if td.exists():
        shutil.rmtree(str(td), ignore_errors=True)
        print(f"Removed temporary directory: {td.name}")

print("\nRepository cleanup completed successfully.")
