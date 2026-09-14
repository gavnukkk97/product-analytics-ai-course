---
title: "SQL для продуктового аналитика — Карьерник"
source: https://kariernik.ru/blog/sql-zaprosy-dlya-produktovyh-analitikov
author: Kariernik
modules: [M3.2]
downloaded: 2026-09-14
kind: bonus-open
---

# SQL для продуктового аналитика — Карьерник

*Автор: Kariernik*  
*Источник: https://kariernik.ru/blog/sql-zaprosy-dlya-produktovyh-analitikov*

**Содержание:**

- [Схема данных](#skhema-dannykh)
- [DAU за 30 дней](#1-dau-za-30-dney)
- [Stickiness (DAU/MAU)](#3-stickiness-dau-mau)
- [Retention D7](#4-retention-d7)
- [A/B-тест: конверсия по группам](#10-a-b-test-konversiya-po-gruppam)
- [FAQ](#faq)

Продуктовый аналитик живёт в SQL: DAU, retention, когорты, воронки, A/B — всё это считается запросами к таблице событий. На собесе редко просят вывести формулу метрики на бумаге — обычно дают схему `events` и говорят «посчитай retention D7» или «покажи, где отваливаются пользователи». Ниже — 15 разобранных запросов на PostgreSQL: не просто код, а что он считает, где типичные грабли и как эту задачу подают на интервью. Все примеры работают на простой схеме из трёх таблиц.

## Схема данных

Все запросы строятся вокруг трёх таблиц. `events` — центральная: по одной строке на каждое событие пользователя.

- `users (user_id, registered_at, country, platform)` — пользователи и атрибуты регистрации.
- `events (user_id, event_name, event_time, properties)` — сырой поток событий, из него считается почти всё.
- `ab_test_users (user_id, ab_group, test_id)` — распределение пользователей по группам A/B-тестов.

## 1. DAU за 30 дней

DAU (Daily Active Users) — база продуктовой аналитики. Считаем уникальных пользователей по дням, а не строки событий, поэтому `COUNT(DISTINCT user_id)`. Ключевой момент, который проверяют на собесе: активность определяется конкретным событием (`app_open`), а не «любой строкой» — иначе фоновые пуши и системные события раздуют цифру.

```
SELECT event_time::DATE AS day, COUNT(DISTINCT user_id) AS dau
FROM events
WHERE event_name = 'app_open'
  AND event_time >= CURRENT_DATE - INTERVAL '30 day'
GROUP BY 1 ORDER BY 1;
```

## 2. WAU по неделям

```
SELECT DATE_TRUNC('week', event_time) AS week,
    COUNT(DISTINCT user_id) AS wau
FROM events
WHERE event_name = 'app_open'
GROUP BY 1 ORDER BY 1;
```

`DATE_TRUNC('week', ...)` сдвигает каждое событие к началу его недели, и мы считаем уникальных пользователей внутри недельного окна. WAU сглаживает дневные шумы (выходные, праздники) и лучше показывает тренд, чем DAU. На собесе стоит упомянуть, что по умолчанию неделя в Postgres начинается с понедельника — это влияет на границы когорт.

## 3. Stickiness (DAU/MAU)

```
WITH daily AS (
    SELECT DISTINCT event_time::DATE AS day, user_id
    FROM events WHERE event_name = 'app_open'
),
dau AS (SELECT day, COUNT(DISTINCT user_id) AS dau FROM daily GROUP BY day)
SELECT
    d.day,
    d.dau,
    (SELECT COUNT(DISTINCT user_id)
     FROM daily
     WHERE day BETWEEN d.day - INTERVAL '27 day' AND d.day) AS mau,
    ROUND(d.dau * 1.0
          / NULLIF((SELECT COUNT(DISTINCT user_id)
                    FROM daily
                    WHERE day BETWEEN d.day - INTERVAL '27 day' AND d.day), 0), 3) AS stickiness
FROM dau d
ORDER BY d.day;
```

`COUNT(DISTINCT) OVER (...)` в Postgres не работает, поэтому MAU считаем коррелированным подзапросом.

## 4. Retention D7

```
WITH cohort AS (
    SELECT DISTINCT user_id
    FROM events
    WHERE event_time::DATE = '2026-04-01'
),
d7 AS (
    SELECT DISTINCT user_id
    FROM events
    WHERE event_time::DATE = '2026-04-08'
)
SELECT COUNT(*) * 100.0 / (SELECT COUNT(*) FROM cohort) AS retention_d7
FROM cohort INTERSECT SELECT user_id FROM d7;
```

## 5. Воронка регистрации

```
SELECT
    COUNT(DISTINCT user_id) FILTER (WHERE event = 'landing_visit') AS visits,
    COUNT(DISTINCT user_id) FILTER (WHERE event = 'signup_start') AS starts,
    COUNT(DISTINCT user_id) FILTER (WHERE event = 'signup_complete') AS signups,
    COUNT(DISTINCT user_id) FILTER (WHERE event = 'email_confirm') AS confirmed
FROM events
WHERE event_time >= CURRENT_DATE - INTERVAL '30 day';
```

Если хочется сразу закрепить тему на практике — [открой тренажёр в Telegram](https://t.me/kariernik_bot/app?startapp=web_blog_sql-zaprosy-dlya-produktovyh-analitikov_mid1). 10 минут в день — и синтаксис в пальцах.

## 6. Activation rate (из регистрации в первое действие)

```
SELECT
    COUNT(DISTINCT user_id) FILTER (WHERE registered) AS regs,
    COUNT(DISTINCT user_id) FILTER (WHERE registered AND first_action) AS activated,
    ROUND(
        COUNT(DISTINCT user_id) FILTER (WHERE registered AND first_action) * 100.0 /
        NULLIF(COUNT(DISTINCT user_id) FILTER (WHERE registered), 0), 2
    ) AS activation_rate
FROM user_flags
WHERE registered_at >= CURRENT_DATE - INTERVAL '30 day';
```

## 7. Когортная retention таблица

```
WITH cohort AS (
    SELECT user_id, DATE_TRUNC('week', MIN(event_time))::DATE AS cohort_week
    FROM events GROUP BY user_id
),
activity AS (
    SELECT c.user_id, c.cohort_week,
        (DATE_TRUNC('week', e.event_time)::DATE - c.cohort_week) / 7 AS week_num
    FROM cohort c JOIN events e USING (user_id)
)
SELECT cohort_week, week_num, COUNT(DISTINCT user_id) AS active
FROM activity GROUP BY 1, 2 ORDER BY 1, 2;
```

## 8. Обратная воронка: где отваливаются пользователи

```
SELECT
    step,
    users,
    LAG(users) OVER (ORDER BY step_num) AS prev,
    LAG(users) OVER (ORDER BY step_num) - users AS dropoff,
    ROUND((LAG(users) OVER (ORDER BY step_num) - users) * 100.0 /
        LAG(users) OVER (ORDER BY step_num), 2) AS dropoff_pct
FROM (
    SELECT 1 AS step_num, 'signup' AS step,
        COUNT(DISTINCT user_id) FILTER (WHERE event = 'signup') AS users
    FROM events
    UNION ALL
    SELECT 2, 'activation',
        COUNT(DISTINCT user_id) FILTER (WHERE event = 'first_action')
    FROM events
    -- И так далее
) steps;
```
