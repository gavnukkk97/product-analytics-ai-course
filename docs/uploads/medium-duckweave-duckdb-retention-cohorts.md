---
title: "DuckDB Retention Cohorts With Window Functions"
source: https://medium.com/@duckweave/duckdb-retention-cohorts-with-window-functions-29faf9b4f525
author: Duckweave
modules: [M3.2, M2.3]
downloaded: 2026-09-14
---

# DuckDB Retention Cohorts With Window Functions

*Автор: Duckweave*  
*Источник: https://medium.com/@duckweave/duckdb-retention-cohorts-with-window-functions-29faf9b4f525*

## Use DuckDB window functions to compute clean cohort retention — fast, readable SQL you’ll actually trust in dashboards.

[![Image 1: Duckweave](https://miro.medium.com/v2/resize:fill:32:32/1*Z9K3659o4e5573TBUk_Dlg.png)](https://medium.com/@duckweave?source=post_page---byline--29faf9b4f525-----------------------------------------)

5 min read

Jan 26, 2026

Press enter or click to view image in full size

![Image 2](https://miro.medium.com/v2/resize:fit:700/1*icFkl3A7TK-jFRYphIsfkQ.png)

_Learn DuckDB window functions for retention cohorts: cohorting, month offsets, retention curves, and clean cohort math with production-ready SQL examples._

You know the feeling: retention sounds simple until you write the query.

Suddenly it’s joins on joins, time bucketing weirdness, and that one off-by-one month bug that makes your dashboard… optimistic.

Let’s fix that.

DuckDB is quietly perfect for cohort math because it’s fast, local-friendly, and _honest_ — especially when you lean on window functions instead of spaghetti SQL. And yes, you can compute retention in a way that’s both correct and readable.

This is the cleanest cohort math you’ll write.

## Why Retention Queries Get Messy (And How to Keep Them Clean)

Retention breaks down when you mix three concepts in one step:

1.   **Cohort assignment** (when did the user “start”?)
2.   **Activity measurement** (did the user return?)
3.   **Time offset** (week 0, week 1, month 2… compared to what?)

Most “bad retention SQL” collapses all three into one giant GROUP BY, then tries to patch correctness with DISTINCT and hope.

The clean approach is layered:

*   Build a **user timeline** of activity by period (week/month)
*   Use a window function to compute each user’s **cohort period**
*   Compute **offset** from cohort to activity
*   Aggregate once, at the end

## Architecture Flow: The Cohort Math Pipeline

Here’s the mental model I use — simple, debuggable, hard to mess up:

Raw events

 |

 |

 |

User-period activity (one row per user per period)

 |

 |

 |

Cohort facts (user_id, cohort_period, activity_period, offset)

 |

 |

 |

Retention curve (retained_users / cohort_size)
The magic is step (2): **the cohort is a windowed MIN**. No self-joins. No subqueries that you’re scared to edit.

## Set Up a Tiny Example Dataset

Assume a classic events table:

*   `user_id`
*   `event_ts` (timestamp)
*   `event_name` (optional)

You might have this in Parquet/CSV, but the SQL stays the same.

We’ll do **monthly retention** first (weekly is the same idea with `date_trunc('week', ...)`).

## Step 1: Collapse Events Into User-Month Activity

## Why this matters

If a user triggers 50 events in a month, you still want **one “active” flag** for that month. Otherwise your retention counts inflate.

```sql
WITH user_months AS (
 SELECT
 user_id,
 date_trunc('month', event_ts) AS month
 FROM events
 GROUP BY 1, 2
)
SELECT * FROM user_months;
```
This is the first “make it boring” step. Retention loves boring.

## Step 2: Use a Window Function to Assign Each User’s Cohort

This is the key move:

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
```
 month AS activity_month,

 MIN(month) OVER (PARTITION BY user_id) AS cohort_month

 FROM user_months

)

SELECT * FROM cohorted;
Now every row carries:

*   `cohort_month` = the user’s first active month
*   `activity_month` = a month they were active

This is already enough to debug 80% of retention issues. You can literally filter one user and see their timeline.

## Step 3: Compute the Month Offset (Cohort Age)

DuckDB makes date math straightforward. We’ll compute “months since cohort” as an integer.

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
```
 month AS activity_month,

 MIN(month) OVER (PARTITION BY user_id) AS cohort_month

 FROM user_months

),

facts AS (

```sql
SELECT
 user_id,
 cohort_month,
 activity_month,
 (
 (EXTRACT(year FROM activity_month) - EXTRACT(year FROM cohort_month)) * 12
```
 + (EXTRACT(month FROM activity_month) - EXTRACT(month FROM cohort_month))

 )::INTEGER AS month_offset

 FROM cohorted

)

```sql
SELECT * FROM facts
ORDER BY cohort_month, user_id, activity_month;
```
**Sanity check:**

*   offset 0 = cohort month (the “first month”)
*   offset 1 = next month
*   offset 2 = two months later

If you ever see negative offsets, something upstream is wrong. That’s why we keep layers.

## Step 4: Aggregate Cohort Size and Retained Users

Now we compute the retention curve.

## Get Duckweave’s stories in your inbox

Join Medium for free to get updates from this writer.

Remember me for faster sign in

Two numbers matter:

*   **cohort_size** = number of unique users in that cohort (offset 0)
*   **retained_users** = number of unique users active at each offset

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
```
 month AS activity_month,

 MIN(month) OVER (PARTITION BY user_id) AS cohort_month

 FROM user_months

),

facts AS (

```sql
SELECT
 user_id,
 cohort_month,
 (
 (EXTRACT(year FROM activity_month) - EXTRACT(year FROM cohort_month)) * 12
```
 + (EXTRACT(month FROM activity_month) - EXTRACT(month FROM cohort_month))

 )::INTEGER AS month_offset

 FROM cohorted

),

cohort_sizes AS (

```sql
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
This is the “dashboard-ready” table: each cohort has a curve.

And it reads cleanly because each stage has a job.

## Where Window Functions Make This Better (Not Just Faster)

You might be wondering: couldn’t we compute cohort_month with a join to a “first_event” table?

Sure. But window functions give you three practical advantages:

## 1) Fewer moving parts

No extra join means fewer ways to accidentally duplicate rows.

## 2) Easier debugging

Every activity row carries its cohort right there. Filter one user and inspect.

## 3) Cleaner extensions

Want “cohort by first purchase” instead of first activity? Swap the input rows.

## Real-World Retention: Paid vs Free (One Extra Window Trick)

Let’s say you want cohorts based on whether the user was “paid” at cohort time.

You can join plan history, then use window functions to pick the **first known plan** at or near cohort.

A simple pattern:

*   compute cohort_month
*   join plan snapshots by month
*   pick plan at cohort_month

Conceptually:

```sql
SELECT
 user_id,
 cohort_month,
 plan_tier_at_cohort,
 month_offset,
 retained_users
FROM ...
```
The point: once you’ve built the `facts` table (user_id, cohort_period, offset), segmentation becomes a clean add-on—not a full rewrite.

## Common Mistakes (And the Fixes)

## Mistake 1: Counting events instead of users

**Fix:** collapse to user-period first (`GROUP BY user_id, month`).

## Mistake 2: Off-by-one time buckets

**Fix:** always `date_trunc()` before cohorting and before offset math.

## Mistake 3: Cohort size changes per offset

If cohort_size isn’t constant for a cohort, you’re probably computing it from the wrong table.

**Fix:** compute cohort_size only from `month_offset = 0`.

## Mistake 4: “Retention” includes users before they joined

**Fix:** ensure offset is computed from `cohort_month`, not calendar month indexes.

## Conclusion: Cohort Math Should Feel Like Physics, Not Folklore

Good retention SQL feels inevitable.

You can look at it and think: “Yeah, that’s obviously correct.”

DuckDB window functions get you there — especially the simple trick of:

> `MIN(period) OVER (PARTITION BY user_id)`_for cohort assignment_

If you want, drop a comment with:

*   your table schema (events columns),
*   whether you want weekly or monthly,
*   and your retention definition (active, purchase, session)

…and I’ll adapt the query into a production-ready version for your exact setup.
