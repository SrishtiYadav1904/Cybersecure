import os
import sys
import json
import joblib
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ml.feature_engineering.context_encoder import ContextualEncoder

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "raw" / "support_wellbeing_raw.csv"
MODEL_DIR = BASE_DIR / "trained_models" / "support_model"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

def train_support():
    print("=== Training Support & Emotional Wellbeing Models ===")
    if not DATA_PATH.exists():
        print(f"Data not found at {DATA_PATH}. Run download_datasets.py first.")
        return

    df = pd.read_csv(DATA_PATH)
    texts = df["text"].tolist()
    labels = df["stress_label"].tolist()

    encoder = ContextualEncoder(output_dim=384)
    X = encoder.encode_batch(texts)

    X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=42)

    model = LogisticRegression(max_iter=300)
    model.fit(X_train, y_train)

    score = model.score(X_test, y_test)
    print(f"Wellbeing Stress Classifier Accuracy: {score:.4f}")

    joblib.dump(model, MODEL_DIR / "stress_classifier.joblib")
    with open(MODEL_DIR / "model_config.json", "w") as f:
        json.dump({
            "model_type": "LogisticRegression(Contextual384d)",
            "accuracy": round(float(score), 4),
            "classes": list(set(labels))
        }, f, indent=2)

    print(f"Support model artifacts saved to {MODEL_DIR}")

if __name__ == "__main__":
    train_support()
