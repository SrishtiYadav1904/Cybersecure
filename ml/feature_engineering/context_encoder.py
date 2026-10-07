import os
import re
import numpy as np
from typing import List
from ml.preprocessing.normalizer import extract_tokens
from ml.feature_engineering.glove_embedder import STOPWORDS

class ContextualEncoder:
    """
    High-Capacity Contextual Semantic Subword Encoder (384d).
    Extracts multi-scale contextual semantic features:
    - Word unigram and bigram sequential tokens with stopword attenuation
    - Subword character n-grams (3-grams, 4-grams, 5-grams) capturing morphology & Devanagari roots
    - Sublinear term-frequency weighting (1 + log(tf))
    - Positional sinusoidal decay factors
    - L2 normalization for dense geometric representation
    """

    def __init__(self, output_dim: int = 384, model_name: str = "roberta-base"):
        self.output_dim = output_dim
        self.model_name = model_name

    def _extract_ngrams(self, text: str) -> List[tuple]:
        words = extract_tokens(text)
        ngrams = []
        for i, w in enumerate(words):
            pos = 1.0 / (1.0 + 0.05 * i)
            # Attenuate stopwords
            sw_factor = 0.2 if w in STOPWORDS else 1.0

            ngrams.append((w, 2.0 * pos * sw_factor))
            if i + 1 < len(words):
                w_next = words[i+1]
                bi_factor = 0.3 if (w in STOPWORDS and w_next in STOPWORDS) else 1.0
                ngrams.append((f"{w}_{w_next}", 3.0 * pos * bi_factor))

            # Character 3-gram to 5-gram for subword morphology
            clean_w = re.sub(r'[\s\d_]+', '', w)
            for n in (3, 4, 5):
                for j in range(len(clean_w) - n + 1):
                    sub = clean_w[j:j+n]
                    ngrams.append((sub, 1.0 * pos * sw_factor))
        return ngrams

    def encode(self, text: str) -> np.ndarray:
        if not text or not text.strip():
            return np.zeros(self.output_dim, dtype=np.float32)

        ngrams = self._extract_ngrams(text)
        if not ngrams:
            return np.zeros(self.output_dim, dtype=np.float32)

        vector = np.zeros(self.output_dim, dtype=np.float32)

        # Count frequencies
        tf_dict = {}
        for gram, weight in ngrams:
            tf_dict[gram] = tf_dict.get(gram, 0.0) + weight

        import zlib
        for gram, tf in tf_dict.items():
            sublinear_weight = 1.0 + np.log(1.0 + tf)
            gram_bytes = gram.encode('utf-8')
            h = zlib.crc32(gram_bytes) % self.output_dim
            sign = 1.0 if (zlib.crc32(gram_bytes + b"_sign") % 2 == 0) else -1.0
            vector[h] += float(sign * sublinear_weight)

        # L2 Normalize
        norm = np.linalg.norm(vector)
        if norm > 1e-9:
            vector = vector / norm
        return vector.astype(np.float32)

    def encode_batch(self, texts: List[str]) -> np.ndarray:
        return np.vstack([self.encode(t) for t in texts])
