"""API tests. Needs a trained model at models/model.joblib (run `dvc repro` first)."""
import os

import pytest

if not os.path.exists("models/model.joblib"):
    pytest.skip("No trained model yet - run `dvc repro` first", allow_module_level=True)

from fastapi.testclient import TestClient  # noqa: E402

from api.main import app  # noqa: E402

client = TestClient(app)

GOOD = {"tenure": 2, "MonthlyCharges": 85.5, "TotalCharges": 171.0,
        "SeniorCitizen": 0, "Contract": "Month-to-month",
        "InternetService": "Fiber optic", "PaymentMethod": "Electronic check",
        "PaperlessBilling": "Yes", "TechSupport": "No"}


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["model_loaded"] is True


def test_predict_valid_request():
    r = client.post("/predict", json=GOOD)
    assert r.status_code == 200
    body = r.json()
    assert 0.0 <= body["churn_probability"] <= 1.0
    assert isinstance(body["churn"], bool)


def test_missing_field_rejected():
    bad = {k: v for k, v in GOOD.items() if k != "tenure"}
    assert client.post("/predict", json=bad).status_code == 422


def test_invalid_category_rejected():
    # TODO S2.5: Send a request with Contract="Ten years" and assert status 422.
    pass
