"""Stage 4: evaluate the saved model and write reports/metrics.json."""
import json
import os

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from src.config import FEATURES, METRICS_PATH, MODEL_PATH, PROCESSED_DIR, TARGET


def main():
    model = joblib.load(MODEL_PATH)
    test_df = pd.read_csv(f"{PROCESSED_DIR}/test.csv")
    preds = model.predict(test_df[FEATURES])
    y = test_df[TARGET]
    metrics = {
        "accuracy": round(accuracy_score(y, preds), 4),
        "precision": round(precision_score(y, preds), 4),
        "recall": round(recall_score(y, preds), 4),
        "f1": round(f1_score(y, preds), 4),
    }
    os.makedirs(os.path.dirname(METRICS_PATH), exist_ok=True)
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=2)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
