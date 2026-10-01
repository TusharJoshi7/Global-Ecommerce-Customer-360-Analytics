import os
import json
import pandas as pd
import numpy as np

def run_credit_pipeline():
    raw_path = 'Project-3-Financial-Credit-Risk-Analytics/data/raw_loan_portfolio.csv'
    cleaned_path = 'Project-3-Financial-Credit-Risk-Analytics/data/cleaned_loan_data.csv'
    risk_seg_path = 'Project-3-Financial-Credit-Risk-Analytics/data/credit_risk_segments.csv'
    dashboard_json_path = 'Project-3-Financial-Credit-Risk-Analytics/dashboard/data.json'
    
    if not os.path.exists(raw_path):
        from generate_credit_data import generate_credit_dataset
        generate_credit_dataset()
        
    df = pd.read_csv(raw_path)
    print(f"Loaded raw credit portfolio dataset: {len(df)} rows")
    
    # Feature Engineering
    df['issue_date'] = pd.to_datetime(df['issue_date'])
    df['issue_year_month'] = df['issue_date'].dt.to_period('M').astype(str)
    
    # Flag Default / High Risk
    df['is_default'] = df['loan_status'].apply(lambda s: 1 if s in ['Charged Off', 'Late 31-120 Days'] else 0)
    df['outstanding_balance'] = np.maximum(0, df['loan_amount'] - df['total_principal_paid'])
    
    # Credit Score Tier
    fico_bins = [300, 580, 640, 700, 750, 850]
    fico_labels = ['Poor (<580)', 'Fair (580-639)', 'Good (640-699)', 'Very Good (700-749)', 'Exceptional (750+)']
    df['credit_score_tier'] = pd.cut(df['credit_score'], bins=fico_bins, labels=fico_labels, right=False)
    
    # Risk Category Persona
    def categorize_risk(row):
        if row['is_default'] == 1:
            return 'Defaulted / Non-Performing'
        elif row['loan_status'] in ['Late 16-30 Days', 'In Grace Period']:
            return 'Watchlist / Early Delinquent'
        elif row['dti_ratio'] > 25.0 or row['credit_score'] < 620:
            return 'Elevated Risk'
        else:
            return 'Low Risk / Performing'
            
    df['risk_category'] = df.apply(categorize_risk, axis=1)
    
    df.to_csv(cleaned_path, index=False)
    print(f"Saved cleaned credit portfolio to '{cleaned_path}'")
    
    # Risk Segment Aggregates
    risk_summary = df.groupby('grade').agg(
        total_loans=('loan_id', 'count'),
        total_origination=('loan_amount', 'sum'),
        avg_interest_rate=('interest_rate', 'mean'),
        default_count=('is_default', 'sum'),
        default_rate_pct=('is_default', lambda x: round(x.mean() * 100, 2)),
        total_charged_off_amount=('outstanding_balance', lambda x: round(x[df.loc[x.index, 'is_default'] == 1].sum(), 2))
    ).reset_index().sort_values(by='grade')
    
    risk_summary.to_csv(risk_seg_path, index=False)
    print(f"Saved credit risk segment KPIs to '{risk_seg_path}'")
    
    # Prepare JSON Dashboard Payload
    total_funded = float(df['loan_amount'].sum())
    total_outstanding = float(df['outstanding_balance'].sum())
    overall_default_rate = float(round(df['is_default'].mean() * 100, 2))
    avg_interest = float(round(df['interest_rate'].mean(), 2))
    avg_fico = float(round(df['credit_score'].mean(), 1))
    
    # Vintage Monthly Trajectory
    vintage_trend = df.groupby('issue_year_month').agg(
        loan_volume=('loan_id', 'count'),
        total_disbursed=('loan_amount', 'sum'),
        default_rate=('is_default', lambda x: round(x.mean() * 100, 2))
    ).reset_index()
    
    # Grade Breakdown
    grade_dist = df.groupby('grade').agg(
        loans=('loan_id', 'count'),
        default_rate=('is_default', lambda x: round(x.mean() * 100, 2))
    ).to_dict(orient='index')
    
    # FICO Tier Breakdown
    fico_dist = df.groupby('credit_score_tier', observed=False).agg(
        loans=('loan_id', 'count'),
        default_rate=('is_default', lambda x: round(x.mean() * 100, 2))
    ).to_dict(orient='index')
    
    # Top 10 High Risk Loans
    high_risk_loans = df[df['is_default'] == 1].sort_values(by='loan_amount', ascending=False).head(10)[
        ['loan_id', 'borrower_id', 'grade', 'loan_amount', 'interest_rate', 'credit_score', 'dti_ratio', 'loan_status', 'outstanding_balance']
    ].to_dict(orient='records')
    
    payload = {
        'summary': {
            'total_funded_volume': total_funded,
            'total_outstanding_balance': total_outstanding,
            'overall_default_rate_pct': overall_default_rate,
            'avg_interest_rate_pct': avg_interest,
            'avg_fico_score': avg_fico
        },
        'vintage_trend': vintage_trend.to_dict(orient='records'),
        'grade_breakdown': grade_dist,
        'fico_breakdown': fico_dist,
        'high_risk_loans': high_risk_loans
    }
    
    os.makedirs(os.path.dirname(dashboard_json_path), exist_ok=True)
    with open(dashboard_json_path, 'w') as f:
        json.dump(payload, f, indent=2)
        
    print(f"Exported dashboard payload to '{dashboard_json_path}'")
    print("=== Financial Credit Risk Pipeline Completed Successfully! ===")

if __name__ == '__main__':
    run_credit_pipeline()
