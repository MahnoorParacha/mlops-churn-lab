"""Shared settings: feature lists and a helper to read params.yaml."""
import yaml

NUMERIC_FEATURES = ["tenure", "MonthlyCharges", "TotalCharges", "SeniorCitizen"]
CATEGORICAL_FEATURES = ["Contract", "InternetService", "PaymentMethod",
                        "PaperlessBilling", "TechSupport"]
FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES
TARGET = "Churn"

PROCESSED_DIR = "data/processed"
MODEL_PATH = "models/model.joblib"
METRICS_PATH = "reports/metrics.json"


def load_params(path: str = "params.yaml") -> dict:
    with open(path) as f:
        return yaml.safe_load(f)
