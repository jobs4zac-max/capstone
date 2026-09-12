#!/usr/bin/env bash
# Start the local stack (PROJECT_PLAN.md section 14.3).
#
#   Streamlit UI            :8501   deployment/app.py
#   Policy Agent (A2A)      :8001   a2a/server.py        [extension]
#   MCP server              stdio   mcp_tools/server.py  [spawned by the app]
#
# Set A2A_TRANSPORT=inproc in .env to skip the Policy Agent service entirely.
#
# Usage: ./scripts/dev.sh

set -euo pipefail
cd "$(dirname "$0")/.."

if [[ ! -f .env ]]; then
  echo "No .env found. Run: cp .env.example .env  (then add your API key)" >&2
  exit 1
fi

pids=()
cleanup() {
  echo ""
  echo "shutting down..."
  for pid in "${pids[@]:-}"; do
    kill "$pid" 2>/dev/null || true
  done
}
trap cleanup EXIT INT TERM

transport="$(grep -E '^A2A_TRANSPORT=' .env | cut -d= -f2 || echo http)"

if [[ "$transport" == "http" ]]; then
  echo "starting Policy Agent service on :8001 ..."
  # TODO(T-034): uncomment once a2a/server.py defines `app`
  # uv run uvicorn a2a.server:app --port 8001 --reload &
  # pids+=($!)
  echo "  (skipped - a2a/server.py is still a skeleton)"
fi

echo "starting Streamlit UI on :8501 ..."
uv run streamlit run deployment/app.py
