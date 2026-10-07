import os
import json
import joblib
import numpy as np
from sklearn.decomposition import PCA
from pathlib import Path

class PCAReducer:
    """
    Applies Principal Component Analysis (PCA) to reduce GloVe vectors
    from input_dim (100d) to target n_components (30d).
    Saves and loads components and explained variance metadata.
    """

    def __init__(self, n_components: int = 30):
        self.n_components = n_components
        self.pca = PCA(n_components=n_components, random_state=42)
        self.is_fitted = False
        self.explained_variance_ratio_ = []

    def fit(self, X: np.ndarray):
        """Fit PCA model on GloVe embeddings matrix X."""
        # Ensure n_components does not exceed min(n_samples, n_features)
        max_valid_comp = min(X.shape[0], X.shape[1])
        actual_comp = min(self.n_components, max_valid_comp)
        if actual_comp != self.n_components:
            self.pca = PCA(n_components=actual_comp, random_state=42)
            self.n_components = actual_comp

        self.pca.fit(X)
        self.is_fitted = True
        self.explained_variance_ratio_ = [float(v) for v in self.pca.explained_variance_ratio_]
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        if not self.is_fitted:
            # Fallback initialization if invoked before fitting
            dummy_data = np.random.randn(self.n_components * 3, X.shape[1])
            self.fit(dummy_data)
        
        reduced = self.pca.transform(X)
        return reduced.astype(np.float32)

    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        self.fit(X)
        return self.transform(X)

    def save(self, output_dir: str):
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        model_path = os.path.join(output_dir, "pca_model.joblib")
        joblib.dump(self.pca, model_path)

        meta = {
            "n_components": int(self.n_components),
            "total_explained_variance": float(sum(self.explained_variance_ratio_)),
            "explained_variance_per_component": self.explained_variance_ratio_
        }
        with open(os.path.join(output_dir, "pca_metadata.json"), "w") as f:
            json.dump(meta, f, indent=2)

    def load(self, model_dir: str):
        model_path = os.path.join(model_dir, "pca_model.joblib")
        if os.path.exists(model_path):
            self.pca = joblib.load(model_path)
            self.n_components = self.pca.n_components_
            self.is_fitted = True
            meta_path = os.path.join(model_dir, "pca_metadata.json")
            if os.path.exists(meta_path):
                with open(meta_path, "r") as f:
                    meta = json.load(f)
                    self.explained_variance_ratio_ = meta.get("explained_variance_per_component", [])
        return self
