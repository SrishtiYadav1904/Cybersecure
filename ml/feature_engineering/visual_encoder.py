import os
import io
import cv2
import numpy as np
from PIL import Image
from typing import Union, List

class VisualEncoder:
    """
    High-Capacity Visual Feature Encoder (128d):
    Extracts deep visual, spatial, and structural representations from image pixels:
    - 64d Spatial Quadrant Color & Intensity Distribution (capturing template composition, dark/light theme, UI cards)
    - 32d Structural Edge & High-Contrast Gradient Spectrum (capturing text bubbles, overlay banners, meme typography)
    - 32d Frequency & Texture Spatial Coefficients (perceptual DCT coefficients distinguishing meme templates)
    - L2-normalized 128-dimensional dense visual embedding.
    """

    def __init__(self, visual_dim: int = 128):
        self.visual_dim = visual_dim

    def encode_image(self, image_input: Union[str, bytes, Image.Image, np.ndarray]) -> np.ndarray:
        """
        Encode an image into a 128-dimensional dense visual embedding.
        Accepts: filepath (str), raw image bytes, PIL Image, or numpy array.
        """
        if image_input is None:
            return np.zeros(self.visual_dim, dtype=np.float32)

        try:
            # 1. Load to OpenCV BGR numpy array
            if isinstance(image_input, (str, os.PathLike)):
                if not os.path.exists(image_input):
                    return np.zeros(self.visual_dim, dtype=np.float32)
                img = cv2.imread(str(image_input))
            elif isinstance(image_input, bytes):
                np_arr = np.frombuffer(image_input, np.uint8)
                img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            elif isinstance(image_input, Image.Image):
                img = cv2.cvtColor(np.array(image_input.convert("RGB")), cv2.COLOR_RGB2BGR)
            elif isinstance(image_input, np.ndarray):
                img = image_input
            else:
                return np.zeros(self.visual_dim, dtype=np.float32)

            if img is None or img.size == 0:
                return np.zeros(self.visual_dim, dtype=np.float32)

            # Resize to standardized visual canvas (224x224)
            canvas = cv2.resize(img, (224, 224), interpolation=cv2.INTER_AREA)
            h, w = canvas.shape[:2]

            features = []

            # A. 64d Spatial Quadrant Color & Intensity (4 quadrants x 16 bins)
            gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
            half_h, half_w = h // 2, w // 2
            quadrants = [
                canvas[0:half_h, 0:half_w],        # Top-Left
                canvas[0:half_h, half_w:w],         # Top-Right
                canvas[half_h:h, 0:half_w],         # Bottom-Left
                canvas[half_h:h, half_w:w]          # Bottom-Right
            ]
            for quad in quadrants:
                quad_gray = cv2.cvtColor(quad, cv2.COLOR_BGR2GRAY)
                hist, _ = np.histogram(quad_gray, bins=16, range=(0, 256), density=True)
                features.extend(hist)

            # B. 32d Structural Edge Spectrum (Sobel X + Sobel Y + Laplacian gradients)
            sobelx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
            sobely = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
            grad_mag = np.sqrt(sobelx**2 + sobely**2)
            edge_hist, _ = np.histogram(grad_mag, bins=16, range=(0, 255), density=True)
            features.extend(edge_hist)

            laplacian = np.abs(cv2.Laplacian(gray, cv2.CV_32F))
            lap_hist, _ = np.histogram(laplacian, bins=16, range=(0, 255), density=True)
            features.extend(lap_hist)

            # C. 32d Frequency / DCT Texture Coefficients
            float_gray = np.float32(gray) / 255.0
            dct = cv2.dct(float_gray)
            # Sample low-to-mid frequency 32-coefficient zigzag block
            dct_coeffs = dct[:8, :4].flatten()
            features.extend(dct_coeffs)

            feature_vec = np.array(features, dtype=np.float32)
            if len(feature_vec) > self.visual_dim:
                feature_vec = feature_vec[:self.visual_dim]
            elif len(feature_vec) < self.visual_dim:
                pad = np.zeros(self.visual_dim - len(feature_vec), dtype=np.float32)
                feature_vec = np.concatenate([feature_vec, pad])

            # L2 Normalization
            norm = np.linalg.norm(feature_vec)
            if norm > 1e-9:
                feature_vec = feature_vec / norm

            return feature_vec.astype(np.float32)

        except Exception as e:
            return np.zeros(self.visual_dim, dtype=np.float32)

    def encode_batch(self, images: List[Union[str, bytes, Image.Image, np.ndarray]]) -> np.ndarray:
        return np.vstack([self.encode_image(img) for img in images])
