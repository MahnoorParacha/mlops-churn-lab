"""Quality gate: exit with code 1 if the model is not good enough.

A non-zero exit code makes the GitHub Actions job FAIL,
which stops the deployment job from running.
"""
import json
import sys

from src.config import METRICS_PATH, load_params


def main():
    min_f1 = load_params()["evaluate"]["min_f1"]
    with open(METRICS_PATH) as f:
        f1 = json.load(f)["f1"]

    if f1 < min_f1:  # S3.1
        print(f"QUALITY GATE FAILED: f1={f1:.2f} < min_f1={min_f1}")
        sys.exit(1)
    print(f"QUALITY GATE PASSED: f1={f1:.2f} >= min_f1={min_f1}")
if __name__ == "__main__":
    main()
