"""Unit tests for the cleaning step. Run:  pytest -q"""
import pandas as pd

from src.config import FEATURES, TARGET
from src.prepare import clean


def make_raw():
    row = {"customerID": "1", "tenure": 5, "MonthlyCharges": 50.0,
           "TotalCharges": "250.0", "SeniorCitizen": 0, "Contract": "One year",
           "InternetService": "DSL", "PaymentMethod": "Mailed check",
           "PaperlessBilling": "No", "TechSupport": "Yes", "Churn": "No"}
    blank = {**row, "customerID": "2", "TotalCharges": " ", "Churn": "Yes"}
    return pd.DataFrame([row, row, blank])  # duplicate + blank TotalCharges


def test_duplicates_and_blanks_removed():
    df = clean(make_raw())
    assert len(df) == 1


def test_target_is_numeric():
    df = clean(make_raw())
    assert set(df[TARGET].unique()) <= {0, 1}


def test_only_model_columns_kept():
    df = clean(make_raw())
    assert list(df.columns) == FEATURES + [TARGET]
