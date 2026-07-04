"""Lazy-loaded singleton wrapper around the trained toxicity model.

Usage:
    from ai.toxicity_detector import get_detector
    is_toxic, score = get_detector().predict("you are awesome")
"""
import os
from typing import Tuple

import joblib

from config import Config


class ToxicityDetector:
    def __init__(self, model_path: str, threshold: float):
        self.model_path = model_path
        self.threshold = threshold
        self._pipeline = None

    def _load(self):
        if self._pipeline is not None:
            return
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"Toxicity model not found at {self.model_path}. "
                "Run `python ai/train_toxicity.py` first."
            )
        self._pipeline = joblib.load(self.model_path)

    def predict(self, text: str) -> Tuple[bool, float]:
        """Return (is_toxic, probability_of_toxic) for one chat message."""
        self._load()
        text = (text or "").strip()
        if not text:
            return False, 0.0
        proba = self._pipeline.predict_proba([text])[0]
        # column 1 is the toxic class probability
        score = float(proba[1])
        return score >= self.threshold, score


_detector: ToxicityDetector | None = None


def get_detector() -> ToxicityDetector:
    global _detector
    if _detector is None:
        _detector = ToxicityDetector(
            Config.TOXICITY_MODEL_PATH, Config.TOXICITY_THRESHOLD
        )
    return _detector
