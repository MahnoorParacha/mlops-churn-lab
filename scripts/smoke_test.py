"""Check that a deployed API is really working.

Usage:  python scripts/smoke_test.py https://your-api-url
Retries for up to ~10 minutes because cloud builds take time.
"""
import sys
import time

import requests

SAMPLE = {"tenure": 2, "MonthlyCharges": 85.5, "TotalCharges": 171.0,
          "SeniorCitizen": 0, "Contract": "Month-to-month",
          "InternetService": "Fiber optic", "PaymentMethod": "Electronic check",
          "PaperlessBilling": "Yes", "TechSupport": "No"}

base = sys.argv[1].rstrip("/")
for attempt in range(1, 41):
    try:
        h = requests.get(f"{base}/health", timeout=10)
        if h.status_code == 200:
            p = requests.post(f"{base}/predict", json=SAMPLE, timeout=10)
            p.raise_for_status()
            print("HEALTH :", h.json())
            print("PREDICT:", p.json())
            print("VERSION:", requests.get(f"{base}/version", timeout=10).json())
            print("SMOKE TEST PASSED")
            sys.exit(0)
    except requests.RequestException as e:
        print(f"attempt {attempt}: {e.__class__.__name__}")
    time.sleep(15)
print("SMOKE TEST FAILED: API never became healthy")
sys.exit(1)
