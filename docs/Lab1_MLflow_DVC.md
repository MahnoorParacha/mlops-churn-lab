# Lab 1 — Project Setup, 10 Experiments with MLflow, Pipeline with DVC

## Lecture (25 min)
- **Problem:** notebooks work once; no one can redo them. MLOps = make ML repeatable, traceable, deployable.
- **Our project:** predict customer churn (IBM Telco, 7,043 rows). Over 4 sessions it becomes a live API.
- **MLflow** records every training run: parameters, metrics, model. You choose the best model from evidence.
- **DVC** versions data and defines a pipeline (`get_data → prepare → train → evaluate`). It re-runs only what changed.
- **params.yaml** holds all settings, so code never changes for a new experiment.

## Lab (150 min)
TODOs marked `S1.x` in code. Find them: `grep -rn "TODO S1" .`

### Step 1 — Get the repo (10 min)
1. Open the course repo on GitHub → **Use this template** → tick **Include all branches** → create a **public** repo `mlops-churn-lab` in your account.
2. Clone and install (Python 3.11):
```bash
git clone https://github.com/<you>/mlops-churn-lab.git
cd mlops-churn-lab
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
No working Python/Docker? Use **Code → Codespaces → Create codespace**.

### Step 2 — Download and look at the data (15 min)
```bash
python -m src.get_data
python -c "import pandas as pd; d=pd.read_csv('data/raw/churn.csv'); print(d.shape); print(d.dtypes); print((d.TotalCharges==' ').sum())"
```
Expected: `(7043, 21)`, `TotalCharges` is `object` (text), and 11 blank values. This is what you will clean.

### Step 3 — Basic cleaning: TODO S1.1–S1.4 in `src/prepare.py` (20 min)
Remove duplicates, convert `TotalCharges` to numbers, drop missing rows, map `Churn` Yes/No → 1/0.
```bash
pytest -q tests/test_prepare.py     # expect: 3 passed
python -m src.prepare
```
Expected: `Raw rows: 7043 -> Clean rows: 7032` and `Train: 5625 rows, Test: 1407 rows`.

### Step 4 — Log one run to MLflow: TODO S1.5–S1.7 in `src/train.py` (20 min)
```bash
python -m src.train
mlflow ui                 # open http://127.0.0.1:5000
```
Open experiment **churn-prediction** → run **dvc-pipeline**. Check that Parameters, Metrics (f1 ≈ 0.62) and the **model** artifact are there. Stop the UI with Ctrl+C.

### Step 5 — Run 10 experiments: TODO S1.8–S1.9 in `src/run_experiments.py` (30 min)
Add 7 more settings (total 10), then merge base settings with changes and call `train_and_log`.
```bash
python -m src.run_experiments     # prints exp-01 ... exp-10
mlflow ui
```
In the UI: select all 10 runs → **Compare** → sort by `f1`. Fill this table in your notebook:

| Run | model | n_estimators | max_depth | f1 | recall |
|---|---|---|---|---|---|
| exp-01 | random_forest | 50 | 4 | | |
| exp-02 | random_forest | 100 | 6 | | |
| exp-03 | random_forest | 200 | 8 | | |
| exp-04 | random_forest | 300 | 12 | | |
| exp-05 | random_forest | 100 | 12 | 0.631 | 0.781 |
| exp-06 | random_forest | 300 | 6 | | |
| exp-07 | random_forest | 200 | 4 | | |
| exp-08 | logistic_regression | - | - | | |
| exp-09 | logistic_regression | - | - | | |
| exp-10 | logistic_regression | - | - | | |

I chose exp-05 (random forest, 100 trees, max_depth 12, min_samples_leaf 10) because it had the highest f1 (0.631) of all 10 runs, with a recall of 0.781.

### Step 6 — Build the DVC pipeline: TODO S1.10–S1.11 in `dvc.yaml` (25 min)
Complete the `train` and `evaluate` stages. Example of a metrics stage:
```yaml
    metrics:
      - reports/metrics.json:
          cache: false
```
```bash
dvc init
dvc dag            # shows get_data → prepare → train/evaluate
dvc repro          # runs all 4 stages
dvc metrics show
```

### Step 7 — Prove reproducibility (15 min)
```bash
dvc repro          # run again: every stage says "didn't change, skipping"
```
Change `max_depth` in `params.yaml`, then:
```bash
dvc params diff
dvc repro          # only train + evaluate re-run
dvc metrics diff
```

### Step 8 — Version data with a remote (10 min)
```bash
dvc remote add -d localstore ../dvc-storage
dvc push
rm data/raw/churn.csv     # Windows: del data\raw\churn.csv
dvc pull                  # the file comes back
```

### Step 9 — Commit (5 min)
```bash
git add .
git commit -m "Session 1: cleaning, MLflow, DVC pipeline"
git push
```

## Done when
- [ ] 10 runs visible in MLflow, best one chosen with a reason
- [ ] `dvc repro` runs end to end and skips when nothing changed
- [ ] `dvc.lock` committed

## If it does not work
| Problem | Fix |
|---|---|
| `ModuleNotFoundError: src` | Run commands from repo root using `python -m src.xxx` |
| `could not convert string to float` | TODO S1.2 not done |
| `_DIR_MARK` error from DVC | `pip install pathspec==0.12.1` |
| MLflow UI port busy | `mlflow ui --port 5001` |
