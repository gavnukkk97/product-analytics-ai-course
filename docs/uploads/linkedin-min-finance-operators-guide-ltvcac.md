---
title: "A Finance Operator's Guide to LTV/CAC"
source: https://www.linkedin.com/pulse/finance-operators-guide-ltvcac-elaine-min-mba-cfa
author: Elaine Min, MBA, CFA
modules: [M1.3]
downloaded: 2026-09-14
---

# A Finance Operator's Guide to LTV/CAC

*Автор: Elaine Min, MBA, CFA*  
*Источник: https://www.linkedin.com/pulse/finance-operators-guide-ltvcac-elaine-min-mba-cfa*

![A Finance Operator's Guide to LTV/CAC](https://media.licdn.com/dms/image/v2/D5612AQGrXnY37xqqUw/article-cover_image-shrink_720_1280/article-cover_image-shrink_720_1280/0/1679490868117?e=2147483647&v=beta&t=vZI9NS75DFosA8ZnwhD59Qhny_sT9wfNpP7uJK35sRg)

 

# A Finance Operator's Guide to LTV/CAC


[Elaine Min, MBA, CFA](https://cn.linkedin.com/in/elainemin)
![Elaine Min, MBA, CFA]()

### Elaine Min, MBA, CFA

Published Mar 22, 2023

[+ Follow](https://www.linkedin.com/signup/cold-join?session_redirect=%2Fpulse%2Ffinance-operators-guide-ltvcac-elaine-min-mba-cfa&trk=article-ssr-frontend-pulse_publisher-author-card)

People who have worked with me know that I am an enthusiastic evangelist of LTV/CAC. LTV/CAC is one of the most important profitability metrics. The key to drive profitability lies in moving this critical metric to the right place.

In the current macro-environment where fund raising is challenging for startups, very few investors are willing to fund “growth at all costs” and the emphasis on profitable growth is back into the limelight.

As a finance operator, I wrote this practical guide on how startups can estimate their customer LTV, track CAC and use the LTV/CAC framework to set their profitability strategy.

---

Follow [me](https://www.linkedin.com/in/elainemin/?trk=article-ssr-frontend-pulse_little-text-block) if you like reading about everything finance of startup and scaleup businesses.

If you like to read more, check out my previous article [here](https://www.linkedin.com/pulse/primer-key-saas-financial-metrics-non-finance-elaine-min-mba-cfa/?trk=article-ssr-frontend-pulse_little-text-block) on another critical financial metric in SaaS - Annual Recurring Revenue (ARR).

---

First things first, to set the context:

- What is LTV?

Customer LTV stands for Customer Lifetime Value. It is a critical metric used by businesses to estimate the total value that an average customer brings to the business over their lifetime as a customer. The most commonly used proxy for value is revenue. Revenue-based LTV estimates the total amount of revenue that a customer generates for the business over their lifetime as a customer.

(It is worth calling out upfront that revenue-based LTV might not be the most accurate picture of customer value compared with gross-profit-based LTV. Gross-profit-based LTV is a “truer” value proxy after netting the cost of servicing the customer. We will use revenue-based LTV for now as it is easier to understand and the difference is explained in this article in a later section.)

- What is CAC?

CAC stands for Customer Acquisition Cost. This metric tracks the cost associated with acquiring a new customer, usually sales and marketing expenses.

- Why is LTV/CAC an important ratio?

The ratio of LTV/CAC compares the value of an average customer with the cost associated with acquiring them. We would want the ratio to be at least greater than 1x because we don’t want to invest $1 to acquire a customer that is worth only 90 cents. Greater than 1x is not enough - industry standard of “good” economics typically requires 3x. LTV/CAC is a northstar profitability metric as it measures the ROI of the company’s customer acquisition and growth investments.

![No alt text provided for this image]()

Photo by Giorgio Trovato on Unsplash

---

Here starts the practical, step-by-step guide for finance practitioners:

Part 1: How to estimate LTV

There are two commonly-used ways of estimating LTV, each having pros and cons depending on the use case. I call them: 1) the “napkin math” method and 2) the operators’ method.

1️⃣ The “Napkin Math” method

LTV = Average Revenue Per Account (ARPA) \* estimated lifetime

ARPA is not a GAAP metric and there are many different ways to calculate it. I normally take the ARR or MRR of the most recent period and divide it by the customer count of that period.

Estimated lifetime can be approximated by 1/average churn rate. E.g. if the annual churn rate is 25%, estimated lifetime is 4 years (1/25%).  If you are further interested in why 1/churn rate is a good estimate of lifetime, refer to the illustrative example in the appendix section.

✅ Pros: Easy to do. You can do it on a napkin without a complex cohort analysis. Especially handy when customer cohort data is not available for early stage companies without good data infrastructure. VCs commonly use it to get a general sense of profitability when evaluating potential investment targets.

❌ Cons: Limited accuracy and limited insights for operators

- ARPA is a blended average revenue of all different customer cohorts of different ages. This does not have the insights in terms of how revenue per customer changes during the customer’s lifecycle, which is normally going up driven by upsells, seat expansions and price increases
- Using 1/churn rate to approximate average lifetime might not be accurate as it assumes a flat churn rate throughout the years and that is hardly the case in reality

In summary, even though the “Napkin Math” method is easy to do, it does not have a great deal of granularity and does not generate the operational level insights that operators need to inform their decision making.

2️⃣ The Operators’ Method

The operators’ method is based on customer cohort analysis. It breaks down LTV into two drivers: retention and MRR.

- First things first: how long is a customer’s “lifetime”?

Customer lifetime varies across different industries and companies depending on various factors such as the type of the product offering and the profile of the target customers. In SAAS, the most commonly used LTV time frame is 3-year or 5-year. The 3-year time frame is more often used than 5-year as 3-year is on the more conservative end. However, if the retention rate of the company is particularly strong, 5-year or an even longer timeframe can also be justifiable. (As a rule of thumb, you can use 1/churn rate in the “napkin math” method to determine what LTV timeframe to use.) However, I would be wary if I see a company using a very long time frame such as 10-year because things can change dramatically in tech and companies could be disrupted and become completely obsolete in 10 years.

- Next, what is a cohort analysis?

A cohort analysis groups customers according to the month when they first onboarded and analyzes the change in customer behavior such as retention and revenue generation over time as the cohort ages.

- Plot the average retention curve based on the cohort analysis

With customers grouped into monthly cohorts based on the month when they first onboarded, retention rate at different monthly tenures can be analyzed for each historical cohort.

For each cohort, determine how many customers are active in each of the months after onboarding until the most recent month and calculate retention rate.

Below is an illustrative table on cohort retention rates. Taking the Jan 2022 cohort (customers who onboarded in Jan 2022) as an example, let’s say the company acquired 100 customers in Jan 2022. Retention rate in month 0 (Jan 2022) was 100% because month 0 was the inception month for these 100 customers. When the cohort aged to month 3 (Apr 2022), there were 97 customers who stayed active and paying, which implies a M3 retention rate of 97%. When the cohort further aged to month 13 (Feb 2023, which is the latest closing month), there were 91 customers retained, which implies a M13 retention rate of 91%.

![No alt text provided for this image]()

While this illustrative example starts with the Jan 2022 cohort, I would recommend going back to look at all historical cohorts in the most recent ~3 years to have a good amount of data points. It is not necessarily helpful to go back too far though as retention trends in the most recent years are the most relevant for estimating LTV.

With retention rates of all historical cohorts of the past 3 years spread out, an average retention curve can be plotted. This retention curve can predict the retention behavior of the customers that the company acquires in the near future. When plotting the average retention rate, a great deal of adjustments and assumptions need to be made such as excluding outlier cohorts with steep discounting experiments that have been discontinued. It is usually safe to assume that retention rate flattens after certain periods (e.g. 2 years) as customers become quite loyal if they have stayed with the company for more than 2 years.

Below is an illustrative average retention curve plotted out to month 36 for a 3-year LTV estimate.

## Recommended by LinkedIn

[![Why Valley Ventures Invested in Stuut]()

Why Valley Ventures Invested in Stuut

Jeff Allen

1 year ago](https://www.linkedin.com/pulse/why-valley-ventures-invested-stuut-jeff-allen-qbanc)

[![The Key Ratios for VC Funding]()

The Key Ratios for VC Funding

Patrick Molyneux

1 year ago](https://www.linkedin.com/pulse/key-ratios-vc-funding-patrick-molyneux-qe47e)

[![The AI Cashflow Tool Your Business Doesn't Actually Need (And the One Thing You Do)]()

The AI Cashflow Tool Your Business Doesn't Actually…

Steve Price

7 months ago](https://www.linkedin.com/pulse/ai-cashflow-tool-your-business-doesnt-actually-need-one-steve-price-rlgle)

![No alt text provided for this image]()

- Plot the average MRR curve based on the cohort analysis

Similarly for each cohort, analyze the average revenue per retained customer in each of the months after onboarding until the most recent month and calculate average revenue / active customer. Similar to the retention curve, an average MRR curve can be plotted out to month 36 for a 3-year LTV estimate. Note that typically the MRR curve goes up as retained customers got upsold additional product modules, upgraded plans, added seats, etc.

![No alt text provided for this image]()

![No alt text provided for this image]()

- Multiplying the retention curve and MRR curve to get LTV

![No alt text provided for this image]()

You can get the LTV curve by multiplying the retention curve and MRR curve together. This curve also called the Net Retention Curve as it measures gross retention offset by upsell. In this example, the 3-year customer LTV is $4000 by summing up from M0 to M36.

✅ Pros:

- Accuracy
- Tons of operational insights around customer lifecycle

❌ Cons:

- Cohort analysis requires good customer data infrastructure, which might not be available at early-stage startups

Part 2: How to track CAC

Compared to LTV which is an estimate based on lots of assumptions, CAC is way more straight-forward as it is a factual metric. CAC are the costs associated with customer acquisition, which are typically sales and marketing costs. To get the full picture of all customer acquisition investments, fully-loaded CAC is often used which includes:

- Variable marketing costs including campaigns, paid marketing, brand marketing, content marketing, events, etc.
- People costs (salaries, benefits, commissions, bonuses) of the sales and marketing teams, as well as direct revenue supporting functions such as sales operations
- Other costs that support customer acquisition such as sales and marketing related software and tools

CAC / new customer = Fully-loaded CAC in a given period / # of new customers acquired in the same period

---

More context on how to use the LTV/CAC framework:

💡 Revenue-based LTV vs. gross-profit-based LTV - which one should be used?

Revenue-based LTV is a slightly inflated estimate because there are costs associated with having the customers onboard, such as hosting cost to have the customer on the server, one-time software implementation cost, customer support cost to answer additional cases, etc. These are the costs of servicing the customers and are typically included in the company’s COGS. Therefore gross profit is a more accurate measure for value as it is the net value after taking out costs of servicing.

Note that only variable costs are to be deducted here, i.e. the costs that only incur when the business actually has the customer. Fixed costs, such as the costs of the developers to write the software and corporate overhead (e.g. rent) should not be included because those costs are not related to customer acquisition and they will incur with or without acquiring the customers.

Special caution: I have seen some platform companies use GMV or other transaction volume metrics as the value proxy for customer LTV. This is a vastly overstated measurement as the transaction volume that the platform facilitates is not revenue going into the company’s pocket. The revenue take rate of a platform is usually quite thin, measured in single digit percentage points or even in bps.

![No alt text provided for this image]()

Photo by AbsolutVision on Unsplash

💡 Is LTV/CAC the higher the better?

An LTV/CAC ratio that is less than 1 signals that the business is selling $1 for 90 cents. An LTV/CAC ratio of 3 - 5x is generally considered good economics in SAAS. But this does not mean the ratio is the higher the better. A company with 10x LTV/CAC might seem stellar on the surface but in essence this reveals that the business is vastly under investing in customer acquisition. The business should invest more until the marginal return of additional investment diminishes so that the overall LTV/CAC ratio regresses to 3-5x in order to maximize growth potential.

💡 A blended LTV/CAC is pretty much useless. You always need segmented LTV/CAC

Let’s say you did all your work with the cohort analysis according to the Operators’ Method and you get an LTV/CAC ratio of 1.5x. Being less than 3x, does this mean that your company’s customer acquisition investment is not quite cost-effective and the GTM strategy is not scalable?

Not necessarily! The biggest myth here is that the 1.5x is a blended average of the entire customer base and we all know that not all customers are created equal. Different customer segments might have very different retention and MRR profile and hence very different LTV. You always need to do a segmented LTV estimate in order to have GTM strategies targeted to each segment. With segmentation you can identify low-LTV segments and set up guardrails around CAC investment into this segment. You can also identify high-LTV segments for the business to double down on acquisition investment.

---

Thanks for reading if you got this far! ❤️

Follow [me](https://www.linkedin.com/in/elainemin/?trk=article-ssr-frontend-pulse_little-text-block) to stay tuned to my next write-ups on how finance operators can practically use the LTV/CAC framework to set up key metrics for sales and marketing teams, influence business decisions, and drive profitability.

---

❓ Appendix - why 1/churn rate is a good proxy for lifetime

E.g. if the annual churn rate for a company is 25% and the company starts with 100 customers at the beginning of year 1, below is a waterfall table of customer count until the cohort completely churns off:

![No alt text provided for this image]()

As shown in the table, there are 75 customers who made it to the end of year 1, 56 made it to the end of year 2, 42 to the end of year 3, …

And if you take the average # of years weighted by the ending customer count who made it through that year (which represents the probability of a customer making it through that year), you get the probability-weighted expected lifetime of 4 years.

If you are as nerdy as me and interested in the exact math proof behind it, check out [this wiki page](https://en.wikipedia.org/wiki/Geometric_distribution?trk=article-ssr-frontend-pulse_little-text-block).

[#ltv](https://www.linkedin.com/feed/hashtag/ltv?trk=article-ssr-frontend-pulse_little-text-block) [#cac](https://www.linkedin.com/feed/hashtag/cac?trk=article-ssr-frontend-pulse_little-text-block) [#saas](https://www.linkedin.com/feed/hashtag/saas?trk=article-ssr-frontend-pulse_little-text-block) [#saasstartup](https://www.linkedin.com/feed/hashtag/saasstartup?trk=article-ssr-frontend-pulse_little-text-block) [#startupfinance](https://www.linkedin.com/feed/hashtag/startupfinance?trk=article-ssr-frontend-pulse_little-text-block) [#tech](https://www.linkedin.com/feed/hashtag/tech?trk=article-ssr-frontend-pulse_little-text-block) [#profitability](https://www.linkedin.com/feed/hashtag/profitability?trk=article-ssr-frontend-pulse_little-text-block) [#profitablegrowth](https://www.linkedin.com/feed/hashtag/profitablegrowth?trk=article-ssr-frontend-pulse_little-text-block)
