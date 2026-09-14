---
title: "DuckDB Retention Cohorts With Window Functions"
source: https://medium.com/@duckweave/duckdb-retention-cohorts-with-window-functions-29faf9b4f525
author: duckweave
modules: [M3.2, M2.3]
downloaded: 2026-09-14
---

# DuckDB Retention Cohorts With Window Functions

> Medium export for course Context (private). Do not republish.

DuckDB Retention Cohorts With Window Functions

Use DuckDB window functions to compute clean cohort retention — fast, readable SQL you’ll actually trust in dashboards.

Learn DuckDB window functions for retention cohorts: cohorting, month offsets, retention curves, and clean cohort math with production-ready SQL examples.

You know the feeling: retention sounds simple until you write the query. Suddenly it’s joins on joins, time bucketing weirdness, and that one off-by-one month bug that makes your dashboard… optimistic.

Let’s fix that.

DuckDB is quietly perfect for cohort math because it’s fast, local-friendly, and honest — especially when you lean on window functions instead of spaghetti SQL. And yes, you can compute retention in a way that’s both correct and readable.

This is the cleanest cohort math you’ll write.

## Why Retention Queries Get Messy (And How to Keep Them Clean)

Retention breaks down when you mix three concepts in one step:

- Cohort assignment (when did the user “start”?)
- Activity measurement (did the user return?)
- Time offset (week 0, week 1, month 2… compared to what?)

Most “bad retention SQL” collapses all three into one giant GROUP BY, then tries to patch correctness with DISTINCT and hope.

The clean approach is layered:

1. Build a user timeline of activity by period (week/month)
2. Use a window function to compute each user’s cohort period
3. Compute offset from cohort to activity
4. Aggregate once, at the end

## Architecture Flow: The Cohort Math Pipeline

The magic is step (2): the cohort is a windowed MIN. No self-joins.

## Step 1: Collapse Events Into User-Month Activity

```sql
-- 1) One row per user per month they were active
WITH user_months AS (
  SELECT
    user_id,
    date_trunc('month', event_ts) AS month
  FROM events
  GROUP BY 1, 2
)
SELECT * FROM user_months;
```

## Step 2: Use a Window Function to Assign Each User’s Cohort

```sql
WITH user_months AS (
  SELECT
    user_id,
    date_trunc('month', event_ts) AS month
  FROM events
  GROUP BY 1, 2
),
cohorted AS (
  SELECT
    user_id,
    month AS activity_month,
    MIN(month) OVER (PARTITION BY user_id) AS cohort_month
  FROM user_months
)
SELECT * FROM cohorted;
```

## Step 3: Compute the Month Offset (Cohort Age)

```sql
WITH user_months AS (
  SELECT
    user_id,
    date_trunc('month', event_ts) AS month
  FROM events
  GROUP BY 1, 2
),
cohorted AS (
  SELECT
    user_id,
    month AS activity_month,
    MIN(month) OVER (PARTITION BY user_id) AS cohort_month
  FROM user_months
),
facts AS (
  SELECT
    user_id,
    cohort_month,
    activity_month,
    (
      (EXTRACT(year FROM activity_month) - EXTRACT(year FROM cohort_month)) * 12
      + (EXTRACT(month FROM activity_month) - EXTRACT(month FROM cohort_month))
    )::INTEGER AS month_offset
  FROM cohorted
)
SELECT * FROM facts
ORDER BY cohort_month, user_id, activity_month;
```

## Step 4: Aggregate Cohort Size and Retained Users

```sql
WITH user_months AS (
  SELECT
    user_id,
    date_trunc('month', event_ts) AS month
  FROM events
  GROUP BY 1, 2
),
cohorted AS (
  SELECT
    user_id,
    month AS activity_month,
    MIN(month) OVER (PARTITION BY user_id) AS cohort_month
  FROM user_months
),
facts AS (
  SELECT
    user_id,
    cohort_month,
    (
      (EXTRACT(year FROM activity_month) - EXTRACT(year FROM cohort_month)) * 12
      + (EXTRACT(month FROM activity_month) - EXTRACT(month FROM cohort_month))
    )::INTEGER AS month_offset
  FROM cohorted
),
cohort_sizes AS (
  SELECT
    cohort_month,
    COUNT(DISTINCT user_id) AS cohort_size
  FROM facts
  WHERE month_offset = 0
  GROUP BY 1
),
retention AS (
  SELECT
    cohort_month,
    month_offset,
    COUNT(DISTINCT user_id) AS retained_users
  FROM facts
  GROUP BY 1, 2
)
SELECT
  r.cohort_month,
  r.month_offset,
  s.cohort_size,
  r.retained_users,
  ROUND(r.retained_users * 1.0 / s.cohort_size, 4) AS retention_rate
FROM retention r
JOIN cohort_sizes s USING (cohort_month)
ORDER BY cohort_month, month_offset;
```

## Common Mistakes

1. Counting events instead of users — collapse to user-period first.
2. Off-by-one time buckets — always date_trunc() before cohorting.
3. Cohort size changes per offset — compute cohort_size only from month_offset = 0.
4. Retention includes users before they joined — offset from cohort_month.

## Conclusion

DuckDB window functions get you there — especially `MIN(period) OVER (PARTITION BY user_id)` for cohort assignment.
