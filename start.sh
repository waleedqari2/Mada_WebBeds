#!/usr/bin/env bash
set -e

# Simple start script — loads .env and starts uvicorn
if [ -f .env ]; then
  # export variables from .env (simple approach)
  set -o allexport
  source .env
  set +o allexport
else
  echo ".env not found — copy .env.example to .env and edit values."
fi

HOST="${UVICORN_HOST:-127.0.0.1}"
PORT="${UVICORN_PORT:-8000}"
WORKERS="${WORKERS:-1}"

echo "Starting uvicorn on ${HOST}:${PORT} (workers=${WORKERS})"
uvicorn api.main:app --host "${HOST}" --port "${PORT}" --reload