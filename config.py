"""Application configuration.

All paths are relative to the project root so the app runs the same
on Windows, Linux, or macOS.
"""
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "metaverse-threat-detection-dev-key")

    # SQLite DB stored under instance/
    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" + os.path.join(BASE_DIR, "instance", "metaverse.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Trained model paths
    TOXICITY_MODEL_PATH = os.path.join(BASE_DIR, "models_pkl", "toxicity_model.pkl")
    PHISHING_MODEL_PATH = os.path.join(BASE_DIR, "models_pkl", "phishing_model.pkl")

    # Decision thresholds (tunable for the viva)
    TOXICITY_THRESHOLD = 0.6
    PHISHING_THRESHOLD = 0.6

    # Metaverse room geometry (pixels)
    ROOM_WIDTH = 800
    ROOM_HEIGHT = 500
    AVATAR_RADIUS = 18
