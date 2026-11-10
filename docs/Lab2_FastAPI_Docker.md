# Lab 2 — Serve the Model with FastAPI and Docker

## Lecture (25 min)
- A model file is useless to other people. An **API** lets any app send customer data and get a prediction.
- **FastAPI**: define endpoints in Python; **Pydantic** schemas reject bad input automatically (HTTP 422).
- We save preprocessing + model as **one pipeline**, so the API transforms data exactly like training did.
- **Docker** packages code + libraries + model into an image that runs the same everywhere (Hugging Face, Azure).
- `requirements-serving.txt` holds only what the API needs — smaller, safer image.

## Lab (150 min)
TODOs marked `S2.x`. Start with: `dvc repro` (you need `models/model.joblib`).

### Step 1 — Read the schema (10 min)
Open `api/schemas.py`. Note the 9 input fields and the allowed values (`Literal[...]`). This is the API "contract".

### Step 2 — Write the API: TODO S2.1–S2.4 in `api/main.py` (30 min)
Load the model once, return health, build a one-row DataFrame, return probability.
```bash
uvicorn api.main:app --reload
```
Open http://127.0.0.1:8000/docs → **POST /predict → Try it out → Execute**.
Expected: `{"churn": true, "churn_probability": 0.87}` (approx).
Also try `/health` and `/version`.

### Step 3 — Break it on purpose (10 min)
In /docs, change `"Contract"` to `"Ten years"` → you get **422**. Remove `tenure` → **422**. This is validation working.

### Step 4 — Tests: TODO S2.5 in `tests/test_api.py` (20 min)
```bash
pytest -q          # expect: 7 passed
```

### Step 5 — Dockerfile: TODO S2.6–S2.7 (20 min)
Copy and install `requirements-serving.txt`, then copy `api/` and `models/`.

### Step 6 — Build and run the container (30 min)
Docker Desktop must be running (or use Codespaces).
```bash
docker build -t churn-api .
docker run -p 7860:7860 churn-api
```
Open http://127.0.0.1:7860/docs and predict again. In a second terminal:
```bash
python scripts/smoke_test.py http://127.0.0.1:7860     # expect: SMOKE TEST PASSED
```

### Step 7 — Release folder (10 min)
```bash
bash scripts/build_release.sh
```
Look at `release/` — only what the server needs. This exact folder goes to Hugging Face and Azure later.

### Step 8 — Commit (5 min)
```bash
git add . && git commit -m "Session 2: FastAPI + Docker" && git push
```

## Done when
- [ ] `/predict` works locally and inside Docker
- [ ] invalid input returns 422
- [ ] `pytest` all passed, smoke test passed

## If it does not work
| Problem | Fix |
|---|---|
| `FileNotFoundError models/model.joblib` | Run `dvc repro` first |
| `'NoneType' has no attribute predict_proba` | TODO S2.1 not done |
| Docker "cannot connect to daemon" | Start Docker Desktop |
| `COPY models/` fails | Model not trained yet: `dvc repro` |
| `bash` not found on Windows | Use Git Bash or Codespaces |
