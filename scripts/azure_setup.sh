#!/usr/bin/env bash
# Run these in Azure Cloud Shell (Bash) - https://shell.azure.com
# Lab 4 tells you WHEN to run each part. Do not run the whole file at once.

# ---------- PART A: names (change YOURNAME to something unique, lowercase, no spaces) ----------
YOURNAME=ali123
RG=rg-mlops-$YOURNAME
LOCATION=eastus
ACR=acrmlops$YOURNAME            # must be globally unique, letters+numbers only
ENVNAME=env-mlops-$YOURNAME
APP=churn-api-$YOURNAME

# ---------- PART B: one-time setup ----------
az provider register --namespace Microsoft.App --wait
az provider register --namespace Microsoft.OperationalInsights --wait
az provider register --namespace Microsoft.ContainerRegistry --wait

az group create --name $RG --location $LOCATION
az acr create --resource-group $RG --name $ACR --sku Basic --admin-enabled true
az acr show --name $ACR --query loginServer -o tsv          # -> ACR_LOGIN_SERVER
az acr credential show --name $ACR --query username -o tsv  # -> ACR_USERNAME
az acr credential show --name $ACR --query "passwords[0].value" -o tsv  # -> ACR_PASSWORD

az containerapp env create --name $ENVNAME --resource-group $RG --location $LOCATION

# ---------- PART C: create the app (AFTER GitHub Actions pushed the image) ----------
az containerapp create \
  --name $APP --resource-group $RG --environment $ENVNAME \
  --image $ACR.azurecr.io/churn-api:latest \
  --registry-server $ACR.azurecr.io \
  --registry-username $(az acr credential show -n $ACR --query username -o tsv) \
  --registry-password $(az acr credential show -n $ACR --query "passwords[0].value" -o tsv) \
  --target-port 7860 --ingress external \
  --cpu 0.5 --memory 1.0Gi --min-replicas 0 --max-replicas 1 \
  --query properties.configuration.ingress.fqdn -o tsv

# ---------- PART D: roll out a specific image later ----------
# az containerapp update -n $APP -g $RG --image $ACR.azurecr.io/churn-api:<git-sha>
# az containerapp revision list -n $APP -g $RG -o table

# ---------- PART E: CLEAN UP when the course ends (stops all charges) ----------
# az group delete --name $RG --yes --no-wait
