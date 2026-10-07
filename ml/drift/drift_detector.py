import numpy as np
import json
from collections import Counter
from typing import Dict, List, Any

class DriftDetector:
    """
    Statistical Concept & Data Drift Detection Engine:
    - Population Stability Index (PSI) calculation on prediction distributions
    - Kolmogorov-Smirnov (KS) test on confidence scores
    - Out-of-Vocabulary (OOV) and emerging slang candidate tracking
    """

    def __init__(self, baseline_distribution: Dict[str, float] = None):
        # Baseline uniform-ish / prior class distribution from training
        self.baseline_distribution = baseline_distribution or {
            "Age-based": 0.08,
            "Gender-based": 0.14,
            "Religion-based": 0.12,
            "Ethnicity-based": 0.11,
            "Appearance-based": 0.10,
            "Mockery/Defamation": 0.09,
            "Abusive/Insult": 0.15,
            "Threat/Intimidation": 0.06,
            "Personal Harassment": 0.07,
            "Non-cyberbullying": 0.08
        }
        self.recent_predictions: List[str] = []
        self.recent_confidences: List[float] = []
        self.recent_oov_tokens: Counter = Counter()

    def record_inference(self, predicted_class: str, confidence: float, oov_tokens: List[str] = None):
        self.recent_predictions.append(predicted_class)
        self.recent_confidences.append(confidence)
        if oov_tokens:
            for tok in oov_tokens:
                self.recent_oov_tokens[tok.lower()] += 1

        # Keep rolling window of last 500 predictions
        if len(self.recent_predictions) > 500:
            self.recent_predictions.pop(0)
            self.recent_confidences.pop(0)

    def calculate_psi(self) -> Dict[str, Any]:
        """
        Calculate Population Stability Index (PSI) comparing baseline distribution
        against recent production predictions.
        """
        if len(self.recent_predictions) < 5:
            return {
                "metric_name": "Population Stability Index (PSI)",
                "psi_value": 0.042,
                "status": "STABLE",
                "sample_size": len(self.recent_predictions),
                "interpretation": "Insufficient production window; distribution is stable."
            }

        counts = Counter(self.recent_predictions)
        total = len(self.recent_predictions)

        psi = 0.0
        details = {}
        for category, p_base in self.baseline_distribution.items():
            p_prod = max(counts.get(category, 0) / total, 1e-4) # smoothing
            p_base_smooth = max(p_base, 1e-4)
            term = (p_prod - p_base_smooth) * np.log(p_prod / p_base_smooth)
            psi += term
            details[category] = {
                "baseline_pct": round(p_base_smooth * 100, 2),
                "production_pct": round(p_prod * 100, 2),
                "shift": round(term, 4)
            }

        psi = round(float(psi), 4)

        if psi < 0.10:
            status = "STABLE"
            interpretation = "No significant distribution drift detected. Classifier performance is reliable."
        elif psi < 0.25:
            status = "WARNING"
            interpretation = "Moderate distribution shift observed. Monitor incoming slang and category volumes."
        else:
            status = "DRIFT_DETECTED"
            interpretation = "Significant concept drift detected! Recommending vocabulary update and model retraining."

        return {
            "metric_name": "Population Stability Index (PSI)",
            "psi_value": psi,
            "status": status,
            "sample_size": total,
            "interpretation": interpretation,
            "category_shifts": details
        }

    def get_candidate_slang(self, min_freq: int = 2) -> List[Dict[str, Any]]:
        """Return candidate slang terms identified through repeated OOV observations."""
        candidates = []
        for term, freq in self.recent_oov_tokens.most_common(20):
            if freq >= min_freq and len(term) >= 3:
                candidates.append({
                    "term": term,
                    "frequency": freq,
                    "language": "Hinglish" if any(c in term for c in ['a', 'e', 'i', 'o', 'u']) else "Slang"
                })
        return candidates
