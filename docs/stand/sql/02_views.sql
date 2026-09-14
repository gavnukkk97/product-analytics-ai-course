-- Учебные витрины для воронок / когорт / качества данных (М3.2, М5.2, М5.4)
-- Не заменяют определения в уроках — удобные отправные точки.

-- Первое habit_created на пользователя
CREATE OR REPLACE VIEW v_first_habit AS
SELECT user_id, min(ts) AS first_habit_at
FROM events
WHERE event_name = 'habit_created'
GROUP BY user_id;

-- Уникальные календарные дни с check_in (МСК) — зерно для depth
CREATE OR REPLACE VIEW v_check_in_days AS
SELECT
    e.user_id,
    coalesce(
        e.props->>'local_date',
        e.props->>'local_day',
        (e.ts AT TIME ZONE 'Europe/Moscow')::date::text
    )::date AS local_day,
    e.props->>'habit_id' AS habit_id,
    count(*) AS raw_events
FROM events e
WHERE e.event_name = 'check_in'
GROUP BY 1, 2, 3;

-- D7 depth ≥3 по когортам недели первого habit (без внутренних)
CREATE OR REPLACE VIEW v_depth_d7 AS
WITH first_habit AS (
    SELECT f.user_id, f.first_habit_at
    FROM v_first_habit f
    JOIN users u ON u.user_id = f.user_id
    WHERE u.is_internal = false
),
check_days AS (
    SELECT
        e.user_id,
        coalesce(
            (e.props->>'local_date')::date,
            (e.props->>'local_day')::date,
            (e.ts AT TIME ZONE 'Europe/Moscow')::date
        ) AS local_day
    FROM events e
    JOIN first_habit f ON f.user_id = e.user_id
    WHERE e.event_name = 'check_in'
      AND e.ts >= f.first_habit_at
      AND e.ts <  f.first_habit_at + interval '7 days'
),
depth AS (
    SELECT user_id, count(DISTINCT local_day) AS days_with_check
    FROM check_days
    GROUP BY user_id
)
SELECT
    date_trunc('week', f.first_habit_at)::date AS cohort_week,
    count(*) AS users_with_habit,
    count(*) FILTER (WHERE coalesce(d.days_with_check, 0) >= 3) AS users_depth_ge3,
    round(
        100.0 * count(*) FILTER (WHERE coalesce(d.days_with_check, 0) >= 3)
        / nullif(count(*), 0),
        2
    ) AS depth_ge3_pct
FROM first_habit f
LEFT JOIN depth d USING (user_id)
GROUP BY 1
ORDER BY 1;

-- Шаги воронки (users, без внутренних) — справочно для дашборда
CREATE OR REPLACE VIEW v_funnel_users AS
WITH base AS (
    SELECT user_id, installed_at, platform, ab_variant
    FROM users
    WHERE is_internal = false
),
flags AS (
    SELECT
        b.user_id,
        b.installed_at,
        b.platform,
        b.ab_variant,
        bool_or(e.event_name = 'onboarding_completed') AS did_onboarding,
        bool_or(e.event_name = 'habit_created') AS did_habit,
        bool_or(e.event_name = 'check_in') AS did_check_in,
        bool_or(e.event_name = 'streak_3_reached') AS did_streak3,
        bool_or(e.event_name = 'paywall_view') AS did_paywall,
        bool_or(e.event_name = 'subscribe_started') AS did_subscribe
    FROM base b
    LEFT JOIN events e ON e.user_id = b.user_id
    GROUP BY 1, 2, 3, 4
)
SELECT * FROM flags;

-- Дубли check_in на (user, habit, день) — QA из М4.3 / М3.2
CREATE OR REPLACE VIEW v_qa_duplicate_check_ins AS
SELECT
    user_id,
    props->>'habit_id' AS habit_id,
    coalesce(props->>'local_date', props->>'local_day') AS local_day,
    count(*) AS n
FROM events
WHERE event_name = 'check_in'
GROUP BY 1, 2, 3
HAVING count(*) > 1
ORDER BY n DESC;

-- paywall_view без предшествующего habit_created
CREATE OR REPLACE VIEW v_qa_paywall_without_habit AS
SELECT DISTINCT e.user_id, e.ts AS paywall_ts
FROM events e
WHERE e.event_name = 'paywall_view'
  AND NOT EXISTS (
      SELECT 1
      FROM events h
      WHERE h.user_id = e.user_id
        AND h.event_name = 'habit_created'
        AND h.ts <= e.ts
  );
