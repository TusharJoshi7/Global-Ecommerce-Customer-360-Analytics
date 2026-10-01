-- Advanced Healthcare Operations SQL Analytics Queries
-- Production-Grade Window Functions, CTEs, and Business Intelligence Metrics

-- ============================================================================
-- 1. Departmental Bottleneck Analysis: Avg Wait Time, LOS & Volume Ranking
-- ============================================================================
WITH dept_stats AS (
    SELECT 
        department,
        COUNT(admission_id) AS total_admissions,
        ROUND(AVG(wait_time_minutes), 1) AS avg_wait_min,
        ROUND(AVG(length_of_stay_days), 2) AS avg_los_days,
        ROUND(SUM(treatment_cost), 2) AS total_revenue
    FROM patient_admissions
    GROUP BY department
)
SELECT 
    department,
    total_admissions,
    avg_wait_min,
    avg_los_days,
    total_revenue,
    RANK() OVER (ORDER BY total_admissions DESC) AS volume_rank,
    RANK() OVER (ORDER BY avg_wait_min DESC) AS wait_time_rank
FROM dept_stats
ORDER BY total_admissions DESC;


-- ============================================================================
-- 2. Emergency Department Triage Bottleneck & Service Level Agreement (SLA) Violations
--    (SLA Target: Triage 1 <= 10m, Triage 2 <= 20m, Triage 3 <= 45m)
-- ============================================================================
WITH triage_sla AS (
    SELECT 
        admission_id,
        department,
        triage_level,
        wait_time_minutes,
        CASE 
            WHEN triage_level = 1 AND wait_time_minutes > 10 THEN 1
            WHEN triage_level = 2 AND wait_time_minutes > 20 THEN 1
            WHEN triage_level = 3 AND wait_time_minutes > 45 THEN 1
            ELSE 0
        END AS sla_breached
    FROM patient_admissions
    WHERE department = 'Emergency'
)
SELECT 
    triage_level,
    COUNT(admission_id) AS total_cases,
    SUM(sla_breached) AS sla_breaches,
    ROUND((SUM(sla_breached)::NUMERIC / COUNT(admission_id)) * 100, 2) AS breach_rate_pct,
    ROUND(AVG(wait_time_minutes), 1) AS avg_wait_minutes
FROM triage_sla
GROUP BY triage_level
ORDER BY triage_level;


-- ============================================================================
-- 3. 30-Day Readmission Risk Stratification by Age Group & High-Risk Departments
-- ============================================================================
WITH age_bracket_data AS (
    SELECT 
        admission_id,
        department,
        readmission_30d,
        CASE 
            WHEN age < 18 THEN '0-17 Pediatric'
            WHEN age BETWEEN 18 AND 49 THEN '18-49 Adult'
            WHEN age BETWEEN 50 AND 64 THEN '50-64 Middle-Aged'
            ELSE '65+ Senior'
        END AS age_group
    FROM patient_admissions
)
SELECT 
    age_group,
    department,
    COUNT(admission_id) AS total_admissions,
    SUM(readmission_30d) AS readmitted_patients,
    ROUND((SUM(readmission_30d)::NUMERIC / COUNT(admission_id)) * 100, 2) AS readmission_rate_pct,
    DENSE_RANK() OVER (PARTITION BY age_group ORDER BY (SUM(readmission_30d)::NUMERIC / COUNT(admission_id)) DESC) AS risk_rank_within_age
FROM age_bracket_data
GROUP BY age_group, department
ORDER BY age_group, readmission_rate_pct DESC;


-- ============================================================================
-- 4. Monthly Patient Volume & Rolling 3-Month Average Growth Rate
-- ============================================================================
WITH monthly_volume AS (
    SELECT 
        TO_CHAR(admission_date, 'YYYY-MM') AS year_month,
        COUNT(admission_id) AS monthly_admissions,
        ROUND(SUM(treatment_cost), 2) AS monthly_cost
    FROM patient_admissions
    GROUP BY 1
)
SELECT 
    year_month,
    monthly_admissions,
    ROUND(AVG(monthly_admissions) OVER (
        ORDER BY year_month 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 1) AS rolling_3m_avg_admissions,
    monthly_cost,
    LAG(monthly_cost, 1) OVER (ORDER BY year_month) AS prev_month_cost,
    ROUND(
        ((monthly_cost - LAG(monthly_cost, 1) OVER (ORDER BY year_month)) / 
        NULLIF(LAG(monthly_cost, 1) OVER (ORDER BY year_month), 0)) * 100, 2
    ) AS mom_revenue_growth_pct
FROM monthly_volume
ORDER BY year_month;
