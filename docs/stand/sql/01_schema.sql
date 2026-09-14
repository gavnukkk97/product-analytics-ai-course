-- Схема Ритм (М4.3 / М3.2 / М5.4)
-- Зерно: users = 1 user; events = 1 факт; subscriptions = факт подписки/статуса

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE users (
    user_id         text PRIMARY KEY,
    installed_at    timestamptz NOT NULL,
    platform        text NOT NULL CHECK (platform IN ('ios', 'android', 'web')),
    is_internal     boolean NOT NULL DEFAULT false,
    -- Учебный A/B (paywall timing): control | treatment; NULL = вне эксперимента
    ab_variant      text CHECK (ab_variant IS NULL OR ab_variant IN ('control', 'treatment')),
    ab_experiment   text DEFAULT 'paywall_timing_2026q3',
    country         text DEFAULT 'RU'
);

CREATE TABLE events (
    event_id        text PRIMARY KEY,
    user_id         text NOT NULL REFERENCES users (user_id),
    event_name      text NOT NULL,
    ts              timestamptz NOT NULL,
    props           jsonb NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX idx_events_user_ts ON events (user_id, ts);
CREATE INDEX idx_events_name_ts ON events (event_name, ts);
CREATE INDEX idx_events_props_gin ON events USING gin (props);

CREATE TABLE subscriptions (
    subscription_id text PRIMARY KEY,
    user_id         text NOT NULL REFERENCES users (user_id),
    started_at      timestamptz NOT NULL,
    plan            text NOT NULL CHECK (plan IN ('month', 'year')),
    status          text NOT NULL CHECK (status IN ('active', 'canceled', 'expired')),
    price_rub       integer NOT NULL,
    ended_at        timestamptz
);

CREATE INDEX idx_subscriptions_user ON subscriptions (user_id);
CREATE INDEX idx_subscriptions_started ON subscriptions (started_at);

COMMENT ON TABLE users IS 'Одна строка = один пользователь Ритма';
COMMENT ON TABLE events IS 'Сырой поток событий (tracking plan М4.3)';
COMMENT ON TABLE subscriptions IS 'Факт оплаты / статуса Pro';
COMMENT ON COLUMN users.ab_variant IS 'Вариант A/B paywall_timing; ключ исхода только у преподавателя';
COMMENT ON COLUMN events.props IS 'jsonb: habit_id, plan, trigger, local_date, schema_version, …';
