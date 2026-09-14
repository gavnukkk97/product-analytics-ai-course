---
title: "Monthly Cohort Retention in SQL: Crack This Databricks Interview Question Like a Pro"
source: https://medium.com/@mohitdaxini75/monthly-cohort-retention-in-sql-crack-this-databricks-interview-question-like-a-pro-dac73335f8ec
friends_link: https://medium.com/@mohitdaxini75/dac73335f8ec?sk=f2e66e2fcfbddb969ce22a5b986ab273
author: Mohit Daxini
modules: [M3.2]
downloaded: 2026-09-14
---

# Monthly Cohort Retention in SQL: Crack This Databricks Interview Question Like a Pro

*Автор: Mohit Daxini*  
*Источник: https://medium.com/@mohitdaxini75/monthly-cohort-retention-in-sql-crack-this-databricks-interview-question-like-a-pro-dac73335f8ec*

[AWS](https://medium.com/tag/aws?source=post_page---header_tags--dac73335f8ec-----------------------------------------)

[Data Engineering](https://medium.com/tag/data-engineering?source=post_page---header_tags--dac73335f8ec-----------------------------------------)

[Sql](https://medium.com/tag/sql?source=post_page---header_tags--dac73335f8ec-----------------------------------------)

[Big Data](https://medium.com/tag/big-data?source=post_page---header_tags--dac73335f8ec-----------------------------------------)

[Interview](https://medium.com/tag/interview?source=post_page---header_tags--dac73335f8ec-----------------------------------------)

# Monthly Cohort Retention in SQL: Crack This Databricks Interview Question Like a Pro

[![Mohit Daxini](https://miro.medium.com/v2/resize:fill:64:64/1*1qSBYRgBYXGqD-YhEcrjuQ.jpeg)](https://medium.com/@mohitdaxini75?source=post_page---byline--dac73335f8ec-----------------------------------------)

[Mohit Daxini](https://medium.com/@mohitdaxini75?source=post_page---byline--dac73335f8ec-----------------------------------------)

5 min read

·

Jun 25, 2026

> ***Learn how to solve one of the most common SQL interview problems — Monthly Cohort Retention Analysis. This guide covers the intuition, step-by-step SQL solution, optimization tips, common mistakes, and interview follow-up questions frequently asked at companies like Databricks.***


Retention is one of the most important metrics in product analytics. Whether you’re building an e-commerce platform, a SaaS product, or a social media application, companies want to know:

> ***“Do users keep coming back?”***

This is exactly why **cohort retention analysis** is one of the most frequently asked SQL interview topics in product-based companies.

In this article, we’ll solve a real interview-style SQL question inspired by **Databricks**, understand the business logic behind it, discuss multiple approaches, optimize the solution, and cover common interview follow-up questions.

## The Interview Problem

You are given the following table:

### Table: `user_activity`


![](https://miro.medium.com/v2/resize:fit:1400/1*26VClFgP_y57TTE56Ra14g.png)

For every monthly cohort (the month a user first appeared), calculate the number of retained users in:

- Month 0
- Month 1
- Month 2

Where:

- **Month 0** → User was active in their joining month.
- **Month 1** → User returned exactly one month later.
- **Month 2** → User returned exactly two months later.

Return:

- `cohort_month`
- `months_since_start`
- `retained_users`

ordered by cohort month and month offset.

## Understanding Cohort Retention

Let’s first understand what a cohort actually means.

Imagine the following users:

![](https://miro.medium.com/v2/resize:fit:1252/1*PI9NlBgQ6IbjA2-yDYySvw.jpeg)

Here,

- Users A and B belong to the **January Cohort**
- User C belongs to the **February Cohort**
- User D belongs to the **March Cohort**

Now suppose User A was active again in February.

That means:

- Month 0 → January
- Month 1 → February

If User A returns again in March:

- Month 2 → March

The objective is simply counting how many users from each cohort returned after 0, 1 and 2 months.

## Visualizing the Problem

```
January Cohort  
Jan  ✓ Month 0  
Feb  ✓ Month 1  
Mar  ✓ Month 2  
  
February Cohort  
Feb ✓ Month 0  
Mar ✓ Month 1  
Apr ✓ Month 2
```

### Step 1: Find Each User’s Cohort Month

The cohort is simply the earliest activity month.

```
SELECT  
    user_id,  
    DATE_TRUNC('month', MIN(activity_date)) AS cohort_month  
FROM user_activity  
GROUP BY user_id;
```

Example output:


![](https://miro.medium.com/v2/resize:fit:1400/1*rJjm7FufeCc9O_iQzfchOA.png)

Step 2: Attach Cohort Information to Every Activity

Next, join every activity back with the user’s cohort.

This allows us to calculate:

```
Current Activity Month  
            -  
 Cohort Month
```

which gives the month offset.

### Step 3: Calculate Month Difference

Most SQL dialects support functions similar to:

```
TIMESTAMPDIFF(  
MONTH,  
cohort_month,  
activity_month  
)
```

or

```
DATEDIFF(month,...)
```

depending on the database.

This gives:


![](https://miro.medium.com/v2/resize:fit:1400/1*goD3dyaaMaM_-iuueFg2Mw.png)

### Step 4: Count Distinct Users

Finally,

Group by

- cohort
- month difference

and count unique users.

## Complete SQL Solution

```
WITH cohort AS (  
    SELECT  
        user_id,  
        DATE_TRUNC('month', MIN(activity_date)) AS cohort_month  
    FROM user_activity  
    GROUP BY user_id  
),  
retention AS (  
    SELECT  
        c.cohort_month,  
        TIMESTAMPDIFF(  
            MONTH,  
            c.cohort_month,  
            DATE_TRUNC('month', ua.activity_date)  
        ) AS months_since_start,  
        ua.user_id  
    FROM user_activity ua  
    JOIN cohort c  
        ON ua.user_id = c.user_id  
)  
SELECT  
    DATE_FORMAT(cohort_month, '%Y-%m') AS cohort_month,  
    months_since_start,  
    COUNT(DISTINCT user_id) AS retained_users  
FROM retention  
WHERE months_since_start IN (0, 1, 2)  
GROUP BY  
    cohort_month,  
    months_since_start  
ORDER BY  
    cohort_month,  
    months_since_start;
```

## How the Query Works

### CTE 1 — `cohort`

Finds the first month every user appeared.

```
User  
 ↓  
MIN(activity_date)  
 ↓  
Cohort Month
```

### CTE 2 — `retention`

Joins every activity back to its cohort.

```
Activity  
     +  
Cohort  
     ↓  
Month Difference
```

### Final Query

Groups by:

```
Cohort  
      +  
Month Difference
```

and counts unique users.

## Example Output


![](https://miro.medium.com/v2/resize:fit:1400/1*rdG6y4USR4QWSf0G3LJrkg.png)

This forms the basis of a cohort retention table.

## Time Complexity

Let **N** be the number of activity records.

Finding cohorts:

```
O(N)
```

Joining:

```
O(N)
```

Grouping:

```
O(N)
```

Overall:

> ***O(N)***

This is optimal for large datasets.

## Common Interview Mistakes

### 1. Using Activity Date Instead of Activity Month

Retention is monthly.

Always truncate dates:

```
DATE_TRUNC('month', activity_date)
```

### 2. Forgetting DISTINCT

A user may have multiple activities in the same month.

Wrong:

```
COUNT(user_id)
```

Correct:

```
COUNT(DISTINCT user_id)
```

### 3. Using First Activity Date Instead of First Activity Month

If a user joins on:

```
2024-01-25
```

their cohort is still

```
2024-01
```

not January 25.

### 4. Incorrect Month Difference Calculation

Always calculate difference between:

```
Activity Month
```

```
and
```

```
Cohort Month
```

Not between raw dates.

### Interview Follow-Up Questions

Once you solve the basic problem, interviewers often extend it with follow-up scenarios such as:

- Return the **retention percentage** instead of counts.
- Build a **cohort retention matrix** with months as columns.
- Calculate retention for **Day 1**, **Day 7**, and **Day 30**.
- Handle **weekly** or **quarterly** cohorts.
- Show cohorts even when there are **zero retained users** for a month.
- Optimize the query for tables containing **hundreds of millions of activity records**.
- Explain how you would implement this efficiently in **Spark SQL** or **Databricks**.

Being comfortable with these variations demonstrates that you understand the concept rather than just memorizing a solution.

### How to Optimize This Query on Large Datasets

When working with massive activity tables, consider the following optimizations:

- **Partition data** by activity month to reduce scan volume.
- **Precompute cohort assignments** in a dimension table if they’re reused across reports.
- **Deduplicate user-month activity** before calculating retention to avoid unnecessary processing.
- **Push filters early** (for example, restricting analysis to recent cohorts when appropriate).
- In distributed systems like Spark or Databricks, avoid unnecessary shuffles by partitioning on `user_id` where feasible and leveraging efficient join strategies.

These techniques become increasingly important as event tables grow into the billions of rows.

### Why This Question Matters

This isn’t just an interview exercise.

Cohort retention powers dashboards used by:

- SaaS companies
- Subscription platforms
- Streaming services
- Gaming companies
- E-commerce businesses
- FinTech applications

Product managers, growth teams, and leadership rely on retention metrics to evaluate product health, customer engagement, and long-term business performance.

### Practice More SQL Interview Questions

If you’re preparing for SQL interviews at top product companies, consistent practice with realistic problems is one of the fastest ways to improve.

I’ve found [**PracHub**](https://prachub.com/?utm_source=medium&utm_campaign=Mohit_Daxini) to be a useful platform for practicing SQL, Data Engineering, and analytics interview questions across varying difficulty levels.

### Key Takeaways

- A **cohort** is defined by the user’s first activity month.
- Retention measures whether users return after joining.
- Use `MIN(activity_date)` to determine the cohort.
- Calculate the month difference between the cohort month and activity month.
- Count **distinct users** for each `(cohort_month, months_since_start)` combination.
- Deduplicate user-month activity and partition data appropriately when working with large datasets.

> *If this article helped you,* ***follow*** *for more advanced SQL, PySpark, Spark optimization, and Data Engineering interview content.*

## Extracted SQL / code blocks

```sql
SELECT
    user_id,
    DATE_TRUNC('month', MIN(activity_date)) AS cohort_month
FROM user_activity
GROUP BY user_id;
```

```sql
WITH cohort AS (
    SELECT
        user_id,
        DATE_TRUNC('month', MIN(activity_date)) AS cohort_month
    FROM user_activity
    GROUP BY user_id
),
retention AS (
    SELECT
        c.cohort_month,
        TIMESTAMPDIFF(
            MONTH,
            c.cohort_month,
            DATE_TRUNC('month', ua.activity_date)
        ) AS months_since_start,
        ua.user_id
    FROM user_activity ua
    JOIN cohort c
        ON ua.user_id = c.user_id
)
SELECT
    DATE_FORMAT(cohort_month, '%Y-%m') AS cohort_month,
    months_since_start,
    COUNT(DISTINCT user_id) AS retained_users
FROM retention
WHERE months_since_start IN (0, 1, 2)
GROUP BY
    cohort_month,
    months_since_start
ORDER BY
    cohort_month,
    months_since_start;
```


