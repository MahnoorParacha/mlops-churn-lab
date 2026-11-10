# Lab 3 — Automate with GitHub Actions, Deploy to Hugging Face

## Lecture (25 min)
- **CI/CD**: every push automatically tests, trains, checks quality and deploys. No "works on my laptop".
- A workflow = **trigger** (`on:`) → **jobs** (machines) → **steps** (commands). `needs:` orders jobs.
- **Quality gate**: a script that exits with code 1 if F1 is too low → job fails → deploy never happens.
- **Artifact handoff**: deploy uses exactly the model that passed the gate (upload → download artifact).
- **Secrets** (tokens) are never written in code; they live in GitHub Settings.

## Lab (150 min)
TODOs marked `S3.x`.

### Step 1 — Quality gate: TODO S3.1 in `src/check_gate.py` (15 min)
```bash
dvc repro
python -m src.check_gate      # expect: QUALITY GATE PASSED: f1=0.62 >= min_f1=0.55
```
Set `min_f1: 0.90` in `params.yaml`, run again → FAILED, and `echo $?` shows 1. Set it back to 0.55.

### Step 2 — Create the Hugging Face Space (15 min)
1. Sign in at huggingface.co → **New → Space** → name `churn-api` → SDK **Docker** → Blank → Public → Create.
2. **Settings → Access Tokens → New token** → type **Write** → copy it.

### Step 3 — Add secrets to GitHub (10 min)
Your repo → **Settings → Secrets and variables → Actions**:
- **Secrets** tab → `HF_TOKEN` = your token
- **Variables** tab → `HF_SPACE` = `your-hf-username/churn-api`

### Step 4 — Complete the workflow: TODO S3.2–S3.7 (40 min)
```bash
mkdir -p .github/workflows
git mv workflow_templates/ml-pipeline.yml .github/workflows/ml-pipeline.yml
```
Fill: triggers, `dvc repro`, gate, upload artifact, `needs: train`, secret/variable. Leave the Session 4 placeholder as is.
Check YAML: `python -c "import yaml; yaml.safe_load(open('.github/workflows/ml-pipeline.yml'))"`

### Step 5 — Push and watch (20 min)
```bash
git add . && git commit -m "Session 3: CI/CD" && git push
```
GitHub → **Actions** tab → open the run. Job `train` then `deploy-hf` should be green. Read the gate line in the logs.

### Step 6 — Test the live API (15 min)
Space builds in 2–5 min (Space page → Logs). Then:
```bash
python scripts/smoke_test.py https://your-hf-username-churn-api.hf.space
```
Also open `.../docs` in the browser. `/version` shows the git commit that built it.

### Step 7 — Block a bad model (20 min)
Set `min_f1: 0.90`, commit, push. In Actions: `train` fails at **Quality gate**, `deploy-hf` is **skipped**. The live Space still runs the old good model. Revert to 0.55 and push again.

## Done when
- [ ] Green run that deployed to Hugging Face
- [ ] Red run where the gate blocked deployment
- [ ] Smoke test passes on the HF URL

## If it does not work
| Problem | Fix |
|---|---|
| `deploy-hf` skipped on a green run | `HF_SPACE` variable missing (Variables tab, not Secrets) |
| 401/403 on upload | Token must be **Write** type; check `HF_SPACE` spelling |
| Space shows "Build error" | Space → Logs; usually Dockerfile TODO S2.6/S2.7 |
| Workflow not starting | File must be in `.github/workflows/`; TODO S3.2 trigger |
