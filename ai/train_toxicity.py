"""Train the toxicity classifier (TF-IDF + Logistic Regression).

Run from project root:
    python ai/train_toxicity.py

Outputs:
    models_pkl/toxicity_model.pkl
"""
import os
import sys

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

# Make project root importable when running this script directly
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from config import Config  # noqa: E402

DATA_PATH = os.path.join(PROJECT_ROOT, "data", "toxic_comments.csv")


def main() -> None:
    print(f"[toxicity] Loading dataset: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    df = df.dropna()
    df["text"] = df["text"].astype(str)
    print(f"[toxicity] Rows: {len(df)} | "
          f"Toxic: {(df.label == 1).sum()} | Clean: {(df.label == 0).sum()}")

    X_train, X_test, y_train, y_test = train_test_split(
        df["text"].values,
        df["label"].values,
        test_size=0.2,
        random_state=42,
        stratify=df["label"].values,
    )

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=10000,
            min_df=1,
            sublinear_tf=True,
        )),
        ("clf", LogisticRegression(
            C=4.0,
            class_weight="balanced",
            max_iter=1000,
            solver="liblinear",
        )),
    ])

    print("[toxicity] Training...")
    pipeline.fit(X_train, y_train)

    print("\n[toxicity] === Evaluation on hold-out set ===")
    y_pred = pipeline.predict(X_test)
    print("Accuracy:",
          (y_pred == y_test).mean())
    print("\nConfusion matrix (rows = true, cols = pred):")
    print(confusion_matrix(y_test, y_pred))
    print("\nClassification report:")
    print(classification_report(y_test, y_pred,
                                target_names=["clean", "toxic"]))

    os.makedirs(os.path.dirname(Config.TOXICITY_MODEL_PATH), exist_ok=True)
    joblib.dump(pipeline, Config.TOXICITY_MODEL_PATH)
    print(f"[toxicity] Saved model to: {Config.TOXICITY_MODEL_PATH}")

    # Quick sanity tests
    print("\n[toxicity] Sample predictions:")
    samples = [
        "hello everyone how are you today",
        "you are so stupid get out of here",
        "thanks for your help today",
        "i hate you and hope you fail",
    ]
    for s in samples:
        proba = pipeline.predict_proba([s])[0][1]
        verdict = "TOXIC " if proba >= Config.TOXICITY_THRESHOLD else "clean "
        print(f"  [{verdict}] p={proba:.2f}  {s!r}")


if __name__ == "__main__":
    main()
