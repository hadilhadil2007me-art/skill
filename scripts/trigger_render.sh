#!/usr/bin/env bash
set -euo pipefail

if [ -z "${RENDER_API_KEY:-}" ] || [ -z "${RENDER_SERVICE_ID:-}" ]; then
  echo "Set RENDER_API_KEY and RENDER_SERVICE_ID environment variables to trigger a Render deploy."
  exit 1
fi

echo "Triggering Render deploy for service $RENDER_SERVICE_ID"
curl -sS -X POST "https://api.render.com/v1/services/$RENDER_SERVICE_ID/deploys" \
  -H "Authorization: Bearer $RENDER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}' \
  | jq .

echo "Triggered Render deploy (response above)."
