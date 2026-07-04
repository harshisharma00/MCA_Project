"""Train the phishing URL classifier (hand-crafted features + Logistic Regression).

Run from project root:
    python ai/train_phishing.py

Outputs:
    models_pkl/phishing_model.pkl
"""
import os
import sys

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from ai.url_features import FEATURE_NAMES, extract_feature_vector  # noqa: E402
from config import Config  # noqa: E402

DATA_PATH = os.path.join(PROJECT_ROOT, "data", "phishing_urls.csv")


def main() -> None:
    print(f"[phishing] Loading dataset: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    df = df.dropna()
    print(f"[phishing] Rows: {len(df)} | "
          f"Phishing: {(df.label == 1).sum()} | Legit: {(df.label == 0).sum()}")

    print("[phishing] Extracting URL features...")
    X = np.array([extract_feature_vector(u) for u in df["url"].astype(str)])
    y = df["label"].values.astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(
            C=2.0,
            class_weight="balanced",
            max_iter=2000,
            solver="liblinear",
        )),
    ])

    print("[phishing] Training...")
    pipeline.fit(X_train, y_train)

    print("\n[phishing] === Evaluation on hold-out set ===")
    y_pred = pipeline.predict(X_test)
    print("Accuracy:", (y_pred == y_test).mean())
    print("\nConfusion matrix (rows = true, cols = pred):")
    print(confusion_matrix(y_test, y_pred))
    print("\nClassification report:")
    print(classification_report(y_test, y_pred,
                                target_names=["legit", "phishing"]))

    # Show feature importances (logistic regression coefficients)
    coefs = pipeline.named_steps["clf"].coef_[0]
    print("\n[phishing] Feature weights (positive = pushes towards phishing):")
    for name, coef in sorted(zip(FEATURE_NAMES, coefs),
                             key=lambda kv: -abs(kv[1])):
        print(f"  {name:<25} {coef:+.3f}")

    os.makedirs(os.path.dirname(Config.PHISHING_MODEL_PATH), exist_ok=True)
    joblib.dump(pipeline, Config.PHISHING_MODEL_PATH)
    print(f"\n[phishing] Saved model to: {Config.PHISHING_MODEL_PATH}")

    # Sanity tests
    print("\n[phishing] Sample predictions:")
    samples = [
        "https://www.google.com",
        "https://github.com/anthropics/claude-code",
        "http://paypal.com@evil-site.tk/login",
        "http://192.168.1.45/paypal/login",
        "http://free-robux-generator.cf/auth",
    ]
    for s in samples:
        feats = np.array([extract_feature_vector(s)])
        proba = pipeline.predict_proba(feats)[0][1]
        verdict = "PHISH" if proba >= Config.PHISHING_THRESHOLD else "legit"
        print(f"  [{verdict}] p={proba:.2f}  {s}")


if __name__ == "__main__":
    main()
