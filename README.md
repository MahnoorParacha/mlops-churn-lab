# MLOps Churn Lab — Module 7

One small project that goes through the full MLOps pipeline in 4 sessions:

| Session | You build | Tools |
|---|---|---|
| 1 | Clean data, run **10 training experiments**, reproducible pipeline | pandas, scikit-learn, MLflow, DVC |
| 2 | Turn the best model into a **prediction API** and package it | FastAPI, pytest, Docker |
| 3 | Automate test → train → quality gate → deploy | GitHub Actions, Hugging Face Spaces |
| 4 | Deploy the **same container** to the cloud | Azure Container Registry, Azure Container Apps |

**Dataset:** IBM Telco Customer Churn (≈7,000 customers). Goal: predict whether a customer will leave (`Churn`).

## Where to write code

Every place you must write code is marked like this:

```python
# TODO S1.2: 'TotalCharges' is stored as text ...
# Hint: pd.to_numeric(..., errors="coerce")
pass
```

`S1.2` means **Session 1, task 2**. Your lab sheet explains each TODO step by step.
Find all of them with:

```bash
grep -rn "TODO S1" .     # Session 1 tasks   (Windows PowerShell: Select-String -Path *,src\*,api\*,tests\* -Pattern "TODO S1")
```

## Project layout

```
params.yaml              all settings (data split, model hyper-parameters, quality gate)
dvc.yaml                 the pipeline: get_data -> prepare -> train -> evaluate
src/
  config.py              feature lists + params loader          (given)
  get_data.py            downloads the CSV                      (given)
  prepare.py             basic cleaning + split                 (TODO S1.1-S1.4)
  model.py               preprocessing + model pipeline         (given)
  train.py               train one model + MLflow logging       (TODO S1.5-S1.7)
  run_experiments.py     run 10 experiments                     (TODO S1.8-S1.9)
  evaluate.py            writes reports/metrics.json            (given)
  check_gate.py          quality gate                           (TODO S3.1)
api/
  schemas.py             request/response validation            (given)
  main.py                FastAPI app                            (TODO S2.1-S2.4)
tests/                   pytest tests                           (TODO S2.5)
Dockerfile               container image                        (TODO S2.6-S2.7)
workflow_templates/      GitHub Actions workflow (moved into .github/ in Session 3)
hf_space/README.md       Hugging Face Space settings
scripts/                 release, deploy, smoke-test and Azure helper scripts
```

## Quick start

```bash
python -m venv .venv
# macOS/Linux:  source .venv/bin/activate      Windows:  .venv\Scripts\activate
pip install -r requirements.txt
dvc repro            # will fail until you finish the Session 1 TODOs - that is expected
```

Use **Python 3.11**. If something is broken on your laptop, open the repo in **GitHub Codespaces** (Code → Codespaces → Create) — it already has Python and Docker.

## Stuck?

The `solution` branch contains finished code. Use it to **compare**, not to copy:

```bash
git fetch origin
git diff origin/solution -- src/prepare.py
```
