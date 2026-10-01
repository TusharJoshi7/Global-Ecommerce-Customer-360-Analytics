import os
import nbformat as nbf

def build_notebook_1():
    nb = nbf.v4.new_notebook()
    
    nb.cells.append(nbf.v4.new_markdown_cell("""# 💳 Notebook 01: Loan Portfolio & Credit Risk EDA
> **Project**: Financial Credit Risk & Loan Portfolio Intelligence Platform  
> **Author**: Tushar Joshi (Data Analyst & Analytics Engineer)

## 📌 Executive Summary
This notebook performs **Exploratory Data Analysis (EDA)** on 6,000+ loan portfolio records to analyze interest rate pricing sensitivity, FICO score distributions, Debt-To-Income (DTI) metrics, and loan status distributions.
"""))

    nb.cells.append(nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style='whitegrid', palette='mako')
plt.rcParams['figure.figsize'] = (10, 6)

df = pd.read_csv('../data/cleaned_loan_data.csv')
print(f"Loaded {len(df)} loan records.")
df.head()
"""))

    nb.cells.append(nbf.v4.new_markdown_cell("""## 📊 1. Loan Volume & Interest Rate by Credit Grade"""))

    nb.cells.append(nbf.v4.new_code_cell("""grade_stats = df.groupby('grade').agg(
    total_loans=('loan_id', 'count'),
    total_funded=('loan_amount', 'sum'),
    avg_rate=('interest_rate', 'mean'),
    avg_dti=('dti_ratio', 'mean')
).reset_index()

print(grade_stats)

fig, ax1 = plt.subplots(figsize=(10, 5))
sns.barplot(data=grade_stats, x='grade', y='total_funded', ax=ax1, palette='crest')
ax1.set_ylabel('Total Disbursed Volume ($)', color='teal')
ax1.set_title('Loan Origination Volume & Interest Rate by Risk Grade', fontsize=14, fontweight='bold')

ax2 = ax1.twinx()
sns.lineplot(data=grade_stats, x='grade', y='avg_rate', ax=ax2, color='crimson', marker='o', linewidth=2.5)
ax2.set_ylabel('Avg Interest Rate (%)', color='crimson')
plt.tight_layout()
plt.show()
"""))

    nb_path = 'Project-3-Financial-Credit-Risk-Analytics/notebooks/01_loan_portfolio_eda.ipynb'
    with open(nb_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f"Created notebook: {nb_path}")

def build_notebook_2():
    nb = nbf.v4.new_notebook()
    
    nb.cells.append(nbf.v4.new_markdown_cell("""# 📉 Notebook 02: Default Probability & Vintage Loss Cohort Analysis
> **Project**: Financial Credit Risk & Loan Portfolio Intelligence Platform  
> **Author**: Tushar Joshi (Data Analyst & Analytics Engineer)

## 📌 Objectives
1. Analyze **Default Decay & Loss Rates** across FICO score bands and DTI ratios.
2. Build a cohort matrix for **Vintage Loss Tracking (MoM)**.
3. Formulate risk mitigation recommendations for high-risk loan origination.
"""))

    nb.cells.append(nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('../data/cleaned_loan_data.csv')
print(f"Overall Portfolio Default Rate: {df['is_default'].mean()*100:.2f}%")
"""))

    nb.cells.append(nbf.v4.new_markdown_cell("""## 🎯 Default Rate Heatmap: Credit Grade vs FICO Tier"""))

    nb.cells.append(nbf.v4.new_code_cell("""pivot_default = df.pivot_table(
    index='grade',
    columns='credit_score_tier',
    values='is_default',
    aggfunc='mean'
) * 100

plt.figure(figsize=(11, 5))
sns.heatmap(pivot_default, annot=True, fmt='.1f', cmap='Reds', cbar_kws={'label': 'Default Rate %'})
plt.title('Default Rate Matrix (%): Risk Grade vs Credit Score Tier', fontsize=14, fontweight='bold')
plt.xlabel('FICO Score Tier')
plt.ylabel('Loan Grade')
plt.tight_layout()
plt.show()
"""))

    nb_path = 'Project-3-Financial-Credit-Risk-Analytics/notebooks/02_vintage_loss_and_default_model.ipynb'
    with open(nb_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f"Created notebook: {nb_path}")

if __name__ == '__main__':
    os.makedirs('Project-3-Financial-Credit-Risk-Analytics/notebooks', exist_ok=True)
    build_notebook_1()
    build_notebook_2()
