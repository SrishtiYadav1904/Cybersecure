import numpy as np

class FeatureFusion:
    """
    Feature Fusion Layer:
    Combines low-rank PCA-GloVe semantic vector (30d) with
    RoBERTa/Contextual semantic vector (384d).
    Output: Unified, normalized feature representation (414d).
    """

    def __init__(self, pca_weight: float = 1.0, ctx_weight: float = 1.2):
        self.pca_weight = pca_weight
        self.ctx_weight = ctx_weight

    def fuse(self, v_pca: np.ndarray, v_ctx: np.ndarray) -> np.ndarray:
        """
        Fuse single or 2D batch of vectors.
        v_pca: (30,) or (N, 30)
        v_ctx: (384,) or (N, 384)
        """
        is_1d = (v_pca.ndim == 1)
        if is_1d:
            v_pca = v_pca.reshape(1, -1)
            v_ctx = v_ctx.reshape(1, -1)

        # Normalize components individually
        norm_pca = np.linalg.norm(v_pca, axis=1, keepdims=True)
        norm_ctx = np.linalg.norm(v_ctx, axis=1, keepdims=True)

        v_pca_norm = v_pca / np.maximum(norm_pca, 1e-9) * self.pca_weight
        v_ctx_norm = v_ctx / np.maximum(norm_ctx, 1e-9) * self.ctx_weight

        # Concatenate horizontally
        fused = np.hstack([v_pca_norm, v_ctx_norm])

        # Global L2 normalization
        fused_norm = np.linalg.norm(fused, axis=1, keepdims=True)
        fused = fused / np.maximum(fused_norm, 1e-9)

        if is_1d:
            return fused.squeeze(0).astype(np.float32)
        return fused.astype(np.float32)
