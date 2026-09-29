import pandas as pd
import numpy as np
import json
import os
from datetime import datetime

def run_analytics_pipeline():
    print("=== Starting E-Commerce Analytics Pipeline ===")
    
    # 1. Load Raw Data
    raw_path = os.path.join("data", "raw_ecommerce_data.csv")
    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Raw dataset not found at {raw_path}")
        
    df = pd.read_csv(raw_path)
    print(f"Loaded raw dataset: {df.shape[0]} rows, {df.shape[1]} columns")

    # 2. Data Cleaning & Type Casting
    df["order_date"] = pd.to_datetime(df["order_date"])
    
    # Impute missing payment_method with 'Credit Card' (Mode)
    mode_payment = df["payment_method"].mode()[0]
    df["payment_method"] = df["payment_method"].fillna(mode_payment)
    
    # Filter out cancelled orders for revenue analysis, but keep track of net revenue
    df_completed = df[df["order_status"] != "Cancelled"].copy()
    
    # Add time features
    df_completed["year_month"] = df_completed["order_date"].dt.to_period("M").astype(str)
    df_completed["order_year"] = df_completed["order_date"].dt.year
    df_completed["order_quarter"] = df_completed["order_date"].dt.to_period("Q").astype(str)
    df_completed["day_of_week"] = df_completed["order_date"].dt.day_name()

    cleaned_path = os.path.join("data", "cleaned_ecommerce_data.csv")
    df_completed.to_csv(cleaned_path, index=False)
    print(f"Saved cleaned dataset to '{cleaned_path}' ({len(df_completed)} valid transactions)")

    # 3. RFM Analysis (Recency, Frequency, Monetary)
    snapshot_date = df_completed["order_date"].max() + pd.Timedelta(days=1)
    
    rfm = df_completed.groupby("customer_id").agg({
        "order_date": lambda x: (snapshot_date - x.max()).days, # Recency
        "order_id": "nunique",                                 # Frequency
        "total_revenue": "sum",                                # Monetary
        "region": "first"                                       # Customer Region
    }).reset_index()

    rfm.rename(columns={
        "order_date": "recency_days",
        "order_id": "frequency",
        "total_revenue": "monetary"
    }, inplace=True)

    # Calculate RFM Scores (1 to 5) using rank-based qcut to handle tie values smoothly
    rfm["R_Score"] = pd.qcut(rfm["recency_days"].rank(method='first', ascending=False), q=5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm["F_Score"] = pd.qcut(rfm["frequency"].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm["M_Score"] = pd.qcut(rfm["monetary"].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5]).astype(int)

    rfm["RFM_Score_Comb"] = rfm["R_Score"].astype(str) + rfm["F_Score"].astype(str) + rfm["M_Score"].astype(str)
    rfm["RFM_Score_Avg"] = ((rfm["R_Score"] + rfm["F_Score"] + rfm["M_Score"]) / 3.0).round(2)

    # Segment Classification Function
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

    rfm_path = os.path.join("data", "rfm_segmented_customers.csv")
    rfm.to_csv(rfm_path, index=False)
    print(f"Saved RFM customer segmentation to '{rfm_path}' ({len(rfm)} unique customers)")

    # 4. Cohort Retention Matrix Calculation
    df_completed["cohort_month"] = df_completed.groupby("customer_id")["order_date"].transform("min").dt.to_period("M").astype(str)
    df_completed["order_month"] = df_completed["order_date"].dt.to_period("M").astype(str)

    def get_month_index(df):
        cohort_yr = pd.to_datetime(df["cohort_month"]).dt.year
        cohort_mo = pd.to_datetime(df["cohort_month"]).dt.month
        order_yr = pd.to_datetime(df["order_month"]).dt.year
        order_mo = pd.to_datetime(df["order_month"]).dt.month
        return (order_yr - cohort_yr) * 12 + (order_mo - cohort_mo)

    df_completed["cohort_index"] = get_month_index(df_completed)

    cohort_group = df_completed.groupby(["cohort_month", "cohort_index"])["customer_id"].nunique().reset_index()
    cohort_pivot = cohort_group.pivot(index="cohort_month", columns="cohort_index", values="customer_id")
    cohort_size = cohort_pivot.iloc[:, 0]
    retention_matrix = cohort_pivot.divide(cohort_size, axis=0).round(4) * 100

    # 5. Export JSON summary data for Dashboard
    total_rev = float(df_completed["total_revenue"].sum())
    total_orders = int(len(df_completed))
    total_cust = int(rfm["customer_id"].nunique())
    aov = float(df_completed["total_revenue"].mean())
    avg_clv = float(rfm["monetary"].mean())
    churn_rate = float((rfm["Customer_Segment"].isin(["At Risk", "Lost / Hibernating"]).sum() / total_cust) * 100)

    # Monthly Trends
    monthly_rev = df_completed.groupby("year_month").agg(
        revenue=("total_revenue", "sum"),
        orders=("order_id", "nunique"),
        avg_order=("total_revenue", "mean")
    ).reset_index()
    monthly_rev["revenue"] = monthly_rev["revenue"].round(2)
    monthly_rev["avg_order"] = monthly_rev["avg_order"].round(2)
    monthly_rev_list = monthly_rev.to_dict(orient="records")

    # Segment Breakdown
    segment_counts = rfm["Customer_Segment"].value_counts().to_dict()

    # Regional Revenue
    region_rev = df_completed.groupby("region")["total_revenue"].sum().round(2).to_dict()

    # Category Revenue
    category_rev = df_completed.groupby("category")["total_revenue"].sum().round(2).to_dict()

    dashboard_data = {
        "kpis": {
            "total_revenue": round(total_rev, 2),
            "total_orders": total_orders,
            "total_customers": total_cust,
            "aov": round(aov, 2),
            "avg_clv": round(avg_clv, 2),
            "churn_rate_pct": round(churn_rate, 1)
        },
        "monthly_trends": monthly_rev_list,
        "customer_segments": segment_counts,
        "regional_revenue": region_rev,
        "category_revenue": category_rev,
        "top_customers": rfm.sort_values(by="monetary", ascending=False).head(10)[["customer_id", "region", "frequency", "monetary", "Customer_Segment"]].to_dict(orient="records")
    }

    os.makedirs("dashboard", exist_ok=True)
    json_path = os.path.join("dashboard", "data.json")
    with open(json_path, "w") as f:
        json.dump(dashboard_data, f, indent=2)

    print(f"Exported dashboard JSON data to '{json_path}'")
    print("=== Pipeline Execution Completed Successfully! ===")

if __name__ == "__main__":
    run_analytics_pipeline()
