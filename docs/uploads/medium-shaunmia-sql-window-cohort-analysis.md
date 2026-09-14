---
title: "Advanced SQL — Window Functions & Cohort Analysis"
source: https://medium.com/@shaunmia/advanced-sql-window-functions-cohort-analysis-400684dfd25b
author: Shaun Mia
modules: [M3.2]
downloaded: 2026-09-14
---

# Advanced SQL — Window Functions & Cohort Analysis

*Автор: Shaun Mia*  
*Источник: https://medium.com/@shaunmia/advanced-sql-window-functions-cohort-analysis-400684dfd25b*

![Image 1](https://miro.medium.com/v2/resize:fit:400/1*bthcJ0LOKikOTXRaXoAMVA.png)

## Mastering Ranking, Time-Based Insights & Customer Retention in SQL

[![Image 2: Shaun Mia](https://miro.medium.com/v2/resize:fill:32:32/1*3HHLeqgcdE1L4xpATdwveA.jpeg)](https://medium.com/@shaunmia?source=post_page---byline--400684dfd25b-----------------------------------------)

4 min read

May 18, 2025

--

--

As you dive deeper into SQL, you’ll find that **basic queries** (like `GROUP BY`, `COUNT()`, or `JOIN`) are helpful—but not always enough when you want to do advanced analytics.

That’s where **Window Functions** and **Cohort Analysis** come in.

In this final article of the series, we’ll cover:

✅ Ranking with `ROW_NUMBER`, `RANK`, `DENSE_RANK`

 ✅ Looking forward and backward with `LEAD`, `LAG`, `FIRST_VALUE`

 ✅ Tracking changes over time: moving average & month-over-month (MoM)

 ✅ Performing **Cohort Analysis** using SQL

 ✅ A quick bonus on using **Google Colab + BigQuery** together

### 🧠 What is a Window Function?

A **Window Function** lets you **do calculations across rows** that are somehow related — without grouping them into a single row like `GROUP BY` does.

Imagine looking at a spreadsheet and writing notes next to each row like:

*   “You’re the 2nd highest sale this month!”
*   “Your revenue is $500 more than the previous order.”

That’s what window functions allow you to do — in **SQL**, inside your query.

### 🔢 Part 1: Ranking Rows — ROW_NUMBER, RANK, DENSE_RANK

These functions help you assign a **rank or position** to each row in a group.🧮

`ROW_NUMBER()`

Gives each row a unique number in a group, **even if values are tied**.

```sql
SELECT 
 customer_id, 
 order_amount,
 ROW_NUMBER() OVER (ORDER BY order_amount DESC) AS row_num
FROM orders;
`RANK()`
```
Ranks rows, but **ties get the same rank**, and **next rank is skipped**.

RANK() OVER (ORDER BY order_amount DESC)
`DENSE_RANK()`

Similar to `RANK()` but **does not skip numbers**.

DENSE_RANK() OVER (ORDER BY order_amount DESC)
**Use Case**: Find top 5 customers per month or best-selling products by ranking them.

### **⏪ Part 2: LEAD, LAG & FIRST_VALUE**

These functions help you **compare data between rows** without writing self-joins.

🔼 `LEAD()`: See the "next" row

LEAD(order_amount) OVER (ORDER BY order_date)
Gives you the next order’s amount (same table, different row).

🔽 `LAG()`: See the "previous" row

LAG(order_amount) OVER (ORDER BY order_date)
Lets you compare each row to the one before it.

### **🥇**`FIRST_VALUE()`**: Always shows the first value in the window**

FIRST_VALUE(order_amount) OVER (PARTITION BY customer_id ORDER BY order_date)
Finds the first order amount for every customer.

## Get Shaun Mia’s stories in your inbox

Join Medium for free to get updates from this writer.

Remember me for faster sign in

**Use Case**:

*   Compare current vs previous order
*   Calculate change from one row to the next
*   Understand customer’s first purchase

## 📉 Part 3: Moving Average & MoM Change (Time-Based Trends)

These functions are great for **time-series data**, like daily sales or monthly revenue.

## 🔄 Moving Average

A **moving average** smooths out data by calculating the average over the last few rows.

```sql
SELECT 
 order_date,
 SUM(order_amount) OVER (
 ORDER BY order_date
```
 ROWS BETWEEN 2 PRECEDING AND CURRENT ROW

 ) / 3 AS moving_avg

FROM orders;
→ This gives the average of the **current day + last 2 days**.

## 📈 Month-over-Month (MoM) Change

You can calculate the **percent change from last month** using `LAG()`.

```sql
SELECT 
 month,
 revenue,
 LAG(revenue) OVER (ORDER BY month) AS prev_month,
 (revenue - LAG(revenue) OVER (ORDER BY month)) / LAG(revenue) OVER (ORDER BY month) * 100 AS mom_change
FROM monthly_revenue;
```
**Use Case**:

*   Track growth
*   Detect drops or spikes in sales
*   Visualize trends on dashboards

### 📊 Part 4: Cohort Analysis Using SQL

**Cohort Analysis** helps you track groups of users over time — especially useful for **retention analysis**.

### 🧾 What’s a Cohort?

A **cohort** is a group of users who share something in common — like the month they signed up.

**Goal**: See how many users from each cohort are still active after 1, 2, 3 months, etc.

### ✅ Step-by-Step Example:

Assume you have a `users` table and a `logins` table.

Step 1: Assign a cohort based on signup month

```sql
WITH user_cohort AS (
 SELECT 
 user_id,
 DATE_TRUNC(
 FROM users
)
```
Step 2: Calculate how many months since signup

, login_activity AS (

```sql
SELECT 
 l.user_id,
 DATE_TRUNC(
 FROM logins l
)
```
Step 3: Combine the two and calculate “month number”

, combined AS (

```sql
SELECT 
 uc.user_id,
 uc.cohort_month,
 la.login_month,
 DATE_DIFF(la.login_month, uc.cohort_month, MONTH) AS month_number
 FROM user_cohort uc
 JOIN login_activity la ON uc.user_id = la.user_id
)
```
Step 4: Count how many users came back in each month

```sql
SELECT 
 cohort_month,
 month_number,
 COUNT(DISTINCT user_id) AS active_users
FROM combined
GROUP BY cohort_month, month_number
ORDER BY cohort_month, month_number;
```
### **This gives you a full Cohort Table!**

You can now use this for:

*   Retention rate calculations
*   Visual heatmaps in dashboards
*   Marketing campaign performance tracking

### 🤖 Bonus: Google Colab + BigQuery Integration

If you want to analyze big data with Python + SQL:

1.   Use **Google BigQuery** to store your data.
2.   Connect it to **Google Colab** using the BigQuery magic commands:

from google.colab import auth

auth.authenticate_user()# Run SQL query using BigQuery

%load_ext google.cloud.bigquery

%%bigquery df

SELECT * FROM `your_project.dataset.table` LIMIT 10
Now you can:

*   Run SQL
*   Analyze with pandas
*   Visualize in Python

Great for data science workflows and dashboards!

### 🧠 Summary

Concept What It Does Use Cases `ROW_NUMBER()` Assigns unique row numbers Ranking, pagination `RANK()` Ranks with gaps for ties Leaderboards, performance metrics `DENSE_RANK()` Ranks without skipping numbers Reporting ranks `LEAD()` Get value from next row Compare current vs future values `LAG()` Get value from previous row Compare current vs past `FIRST_VALUE()` Gets the first value in a partition Track first event Moving Avg Averages over past rows Smoothing time trends MoM Change Calculates percent change month-to-month Growth trends Cohort Analysis Tracks group behavior over time Retention, churn, loyalty

### ✅ Final Challenge: Practice These Concepts

1.   **Use**`ROW_NUMBER()` to find each customer’s first purchase.
2.   **Use**`LAG()` to calculate revenue change between orders.
3.   **Build a Cohort Table** for a signup + login dataset.
4.   **Plot a MoM trend** of sales using `LAG()` and `window functions`.
5.   **Use Colab + BigQuery** to combine Python and SQL together.
