---
title: "Top 5 DuckDB Window-Function Recipes for Instant Cohorts"
source: https://medium.com/@connect.hashblock/top-5-duckdb-window-function-recipes-for-instant-cohorts-8747275c939c
author: Hash Block
modules: [M3.2, M2.3]
downloaded: 2026-09-14
---

# Top 5 DuckDB Window-Function Recipes for Instant Cohorts

*Автор: Hash Block*  
*Источник: https://medium.com/@connect.hashblock/top-5-duckdb-window-function-recipes-for-instant-cohorts-8747275c939c*

## Practical SQL patterns to build retention, revenue, and churn cohorts directly in DuckDB — no heavy pipelines needed.

[![Image 1: Hash Block](https://miro.medium.com/v2/resize:fill:32:32/1*UrC7GhWrhoYXKDpDaXbM5A.jpeg)](https://medium.com/@connect.hashblock?source=post_page---byline--8747275c939c-----------------------------------------)

6 min read

Oct 9, 2025

Press enter or click to view image in full size

![Image 2](https://miro.medium.com/v2/resize:fit:700/1*GaD9dJ6FH5bUhxAY3yuIrQ.png)

_Five battle-tested DuckDB window-function recipes to build cohort analyses fast — retention grids, revenue curves, churn flags, and funnel conversion in pure SQL._

You don’t need a warehouse team to get clean cohort analytics.

You need a tidy events table, a few smart windows, and — let’s be real — the discipline to keep it simple.

Below are five recipes I use to go from raw clicks to “board-ready” cohort charts in minutes. All run locally in DuckDB, scale to millions of rows on a laptop, and play nicely with Parquet.

## The data we’ll use (mental model)

*   `events(user_id, event_time, event_name, amount)` — long table of user events
*   We’ll treat the **first purchase** (or first seen event) as the cohort anchor.
*   All examples are DuckDB SQL; paste into your session and adapt.

-- Think of the shape like this:

-- user_id | event_time | event_name | amount

-- 1001 | 2025-01-03 10:01:00 | visit | NULL

-- 1001 | 2025-01-05 12:10:00 | purchase | 39.00

-- 1002 | 2025-02-01 09:55:00 | signup | NULL

## 1) First-Touch Cohorts in One Pass

**Goal:** assign each user to a cohort (e.g., month of first purchase or first event).

```sql
WITH first_touch AS (
 SELECT
 user_id,
 MIN(event_time) OVER (PARTITION BY user_id) AS first_seen_at,
 DATE_TRUNC('month', MIN(event_time) OVER (PARTITION BY user_id)) AS cohort_month,
 event_time,
 event_name,
 amount
 FROM events
)
SELECT *
FROM first_touch
LIMIT 10;
```
**Why it works:**`MIN(...) OVER (PARTITION BY user_id)` gives you the anchor time without collapsing the rowset—so you can still analyze downstream events while carrying the cohort label on every row.

## Get Hash Block’s stories in your inbox

Join Medium for free to get updates from this writer.

Remember me for faster sign in

**Pro tip:** If “purchase” defines your cohort, just compute `MIN(CASE WHEN event_name='purchase' THEN event_time END) OVER (...)` and keep a fallback if you need it.

## 2) Retention Grid — No PIVOT Needed

**Goal:** compute week-over-week retention by cohort.

 We’ll track whether a user returned in week `k` after their cohort start.

```sql
WITH base AS (
 SELECT
 user_id,
 DATE_TRUNC('month', MIN(CASE WHEN event_name = 'purchase' THEN event_time END)
 ) OVER (PARTITION BY user_id) AS cohort_month,
 event_time
 FROM events
),
returns AS (
 SELECT
 user_id,
 cohort_month,
 CAST(DATEDIFF('week', cohort_month, event_time) AS INT) AS week_num
 FROM base
 WHERE event_time >= cohort_month
),
cohort_sizes AS (
 SELECT cohort_month, COUNT(DISTINCT user_id) AS cohort_users
 FROM returns
 WHERE week_num = 0 
 GROUP BY 1
),
retention AS (
 SELECT
 cohort_month,
 week_num,
 COUNT(DISTINCT user_id) AS active_users
 FROM returns
 GROUP BY 1,2
)
SELECT
 r.cohort_month,
 r.week_num,
 ROUND(100.0 * r.active_users / cs.cohort_users, 1) AS retained_pct
FROM retention r
JOIN cohort_sizes cs USING (cohort_month)
WHERE r.week_num BETWEEN 0 AND 12
ORDER BY r.cohort_month, r.week_num;
```
**Result you can chart:** each row is a cell in the cohort matrix: cohort × week ⇒ % retained. It’s small, legible, and loads instantly even on big event logs.

## 3) Revenue Cohorts with Cumulative Curves

**Goal:** plot average cumulative revenue per user over time, aligned by cohort.

```sql
WITH first_buy AS (
 SELECT
 user_id,
 MIN(CASE WHEN event_name='purchase' THEN event_time END)
 OVER (PARTITION BY user_id) AS first_purchase_at
 FROM events
),
purchases AS (
 SELECT
 e.user_id,
 DATE_TRUNC('month', f.first_purchase_at) AS cohort_month,
 e.event_time,
 COALESCE(e.amount, 0) AS amount
 FROM events e
 JOIN first_buy f USING (user_id)
 WHERE e.event_name='purchase'
 AND f.first_purchase_at IS NOT NULL
),
user_curves AS (
 SELECT
 user_id,
 cohort_month,
 CAST(DATEDIFF('week', cohort_month, event_time) AS INT) AS week_num,
 SUM(amount) OVER (
 PARTITION BY user_id
 ORDER BY event_time
```
 ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW

 ) AS user_cum_revenue

 FROM purchases

)

```sql
SELECT
 cohort_month,
 week_num,
 ROUND(AVG(user_cum_revenue), 2) AS avg_cum_rev_per_user
FROM user_curves
WHERE week_num BETWEEN 0 AND 12
GROUP BY 1,2
ORDER BY 1,2;
```
**Why it’s powerful:** You get clean **LTV curves** by cohort without pre-aggregation. Stakeholders love the “Week 4 vs Week 8” comparison to see whether acquisition quality is improving.

## 4) Churn & Reactivation with LAG Gaps

**Goal:** define churn as “no activity for 28+ days,” detect reactivation later, and summarize by cohort.

```sql
WITH touch AS (
 SELECT
 user_id,
 DATE_TRUNC('month',
 MIN(event_time) OVER (PARTITION BY user_id)
 ) AS cohort_month,
 event_time
 FROM events
),
gaps AS (
 SELECT
 user_id,
 cohort_month,
 event_time,
 LAG(event_time) OVER (PARTITION BY user_id ORDER BY event_time) AS prev_time,
 DATEDIFF('day',
 LAG(event_time) OVER (PARTITION BY user_id ORDER BY event_time),
 event_time
 ) AS gap_days
 FROM touch
),
labels AS (
 SELECT
 *,
 CASE WHEN gap_days >= 28 THEN 1 ELSE 0 END AS churn_event,
 CASE
 WHEN gap_days >= 28 THEN 1
 WHEN gap_days IS NULL THEN 0
 ELSE 0
 END AS churn_boundary
 FROM gaps
)
SELECT
 cohort_month,
 COUNT(DISTINCT user_id) FILTER (WHERE churn_boundary=1) AS churned_users,
 COUNT(DISTINCT user_id) AS total_users,
 ROUND(100.0 * COUNT(DISTINCT user_id) FILTER (WHERE churn_boundary=1)
```
 / NULLIF(COUNT(DISTINCT user_id),0), 1) AS churn_pct

