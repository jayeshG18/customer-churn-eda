import sqlite3
import warnings
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

warnings.filterwarnings('ignore')

# Set professional theme for visuals
sns.set_theme(style='whitegrid', palette='muted')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'

print('==================================================')
print('Starting Customer Churn EDA & SQL Analysis...')
print('==================================================\n')

# 1. Load Dataset from Stable Open Source Repository
DATA_URL = 'https://raw.githubusercontent.com/treselle-systems/customer_churn_analysis/master/WA_Fn-UseC_-Telco-Customer-Churn.csv'

try:
  df = pd.read_csv(DATA_URL)
  print(f'[SUCCESS] Dataset loaded! Shape: {df.shape[0]} rows, {df.shape[1]} columns')
except Exception as e:
  print(f'[ERROR] Failed to load dataset: {e}')
  exit()

# 2. Data Preprocessing & Cleaning
print('\n--- Step 1: Data Cleaning & Transformation ---')

# Handling 'TotalCharges' string space issue
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'].str.strip(), errors='coerce')
df['TotalCharges'].fillna(df['TotalCharges'].median(), inplace=True)

# Encode Churn to Binary for analytical operations
df['Churn_Numeric'] = df['Churn'].apply(lambda x: 1 if x == 'Yes' else 0)

print('Missing values handled successfully.')
print(f'Total Null Values Remaining: {df.isnull().sum().sum()}')

# 3. Load Data into SQLite Engine for In-Memory SQL Queries
print('\n--- Step 2: Executing Embedded SQL Queries ---')

conn = sqlite3.connect(':memory:')
df.to_sql('customer_churn', conn, index=False, if_exists='replace')

# Query 1: Overall Churn Rate & Revenue Loss
query_1 = """
SELECT 
    COUNT(*) AS total_customers,
    SUM(Churn_Numeric) AS churned_customers,
    ROUND(AVG(Churn_Numeric) * 100, 2) AS churn_rate_percentage,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN MonthlyCharges ELSE 0 END), 2) AS monthly_revenue_at_risk
FROM customer_churn;
"""
res_1 = pd.read_sql_query(query_1, conn)
print('\n[SQL Result 1] Overall Churn Summary:')
print(res_1.to_string(index=False))

# Query 2: Churn by Contract Type & Avg Monthly Charges
query_2 = """
SELECT 
    Contract,
    COUNT(*) AS total_users,
    SUM(Churn_Numeric) AS churned_users,
    ROUND(AVG(Churn_Numeric) * 100, 2) AS churn_rate_pct,
    ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charge
FROM customer_churn
GROUP BY Contract
ORDER BY churn_rate_pct DESC;
"""
res_2 = pd.read_sql_query(query_2, conn)
print('\n[SQL Result 2] Churn breakdown by Contract Type:')
print(res_2.to_string(index=False))

# Query 3: High Risk Payment Methods
query_3 = """
SELECT 
    PaymentMethod,
    COUNT(*) AS total_users,
    ROUND(AVG(Churn_Numeric) * 100, 2) AS churn_rate_pct
FROM customer_churn
GROUP BY PaymentMethod
ORDER BY churn_rate_pct DESC;
"""
res_3 = pd.read_sql_query(query_3, conn)
print('\n[SQL Result 3] Churn by Payment Method:')
print(res_3.to_string(index=False))

# 4. Data Visualizations (Seaborn & Matplotlib)
print('\n--- Step 3: Generating Visualizations ---')

fig, axes = plt.subplots(2, 2, figsize=(15, 11))

# Plot 1: Overall Churn Distribution
sns.countplot(
    x='Churn',
    data=df,
    ax=axes[0, 0],
    palette=['#2ecc71', '#e74c3c']
)
axes[0, 0].set_title('Overall Customer Churn Count', fontsize=12, fontweight='bold')
axes[0, 0].set_xlabel('Customer Status')
axes[0, 0].set_ylabel('Customer Count')

# Plot 2: Churn by Contract Type
sns.countplot(
    x='Contract',
    hue='Churn',
    data=df,
    ax=axes[0, 1],
    palette=['#2ecc71', '#e74c3c']
)
axes[0, 1].set_title('Churn Rate by Contract Type', fontsize=12, fontweight='bold')
axes[0, 1].set_xlabel('Contract Type')
axes[0, 1].set_ylabel('Customer Count')

# Plot 3: Monthly Charges vs Churn (KDE)
sns.kdeplot(
    data=df,
    x='MonthlyCharges',
    hue='Churn',
    fill=True,
    ax=axes[1, 0],
    palette=['#2ecc71', '#e74c3c'],
    common_norm=False
)
axes[1, 0].set_title('Monthly Charges Distribution by Churn Status', fontsize=12, fontweight='bold')
axes[1, 0].set_xlabel('Monthly Charges ($)')

# Plot 4: Tenure vs Churn Boxplot
sns.boxplot(
    x='Churn',
    y='tenure',
    data=df,
    ax=axes[1, 1],
    palette=['#2ecc71', '#e74c3c']
)
axes[1, 1].set_title('Customer Tenure (Months) vs Churn Status', fontsize=12, fontweight='bold')
axes[1, 1].set_xlabel('Churn Status')
axes[1, 1].set_ylabel('Tenure (Months)')

plt.tight_layout()
plt.savefig('churn_analysis_grid.png', dpi=300)
print('[SUCCESS] Visualizations saved as "churn_analysis_grid.png".')

conn.close()
print('\n==================================================')
print('EDA Project Execution Completed Successfully!')
print('==================================================')