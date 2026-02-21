#!/usr/bin/env bash
# fix-railway-api.sh — Fix Railway root directory trailing spaces via GraphQL API
# Usage: RAILWAY_API_TOKEN=<token> bash fix-railway-api.sh
#    or: bash fix-railway-api.sh   (will prompt for token)

set -euo pipefail

# ── Configuration ──────────────────────────────────────────────────────────────
API="https://backboard.railway.com/graphql/v2"
ENV_ID="5a2bfd87-fd38-4a49-9eba-1518a0eea94d"

declare -A SERVICES=(
  ["backend"]="223bf3e7-f97e-4e0a-84e2-5a411d83e797"
  ["auth-server"]="f3f128e4-868a-4f4f-9fb9-ea8189844e45"
  ["content"]="212a36e6-6cbb-49bd-8662-9ed9cb7b8149"
)

declare -A ROOT_DIRS=(
  ["backend"]="/intellistack/backend"
  ["auth-server"]="/intellistack/auth-server"
  ["content"]="/intellistack/content"
)

# ── Get token ──────────────────────────────────────────────────────────────────
if [ -z "${RAILWAY_API_TOKEN:-}" ]; then
  echo "No RAILWAY_API_TOKEN found in environment."
  echo "Get one at: https://railway.com/account/tokens"
  read -rsp "Paste your Railway API token: " RAILWAY_API_TOKEN
  echo
fi

if [ -z "$RAILWAY_API_TOKEN" ]; then
  echo "ERROR: Token cannot be empty."
  exit 1
fi

# ── Helper: call Railway GraphQL API ───────────────────────────────────────────
gql() {
  local query="$1"
  curl -sS -X POST "$API" \
    -H "Authorization: Bearer $RAILWAY_API_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"query\": \"$query\"}"
}

# ── Step 1: Update root directories ───────────────────────────────────────────
echo "=== Step 1: Updating root directories (removing trailing spaces) ==="
echo

for svc in backend auth-server content; do
  sid="${SERVICES[$svc]}"
  root="${ROOT_DIRS[$svc]}"
  echo "  Updating $svc → rootDirectory: \"$root\""

  result=$(gql "mutation { serviceInstanceUpdate(serviceId: \\\"$sid\\\", environmentId: \\\"$ENV_ID\\\", input: { rootDirectory: \\\"$root\\\" }) }")

  if echo "$result" | grep -q '"errors"'; then
    echo "  ERROR for $svc: $result"
  else
    echo "  OK"
  fi
done

echo
echo "=== Step 2: Triggering redeployments ==="
echo

# ── Step 2: Redeploy each service ─────────────────────────────────────────────
for svc in backend auth-server content; do
  sid="${SERVICES[$svc]}"
  echo "  Redeploying $svc ..."

  result=$(gql "mutation { serviceInstanceRedeploy(serviceId: \\\"$sid\\\", environmentId: \\\"$ENV_ID\\\") }")

  if echo "$result" | grep -q '"errors"'; then
    echo "  ERROR for $svc: $result"
  else
    echo "  OK — deployment triggered"
  fi
done

echo
echo "=== Done ==="
echo "All 3 services have been updated and redeployment triggered."
echo "Wait ~5-10 minutes for builds to complete, then verify with:"
echo "  railway logs --service backend"
echo "  railway logs --service auth-server"
echo "  railway logs --service content"
echo
echo "Or check the Railway dashboard: https://railway.com/project/1c394e87-e809-442b-aa14-55ceabb26d9c"
