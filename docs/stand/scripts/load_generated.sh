#!/usr/bin/env bash
# Полная (или кастомная) генерация + загрузка в Postgres.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
N_USERS="${1:-2500}"
SEED="${2:-42}"

python3 "$ROOT/generator/generate_ritm.py" --n-users "$N_USERS" --seed "$SEED" --out "$ROOT/seed" --no-key
bash "$ROOT/scripts/load_seed.sh"
