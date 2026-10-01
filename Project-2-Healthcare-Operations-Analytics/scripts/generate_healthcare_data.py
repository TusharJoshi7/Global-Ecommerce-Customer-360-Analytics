import os
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_healthcare_dataset(num_records=5000, seed=42):
    random.seed(seed)
    np.random.seed(seed)
    
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2026, 6, 30)
    time_span_days = (end_date - start_date).days
    
    departments = ['Emergency', 'Cardiology', 'Orthopedics', 'Neurology', 'General Medicine', 'Pediatrics', 'Oncology']
    dept_weights = [0.35, 0.15, 0.15, 0.10, 0.15, 0.05, 0.05]
    
    admission_types = ['Emergency', 'Elective', 'Urgent']
    type_weights = [0.55, 0.30, 0.15]
    
    triage_levels = [1, 2, 3, 4, 5] # 1: Resuscitation (Critical), 5: Non-urgent
    triage_weights = [0.08, 0.22, 0.40, 0.20, 0.10]
    
    doctors = [f"DOC-{100 + i}" for i in range(1, 26)]
    insurance_providers = ['Medicare', 'Medicaid', 'BlueCross', 'Aetna', 'UnitedHealth', 'Self-Pay']
    insurance_weights = [0.30, 0.20, 0.22, 0.13, 0.10, 0.05]
    
    discharge_statuses = ['Discharged Home', 'Transferred', 'Referred to Rehab', 'Expired', 'AMA (Against Medical Advice)']
    discharge_weights = [0.82, 0.08, 0.06, 0.02, 0.02]

    data = []
    
    for i in range(1, num_records + 1):
        adm_id = f"ADM-{10000 + i}"
        patient_id = f"PAT-{random.randint(1000, 2500)}"
        age = int(np.random.choice(
            a=[random.randint(1, 17), random.randint(18, 45), random.randint(46, 70), random.randint(71, 92)],
            p=[0.08, 0.35, 0.37, 0.20]
        ))
        gender = random.choice(['Male', 'Female'])
        dept = np.random.choice(departments, p=dept_weights)
        adm_type = np.random.choice(admission_types, p=type_weights)
        triage = int(np.random.choice(triage_levels, p=triage_weights))
        
        adm_date = start_date + timedelta(days=random.randint(0, time_span_days), minutes=random.randint(0, 1439))
        
        # Calculate realistic wait time based on triage and dept
        base_wait = {1: 5, 2: 18, 3: 45, 4: 85, 5: 120}[triage]
        wait_time = max(2, int(np.random.exponential(scale=base_wait)))
        
        # Length of stay (days)
        if dept == 'Emergency' and triage >= 4:
            los_days = round(random.uniform(0.2, 1.5), 1)
        else:
            base_los = {1: 7.5, 2: 5.2, 3: 3.8, 4: 2.1, 5: 1.2}[triage]
            los_days = max(0.5, round(np.random.gamma(shape=2.0, scale=base_los / 2.0), 1))
            
        discharge_date = adm_date + timedelta(days=los_days)
        
        # Treatment Cost calculation
        daily_rate = {'Cardiology': 2800, 'Neurology': 2600, 'Orthopedics': 2400, 'Emergency': 1900, 'Oncology': 3100, 'General Medicine': 1500, 'Pediatrics': 1600}[dept]
        procedure_cost = random.randint(500, 8500) if random.random() > 0.4 else 0
        total_cost = round((los_days * daily_rate) + procedure_cost + (wait_time * 2.5), 2)
        
        # Readmission probability increases with age, certain departments, shorter initial LOS, and triage priority
        readmit_prob = 0.08
        if age > 65: readmit_prob += 0.07
        if triage <= 2: readmit_prob += 0.08
        if dept in ['Cardiology', 'Neurology']: readmit_prob += 0.06
        readmission_30d = 1 if (random.random() < readmit_prob) else 0
        
        insurance = np.random.choice(insurance_providers, p=insurance_weights)
        discharge_status = np.random.choice(discharge_statuses, p=discharge_weights)
        doctor_id = random.choice(doctors)
        
        data.append({
            'admission_id': adm_id,
            'patient_id': patient_id,
            'admission_date': adm_date.strftime('%Y-%m-%d %H:%M:%S'),
            'discharge_date': discharge_date.strftime('%Y-%m-%d %H:%M:%S'),
            'age': age,
            'gender': gender,
            'department': dept,
            'admission_type': adm_type,
            'triage_level': triage,
            'wait_time_minutes': wait_time,
            'length_of_stay_days': los_days,
            'readmission_30d': readmission_30d,
            'treatment_cost': total_cost,
            'insurance_provider': insurance,
            'discharge_status': discharge_status,
            'doctor_id': doctor_id
        })
        
    df = pd.DataFrame(data)
    os.makedirs('Project-2-Healthcare-Operations-Analytics/data', exist_ok=True)
    raw_path = 'Project-2-Healthcare-Operations-Analytics/data/raw_patient_admissions.csv'
    df.to_csv(raw_path, index=False)
    print(f"Healthcare dataset generated successfully: {len(df)} rows saved to '{raw_path}'")
    return df

if __name__ == '__main__':
    generate_healthcare_dataset()
