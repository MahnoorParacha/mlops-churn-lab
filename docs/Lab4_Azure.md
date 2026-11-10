# Lab 4 — Deploy the Same Container to Azure

## Lecture (25 min)
- Same Docker image, different host. That is the point of containers.
- **Azure Container Registry (ACR)**: private storage for your images.
- **Azure Container Apps**: runs a container with a public HTTPS URL; scales to zero when idle.
- Flow: GitHub Actions builds image → pushes to ACR (tag = git commit) → Container App runs it.
- **Rollback** = point the app back to an older image tag. **Monitoring**: watch logs and input drift; drift means "investigate", not "auto-deploy".
- Cost: always delete your resource group at the end.

## Lab (150 min)
Use **Azure for Students** and **Azure Cloud Shell (Bash)**: https://shell.azure.com. All commands are in `scripts/azure_setup.sh`.

### Step 1 — Set names (10 min)
In Cloud Shell, paste **PART A** of `scripts/azure_setup.sh`, with your own `YOURNAME` (lowercase letters/numbers).

### Step 2 — Create registry and environment (25 min)
Paste **PART B**. Save the three printed values: login server, username, password.

### Step 3 — Add to GitHub (10 min)
Repo → Settings → Secrets and variables → Actions:
- Variable `ACR_LOGIN_SERVER` = e.g. `acrmlopsali123.azurecr.io`
- Secret `ACR_USERNAME`, Secret `ACR_PASSWORD`

### Step 4 — Add the Azure job to the workflow (20 min)
Replace the Session 4 placeholder comment at the bottom of `.github/workflows/ml-pipeline.yml` with the `deploy-azure` job from the **solution** branch:
```bash
git fetch origin
git show origin/solution:.github/workflows/ml-pipeline.yml | tail -50
```
Read it: it downloads the **same release artifact**, logs in to ACR, builds, pushes tags `<sha>` and `latest`.
```bash
git add . && git commit -m "Session 4: Azure image push" && git push
```
Actions: `train`, `deploy-hf`, `deploy-azure` all green.

### Step 5 — Create the Container App (20 min)
In Cloud Shell paste **PART C**. It prints a URL like `churn-api-ali123.xxx.eastus.azurecontainerapps.io`.
```bash
python scripts/smoke_test.py https://<that-url>
```
Also open `https://<that-url>/docs`. Compare `/version` with the Hugging Face one — same commit.

### Step 6 — Ship a new version and roll back (30 min)
1. Change a param (e.g. `n_estimators`), push. Copy the new commit SHA from Actions.
2. Cloud Shell: `az containerapp update -n $APP -g $RG --image $ACR.azurecr.io/churn-api:<new-sha>`
3. Check `/version` → new commit.
4. Roll back: run the same command with the **old** SHA. Check `/version` again.
5. `az containerapp revision list -n $APP -g $RG -o table`

### Step 7 — Look at logs (10 min)
```bash
az containerapp logs show -n $APP -g $RG --tail 20
```
Send a few predictions and watch them appear.

### Step 8 — Final demo + cleanup (25 min)
Show: MLflow 10 runs → `dvc repro` → green pipeline → HF URL → Azure URL → rollback.
After the course: `az group delete --name $RG --yes --no-wait`

### Optional — fully automatic Azure update
Create a service principal, save its JSON as secret `AZURE_CREDENTIALS`, and add variables `AZURE_APP_NAME`, `AZURE_RESOURCE_GROUP`. The workflow's last step then updates the app on every push.

## Done when
- [ ] Image in ACR pushed by GitHub Actions
- [ ] Live Azure URL passes smoke test
- [ ] Rollback shown using `/version`

## If it does not work
| Problem | Fix |
|---|---|
| `MissingSubscriptionRegistration` | Run the `az provider register` lines in PART B |
| ACR name taken | Change `YOURNAME` |
| `deploy-azure` skipped | `ACR_LOGIN_SERVER` variable missing |
| App URL gives 404/timeout | Check `--target-port 7860`; first request after idle takes ~30 s |
| `unauthorized` pulling image | Re-run PART C (registry username/password) |
