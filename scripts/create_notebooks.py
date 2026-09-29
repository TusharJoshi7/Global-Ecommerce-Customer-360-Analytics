import nbformat as nbf
import os

def create_eda_notebook():
    nb = nbf.v4.new_notebook()
    
    nb.cells = [
        nbf.v4.new_markdown_cell("""# 📊 E-Commerce Data Cleaning & Exploratory Data Analysis (EDA)
**Project**: Global E-Commerce & Customer 360 Analytics  
**Author**: Tushar Joshi | Data Analyst Portfolio  

---
### 📌 Notebook Objectives
1. Load raw e-commerce transaction data and perform initial data auditing.
2. Handle missing values, outliers, invalid order statuses, and data type casting.
3. Analyze key sales KPIs: Total Revenue, Average Order Value (AOV), Order Volume over time.
4. Explore regional performance, product category breakdown, and payment preferences.
5. Save the cleaned dataset for downstream RFM segmentation and cohort retention modeling.
"""),
        
        nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as io

# Configure visualization defaults
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["figure.figsize"] = (12, 6)
plt.rcParams["font.size"] = 10

print("Libraries imported successfully!")"""),

        nbf.v4.new_markdown_cell("## 1. Load Raw Data & Audit Schema"),
        nbf.v4.new_code_cell("""# Load raw dataset
df_raw = pd.read_csv("../data/raw_ecommerce_data.csv")
print(f"Dataset Shape: {df_raw.shape}")
df_raw.head()"""),

        nbf.v4.new_code_cell("""# Data info & missing value check
df_raw.info()
print("\\n--- Missing Values Count ---")
print(df_raw.isnull().sum())"""),

        nbf.v4.new_markdown_cell("## 2. Data Wrangling & Feature Engineering"),
        nbf.v4.new_code_cell("""df = df_raw.copy()

# Cast dates to datetime
df["order_date"] = pd.to_datetime(df["order_date"])

# Impute missing payment methods with Mode
mode_payment = df["payment_method"].mode()[0]
df["payment_method"] = df["payment_method"].fillna(mode_payment)

# Filter valid completed & returned orders for financial analysis
df_valid = df[df["order_status"] != "Cancelled"].copy()

# Temporal features
df_valid["year_month"] = df_valid["order_date"].dt.to_period("M").astype(str)
df_valid["order_year"] = df_valid["order_date"].dt.year
df_valid["day_name"] = df_valid["order_date"].dt.day_name()

print(f"Cleaned dataset records: {len(df_valid)} (Removed {len(df) - len(df_valid)} cancelled orders)")"""),

        nbf.v4.new_markdown_cell("## 3. Executive KPI Dashboard Summary"),
        nbf.v4.new_code_cell("""total_revenue = df_valid["total_revenue"].sum()
total_orders = df_valid["order_id"].nunique()
total_customers = df_valid["customer_id"].nunique()
aov = df_valid["total_revenue"].mean()

print(f"💰 Total Revenue:        ${total_revenue:,.2f}")
print(f"📦 Total Completed Orders: {total_orders:,}")
print(f"👥 Unique Customers:      {total_customers:,}")
print(f"🛒 Average Order Value:   ${aov:.2f}")"""),

        nbf.v4.new_markdown_cell("## 4. Sales Trends & Seasonality Analysis"),
        nbf.v4.new_code_cell("""monthly_trend = df_valid.groupby("year_month")["total_revenue"].sum().reset_index()

plt.figure(figsize=(14, 5))
sns.lineplot(data=monthly_trend, x="year_month", y="total_revenue", marker="o", color="#2563eb", linewidth=2.5)
plt.title("Monthly Revenue Trajectory (2024 - 2026)", fontsize=14, fontweight="bold", pad=15)
plt.xlabel("Year-Month")
plt.ylabel("Revenue ($)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()"""),

        nbf.v4.new_markdown_cell("## 5. Regional & Product Category Performance"),
        nbf.v4.new_code_cell("""fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Category Revenue
cat_rev = df_valid.groupby("category")["total_revenue"].sum().sort_values(ascending=False).reset_index()
sns.barplot(data=cat_rev, x="total_revenue", y="category", palette="Blues_r", ax=axes[0])
axes[0].set_title("Revenue by Product Category", fontsize=12, fontweight="bold")
axes[0].set_xlabel("Revenue ($)")

# Regional Distribution
reg_rev = df_valid.groupby("region")["total_revenue"].sum().sort_values(ascending=False).reset_index()
sns.barplot(data=reg_rev, x="region", y="total_revenue", palette="Greens_r", ax=axes[1])
axes[1].set_title("Revenue by Geographic Region", fontsize=12, fontweight="bold")
axes[1].set_ylabel("Revenue ($)")

plt.tight_layout()
plt.show()"""),

        nbf.v4.new_markdown_cell("## 6. Key Takeaways & Export"),
        nbf.v4.new_code_cell("""# Export clean data
os.makedirs("../data", exist_ok=True)
df_valid.to_csv("../data/cleaned_ecommerce_data.csv", index=False)
print("✅ EDA Complete. Cleaned data written to '../data/cleaned_ecommerce_data.csv'")""")
    ]

    os.makedirs("notebooks", exist_ok=True)
    with open("notebooks/01_data_cleaning_and_eda.ipynb", "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    print("Notebook 01 created.")

def create_rfm_notebook():
    nb = nbf.v4.new_notebook()

    nb.cells = [
        nbf.v4.new_markdown_cell("""# 🎯 Customer 360: RFM Segmentation & Cohort Retention Modeling
**Project**: Global E-Commerce Analytics  
**Author**: Tushar Joshi | Data Analyst Portfolio  

---
### 📌 Notebook Objectives
1. Calculate Recency, Frequency, and Monetary (RFM) metrics for every unique customer.
2. Assign quintile RFM scores (1-5) and segment customers into strategic personas (Champions, At Risk, Lost, etc.).
3. Build customer cohort groups based on initial signup month.
4. Generate a Month-by-Month Cohort Retention Heatmap matrix to evaluate retention decay.
5. Formulate actionable data-driven marketing & customer success strategies.
"""),

        nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans

sns.set_theme(style="white", palette="muted")
plt.rcParams["figure.figsize"] = (12, 6)

# Load cleaned dataset
df = pd.read_csv("../data/cleaned_ecommerce_data.csv")
df["order_date"] = pd.to_datetime(df["order_date"])
print(f"Loaded {len(df)} transactions.")"""),

        nbf.v4.new_markdown_cell("## 1. Recency, Frequency, & Monetary (RFM) Calculation"),
        nbf.v4.new_code_cell("""snapshot_date = df["order_date"].max() + pd.Timedelta(days=1)

rfm = df.groupby("customer_id").agg({
    "order_date": lambda x: (snapshot_date - x.max()).days,
    "order_id": "nunique",
    "total_revenue": "sum",
    "region": "first"
}).reset_index()

rfm.columns = ["customer_id", "recency_days", "frequency", "monetary", "region"]
rfm.head()"""),

        nbf.v4.new_markdown_cell("## 2. RFM Quintile Scoring & Segment Mapping"),
        nbf.v4.new_code_cell("""rfm["R_Score"] = pd.qcut(rfm["recency_days"].rank(method='first', ascending=False), q=5, labels=[1, 2, 3, 4, 5]).astype(int)
rfm["F_Score"] = pd.qcut(rfm["frequency"].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5]).astype(int)
rfm["M_Score"] = pd.qcut(rfm["monetary"].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5]).astype(int)

