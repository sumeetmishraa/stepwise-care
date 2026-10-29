#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "Start backend in one terminal: cd \"$ROOT/Backend\" && source .venv/bin/activate && uvicorn app.main:app --reload --port 8000"
echo "Start frontend in another terminal: cd \"$ROOT/Frontend\" && npm install && npm run dev"
