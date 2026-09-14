#!/usr/bin/env bash
# Загрузка семпла CSV в уже поднятый Postgres стенда.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
# shellcheck disable=SC1091
if [[ -f "$ROOT/.env" ]]; then set -a; source "$ROOT/.env"; set +a; fi

HOST="${POSTGRES_HOST:-localhost}"
PORT="${POSTGRES_PORT:-54329}"
USER="${POSTGRES_USER:-ritm}"
DB="${POSTGRES_DB:-ritm}"
export PGPASSWORD="${POSTGRES_PASSWORD:-ritm_local}"

echo "Loading seed CSV into ${USER}@${HOST}:${PORT}/${DB} ..."

psql -h "$HOST" -p "$PORT" -U "$USER" -d "$DB" -v ON_ERROR_STOP=1 <<SQL
TRUNCATE subscriptions, events, users CASCADE;

\\copy users (user_id, installed_at, platform, is_internal, ab_variant, ab_experiment, country) FROM '${ROOT}/seed/users.csv' CSV HEADER NULL '';
\\copy events (event_id, user_id, event_name, ts, props) FROM '${ROOT}/seed/events.csv' CSV HEADER NULL '';
\\copy subscriptions (subscription_id, user_id, started_at, plan, status, price_rub, ended_at) FROM '${ROOT}/seed/subscriptions.csv' CSV HEADER NULL '';

SELECT 'users' AS t, count(*) FROM users
UNION ALL SELECT 'events', count(*) FROM events
UNION ALL SELECT 'subscriptions', count(*) FROM subscriptions;
SQL

echo "OK"
