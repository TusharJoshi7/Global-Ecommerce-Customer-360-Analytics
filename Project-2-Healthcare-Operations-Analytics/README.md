# 🏥 Healthcare Operational Analytics & Patient ER Wait-Time Intelligence
> **End-to-End Clinical Data Analytics Portfolio Project**: Emergency Department Wait-Time Optimization, 30-Day Readmission Risk Stratification, SQL Analytical Queries, and Interactive Executive Dashboard.

[![Python](https://img.shields.io/badge/Python-3.14%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Wrangling-150458?logo=pandas)](https://pandas.pydata.org/)
[![SQL](https://img.shields.io/badge/SQL-Advanced%20CTEs%20%26%20Window%20Functions-336791?logo=postgresql)](./sql/)
[![Dashboard](https://img.shields.io/badge/Dashboard-Interactive%20Chart.js-007acc?logo=chartdotjs)](./dashboard/index.html)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🚀 Executive Project Summary

This project delivers a **Healthcare Operations & Clinical Intelligence Platform** designed to solve critical hospital operational bottlenecks: **Emergency Department (ER) Overcrowding**, **Extended Wait Times**, **30-Day Hospital Readmission Penalties**, and **Resource Utilization**.

By analyzing **5,000+ patient admission records** across 7 major clinical departments, the automated pipeline identifies triage SLA breaches, evaluates Length of Stay (LOS) drivers, stratifies patient age-cohort readmission risks, and powers an interactive executive dashboard for hospital administrators.

### 💡 Core Objectives & Business Impact
1. **ER Wait Time Optimization**: Identify department bottlenecks and triage level SLA breaches (Level 1–5).
2. **30-Day Readmission Risk Drivers**: Pinpoint high-risk patient age brackets (Senior 65+) and clinical specialties to minimize hospital readmission financial penalties.
3. **Capacity & LOS Analytics**: Measure average Length of Stay (LOS) across departments to balance bed turnover.
4. **Data Analytics Engineering**: Deliver automated Python processing scripts, production SQL query suites (CTEs, Window Functions), and a glassmorphism Chart.js Web Dashboard.

---

## 📈 Key Metrics & Healthcare Highlights

| Metric | Business & Operational Value | Analytical Finding |
| :--- | :--- | :--- |
| **Total Admissions** | Patient Volume Throughput | **5,000** processed cases |
| **Avg ER Wait Time** | Emergency Efficiency Target | **44.8 Minutes** overall baseline |
| **Avg Length of Stay** | Inpatient Bed Turnover Rate | **3.84 Days** across all specialties |
| **30-Day Readmission Rate** | Quality Care & Penalty Metric | **14.2%** overall readmission rate |
| **Highest Risk Cohort** | Clinical Targeted Intervention | **Senior 65+** (21.8% readmission rate) |
| **Total Treatment Revenue** | Financial Billing Volume | **$21.4M+** total procedure billing |

---

## 🛠 Project Architecture

```
Project-2-Healthcare-Operations-Analytics/
│
├── README.md                           # Master Project Documentation
├── requirements.txt                    # Python Dependencies
│
├── data/                               # Dataset Storage
│   ├── raw_patient_admissions.csv      # Raw generated 5k admission records
│   ├── cleaned_patient_data.csv        # Cleaned dataset with age brackets
│   └── department_kpis.csv             # Department aggregated KPIs
│
├── notebooks/                          # Jupyter Notebooks
│   ├── 01_patient_demographics_eda.ipynb  # EDA, wait time distributions, triage boxplots
│   └── 02_readmission_and_los_analysis.ipynb # Heatmaps, 30d readmission risk models
│
├── sql/                                # Production SQL Query Suite
│   ├── 01_healthcare_schema.sql        # Table DDL, constraints & performance indexes
│   └── 02_healthcare_analytics.sql     # Window functions, CTEs, SLA breach analysis
│
├── dashboard/                          # Interactive Executive Web Dashboard
│   ├── index.html                      # Glassmorphism HTML5 Dashboard
│   ├── styles.css                      # Dark mode styling
│   ├── app.js                          # Dynamic Chart.js logic
│   └── data.json                       # Pipeline output payload
│
└── scripts/                            # Automation Pipeline
    ├── generate_healthcare_data.py     # Synthetic data generator
    ├── run_healthcare_analysis.py      # Main analytical processing engine
    └── create_healthcare_notebooks.py  # Jupyter notebook generator
```

---

## 💻 Production SQL Query Highlight

```sql
-- Emergency Department Triage SLA Breaches & Performance Ranking
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
```

---

## 🏃 Quickstart Guide

```bash
# Navigate to project directory
cd Project-2-Healthcare-Operations-Analytics

# Run data generator & analytical pipeline
python scripts/generate_healthcare_data.py
python scripts/run_healthcare_analysis.py

# Generate Jupyter Notebooks
python scripts/create_healthcare_notebooks.py

# Open interactive dashboard
# Open dashboard/index.html in your browser!
```

---

## 👤 Author & Contact

**Tushar Joshi**  
*Data Analyst & Analytics Engineer*  
- **GitHub**: [@TusharJoshi7](https://github.com/TusharJoshi7)  
- **Email**: joshitushar265@gmail.com  
