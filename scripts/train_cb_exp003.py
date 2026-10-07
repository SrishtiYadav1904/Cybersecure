import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import catboost
import lightgbm
import pandas as pd
import sklearn
import xgboost

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from ml.feature_engineering.context_encoder import ContextualEncoder
from ml.feature_engineering.fusion import FeatureFusion
from ml.feature_engineering.glove_embedder import GloVeEmbedder
from ml.feature_engineering.pca_reducer import PCAReducer
from ml.models.classifier import CyberbullyingAMLClassifier, UNIFIED_CLASSES
from scripts.train_baseline_and_expanded import evaluate_models, extract_features


def main():
    data_dir = PROJECT_ROOT / "data" / "unified" / "cyberbullying_cb003"
    train_path = data_dir / "train.parquet"
    validation_path = data_dir / "validation.parquet"

    df_train = pd.read_parquet(train_path)
    df_validation = pd.read_parquet(validation_path)

    print(f"Training rows: {len(df_train)}")
    print(f"Validation rows: {len(df_validation)}")

    glove = GloVeEmbedder(embedding_dim=100)
    pca = PCAReducer(n_components=30)
    context_encoder = ContextualEncoder(output_dim=384)
    fusion = FeatureFusion(pca_weight=1.0, ctx_weight=1.2)

    print("Extracting training features...")
    X_train = extract_features(
        df_train["normalized_text"].tolist(),
        glove, pca, context_encoder, fusion, is_train=True,
    )
    y_train = df_train["label"].tolist()

    print("Extracting validation features...")
    X_validation = extract_features(
        df_validation["normalized_text"].tolist(),
        glove, pca, context_encoder, fusion, is_train=False,
    )
    y_validation = df_validation["label"].tolist()

    print("Fitting classifier with out-of-fold stacking...")
    classifier = CyberbullyingAMLClassifier(classes=UNIFIED_CLASSES)
    classifier.fit(X_train, y_train)

    print("Evaluating on validation data...")
    validation_metrics = evaluate_models(
        classifier,
        X_validation,
        y_validation,
        "CB-DATA-003-VALIDATION",
        "CB-EXP-004",
        classifier.classes,
    )

    output_dir = PROJECT_ROOT / "trained_models" / "cyberbullying" / "CB-EXP-004"
    output_dir.mkdir(parents=True, exist_ok=True)
    classifier.save(str(output_dir))
    pca.save(str(output_dir))

    manifest = {
        "model_version": "CB-EXP-004",
        "dataset_version": "CB-DATA-003",
        "training_timestamp": datetime.now(timezone.utc).isoformat(),
        "random_seed": 42,
        "n_train_samples": len(df_train),
        "n_validation_samples": len(df_validation),
        "feature_dim": 414,
        "classes": classifier.classes,
        "validation_metrics": validation_metrics,
        "library_versions": {
            "scikit_learn": sklearn.__version__,
            "xgboost": xgboost.__version__,
            "lightgbm": lightgbm.__version__,
            "catboost": catboost.__version__,
        },
    }

    with (output_dir / "training_manifest.json").open("w", encoding="utf-8") as file:
        json.dump(manifest, file, indent=2)

    with (output_dir / "metrics.json").open("w", encoding="utf-8") as file:
        json.dump(validation_metrics, file, indent=2)

    print(f"Candidate artifacts saved to: {output_dir}")
    for result in validation_metrics:
        print(
            f"{result['model']}: "
            f"macro-F1={result['macro_f1']:.4f}, "
            f"accuracy={result['accuracy']:.4f}"
        )


if __name__ == "__main__":
    main()