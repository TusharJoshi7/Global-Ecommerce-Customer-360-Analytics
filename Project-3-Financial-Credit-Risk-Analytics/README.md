# 💳 Financial Credit Risk & Loan Portfolio Intelligence Platform
> **End-to-End FinTech Data Analytics Portfolio Project**: Loan Default Rate Prediction, FICO Tier Risk Stratification, Vintage Loss Cohort Analysis, Advanced SQL Queries, and Interactive Executive Dashboard.

[![Python](https://img.shields.io/badge/Python-3.14%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Wrangling-150458?logo=pandas)](https://pandas.pydata.org/)
[![SQL](https://img.shields.io/badge/SQL-Advanced%20CTEs%20%26%20Window%20Functions-336791?logo=postgresql)](./sql/)
[![Dashboard](https://img.shields.io/badge/Dashboard-Interactive%20Chart.js-007acc?logo=chartdotjs)](./dashboard/index.html)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🚀 Executive Project Summary

This project delivers a comprehensive **FinTech Credit Risk & Portfolio Intelligence Platform** built to model, quantify, and visualize credit default risk across a loan portfolio of **6,000+ borrower accounts** disbursed between 2024 and 2026.

By combining Python automated processing pipelines, PostgreSQL advanced CTEs and window functions, and a modern glassmorphism Chart.js dashboard, the platform enables financial analysts and chief risk officers (CROs) to evaluate **Loss Given Default (LGD)**, **FICO score rating curves**, **Debt-To-Income (DTI) sensitivity**, and **Vintage Cohort Defaults**.

---

## 📈 Key Portfolio & Risk Highlights

| Metric | Financial & Business Impact | Analytical Finding |
| :--- | :--- | :--- |
| **Total Disbursed Volume** | Portfolio Capital Exposure | **$124.5M+** in cumulative origination |
| **Outstanding Balance** | Principal Risk Exposure | **$46.2M** active balance |
| **Portfolio Default Rate** | Credit Quality Baseline | **11.4%** across all risk grades |
| **Avg Weighted Interest Rate** | Portfolio Risk Yield | **13.8%** APR |
| **Avg FICO Score** | Credit Score Baseline | **684** average score |
| **Highest Risk Grade** | Loss Concentration | **Grade E** (38.2% default rate) |

---

## 🛠 Project Architecture

```
Project-3-Financial-Credit-Risk-Analytics/
│
├── README.md                           # Master Project Documentation
├── requirements.txt                    # Python Dependencies
│
├── data/                               # Dataset Storage
│   ├── raw_loan_portfolio.csv          # Raw generated 6k loan records
│   ├── cleaned_loan_data.csv           # Cleaned dataset with risk tags
│   └── credit_risk_segments.csv        # Credit grade KPI aggregation
│
├── notebooks/                          # Jupyter Notebooks
│   ├── 01_loan_portfolio_eda.ipynb     # EDA, interest rate vs volume, FICO boxplots
│   └── 02_vintage_loss_and_default_model.ipynb # Default rate matrix heatmaps & loss curves
│
├── sql/                                # Production SQL Query Suite
│   ├── 01_credit_risk_schema.sql       # Table DDL, constraints & performance indexes
│   └── 02_credit_risk_analytics.sql    # Window functions, CTEs, cumulative vintage defaults
│
├── dashboard/                          # Interactive Executive Web Dashboard
│   ├── index.html                      # Glassmorphism HTML5 Dashboard
│   ├── styles.css                      # Dark mode styling
│   ├── app.js                          # Dynamic Chart.js logic
│   └── data.json                       # Pipeline output payload
│
└── scripts/                            # Automation Pipeline
    ├── generate_credit_data.py         # Synthetic dataset generator
    ├── run_credit_analysis.py          # Main analytical processing engine
    └── create_credit_notebooks.py      # Jupyter notebook generator
```

---

## 💻 Production SQL Query Highlight

```sql
-- Monthly Vintage Portfolio Growth & Cumulative Default Exposure
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
```

---

## 🏃 Quickstart Guide

```bash
# Navigate to project directory
cd Project-3-Financial-Credit-Risk-Analytics

# Run data generator & analytical pipeline
python scripts/generate_credit_data.py
python scripts/run_credit_analysis.py

# Generate Jupyter Notebooks
python scripts/create_credit_notebooks.py

# Open interactive dashboard
# Open dashboard/index.html in your browser!
```

---

## 👤 Author & Contact

**Tushar Joshi**  
*Data Analyst & Analytics Engineer*  
- **GitHub**: [@TusharJoshi7](https://github.com/TusharJoshi7)  
- **Email**: joshitushar265@gmail.com  
