#!/usr/bin/env bash
set -euo pipefail

if ! command -v gh >/dev/null 2>&1; then
  echo "Error: GitHub CLI 'gh' is required. Install from https://cli.github.com/"
  exit 1
fi

echo "Setting repository secrets via gh CLI. Ensure you're authenticated and in the repo directory."

if [ -z "${DOCKERHUB_USERNAME:-}" ] || [ -z "${DOCKERHUB_TOKEN:-}" ]; then
  echo "Please set DOCKERHUB_USERNAME and DOCKERHUB_TOKEN environment variables before running."
  exit 1
fi

gh secret set DOCKERHUB_USERNAME --body "$DOCKERHUB_USERNAME"
gh secret set DOCKERHUB_TOKEN --body "$DOCKERHUB_TOKEN"

if [ -n "${RENDER_API_KEY:-}" ]; then
  gh secret set RENDER_API_KEY --body "$RENDER_API_KEY"
fi
if [ -n "${RENDER_SERVICE_ID:-}" ]; then
  gh secret set RENDER_SERVICE_ID --body "$RENDER_SERVICE_ID"
fi

echo "Repository secrets set."
