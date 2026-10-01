import os
import nbformat as nbf

def build_notebook_1():
    nb = nbf.v4.new_notebook()
    
    nb.cells.append(nbf.v4.new_markdown_cell("""# 🏥 Notebook 01: Healthcare Operations & ER Wait-Time Analysis
> **Project**: Healthcare Operational Analytics & Patient ER Wait-Time Intelligence  
> **Author**: Tushar Joshi (Data Analyst & Analytics Engineer)

## 📌 Executive Summary
This notebook performs **Exploratory Data Analysis (EDA)** on 5,000+ hospital patient admission records to uncover bottleneck points in emergency wait times, patient age distribution, length of stay (LOS), and hospital cost drivers.
"""))

    nb.cells.append(nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set visual styling
sns.set_theme(style='whitegrid', palette='viridis')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 11

# Load cleaned dataset
df = pd.read_csv('../data/cleaned_patient_data.csv')
df['admission_date'] = pd.to_datetime(df['admission_date'])
print(f"Loaded {len(df)} patient records.")
df.head()
"""))

    nb.cells.append(nbf.v4.new_markdown_cell("""## 📊 1. Departmental Wait Times & Length of Stay (LOS)"""))

    nb.cells.append(nbf.v4.new_code_cell("""dept_summary = df.groupby('department').agg(
    total_patients=('admission_id', 'count'),
    avg_wait_min=('wait_time_minutes', 'mean'),
    median_wait_min=('wait_time_minutes', 'median'),
    avg_los_days=('length_of_stay_days', 'mean')
).reset_index().sort_values(by='avg_wait_min', ascending=False)

print(dept_summary)

plt.figure(figsize=(12, 5))
sns.barplot(data=dept_summary, x='department', y='avg_wait_min', palette='Blues_r')
plt.title('Average Wait Time (Minutes) by Hospital Department', fontsize=14, fontweight='bold')
plt.xlabel('Department')
plt.ylabel('Avg Wait Time (Min)')
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()
"""))

    nb.cells.append(nbf.v4.new_markdown_cell("""## 🚑 2. Emergency Triage Level Analysis"""))

    nb.cells.append(nbf.v4.new_code_cell("""plt.figure(figsize=(10, 5))
sns.boxplot(data=df, x='triage_level', y='wait_time_minutes', palette='Set2')
plt.title('Wait Time Distribution across Emergency Triage Levels', fontsize=14, fontweight='bold')
plt.xlabel('Triage Level (1: Resuscitation, 5: Non-Urgent)')
plt.ylabel('Wait Time (Minutes)')
plt.tight_layout()
plt.show()
"""))

    nb.cells.append(nbf.v4.new_markdown_cell("""## 💰 3. Financial Cost & Insurance Provider Breakdown"""))

    nb.cells.append(nbf.v4.new_code_cell("""insurance_stats = df.groupby('insurance_provider').agg(
    total_cost=('treatment_cost', 'sum'),
    avg_cost=('treatment_cost', 'mean'),
    patient_count=('admission_id', 'count')
).reset_index().sort_values(by='total_cost', ascending=False)

print(insurance_stats)
"""))

    nb_path = 'Project-2-Healthcare-Operations-Analytics/notebooks/01_patient_demographics_eda.ipynb'
    with open(nb_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f"Created notebook: {nb_path}")

def build_notebook_2():
    nb = nbf.v4.new_notebook()
    
    nb.cells.append(nbf.v4.new_markdown_cell("""# 🔁 Notebook 02: 30-Day Patient Readmission Drivers & Capacity Risk Model
> **Project**: Healthcare Operational Analytics & Patient ER Wait-Time Intelligence  
> **Author**: Tushar Joshi (Data Analyst & Analytics Engineer)

## 📌 Objectives
1. Identify clinical and demographic drivers behind **30-day hospital readmissions**.
2. Quantify readmission rates across age groups, triage levels, and discharge statuses.
3. Formulate recommendations for post-discharge care protocols to reduce readmission penalties.
"""))

    nb.cells.append(nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('../data/cleaned_patient_data.csv')
print(f"Overall 30-Day Readmission Rate: {df['readmission_30d'].mean()*100:.2f}%")
"""))

    nb.cells.append(nbf.v4.new_markdown_cell("""## 👴 1. Readmission Rate by Age Group & Department"""))

    nb.cells.append(nbf.v4.new_code_cell("""pivot_readmit = df.pivot_table(
    index='age_group',
    columns='department',
    values='readmission_30d',
    aggfunc='mean'
) * 100

plt.figure(figsize=(12, 6))
sns.heatmap(pivot_readmit, annot=True, fmt='.1f', cmap='YlOrRd', cbar_kws={'label': 'Readmission %'})
plt.title('30-Day Readmission Heatmap (%): Age Group vs Department', fontsize=14, fontweight='bold')
plt.xlabel('Department')
plt.ylabel('Age Group')
plt.tight_layout()
plt.show()
"""))

    nb_path = 'Project-2-Healthcare-Operations-Analytics/notebooks/02_readmission_and_los_analysis.ipynb'
    with open(nb_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f"Created notebook: {nb_path}")

if __name__ == '__main__':
    os.makedirs('Project-2-Healthcare-Operations-Analytics/notebooks', exist_ok=True)
    build_notebook_1()
    build_notebook_2()
