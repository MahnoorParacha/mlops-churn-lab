#!/usr/bin/env bash
# Collects ONLY the files the API needs into release/ (used for HF + Azure).
# Run from the repo root after `dvc repro`:   bash scripts/build_release.sh
set -euo pipefail

rm -rf release
mkdir -p release

cp -r api release/
cp -r models release/
cp requirements-serving.txt Dockerfile release/
cp hf_space/README.md release/README.md

# Record which code + data produced this model (shown by GET /version)
cat > release/models/release.json <<JSON
{
  "git_commit": "$(git rev-parse --short HEAD 2>/dev/null || echo unknown)",
  "built_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "metrics": $(cat reports/metrics.json 2>/dev/null || echo '{}')
}
JSON

find release -name "__pycache__" -type d -prune -exec rm -rf {} +
rm -f release/models/.gitignore
echo "Release folder ready:"
find release -type f | sort
