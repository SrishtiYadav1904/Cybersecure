import numpy as np
from typing import Union, Optional

class MultimodalFeatureFusion:
    """
    Multimodal Feature Fusion Layer:
    Fuses Textual Representation (414d = 30d GloVe/PCA + 384d Contextual)
    with Visual Representation (128d Visual Encoder) into a 542-dimensional unified vector.

    Supports 3 operational modalities:
    1. TEXT_ONLY: Visual components zero-damped; text components weighted.
    2. IMAGE_ONLY: Text components zero-damped; visual components weighted.
    3. MULTIMODAL (IMAGE + TEXT): Both modalities fused with adaptive modality weights.
    """

    def __init__(self, text_dim: int = 414, visual_dim: int = 128, text_weight: float = 1.0, visual_weight: float = 0.8):
        self.text_dim = text_dim
        self.visual_dim = visual_dim
        self.text_weight = text_weight
        self.visual_weight = visual_weight
        self.fused_dim = text_dim + visual_dim # 542d

    def fuse(self, text_features: Optional[np.ndarray], visual_features: Optional[np.ndarray], modality: str = "MULTIMODAL") -> np.ndarray:
        """
        Fuse text and visual vectors for single instance or batch.
        """
        is_batch = (text_features is not None and text_features.ndim > 1) or (visual_features is not None and visual_features.ndim > 1)
        n_samples = 1
        if text_features is not None and text_features.ndim > 1:
            n_samples = text_features.shape[0]
        elif visual_features is not None and visual_features.ndim > 1:
            n_samples = visual_features.shape[0]

        # Prepare Text Matrix
        if text_features is not None:
            t_mat = text_features.copy()
            if not is_batch and t_mat.ndim == 1:
                t_mat = t_mat.reshape(1, -1)
            t_mat = t_mat * self.text_weight
        else:
            t_mat = np.zeros((n_samples, self.text_dim), dtype=np.float32)

        # Prepare Visual Matrix
        if visual_features is not None:
            v_mat = visual_features.copy()
            if not is_batch and v_mat.ndim == 1:
                v_mat = v_mat.reshape(1, -1)
            v_mat = v_mat * self.visual_weight
        else:
            v_mat = np.zeros((n_samples, self.visual_dim), dtype=np.float32)

        # Apply Modality Gates
        if modality == "TEXT_ONLY":
            v_mat = np.zeros_like(v_mat)
        elif modality == "IMAGE_ONLY":
            t_mat = np.zeros_like(t_mat)

        # Concatenate: (N, 414 + 128) = (N, 542)
        fused = np.hstack([t_mat, v_mat]).astype(np.float32)

        # Row-wise L2 Normalization
        norms = np.linalg.norm(fused, axis=1, keepdims=True)
        norms[norms < 1e-9] = 1.0
        normalized = fused / norms

        if not is_batch:
            return normalized[0]
        return normalized
