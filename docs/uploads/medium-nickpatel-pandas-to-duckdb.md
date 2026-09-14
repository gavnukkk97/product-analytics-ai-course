---
title: "From Pandas to DuckDB: Faster Local Analytics"
source: https://medium.com/@2nick2patel2/from-pandas-to-duckdb-faster-local-analytics-39cffd639ebd
author: Nick Patel
modules: [M3.4]
downloaded: 2026-09-14
---

# From Pandas to DuckDB: Faster Local Analytics

*Автор: Nick Patel*  
*Источник: https://medium.com/@2nick2patel2/from-pandas-to-duckdb-faster-local-analytics-39cffd639ebd*

## A practical workflow to keep Python’s ergonomics while getting near-SQL-engine speed on your laptop.

[![Image 1: Codastra](https://miro.medium.com/v2/resize:fill:32:32/1*IZcptplBcXPdWGYUkOqYnA.png)](https://medium.com/@2nick2patel2?source=post_page---byline--39cffd639ebd-----------------------------------------)

5 min read

Nov 1, 2025

Press enter or click to view image in full size

![Image 2](https://miro.medium.com/v2/resize:fit:700/1*cMQ2TzHn7-u7DorpcV6nTw.png)

Upgrade your Python data stack: blend Pandas with DuckDB for lightning-fast, memory-safe analytics on Parquet, CSV, and SQL — without leaving your notebook.

Short version? Pandas is wonderful. But once your CSVs get chunky and your joins get spicy, it starts to sweat. DuckDB slides in like a tiny, embeddable query engine — letting you keep your favorite Python workflow while slicing through data at speeds that feel a little unfair.

Let’s be real: you don’t need a cluster to analyze tens of millions of rows anymore.

## Why this shift is happening

Pandas made single-machine analytics accessible. But it’s row-oriented, RAM-bound, and happiest when everything fits in memory. DuckDB, by contrast, is a **columnar, vectorized SQL engine** compiled into a simple Python package. It can:

*   Query **directly from Parquet/CSV** (no big upfront loads).
*   Push filters down to the file level (**predicate pushdown**).
*   Stream results to Pandas **on demand**.
*   Use efficient **out-of-core** execution so you don’t melt your RAM.

The big unlock: you can keep writing Python and sprinkle in SQL only where it shines.

## The new mental model

Think of Pandas as your **notebook-friendly canvas** — great for modeling, small transforms, and presentation. Think of DuckDB as your **local warehouse engine** — great for scans, joins, aggregations, and file I/O.

Use SQL for the heavy lifting; materialize just what you need back into a DataFrame.

## A 10,000-foot architecture sketch

┌──────────────────────────────────────────────┐

 │ Your Notebook │

 │ (Jupyter, VS Code, Databricks) │

 └──────────────────────────┬───────────────────┘

 │ duckdb.connect()

 ┌────────────┴────────────┐

 │ DuckDB │

 │ (vectorized SQL engine)│

 └────────────┬────────────┘

 ┌──────────────────────┼───────────────────────┐

 │ │ │

 Parquet / CSV on disk Pandas DataFrames Cloud/object storage

 (predicate pushdown) (register as tables) (read via URLs)

## A realistic scenario

You’ve got a folder of monthly Parquet files (web events, sales, logs). Each file is ~1–3 GB, and you need a 90-day cohort analysis. Historically, you’d stack them in Pandas, pray your RAM holds, then write a careful chain of `groupby` calls.

## Get Codastra’s stories in your inbox

Join Medium for free to get updates from this writer.

Remember me for faster sign in

Instead:

1.   Query the files _in place_ with DuckDB.
2.   Return only the final aggregates to Pandas for charting or modeling.

You avoid loading 9 GB when you only needed 40 MB.

## The core workflow, end-to-end

## 1) Setup

import duckdb as ddb

import pandas as pd
con = ddb.connect()

## 2) Query data directly from Parquet (no upfront load)

query = """

```sql
SELECT
 date_trunc('day', event_time) AS day,
 country,
 COUNT(*) AS events,
 approx_count_distinct(user_id) AS users
FROM read_parquet('data/events/*.parquet')
WHERE event_time >= now() - INTERVAL 90 DAY
GROUP BY 1, 2
ORDER BY 1, 2
"""
df_daily = con.execute(query).df()
```
_What happened:_ DuckDB scanned only relevant row groups via Parquet metadata, performed vectorized aggregations, and returned a tidy DataFrame. No gigantic intermediate Pandas objects.

## 3) Join with a Pandas DataFrame (register → SQL)

countries = pd.DataFrame({

 "country": ["US", "IN", "DE", "BR"],

 "region": ["NA", "APAC", "EU", "LATAM"]

})
con.register("countries", countries)

enriched = con.execute("""

```sql
SELECT d.day, d.country, c.region, d.events, d.users
FROM df_daily AS d
LEFT JOIN countries AS c USING (country)
ORDER BY day, country
""").df()
```
You can register any DataFrame as a table. This is great for feature lookups, business logic maps, or model outputs you want to enrich.

## 4) Save back to Parquet (columnar + compressed)

con.execute("""

COPY (SELECT * FROM enriched)

TO 'artifacts/daily_metrics.parquet'

(WIDTH=1, COMPRESSION ZSTD);

""")
DuckDB writes high-quality Parquet files you can reuse anywhere (Spark, Arrow, BigQuery external tables). Your local machine just became a tiny data warehouse.

## Pandas vs DuckDB: choose the right tool in the loop

## Where DuckDB shines

*   Large scans, joins, window functions, group-bys
*   Reading/writing Parquet efficiently
*   SQL you already know from warehouses
*   Out-of-core operations when RAM is tight

## Where Pandas remains perfect

*   Quick column math, small transforms
*   Feature engineering experiments
*   Plotting and model prep
*   Row-wise custom logic or scikit-learn pipelines

**The sweet spot** is not replacing Pandas — it’s letting DuckDB carry the heavy boxes.

## Patterns that feel great in practice

## Pattern 1: “Query-then-plot”

agg = con.execute("""

```sql
SELECT country, sum(events) AS events
FROM read_parquet('data/events/*.parquet')
GROUP BY country
ORDER BY events DESC
LIMIT 10
""").df()
ax = agg.plot(kind="bar", x="country", y="events", title="Top 10 Countries")
```
Minimal data crosses the boundary; Pandas just visualizes.

## Pattern 2: “Feature table as a view”

con.register("features", features_df)
scored = con.execute("""

```sql
SELECT f.user_id,
 f.feature_1,
 f.feature_2,
 CASE WHEN s.events_7d > 5 THEN 1 ELSE 0 END AS label
FROM features f
LEFT JOIN read_parquet('signals/*.parquet') s
 ON f.user_id = s.user_id
""").df()
```
You keep feature engineering in Pandas while joining big signal tables via DuckDB.

## Pattern 3: “Window functions without pain”

rolling = con.execute("""

```sql
WITH base AS (
 SELECT
 date_trunc('day', ts) AS day,
 COUNT(*) AS events
 FROM read_parquet('events/*.parquet')
 GROUP BY 1
)
SELECT
 day,
 events,
 avg(events) OVER (
 ORDER BY day
```
 ROWS BETWEEN 6 PRECEDING AND CURRENT ROW

 ) AS events_7d_ma

FROM base

ORDER BY day

""").df()
Window functions are crisp in SQL; re-implementing them in Pandas often balloons code.

## Guardrails and gotchas

*   **Mind the DataFrame boundary.** Every `.df()` materializes results in RAM. Keep big work inside DuckDB; pull only what you’ll actually use.
*   **Use Parquet when you can.** It’s columnar and plays perfectly with predicate pushdown. If you’re stuck with CSV, consider one-time conversion:

con.execute(""" COPY (SELECT * FROM read_csv_auto('raw/*.csv')) TO

'stage/events.parquet' (COMPRESSION ZSTD); """)
*   **Leverage types.** DuckDB has strong typing and time zone support. Cast early; bugs vanish faster.
*   **UDFs are possible, but…** Once you’re in heavy Python UDF territory, you may give up vectorization. Keep hot paths in SQL.

## Performance expectations (without hype)

You’ll typically see **order-of-magnitude speedups** on scan-heavy tasks once you stop materializing everything in Pandas and let DuckDB push filters into Parquet. The bigger the data (within reason) and the more you filter/aggregate, the larger the payoff. If your workload is small and fiddly, Pandas alone is fine.

## A tiny checklist for your next analysis

*   Store raw inputs as **Parquet**, not CSV
*   Do joins/aggregates with **DuckDB SQL**
*   **Register** small Pandas frames for lookups
*   Materialize **only final** results to Pandas
*   **Persist** golden tables back to Parquet

Tape this to your monitor. Future-you will send thanks.

## The bigger picture: local-first analytics

We’re in a new era where a laptop + smart formats + embeddable engines deliver warehouse-like ergonomics. You might still push to BigQuery or Spark when scale demands it, but for day-to-day product analytics, experiments, or model iteration, the **Pandas ⇄ DuckDB** dance is the right kind of boring: fast, predictable, and cheap.

You might be wondering, “Do I have to become a SQL guru?” Not really. Learn 20% of SQL (SELECT, JOIN, GROUP BY, WHERE, WINDOW), and you’ll unlock 80% of the wins.

## Conclusion

Pandas isn’t going anywhere. But pairing it with DuckDB gives you an unfair advantage: **warehouse-style power, notebook simplicity**. Start by moving your next heavy group-by or multi-file join into DuckDB. Keep your plots and models in Pandas. Measure the time saved — and the RAM you didn’t burn.
