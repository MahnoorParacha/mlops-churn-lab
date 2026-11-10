"""Run 10 training iterations with different settings, all logged to MLflow.

Usage:  python -m src.run_experiments
Then:   mlflow ui      ->  open http://127.0.0.1:5000 and compare runs.
"""
from src.config import load_params
from src.train import train_and_log

# Each experiment only lists what CHANGES compared with params.yaml.
# TODO S1.8: The first 3 experiments are given. Add 7 more so you have 10.
# Ideas: change max_depth (4, 6, 12), n_estimators (50, 100, 300),
#        min_samples_leaf (1, 10, 20), or try logistic_regression with C=0.1, 1, 10.
EXPERIMENTS = [
    {"model": "random_forest", "n_estimators": 50, "max_depth": 4},
    {"model": "random_forest", "n_estimators": 100, "max_depth": 6},
    {"model": "random_forest", "n_estimators": 200, "max_depth": 8},
    {"model": "random_forest", "n_estimators": 300, "max_depth": 12},
    {"model": "random_forest", "n_estimators": 100, "max_depth": 12, "min_samples_leaf": 10},
    {"model": "random_forest", "n_estimators": 300, "max_depth": 6, "min_samples_leaf": 20},
    {"model": "random_forest", "n_estimators": 200, "max_depth": 4, "min_samples_leaf": 1},
    {"model": "logistic_regression", "C": 0.1},
    {"model": "logistic_regression", "C": 1},
    {"model": "logistic_regression", "C": 10},
]


def main():
    base = load_params()["train"]
    print(f"Running {len(EXPERIMENTS)} experiments...")
    for i, changes in enumerate(EXPERIMENTS, start=1):
        settings = {**base, **changes}  # S1.9
        train_and_log(settings, run_name=f"exp-{i:02d}")
    print("Done. Run `mlflow ui` and compare the runs.")


if __name__ == "__main__":
    main()