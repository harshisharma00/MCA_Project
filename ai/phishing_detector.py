"""Lazy-loaded singleton wrapper around the trained phishing-URL model."""
import os
from typing import Tuple

import joblib
import numpy as np

from ai.url_features import extract_feature_vector
from config import Config


class PhishingDetector:
    def __init__(self, model_path: str, threshold: float):
        self.model_path = model_path
        self.threshold = threshold
        self._pipeline = None

    def _load(self):
        if self._pipeline is not None:
            return
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"Phishing model not found at {self.model_path}. "
                "Run `python ai/train_phishing.py` first."
            )
        self._pipeline = joblib.load(self.model_path)

    def predict(self, url: str) -> Tuple[bool, float]:
        """Return (is_phishing, probability_phishing) for one URL."""
        self._load()
        url = (url or "").strip()
        if not url:
            return False, 0.0
        feats = np.array([extract_feature_vector(url)])
        proba = self._pipeline.predict_proba(feats)[0]
        score = float(proba[1])
        return score >= self.threshold, score


_detector: PhishingDetector | None = None


def get_detector() -> PhishingDetector:
    global _detector
    if _detector is None:
        _detector = PhishingDetector(
            Config.PHISHING_MODEL_PATH, Config.PHISHING_THRESHOLD
        )
    return _detector
