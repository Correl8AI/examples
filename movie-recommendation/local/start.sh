#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [[ ! -f .env ]]; then
  echo "Copy local/.env.example to local/.env and set CORREL8_* and OPENAI_API_KEY"
  exit 1
fi

docker compose -f docker-compose.yml up --build
