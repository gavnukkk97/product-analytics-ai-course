---
title: "10 SQL Queries Every Data Analyst Actually Uses (With Real-World Examples)"
source: https://snehagupta-contact.medium.com/10-sql-queries-every-data-analyst-actually-uses-with-real-world-examples-0dcef0cd5fd3
author: Sneha Gupta
modules: [M3.2]
downloaded: 2026-09-14
---

# 10 SQL Queries Every Data Analyst Actually Uses (With Real-World Examples)

*Автор: Sneha Gupta*  
*Источник: https://snehagupta-contact.medium.com/10-sql-queries-every-data-analyst-actually-uses-with-real-world-examples-0dcef0cd5fd3*

## Stop memorizing syntax. Start thinking like an analyst.

[![Image 1: Sneha Gupta](https://miro.medium.com/v2/resize:fill:32:32/1*2Zv32gOtMBhemYqBtWASTA.png)](https://snehagupta-contact.medium.com/?source=post_page---byline--0dcef0cd5fd3-----------------------------------------)

18 min read

Mar 8, 2026

Press enter or click to view image in full size

![Image 2](https://miro.medium.com/v2/resize:fit:700/1*GNsIyrt2oAn-8Ph2XtJ_rw.png)

## Introduction: The Gap Between Learning SQL and Using It

Picture this. You’ve just finished an online SQL course. You aced the exercises, understood the JOIN diagrams, and confidently wrote a few SELECT statements. You feel ready.

Then you land your first data analyst role — or sit in your first interview — and someone asks: _“Can you pull the top 10 customers by revenue for last quarter, broken down by region, and flag anyone whose spending dropped more than 20% compared to the previous quarter?”_

And you freeze.

Not because you don’t know SQL. But because no tutorial ever showed you how SQL actually lives in the real world — messy tables, business questions, and queries that need to _mean_ something.

That’s the gap this article is here to close.

I’ve spent years working with data — pulling reports, answering business questions at 9am standups, debugging queries someone else wrote at midnight. And in all that time, the same 10 types of SQL queries show up over and over again. Not just in my work, but in interviews, dashboards, and every analytics team I’ve ever seen.

These aren’t textbook queries. They’re the ones that actually run in production. The ones that tell a business whether it’s growing or bleeding. The ones that get you hired.

Let’s go through all 10. I’ll explain each one in plain language, show you a real example, give you an analogy that makes it click, point out the mistakes beginners always make, and show you how it shows up in interviews.

By the end, you won’t just know these queries — you’ll understand _why_ they exist.

## What These Queries Really Mean

Before we dive in, a quick mindset shift.

SQL is not about memorizing keywords. It’s about asking questions of data. Every query you write is answering something: Who are my best customers? Where are users dropping off? What happened to sales last month?

The 10 queries in this article map to 10 types of questions that data analysts get asked every single day. Once you see them that way, the syntax becomes the easy part.

## Query 1: The Basic Aggregation — COUNT, SUM, AVG

### The Simple Example

```sql
SELECT 
 product_category,
 COUNT(*) AS total_orders,
 SUM(order_value) AS total_revenue,
 AVG(order_value) AS avg_order_value
FROM orders
GROUP BY product_category
ORDER BY total_revenue DESC;
```
What’s happening here:

*   We’re grouping all orders by their category
*   For each group, we count how many orders exist, add up the revenue, and find the average
*   We sort by total revenue so the biggest categories appear first

## Real-World Scenario

You’re an analyst at an e-commerce company. Your manager walks over and asks: _“Which product categories are driving the most revenue this month?”_

This is your query. You grab the `orders` table, group by `product_category`, sum the revenue, and within 30 seconds you have the answer: Electronics is #1, Home Decor is #2, and Books — despite having the most orders — has the lowest average order value.

That last insight? That’s the one that starts a real business conversation.

## The Analogy

Think of a classroom teacher calculating grades. Instead of looking at each student’s paper one by one, she groups them by subject, counts how many tests were taken, finds the total score, and computes the average. GROUP BY is just that — sorting things into buckets and doing math on each bucket.

## Common Mistakes

1. Forgetting GROUP BY entirely. If you use SUM or COUNT, you almost always need GROUP BY. Without it, SQL either throws an error or gives you one giant number.

2. Grouping by the wrong column. Grouping by `order_id` when you meant `product_category` gives you one row per order — not useful.

3. Using AVG when you should use SUM. If you want total revenue, use SUM. AVG gives you the average per order — a completely different number.

## Interview Angle

_“Write a query to find the top 5 salespersons by total sales amount.”_

This is a classic. The trick is remembering ORDER BY + LIMIT at the end, and making sure you GROUP BY the salesperson correctly.

## Query 2: Filtering with WHERE vs. HAVING

### The Simple Example

```sql
SELECT product_category, SUM(order_value) AS total_revenue
FROM orders
WHERE order_status = 'completed'
GROUP BY product_category
HAVING SUM(order_value) > 10000;
```
The key difference:

*   `WHERE` filters individual rows _before_ any grouping happens
*   `HAVING` filters _groups_ after the aggregation is done

## Real-World Scenario

At a fintech startup, you need to find all customer segments with total transaction volume above $50,000 — but only looking at successful transactions (not failed or pending ones). You use WHERE to remove the noise first, then HAVING to keep only the high-volume segments.

## The Analogy

Imagine you’re sorting a pile of restaurant receipts. First, you throw away all the voided receipts — that’s WHERE. Then you group the remaining ones by table number and only keep tables where the total bill exceeded $200 — that’s HAVING. Two different filters, two different moments in the process.

## Common Mistakes

1. Using HAVING instead of WHERE for row-level filters. HAVING works, but it’s slower — it filters after doing all the aggregation work.

2. Using WHERE on an aggregate. `WHERE SUM(order_value) > 1000` will throw an error. That's HAVING's job.

3. Forgetting HAVING exists. Many beginners just don’t know about it and write messy subqueries when HAVING would solve it in one line.

## Interview Angle

_“What’s the difference between WHERE and HAVING? Can you give an example where HAVING is necessary?”_

The answer: HAVING is necessary when filtering on an aggregated value. WHERE can’t touch aggregates — it runs too early in the query execution order.

## Query 3: JOINs — Connecting the Dots Between Tables

### The Simple Example

```sql
SELECT 
 u.user_id,
 u.name,
 u.email,
 COUNT(o.order_id) AS total_orders,
 SUM(o.order_value) AS lifetime_value
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
GROUP BY u.user_id, u.name, u.email
ORDER BY lifetime_value DESC;
```
What’s happening: We start with the `users` table (every user). We LEFT JOIN `orders` — meaning we keep all users, even those with zero orders. Users with no orders will show NULL for order stats — and that's intentional.

## Real-World Scenario

In product analytics, someone asks: _“How many of our registered users have never made a purchase?”_ A LEFT JOIN is the answer. If you used an INNER JOIN, you’d only see users who _have_ orders. The LEFT JOIN shows you everyone — including the users who signed up and disappeared.

## The Analogy

Think of two class lists. One is a list of all students enrolled at school. The other is a list of students who submitted their homework. An INNER JOIN gives you only students who appear on both lists. A LEFT JOIN gives you all enrolled students, with a blank in the homework column for those who didn’t submit.

## Common Mistakes

1. Using INNER JOIN when LEFT JOIN is needed. This silently drops rows. Beginners often don’t realize they’re missing data.

2. Joining on the wrong column. `ON u.user_id = o.customer_id` — if the column names differ, you must match them correctly.

3. Cartesian explosions. Forgetting the ON clause, or joining on a non-unique column, creates millions of duplicate rows.

4. Not understanding NULL after LEFT JOIN. After a LEFT JOIN, unmatched rows will have NULLs in the right table’s columns. `COUNT(*)` will still count them — use `COUNT(o.order_id)` to count only actual matches.

## Interview Angle

_“Write a query to find all customers who have never placed an order.”_

```sql
SELECT u.user_id, u.name
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
WHERE o.order_id IS NULL;
```
This is the classic LEFT JOIN + WHERE IS NULL pattern. Every interviewer loves it.

## Query 4: Subqueries and CTEs — Queries Within Queries

### The Simple Example

```sql
WITH monthly_revenue AS (
 SELECT 
 DATE_TRUNC('month', order_date) AS month,
 SUM(order_value) AS revenue
 FROM orders
 WHERE order_status = 'completed'
 GROUP BY 1
)
SELECT 
 month,
 revenue,
 LAG(revenue) OVER (ORDER BY month) AS prev_month_revenue,
 ROUND(
 (revenue - LAG(revenue) OVER (ORDER BY month)) / 
 LAG(revenue) OVER (ORDER BY month) * 100, 2
 ) AS growth_pct
FROM monthly_revenue
ORDER BY month;
```
What this does: Calculates monthly revenue, then compares each month to the previous one to show percentage growth. The CTE acts as step one, and then you query it like a normal table in step two.

## Real-World Scenario

Every analyst in a business gets asked some version of: _“How are we trending month over month?”_ CTEs make this readable. Instead of nesting five subqueries inside each other like a data lasagna, you build named steps that are easy to read, debug, and hand off to someone else.

## The Analogy

Think of CTEs like scratch paper in a math exam. Instead of trying to solve everything in one massive equation, you work it out in stages — write the intermediate answer, then use it in the next step. CTEs are your scratch paper.

## Common Mistakes

1. Overusing subqueries when a CTE is cleaner. Nested subqueries become impossible to read after two levels deep.

2. Forgetting the WITH keyword syntax. Multiple CTEs are comma-separated after the first WITH, not multiple WITH keywords.

3. Referencing a CTE outside its scope. CTEs only exist for the query they’re attached to — you can’t call them in a separate query.

## Interview Angle

_“Rewrite this nested subquery using a CTE.”_ This tests whether you understand both forms and know when to use which. If you can read a tangled subquery, break it into named CTEs, and explain why it’s cleaner — that’s a strong signal to any interviewer.

## Query 5: Window Functions — The Analyst’s Secret Weapon

### The Simple Example

```sql
SELECT 
 user_id,
 order_date,
 order_value,
 SUM(order_value) OVER (
 PARTITION BY user_id 
 ORDER BY order_date
```
 ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW

 ) AS running_total

FROM orders

ORDER BY user_id, order_date;
What’s happening: For each user, we’re calculating a running total of their spending over time — without collapsing rows. Every order keeps its own row, but gains a new column showing the cumulative total up to that point.

## Real-World Scenario

A product team wants to understand user spending behavior over their lifetime. When did users hit $500 in total spending? When did they become “VIP”? Window functions let you track per-user running totals, ranks, and trends without losing row-level detail — something GROUP BY can never do.

Other window functions you’ll use constantly:

*   `ROW_NUMBER()` — unique rank for each row
*   `RANK()` — rank with ties allowed
*   `LAG()` / `LEAD()` — look at the previous or next row's value
*   `NTILE(4)` — divide users into quartiles

## The Analogy

Imagine a race where runners cross the finish line one by one. After each runner finishes, a scoreboard updates to show their rank — but the previous runners’ times don’t disappear. Window functions are that scoreboard: they compute something about context (your rank, your running total, the previous value) without erasing the individual records.

## Common Mistakes

1. Confusing PARTITION BY with GROUP BY. GROUP BY collapses rows. PARTITION BY keeps all rows but defines a “window” per group. This is the most important distinction in all of window functions.

2. Forgetting ORDER BY inside OVER(). For running totals and LAG/LEAD, the ORDER BY inside the window function is critical.

3. Mixing window functions with GROUP BY incorrectly. You can’t use a window function directly in a WHERE clause. Wrap it in a CTE first.

## Interview Angle

_“Find the top 3 customers by revenue within each region.”_

This is a ROW_NUMBER() question — partition by region, order by revenue descending, then filter where `row_number <= 3`. It's one of the most common window function questions in analyst interviews.

## Query 6: Date and Time Queries

### The Simple Example

```sql
SELECT 
 DATE_TRUNC('month', order_date) AS month,
 COUNT(*) AS orders,
 SUM(order_value) AS revenue
FROM orders
WHERE order_date >= DATE_TRUNC('year', CURRENT_DATE)
GROUP BY 1
ORDER BY 1;
```
What this does: Pulls monthly order counts and revenue for the current year-to-date. Clean, simple, and something you’ll write in some form every single week as an analyst.

## Real-World Scenario

Almost every business report is time-based. Daily active users. Weekly revenue. Month-over-month growth. Quarter-end summaries. Date manipulation is not optional — it’s foundational.

Key functions to know: `DATE_TRUNC()` rounds a date down to month, week, year. `DATEDIFF()` calculates days between two dates. `EXTRACT()` pulls year, month, or day from a date. `CURRENT_DATE` and `NOW()` give you today's date or timestamp.

## The Analogy

Date functions are like a zoom lens on a timeline. You can zoom in (look at individual days), zoom out (group by month), or calculate distances between two points (how many days since signup). You decide the zoom level; SQL executes it.

## Common Mistakes

1. Comparing dates as strings. `WHERE order_date = '2024-01-15'` works only if your date column is actually a date type — not a VARCHAR storing date-like text.

## Get Sneha Gupta’s stories in your inbox

Join Medium for free to get updates from this writer.

Remember me for faster sign in

2. Off-by-one errors with date ranges. `BETWEEN '2024-01-01' AND '2024-01-31'` misses the last millisecond of Jan 31 if your column stores timestamps. Use `>= '2024-01-01' AND < '2024-02-01'` instead.

3. Timezone blindness. In global products, a transaction at `2024-01-01 00:30:00 UTC` might be Dec 31 in New York. Always be explicit about timezones.

## Interview Angle

_“Write a query to find users who signed up in the last 30 days but haven’t made a purchase.”_

This combines date filtering (`WHERE signup_date >= CURRENT_DATE - INTERVAL '30 days'`) with the LEFT JOIN / IS NULL pattern for non-purchasers. It's testing two concepts at once.

## Query 7: CASE WHEN — Conditional Logic Inside SQL

### The Simple Example

```sql
SELECT 
 user_id,
 total_orders,
 lifetime_value,
 CASE 
 WHEN lifetime_value >= 1000 THEN 
 WHEN lifetime_value >= 500 THEN 
 WHEN lifetime_value >= 100 THEN 
 ELSE 
 END AS customer_segment
FROM user_summary;
```
What this does: Assigns every customer a segment label based on their lifetime spending. No Python. No Excel. Pure SQL.

## Real-World Scenario

Marketing teams constantly need to segment users. Finance needs to flag transactions as “normal” or “suspicious.” Product teams want to bucket users by engagement level. CASE WHEN is how you create those categories directly in your query, without exporting data and manually assigning labels in a spreadsheet.

## The Analogy

CASE WHEN is exactly like an Excel IF statement — but more powerful because you can chain multiple conditions cleanly. If you’ve ever written `=IF(A1>1000,"VIP",IF(A1>500,"Regular","Inactive"))` in Excel, CASE WHEN is the SQL equivalent — and it reads much more cleanly.

## Common Mistakes

1. Forgetting ELSE. Without ELSE, any row that doesn’t match a condition returns NULL — silently, without warning. Always include ELSE to handle edge cases.

2. Order of conditions matters. SQL evaluates WHEN conditions top to bottom and stops at the first match. Put your most specific conditions first, or you’ll accidentally catch values you didn’t mean to.

3. Trying to use CASE WHEN in WHERE. You can, but usually it’s cleaner to put the logic in SELECT and filter afterward.

## Interview Angle

_“Write a query to calculate the percentage of orders that are high-value (above $500) vs low-value.”_

```sql
SELECT 
 ROUND(100.0 * SUM(CASE WHEN order_value > 500 THEN 1 ELSE 0 END) / COUNT(*), 2) AS high_value_pct
FROM orders;
```
This CASE WHEN inside an aggregation pattern shows up constantly in real work and in interviews. Learn it cold.

## Query 8: DISTINCT and Deduplication

### The Simple Example

```sql
SELECT COUNT(DISTINCT user_id) AS unique_buyers
FROM orders
WHERE DATE_TRUNC('month', order_date) = DATE_TRUNC('month', CURRENT_DATE);
```
Why not just COUNT(*)? COUNT(*) counts rows — one user buying 5 times contributes 5 to the count. COUNT(DISTINCT user_id) counts unique people, regardless of how many times they bought. Two completely different numbers.

## Real-World Scenario

In product or marketing analytics, the difference between “events” and “unique users” is enormous. A mobile app might have 100,000 daily sessions — but only 40,000 unique users. DISTINCT is what separates activity volume from actual reach. Both metrics matter, but they answer completely different business questions.

## The Analogy

You’re hosting a party and you have a sign-in sheet. People sign in every time they grab a drink. COUNT(*) tells you how many drinks were grabbed. COUNT(DISTINCT name) tells you how many different people showed up. Both are useful — but they answer completely different questions.

## Common Mistakes

1. Using DISTINCT on the wrong column. `SELECT DISTINCT user_id, order_id` gives you distinct _combinations_ — not just distinct users. The result can look right but be completely wrong.

2. Confusing COUNT(*) and COUNT(DISTINCT). These give very different numbers. Know which question you’re actually answering before you write the query.

3. Deduplication without understanding why duplicates exist. Sometimes duplicates are a data quality issue that needs fixing upstream — not just patched with DISTINCT.

## Interview Angle

_“How would you find the number of active users per day this month?”_

This is `COUNT(DISTINCT user_id)` grouped by date — a fundamental metric in every product analytics setup, and one of the first things any analyst learns to build.

## Query 9: Self Joins — Comparing Rows Within the Same Table

### The Simple Example

```sql
SELECT DISTINCT a.user_id
FROM orders a
JOIN orders b 
 ON a.user_id = b.user_id
 AND DATEDIFF(b.order_date, a.order_date) = 1;
```
What’s happening: We’re joining the `orders` table to itself — comparing each order row against other rows from the same user, exactly one day apart. Same table. Two copies. One join condition.

## Real-World Scenario

Self joins seem weird at first — why join a table to itself? But they unlock comparisons that no other query type can do cleanly: “Which employees earn more than their manager?” “Which transactions happened within 10 minutes of a previous transaction for the same account?” “Find users who bought Product A and then Product B within a week.” All of these need a self join.

## The Analogy

Imagine a list of all flights. To find round trips, you join the flight list to itself — where the departure city of Flight B equals the arrival city of Flight A, for the same passenger. You’re comparing the list against itself.

## Common Mistakes

1. Cartesian explosion. A self join without a careful ON clause multiplies every row by every other row. A table with 10,000 rows becomes 100 million rows. Always think carefully about your matching condition.

2. Not using aliases. Self joins require table aliases (a, b) — without them, SQL can’t tell which copy of the table you’re referencing.

## Interview Angle

_“Write a query to find all employees whose salary is higher than their manager’s salary.”_

```sql
SELECT e.employee_id, e.name, e.salary
FROM employees e
JOIN employees m ON e.manager_id = m.employee_id
WHERE e.salary > m.salary;
```
Classic self join. Every SQL interviewer has asked this question at some point.

## Query 10: Cohort Analysis and Retention Queries

### The Simple Example

```sql
WITH cohort_base AS (
 SELECT 
 user_id,
 DATE_TRUNC(
 FROM orders
 GROUP BY user_id
),
user_activity AS (
 SELECT 
 o.user_id,
 c.cohort_month,
 DATE_TRUNC(
 DATEDIFF(
 DATE_TRUNC(
 FROM orders o
 JOIN cohort_base c ON o.user_id = c.user_id
)
SELECT 
 cohort_month,
 months_since_first,
 COUNT(DISTINCT user_id) AS retained_users
FROM user_activity
GROUP BY 1, 2
ORDER BY 1, 2;
```
What this does: Groups users by the month they first bought something (their “cohort”), then tracks how many of them return to buy in subsequent months. This is the foundation of retention analysis.

## Real-World Scenario

If you want to know whether your product is improving retention over time, cohort analysis is the answer. Are users who joined in Q4 2024 sticking around longer than users who joined in Q4 2023? That’s the question retention cohorts answer — and it’s one of the most important analytical frameworks in any business with recurring customers.

## The Analogy

Imagine tracking 100 students who started school in September. In October, 80 came back. In November, 65. By December, 50. That group who started together in September — that’s a cohort. You’re watching the same group of people over time, not a random cross-section each month. Cohort analysis tells you the real story of retention.

## Common Mistakes

1. Confusing cohort retention with overall retention. Monthly active user counts look at a cross-section. Cohort retention follows the same people. They tell very different stories — and a business can look like it’s growing while actually hemorrhaging users.

2. Defining the cohort wrong. Use `MIN(order_date)` per user to find their first activity. A user's cohort is always the month they _first_ appeared.

3. Forgetting to normalize. Raw retained user counts aren’t comparable across cohorts of different sizes. Divide by cohort size to get a retention rate.

## Interview Angle

_“How would you calculate month-1 retention for users who signed up in January?”_

Month-1 retention = users active in February ÷ users who first appeared in January. This is a staple of product analytics interviews, and being able to write the SQL cleanly is a strong differentiator.

## Common Mistakes Across All SQL Queries

After working with data for years and reviewing countless queries from beginners and junior analysts, the same patterns come up:

1. Not testing with LIMIT first. Before running a heavy query on millions of rows, add `LIMIT 100` to preview the output. It saves time and prevents surprises.

2. Assuming data is clean. Real data has NULLs, duplicates, inconsistent formats, and ghost records. Always check before you trust your results.

3. Writing queries that answer the wrong question. Before writing a single line of SQL, write out the business question in plain English. This single habit saves enormous debugging time.

4. Ignoring query performance. Beginners often write queries that work but take 10 minutes to run. Understanding indexes, avoiding SELECT *, and filtering early in the query matters in production.

5. Not reading the output critically. A query can run perfectly and still return wrong results if the logic was flawed. Always sanity-check your numbers against something you already know.

## Interview Perspective: How These Show Up

SQL interviews for data analyst roles typically fall into three categories:

Conceptual questions: “What’s the difference between LEFT JOIN and INNER JOIN?” “When would you use a CTE over a subquery?”

Write queries from scratch: Given a table schema, answer a business question in SQL. The questions above — top customers, retention, churn, segmentation — are the most common.

Debug a broken query: Given a query with a bug, find and fix it. Common traps include WHERE vs. HAVING mix-ups, wrong JOIN types, and missing GROUP BY columns.

Three tricky questions to prepare for:

_“Write a query to find the second-highest salary without using LIMIT.”_ Use a subquery: `WHERE salary = (SELECT MAX(salary) FROM employees WHERE salary < (SELECT MAX(salary) FROM employees))`.

_“How would you find duplicate records in a table?”_ GROUP BY all relevant columns, then HAVING COUNT(*) > 1.

_“What happens when you GROUP BY a column that has NULLs?”_ SQL treats NULLs as a group together — all NULL values land in the same bucket. Many people don’t know this until they see it happen.

## Practical Tips for Learning These Queries

Use real datasets. The best practice data is messy and meaningful. Try Kaggle (hundreds of real-world datasets), Google BigQuery Public Datasets (production-scale, free to query), or Mode Analytics (pre-loaded datasets with a SQL editor built in).

Build a project. Pick one dataset and answer 10 business questions about it. One query per question. You’ll learn more from 10 real questions than 100 fill-in-the-blank exercises.

Read other people’s queries. GitHub, Mode, and Kaggle all have public notebooks with SQL. Read them like you’d read someone else’s code — understand the logic, not just the syntax.

Explain your query out loud before writing it. Say it in English first: _“I want all users who bought something in January but not in February, grouped by region.”_ Then translate to SQL. This builds the mental model faster than any course.

## Mental Models to Remember SQL Logic

SQL executes in a specific order — not the order you write it. FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT. Your query is evaluated in this sequence, even though you write SELECT at the very top. This explains why you can’t filter on a SELECT alias in WHERE.

Every JOIN tells a story. Before writing a JOIN, ask: What is the relationship between these two tables? One-to-one? One-to-many? Am I losing rows with INNER? The answer shapes your JOIN type.

Aggregation collapses. Window functions preserve. If you need one row per group, use GROUP BY + aggregation. If you need to add context to each existing row without collapsing anything, use a window function.

NULL is not zero and not empty string. NULL means _unknown_. `NULL = NULL` is false in SQL. Use `IS NULL` to check for it.

Work backward for complex queries. Start by picturing what the final output needs to look like — the columns, the grain, the filters. Then work backward to figure out which tables and transformations get you there.

## Mini Practice Section

Try these five problems on any dataset (Kaggle’s e-commerce datasets work perfectly):

Problem 1 — Basic Aggregation: Find the top 5 product categories by total revenue in the last 90 days. Include the number of orders and average order value for each.

Problem 2 — JOIN + Filter: Find all users who signed up more than 60 days ago but have never placed an order. Show their signup date and email.

Problem 3 — Window Function: For each customer, show every order they’ve placed along with a running total of their lifetime spend and their rank by total spend within their region.

Problem 4 — CASE WHEN: Classify every transaction as ‘High’ (>$500), ‘Medium’ ($100–$500), or ‘Low’ (<$100). Calculate what percentage of total revenue comes from each tier.

Problem 5 — Cohort Query: Group users by the month they first purchased. For each cohort, calculate how many users made a second purchase within 30 days. Express this as a retention rate.

If you can write clean, correct SQL for all five, you’re genuinely ready for a data analyst role.

## Conclusion: Think Like an Analyst, Not a Syntax Machine

Here’s the thing about SQL that nobody tells you at the start.

The syntax is the easy part. You can Google syntax. You can look up whether it’s `COUNT(*)` or `COUNT(1)`. You can check if your database uses `DATEDIFF` or `DATE_DIFF`. Documentation exists for a reason.

What you can’t Google is the _thinking_. The ability to hear a business question, visualize the data, and immediately know: _“This is a cohort problem. I need a CTE, a self-join on date, and ROW\_NUMBER() to isolate first purchases.”_ That kind of thinking is what separates a script-reader from an analyst.

The 10 query types in this article aren’t 10 random things to memorize. They’re 10 ways to think about data. Aggregation is about summarizing. JOINs are about connecting. Window functions are about context. CTEs are about clarity. Date functions are about time. CASE WHEN is about categorization. Cohort queries are about behavior across time.

Master those ways of thinking, and the SQL writes itself.

Start with one. Pick the one that feels most relevant to what you’re working on right now. Write three queries with it on a real dataset. Make the output mean something. Then move to the next one.

Progress in SQL isn’t measured by how many functions you know. It’s measured by how confidently you can translate a messy, vague business question into a clean, precise query that tells a true story.

That’s the job. And now you have the tools to do it.

_If this article helped you, bookmark it for your next SQL practice session. And if you’re preparing for a data analyst interview — try every single one of the practice problems. They’re closer to real interview questions than anything you’ll find in a prep guide._

*   SQL
*   Data Analytics
*   Data Science
*   Programming
*   Career Development