FROM labels

GROUP BY 1

ORDER BY 1;
**What you get:** churn counts and rates by cohort. Add a second pass to mark “reactivated” when a post-churn event appears — same pattern, just look for the next event after a long gap.

## 5) Funnel Cohorts with QUALIFY (Dedup Like a Pro)

**Goal:** compute conversion from `view → add_to_cart → purchase` by cohort, counting each step once per user, in order.

```sql
WITH staged AS (
 SELECT
 user_id,
 DATE_TRUNC('month',
 MIN(event_time) OVER (PARTITION BY user_id)
 ) AS cohort_month,
 event_time,
 event_name,
 ROW_NUMBER() OVER (
 PARTITION BY user_id, event_name
 ORDER BY event_time
 ) AS step_rank
 FROM events
 WHERE event_name IN ('view','add_to_cart','purchase')
),
first_steps AS (
 SELECT *
 FROM staged
 QUALIFY step_rank = 1 
),
steps AS (
 SELECT
 user_id,
 cohort_month,
 MAX(CASE WHEN event_name='view' THEN 1 ELSE 0 END) AS did_view,
 MAX(CASE WHEN event_name='add_to_cart' THEN 1 ELSE 0 END) AS did_add,
 MAX(CASE WHEN event_name='purchase' THEN 1 ELSE 0 END) AS did_buy
 FROM first_steps
 GROUP BY 1,2
)
SELECT
 cohort_month,
 COUNT(*) AS cohort_users,
 SUM(did_view) AS viewers,
 SUM(did_add) AS adders,
 SUM(did_buy) AS buyers,
 ROUND(100.0 * SUM(did_add)/NULLIF(SUM(did_view),0),1) AS view_to_cart_pct,
 ROUND(100.0 * SUM(did_buy)/NULLIF(SUM(did_add),0),1) AS cart_to_buy_pct,
 ROUND(100.0 * SUM(did_buy)/NULLIF(COUNT(*),0),1) AS overall_conv_pct
FROM steps
GROUP BY 1
ORDER BY 1;
```
**Why QUALIFY matters:** it lets you keep the rowset “wide” while trimming to the first instance of each step per user — no subqueries or joins just to dedupe.

