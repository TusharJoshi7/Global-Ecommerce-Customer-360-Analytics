-- =====================================================================
-- Advanced Data Analytics SQL Suite (CTEs, Window Functions, RFM & Cohorts)
-- Author: Tushar Joshi | Data Analyst Portfolio
-- =====================================================================

-- ---------------------------------------------------------------------
-- QUERY 1: Monthly Recurring Revenue (MRR) & Month-over-Month (MoM) Growth Rate
-- ---------------------------------------------------------------------
WITH monthly_sales AS (
    SELECT 
        TO_CHAR(order_date, 'YYYY-MM') AS year_month,
        COUNT(DISTINCT order_id) AS total_orders,
        SUM(total_revenue) AS monthly_revenue
    FROM orders
    WHERE order_status != 'Cancelled'
    GROUP BY 1
)
SELECT 
    year_month,
    total_orders,
    ROUND(monthly_revenue, 2) AS monthly_revenue,
    ROUND(LAG(monthly_revenue, 1) OVER (ORDER BY year_month), 2) AS prev_month_revenue,
    ROUND(
        ((monthly_revenue - LAG(monthly_revenue, 1) OVER (ORDER BY year_month)) / 
        NULLIF(LAG(monthly_revenue, 1) OVER (ORDER BY year_month), 0)) * 100, 2
    ) AS mom_growth_pct
FROM monthly_sales
ORDER BY year_month;

-- ---------------------------------------------------------------------
-- QUERY 2: RFM Customer Scoring & Quartile Calculation (SQL Implementation)
-- ---------------------------------------------------------------------
WITH customer_rfm_raw AS (
    SELECT 
        customer_id,
        MAX(order_date) AS last_order_date,
        COUNT(DISTINCT order_id) AS frequency,
        SUM(total_revenue) AS monetary
    FROM orders
    WHERE order_status != 'Cancelled'
    GROUP BY customer_id
),
rfm_scores AS (
    SELECT 
        customer_id,
        (CURRENT_DATE - last_order_date::date) AS recency_days,
        frequency,
        monetary,
        NTILE(5) OVER (ORDER BY (CURRENT_DATE - last_order_date::date) DESC) AS r_score,
        NTILE(5) OVER (ORDER BY frequency ASC) AS f_score,
        NTILE(5) OVER (ORDER BY monetary ASC) AS m_score
    FROM customer_rfm_raw
)
SELECT 
    customer_id,
    recency_days,
    frequency,
    ROUND(monetary, 2) AS monetary,
    r_score,
    f_score,
    m_score,
    (r_score || f_score || m_score) AS rfm_combined,
    CASE 
        WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
        WHEN r_score >= 3 AND f_score >= 3 THEN 'Loyal Customers'
        WHEN r_score >= 3 AND f_score < 3 AND m_score >= 3 THEN 'Potential Loyalists'
        WHEN r_score <= 2 AND f_score >= 3 THEN 'At Risk'
        ELSE 'Lost / Hibernating'
    END AS customer_segment
FROM rfm_scores
ORDER BY monetary DESC;

-- ---------------------------------------------------------------------
-- QUERY 3: Top 3 Revenue-Generating Products per Region (DENSE_RANK)
-- ---------------------------------------------------------------------
WITH regional_product_sales AS (
    SELECT 
        c.region,
        p.product_name,
        p.category,
        SUM(o.total_revenue) AS total_revenue,
        COUNT(DISTINCT o.order_id) AS total_units_sold,
        DENSE_RANK() OVER (PARTITION BY c.region ORDER BY SUM(o.total_revenue) DESC) AS rank_in_region
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    JOIN products p ON o.product_id = p.product_id
    WHERE o.order_status != 'Cancelled'
    GROUP BY c.region, p.product_name, p.category
)
SELECT 
    region,
    rank_in_region,
    product_name,
    category,
    ROUND(total_revenue, 2) AS total_revenue,
    total_units_sold
FROM regional_product_sales
WHERE rank_in_region <= 3
ORDER BY region, rank_in_region;

-- ---------------------------------------------------------------------
-- QUERY 4: Customer Cohort Retention Rate SQL Matrix
-- ---------------------------------------------------------------------
WITH customer_first_order AS (
    SELECT 
        customer_id,
        TO_CHAR(MIN(order_date), 'YYYY-MM') AS cohort_month
    FROM orders
    WHERE order_status != 'Cancelled'
    GROUP BY customer_id
),
order_activity AS (
    SELECT 
        o.customer_id,
        f.cohort_month,
        TO_CHAR(o.order_date, 'YYYY-MM') AS order_month,
        (
            (EXTRACT(YEAR FROM o.order_date) - EXTRACT(YEAR FROM TO_DATE(f.cohort_month, 'YYYY-MM'))) * 12 +
            (EXTRACT(MONTH FROM o.order_date) - EXTRACT(MONTH FROM TO_DATE(f.cohort_month, 'YYYY-MM')))
        ) AS period_number
    FROM orders o
    JOIN customer_first_order f ON o.customer_id = f.customer_id
    WHERE o.order_status != 'Cancelled'
),
cohort_size AS (
    SELECT cohort_month, COUNT(DISTINCT customer_id) AS initial_customers
    FROM customer_first_order
    GROUP BY cohort_month
),
retention AS (
    SELECT 
        a.cohort_month,
        a.period_number,
        COUNT(DISTINCT a.customer_id) AS active_customers
    FROM order_activity a
    GROUP BY a.cohort_month, a.period_number
)
SELECT 
    r.cohort_month,
    cs.initial_customers,
    r.period_number AS months_after_signup,
    r.active_customers,
    ROUND((r.active_customers::numeric / cs.initial_customers) * 100, 2) AS retention_rate_pct
FROM retention r
JOIN cohort_size cs ON r.cohort_month = cs.cohort_month
ORDER BY r.cohort_month, r.period_number;
