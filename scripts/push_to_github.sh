#!/usr/bin/env bash
set -euo pipefail

if [ -z "${GITHUB_REPO:-}" ]; then
  echo "Error: GITHUB_REPO is not set. Example: https://github.com/yourusername/skillup.git"
  exit 1
fi

COMMIT_MSG="${COMMIT_MSG:-chore: prepare repository for deploy}"

git add .
git commit -m "$COMMIT_MSG" || echo "No changes to commit"

# Ensure main branch
git branch -M main || true

# Add remote if missing
if git remote get-url origin >/dev/null 2>&1; then
  echo "Remote 'origin' exists; setting to $GITHUB_REPO"
  git remote set-url origin "$GITHUB_REPO"
else
  git remote add origin "$GITHUB_REPO"
fi

git push -u origin main
echo "Pushed to $GITHUB_REPO"
