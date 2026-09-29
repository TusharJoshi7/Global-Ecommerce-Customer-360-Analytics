# 📊 Global E-Commerce & Customer 360 Analytics Platform
> **End-to-End Data Analytics Portfolio Project**: RFM Customer Segmentation, Cohort Retention Heatmaps, Advanced SQL Analytics, and Interactive Executive Dashboard.

[![Python](https://img.shields.io/badge/Python-3.14%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Wrangling-150458?logo=pandas)](https://pandas.pydata.org/)
[![SQL](https://img.shields.io/badge/SQL-Advanced%20CTEs%20%26%20Window%20Functions-336791?logo=postgresql)](./sql/)
[![Dashboard](https://img.shields.io/badge/Dashboard-Interactive%20Chart.js-007acc?logo=chartdotjs)](./dashboard/index.html)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🚀 Executive Project Summary

This project delivers a **360-degree Business & Customer Intelligence Solution** for an enterprise e-commerce platform operating across **4 global regions** (North America, Europe, Asia-Pacific, Latin America). 

By processing over **10,000 transaction records** spanning 2024 to 2026, the pipeline quantifies key business drivers, performs **RFM (Recency, Frequency, Monetary) Customer Persona Segmentation**, calculates **Month-by-Month Cohort Retention Matrices**, and provides an **Interactive Web Dashboard** for C-suite decision-making.

### 💡 Business Problem & Objectives
1. **Revenue Growth & Trajectory**: Track Monthly Recurring Revenue (MRR) and identify high-converting product categories.
2. **Customer Segmentation**: Group 1,200+ unique customers into actionable personas (*Champions, Loyal, At Risk, Cant Lose Them, Hibernating*) to drive targeted retention campaigns.
3. **Cohort Retention Analysis**: Calculate retention decay rates across customer signup cohorts over 24+ months.
4. **Data Analytics Engineering**: Provide reproducible Python automation pipelines, clean SQL queries (CTEs, Window Functions), and a lightweight executive dashboard.

---

## 📈 Key Metrics & Analytics Highlights

| Metric | Business Insight Value | Analytical Finding |
| :--- | :--- | :--- |
| **Total Gross Revenue** | Top-line Financial Performance | **$1.85M+** across 9,600+ completed orders |
| **Average Order Value (AOV)** | Basket Size / Cart Metric | **$193.50** per transaction |
| **Customer Lifetime Value (LTV)** | Customer Worth Baseline | **$1,540.00** average revenue per customer |
| **Top Performing Region** | Geographic Expansion Target | **North America** (40.2% total revenue share) |
| **Top Category** | Inventory & Merchandising Leader | **Electronics & Home & Living** (~62% revenue) |
| **At-Risk Customer Ratio** | Churn Prevention Target | **18.4%** of customer base flagged for re-engagement |

---

## 🛠 Project Architecture & File Directory

```
Global-Ecommerce-Customer-360-Analytics/
│
├── README.md                           # Master Project Documentation & Executive Summary
├── requirements.txt                    # Project Python Dependencies
│
├── data/                               # Dataset Storage
│   ├── raw_ecommerce_data.csv          # Raw generated 10k transaction records
│   ├── cleaned_ecommerce_data.csv      # Cleaned and feature-engineered dataset
│   └── rfm_segmented_customers.csv     # RFM scored customer profile dataset
│
├── notebooks/                          # Jupyter Notebooks for Deep Exploratory Analysis
│   ├── 01_data_cleaning_and_eda.ipynb  # Data cleaning, EDA, distributions, trend analysis
│   └── 02_rfm_and_cohort_analysis.ipynb# RFM quintile scoring & Cohort Retention Heatmap
│
├── sql/                                # Production SQL Analytics Query Suite
│   ├── 01_schema_setup.sql             # Table DDL, Constraints & Performance Indexes
│   └── 02_advanced_analytics_queries.sql # Window functions, CTEs, MoM growth & Cohorts
│
├── dashboard/                          # Standalone Interactive Executive Web Dashboard
│   ├── index.html                      # Glassmorphism HTML5 Dashboard Page
│   ├── styles.css                      # Modern Dark Mode CSS System
│   ├── app.js                          # Dynamic Chart.js visualizations & controllers
│   └── data.json                       # Pipeline exported metric payloads
│
└── scripts/                            # Python Pipeline Automation Scripts
    ├── generate_dataset.py             # Synthetic data generator script
    ├── run_analysis.py                 # Core analytical processing pipeline
    └── create_notebooks.py             # Jupyter notebook generator script
```

---

## 📊 Analytical Methodology

### 1. RFM Customer Persona Model
Customers are evaluated on a 1-5 scale across three dimensions:
- **Recency ($R$)**: Days elapsed since the last transaction ($R=5$ is most recent).
- **Frequency ($F$)**: Count of unique orders placed ($F=5$ is most frequent).
- **Monetary ($M$)**: Total net spending amount ($M=5$ is highest lifetime value).

```
Customer Personas = f(R, F, M)
├── Champions          : R >= 4, F >= 4, M >= 4  (VIP Tier - Focus on advocacy & early access)
├── Loyal Customers    : R >= 3, F >= 3          (Upsell premium bundles & loyalty rewards)
├── Potential Loyalists: R >= 3, F < 3, M >= 3   (Engage with personalized recommendations)
├── At Risk            : R <= 2, F >= 3          (Trigger win-back email sequences & discounts)
└── Cant Lose Them     : R <= 2, F <= 2, M >= 3  (High-value churn risk - VIP white-glove outreach)
```

### 2. Cohort Retention Decay Matrix
Cohorts are established by the customer's first purchase month ($Month_0$). Subsequent order activity is mapped to calculate retention rates:

$$\text{Retention Rate}_{c, i} = \left( \frac{\text{Active Customers in Month } i \text{ for Cohort } c}{\text{Initial Cohort Size } c} \right) \times 100$$

---

## 💻 SQL Query Highlights

### Example: Monthly Recurring Revenue (MRR) & MoM Growth via Window Functions
```sql
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
```

---

## 🖥 Live Interactive Web Dashboard

The project includes an **interactive dashboard** built with HTML5, CSS3, JavaScript, and Chart.js.

### Features:
- ⚡ **Real-Time Executive KPIs**: Revenue, Order Count, Unique Customers, AOV, LTV, and Churn Risk.
- 📈 **Dynamic Trajectory Line Chart**: Monthly revenue performance visualization.
- 🍩 **RFM Persona Breakdown**: Segment distribution pie chart.
- 🌍 **Regional & Category Revenue Breakdown**: Interactive Bar Charts.
- 📋 **High-Value Customer Directory**: Searchable VIP customer table.

To open the dashboard, simply open [`dashboard/index.html`](./dashboard/index.html) in any web browser!

---

## 🏃 Quickstart Guide

### Prerequisites
- Python 3.9+
- Git

### Installation & Execution
```bash
# 1. Clone the repository
git clone https://github.com/TusharJoshi7/Global-Ecommerce-Customer-360-Analytics.git
cd Global-Ecommerce-Customer-360-Analytics

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate raw data & run analytical pipeline
python scripts/generate_dataset.py
python scripts/run_analysis.py

# 4. Open the Interactive Dashboard
# Double-click or open dashboard/index.html in your browser
```

---

## 👤 Author & Contact

**Tushar Joshi**  
*Data Analyst & Analytics Engineer*  
- **GitHub**: [@TusharJoshi7](https://github.com/TusharJoshi7)  
- **Email**: tushar.joshi-tjyw@qyupe.eazystar.us  

---
*If you find this project valuable for your analysis or portfolio reference, feel free to ⭐ star the repository!*