def assign_segment(row):
    r, f, m = row["R_Score"], row["F_Score"], row["M_Score"]
    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"
    elif r >= 3 and f >= 3:
        return "Loyal Customers"
    elif r >= 3 and f < 3 and m >= 3:
        return "Potential Loyalists"
    elif r >= 4 and f == 1:
        return "New Customers"
    elif r <= 2 and f >= 3:
        return "At Risk"
    elif r <= 2 and f <= 2 and m >= 3:
        return "Cant Lose Them"
    else:
        return "Lost / Hibernating"

rfm["Customer_Segment"] = rfm.apply(assign_segment, axis=1)

print("--- Customer Segment Distribution ---")
print(rfm["Customer_Segment"].value_counts())"""),

        nbf.v4.new_markdown_cell("## 3. Visualizing Customer Segments"),
        nbf.v4.new_code_cell("""plt.figure(figsize=(12, 6))
seg_counts = rfm["Customer_Segment"].value_counts().reset_index()
sns.barplot(data=seg_counts, x="count", y="Customer_Segment", palette="Spectral")
plt.title("Customer Distribution Across RFM Personas", fontsize=14, fontweight="bold")
plt.xlabel("Number of Customers")
plt.ylabel("Segment")
plt.tight_layout()
plt.show()"""),

        nbf.v4.new_markdown_cell("## 4. Cohort Retention Matrix Analysis"),
        nbf.v4.new_code_cell("""df["cohort_month"] = df.groupby("customer_id")["order_date"].transform("min").dt.to_period("M").astype(str)
df["order_month"] = df["order_date"].dt.to_period("M").astype(str)

def get_month_index(df):
    cohort_yr = pd.to_datetime(df["cohort_month"]).dt.year
    cohort_mo = pd.to_datetime(df["cohort_month"]).dt.month
    order_yr = pd.to_datetime(df["order_month"]).dt.year
    order_mo = pd.to_datetime(df["order_month"]).dt.month
    return (order_yr - cohort_yr) * 12 + (order_mo - cohort_mo)

df["cohort_index"] = get_month_index(df)

cohort_group = df.groupby(["cohort_month", "cohort_index"])["customer_id"].nunique().reset_index()
cohort_pivot = cohort_group.pivot(index="cohort_month", columns="cohort_index", values="customer_id")
cohort_size = cohort_pivot.iloc[:, 0]
retention_matrix = cohort_pivot.divide(cohort_size, axis=0).round(4) * 100

plt.figure(figsize=(16, 10))
sns.heatmap(retention_matrix, annot=True, fmt=".1f", cmap="YlGnBu", cbar_kws={'label': 'Retention Rate (%)'})
plt.title("Monthly Cohort Retention Heatmap (%)", fontsize=14, fontweight="bold", pad=15)
plt.xlabel("Months Since First Order")
plt.ylabel("Cohort Month")
plt.tight_layout()
plt.show()"""),

        nbf.v4.new_markdown_cell("## 5. Strategic Recommendations & Export"),
        nbf.v4.new_code_cell("""# Save RFM segmentation data
rfm.to_csv("../data/rfm_segmented_customers.csv", index=False)
print("✅ Segmentation exported to '../data/rfm_segmented_customers.csv'")""")
    ]

    with open("notebooks/02_rfm_and_cohort_analysis.ipynb", "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    print("Notebook 02 created.")

if __name__ == "__main__":
    create_eda_notebook()
    create_rfm_notebook()
