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

    # TODO S3.1: If f1 is below min_f1, print a FAIL message and exit with code 1.
    # Otherwise print a PASS message.
    # Hint: sys.exit(1)
    pass


if __name__ == "__main__":
    main()