## Tiny Architecture Flow (how it fits together)

 Parquet / events table

 │

 DuckDB SQL

 ┌──────────────┼────────────────┐

 │ │ │

 [Cohorts] [Retention] [Revenue/Churn/Funnel]

 MIN() DATEDIFF() LAG(), SUM() OVER

 OVER + COUNT DISTINCT + QUALIFY/ROW_NUMBER

 │ │ │

 └─────────── tidy cohort tables ───┘

 (chart anywhere)
**Reality check:** this is intentionally boring. That’s the point. Boring means reliable, explainable, and fast to iterate.

## A quick case study (numbers you can feel)

*   A consumer app with ~1.8M events/month.
*   Local DuckDB on a 16-GB laptop.
*   Parquet input; the five queries above:
*   **Cohorts:** ~0.5–1.2s
*   **Retention 0–12 weeks:** ~1.6–2.8s
*   **Revenue curves:** ~1.9–3.5s
*   **Churn scan (LAG):** ~1.4–2.2s
*   **Funnel (QUALIFY):** ~1.0–1.8s

Is it the fastest thing on Earth? No. Is it _fast enough to answer product questions before your coffee cools?_ Absolutely.

## Practical tips to keep it snappy

*   **Partition thinking, not files.** Use `PARTITION BY` to keep queries vectorized. Let DuckDB scan columnar Parquet; don’t prematurely slice files.
*   **Anchor early.** Compute cohort anchors (first touch/buy) once and reuse in CTEs to avoid duplicated work.
*   **Prefer DISTINCT in the right place.** Counting distinct users at the **retention** layer, not in base events, keeps IO predictable.
*   **Name the business rules.** “Churn = 28 days” lives in a single CASE expression. Change it once, propagate everywhere.

## Wrap-up

Window functions are the superpower behind instant cohorts in DuckDB. With five compact patterns — **first-touch**, **retention**, **revenue curves**, **churn gaps**, and **funnel dedupe** — you can cover 80% of product analytics without leaving SQL. You might be wondering if you’ll outgrow this. Maybe one day. But for most teams, this is the sweet spot: fast iteration, clear logic, and results that ship.

**CTA:** If you want the queries as a one-file template (with comments and placeholders), say “Template please” and I’ll drop a ready-to-paste version.
