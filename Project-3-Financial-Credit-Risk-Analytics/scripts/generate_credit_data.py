import os
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_credit_dataset(num_records=6000, seed=42):
    random.seed(seed)
    np.random.seed(seed)
    
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2026, 6, 30)
    time_span_days = (end_date - start_date).days
    
    loan_grades = ['A', 'B', 'C', 'D', 'E']
    grade_weights = [0.25, 0.35, 0.22, 0.12, 0.06]
    
    purposes = ['Debt Consolidation', 'Credit Card Refinance', 'Home Improvement', 'Small Business', 'Major Purchase', 'Personal']
    purpose_weights = [0.45, 0.25, 0.12, 0.08, 0.06, 0.04]
    
    home_ownerships = ['MORTGAGE', 'RENT', 'OWN']
    home_weights = [0.48, 0.40, 0.12]
    
    data = []
    
    for i in range(1, num_records + 1):
        loan_id = f"LN-{20000 + i}"
        borrower_id = f"BW-{random.randint(10000, 30000)}"
        
        grade = np.random.choice(loan_grades, p=grade_weights)
        purpose = np.random.choice(purposes, p=purpose_weights)
        home = np.random.choice(home_ownerships, p=home_weights)
        
        emp_length = round(random.uniform(0.5, 12.0), 1)
        annual_income = int(np.random.choice(
            a=[random.randint(30000, 50000), random.randint(50001, 85000), random.randint(85001, 140000), random.randint(140001, 280000)],
            p=[0.30, 0.45, 0.18, 0.07]
        ))
        
        # Credit Score & Interest Rate based on Grade
        grade_params = {
            'A': {'rate': (5.5, 9.5), 'score': (740, 850), 'default_p': 0.03},
            'B': {'rate': (9.6, 13.5), 'score': (680, 739), 'default_p': 0.08},
            'C': {'rate': (13.6, 17.5), 'score': (630, 679), 'default_p': 0.15},
            'D': {'rate': (17.6, 22.0), 'score': (580, 629), 'default_p': 0.24},
            'E': {'rate': (22.1, 28.5), 'score': (520, 579), 'default_p': 0.38}
        }
        
        rate_min, rate_max = grade_params[grade]['rate']
        score_min, score_max = grade_params[grade]['score']
        
        interest_rate = round(random.uniform(rate_min, rate_max), 2)
        credit_score = random.randint(score_min, score_max)
        
        loan_amount = int(round(random.uniform(2500, 40000), -2))
        dti_ratio = round(random.uniform(5.0, 38.0), 2)
        
        issue_date = start_date + timedelta(days=random.randint(0, time_span_days))
        
        # Determine status
        def_prob = grade_params[grade]['default_p']
        if dti_ratio > 28.0: def_prob += 0.05
        if credit_score < 620: def_prob += 0.08
        
        rand_val = random.random()
        if rand_val < def_prob:
            loan_status = np.random.choice(['Charged Off', 'Late 31-120 Days', 'Late 16-30 Days'], p=[0.60, 0.25, 0.15])
        elif rand_val < def_prob + 0.05:
            loan_status = 'In Grace Period'
        else:
            loan_status = np.random.choice(['Fully Paid', 'Current'], p=[0.45, 0.55])
            
        # Recovery / Payments
        if loan_status == 'Fully Paid':
            principal_paid = loan_amount
            interest_paid = round(loan_amount * (interest_rate / 100) * 2.2, 2)
        elif loan_status == 'Current':
            pct = random.uniform(0.2, 0.8)
            principal_paid = round(loan_amount * pct, 2)
            interest_paid = round(principal_paid * (interest_rate / 100) * 1.1, 2)
        else:
            pct = random.uniform(0.05, 0.35)
            principal_paid = round(loan_amount * pct, 2)
            interest_paid = round(principal_paid * (interest_rate / 100) * 0.5, 2)
            
        delinquency_2yrs = random.randint(0, 4) if random.random() < 0.2 else 0
        
        data.append({
            'loan_id': loan_id,
            'borrower_id': borrower_id,
            'issue_date': issue_date.strftime('%Y-%m-%d'),
            'loan_amount': loan_amount,
            'interest_rate': interest_rate,
            'grade': grade,
            'employment_length_years': emp_length,
            'home_ownership': home,
            'annual_income': annual_income,
            'dti_ratio': dti_ratio,
            'credit_score': credit_score,
            'loan_purpose': purpose,
            'loan_status': loan_status,
            'total_principal_paid': principal_paid,
            'total_interest_paid': interest_paid,
            'delinquency_2yrs': delinquency_2yrs
        })
        
    df = pd.DataFrame(data)
    os.makedirs('Project-3-Financial-Credit-Risk-Analytics/data', exist_ok=True)
    raw_path = 'Project-3-Financial-Credit-Risk-Analytics/data/raw_loan_portfolio.csv'
    df.to_csv(raw_path, index=False)
    print(f"Credit dataset generated successfully: {len(df)} rows saved to '{raw_path}'")
    return df

if __name__ == '__main__':
    generate_credit_dataset()
