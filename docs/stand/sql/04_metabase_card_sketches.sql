-- Эскизы SQL-карточек для М5.4 (диагностика недели).
-- Подключайте как Native Query в Metabase к БД ritm.

-- 1) Depth ≥3 (когорта last complete week по first habit)
WITH bounds AS (
  SELECT date_trunc('week', current_date)::date - 7 AS week_start,
         date_trunc('week', current_date)::date AS week_end
),
first_habit AS (
  SELECT e.user_id, min(e.ts) AS habit_at
  FROM events e
  JOIN users u ON u.user_id = e.user_id
  CROSS JOIN bounds b
  WHERE e.event_name = 'habit_created'
    AND u.is_internal = false
    AND e.ts >= b.week_start AND e.ts < b.week_end
  GROUP BY 1
),
check_days AS (
  SELECT e.user_id,
         coalesce(
           (e.props->>'local_date')::date,
           (e.props->>'local_day')::date,
           (e.ts AT TIME ZONE 'Europe/Moscow')::date
         ) AS local_day
  FROM events e
  JOIN first_habit f ON f.user_id = e.user_id
  WHERE e.event_name = 'check_in'
    AND e.ts >= f.habit_at
    AND e.ts <  f.habit_at + interval '7 days'
),
depth AS (
  SELECT user_id, count(DISTINCT local_day) AS days_with_check
  FROM check_days GROUP BY 1
)
SELECT
  round(100.0 * count(*) FILTER (WHERE coalesce(d.days_with_check,0) >= 3)
        / nullif(count(*), 0), 2) AS depth_ge3_pct,
  count(*) AS denom_users
FROM first_habit f
LEFT JOIN depth d USING (user_id);

-- 2) Habit → ≥1 check_in за 7д
WITH first_habit AS (
  SELECT user_id, min(ts) AS habit_at
  FROM events WHERE event_name = 'habit_created' GROUP BY 1
)
SELECT round(100.0 * count(*) FILTER (WHERE EXISTS (
         SELECT 1 FROM events c
         WHERE c.user_id = f.user_id AND c.event_name = 'check_in'
           AND c.ts >= f.habit_at AND c.ts < f.habit_at + interval '7 days'
       )) / nullif(count(*), 0), 2) AS habit_to_checkin_7d_pct
FROM first_habit f
JOIN users u USING (user_id)
WHERE u.is_internal = false;

-- 3) Доля paywall_view с trigger до streak_3 (early)
SELECT round(
  100.0 * count(*) FILTER (WHERE props->>'trigger' IN ('day_7', 'feature_lock'))
  / nullif(count(*), 0), 2
) AS early_paywall_share_pct
FROM events e
JOIN users u USING (user_id)
WHERE e.event_name = 'paywall_view'
  AND u.is_internal = false
  AND coalesce((e.props->>'dup')::boolean, false) IS NOT TRUE;

-- 4) New Pro (users с subscribe_started за 7д)
SELECT count(DISTINCT e.user_id) AS new_pro_users
FROM events e
JOIN users u USING (user_id)
WHERE e.event_name = 'subscribe_started'
  AND u.is_internal = false
  AND e.ts >= current_date - 7;

-- 5) Сырое: onboarding без habit за 24ч
SELECT o.user_id, o.ts AS onboarding_at
FROM events o
JOIN users u ON u.user_id = o.user_id
WHERE o.event_name = 'onboarding_completed'
  AND u.is_internal = false
  AND NOT EXISTS (
    SELECT 1 FROM events h
    WHERE h.user_id = o.user_id
      AND h.event_name = 'habit_created'
      AND h.ts <= o.ts + interval '24 hours'
  )
ORDER BY o.ts DESC
LIMIT 50;

-- Бонус: freshness
SELECT max(ts) AS max_event_ts,
       now() - max(ts) AS staleness
FROM events;
