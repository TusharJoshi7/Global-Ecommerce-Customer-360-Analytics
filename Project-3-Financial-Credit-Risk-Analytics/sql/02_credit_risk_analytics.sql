-- Advanced Credit Risk & Loan Portfolio SQL Analytics Queries
-- Production Window Functions, Vintage CTEs, and Delinquency Analysis

-- ============================================================================
-- 1. Loan Portfolio Default Rate & Principal at Risk by Grade
-- ============================================================================
WITH grade_risk AS (
    SELECT 
        grade,
        COUNT(loan_id) AS total_loans,
        SUM(loan_amount) AS total_disbursed,
        ROUND(AVG(interest_rate), 2) AS avg_interest_rate,
        SUM(CASE WHEN loan_status IN ('Charged Off', 'Late 31-120 Days') THEN 1 ELSE 0 END) AS defaulted_loans,
        SUM(CASE WHEN loan_status IN ('Charged Off', 'Late 31-120 Days') THEN (loan_amount - total_principal_paid) ELSE 0 END) AS charged_off_principal
    FROM loan_portfolio
    GROUP BY grade
)
SELECT 
    grade,
    total_loans,
    ROUND(total_disbursed, 2) AS total_disbursed_usd,
    avg_interest_rate,
    defaulted_loans,
    ROUND((defaulted_loans::NUMERIC / total_loans) * 100, 2) AS default_rate_pct,
    ROUND(charged_off_principal, 2) AS principal_loss_usd,
    RANK() OVER (ORDER BY (defaulted_loans::NUMERIC / total_loans) DESC) AS risk_rank
FROM grade_risk
ORDER BY grade;


-- ============================================================================
-- 2. Credit Score (FICO) Band vs Default Loss Exposure
-- ============================================================================
WITH fico_brackets AS (
    SELECT 
        loan_id,
        loan_amount,
        total_principal_paid,
        loan_status,
        CASE 
            WHEN credit_score < 580 THEN '1. Poor (<580)'
            WHEN credit_score BETWEEN 580 AND 639 THEN '2. Fair (580-639)'
            WHEN credit_score BETWEEN 640 AND 699 THEN '3. Good (640-699)'
            WHEN credit_score BETWEEN 700 AND 749 THEN '4. Very Good (700-749)'
            ELSE '5. Exceptional (750+)'
        END AS fico_band
    FROM loan_portfolio
)
SELECT 
    fico_band,
    COUNT(loan_id) AS loan_count,
    ROUND(SUM(loan_amount), 2) AS total_originated,
    SUM(CASE WHEN loan_status IN ('Charged Off', 'Late 31-120 Days') THEN 1 ELSE 0 END) AS default_count,
    ROUND((SUM(CASE WHEN loan_status IN ('Charged Off', 'Late 31-120 Days') THEN 1 ELSE 0 END)::NUMERIC / COUNT(loan_id)) * 100, 2) AS default_pct
FROM fico_brackets
GROUP BY fico_band
ORDER BY fico_band;


-- ============================================================================
-- 3. Monthly Vintage Portfolio Growth & Cumulative Default Exposure
-- ============================================================================
WITH monthly_vintage AS (
    SELECT 
        TO_CHAR(issue_date, 'YYYY-MM') AS vintage_month,
        COUNT(loan_id) AS loans_issued,
        SUM(loan_amount) AS total_amount_issued,
        SUM(CASE WHEN loan_status = 'Charged Off' THEN 1 ELSE 0 END) AS charged_off_loans
    FROM loan_portfolio
    GROUP BY 1
)
SELECT 
    vintage_month,
    loans_issued,
    ROUND(total_amount_issued, 2) AS total_amount_issued,
    charged_off_loans,
    SUM(total_amount_issued) OVER (ORDER BY vintage_month) AS cumulative_portfolio_volume,
    ROUND(
        (charged_off_loans::NUMERIC / NULLIF(loans_issued, 0)) * 100, 2
    ) AS vintage_default_rate_pct
FROM monthly_vintage
ORDER BY vintage_month;
