import os
import json
import pandas as pd
import numpy as np

def run_healthcare_pipeline():
    raw_path = 'Project-2-Healthcare-Operations-Analytics/data/raw_patient_admissions.csv'
    cleaned_path = 'Project-2-Healthcare-Operations-Analytics/data/cleaned_patient_data.csv'
    kpi_path = 'Project-2-Healthcare-Operations-Analytics/data/department_kpis.csv'
    dashboard_json_path = 'Project-2-Healthcare-Operations-Analytics/dashboard/data.json'
    
    if not os.path.exists(raw_path):
        from generate_healthcare_data import generate_healthcare_dataset
        generate_healthcare_dataset()
        
    df = pd.read_csv(raw_path)
    print(f"Loaded raw healthcare dataset: {len(df)} rows")
    
    # Cleaning & Validation
    df['admission_date'] = pd.to_datetime(df['admission_date'])
    df['discharge_date'] = pd.to_datetime(df['discharge_date'])
    df['year_month'] = df['admission_date'].dt.to_period('M').astype(str)
    
    # Age Brackets
    bins = [0, 18, 35, 50, 65, 100]
    labels = ['Pediatric (0-17)', 'Young Adult (18-34)', 'Adult (35-49)', 'Middle Aged (50-64)', 'Senior (65+)']
    df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)
    
    df.to_csv(cleaned_path, index=False)
    print(f"Saved cleaned dataset to '{cleaned_path}'")
    
    # Department KPIs
    dept_kpis = df.groupby('department').agg(
        total_admissions=('admission_id', 'count'),
        avg_wait_time_min=('wait_time_minutes', lambda x: round(x.mean(), 1)),
        avg_length_of_stay_days=('length_of_stay_days', lambda x: round(x.mean(), 2)),
        readmission_rate_pct=('readmission_30d', lambda x: round(x.mean() * 100, 2)),
        avg_treatment_cost=('treatment_cost', lambda x: round(x.mean(), 2)),
        total_revenue=('treatment_cost', lambda x: round(x.sum(), 2))
    ).reset_index().sort_values(by='total_admissions', ascending=False)
    
    dept_kpis.to_csv(kpi_path, index=False)
    print(f"Saved department KPIs to '{kpi_path}'")
    
    # Dashboard JSON Construction
    total_patients = int(len(df))
    avg_wait = float(round(df['wait_time_minutes'].mean(), 1))
    avg_los = float(round(df['length_of_stay_days'].mean(), 2))
    readmission_rate = float(round(df['readmission_30d'].mean() * 100, 2))
    total_cost = float(round(df['treatment_cost'].sum(), 2))
    
    # Monthly Admissions Trend
    monthly_trend = df.groupby('year_month').agg(
        admissions=('admission_id', 'count'),
        avg_wait=('wait_time_minutes', 'mean')
    ).reset_index()
    monthly_trend['avg_wait'] = monthly_trend['avg_wait'].round(1)
    
    # Triage Distribution
    triage_counts = df['triage_level'].value_counts().sort_index().to_dict()
    triage_labels = {1: 'Level 1: Resuscitation', 2: 'Level 2: Emergent', 3: 'Level 3: Urgent', 4: 'Level 4: Less Urgent', 5: 'Level 5: Non-Urgent'}
    triage_dist = {triage_labels[k]: int(v) for k, v in triage_counts.items()}
    
    # Readmission by Age Group
    readmit_age = df.groupby('age_group', observed=False)['readmission_30d'].mean().mul(100).round(2).to_dict()
    
    # Top 10 High Cost Admissions
    top_cost = df.sort_values(by='treatment_cost', ascending=False).head(10)[
        ['patient_id', 'age', 'gender', 'department', 'triage_level', 'length_of_stay_days', 'treatment_cost', 'readmission_30d']
    ].to_dict(orient='records')
    
    payload = {
        'summary': {
            'total_admissions': total_patients,
            'avg_wait_time_min': avg_wait,
            'avg_length_of_stay_days': avg_los,
            'readmission_rate_pct': readmission_rate,
            'total_treatment_cost': total_cost
        },
        'monthly_trend': monthly_trend.to_dict(orient='records'),
        'department_kpis': dept_kpis.to_dict(orient='records'),
        'triage_distribution': triage_dist,
        'readmission_by_age': readmit_age,
        'top_cost_admissions': top_cost
    }
    
    os.makedirs(os.path.dirname(dashboard_json_path), exist_ok=True)
    with open(dashboard_json_path, 'w') as f:
        json.dump(payload, f, indent=2)
        
    print(f"Exported dashboard payload to '{dashboard_json_path}'")
    print("=== Healthcare Analytics Pipeline Completed Successfully! ===")

if __name__ == '__main__':
    run_healthcare_pipeline()
