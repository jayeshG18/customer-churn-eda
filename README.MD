# Customer Churn & Retention - Exploratory Data Analysis (EDA) with SQL & Python

A business-focused Exploratory Data Analysis (EDA) project analyzing telecom customer retention patterns, revenue loss drivers, and high-risk churn segments using Python and embedded SQL.

---

## 🚀 Executive Summary & Key Business Findings
Customer retention is critical for subscription-based business models. Through data cleaning, exploratory visual analysis, and SQL aggregations, this project answers key business questions:
1. **Contract Type Risk:** Customers on **Month-to-Month contracts** have the highest churn rate (~42%), whereas 2-year contract customers show less than 3% churn.
2. **Pricing Sensitivity:** Churned customers have a significantly higher **Average Monthly Charge ($74.44)** compared to retained customers ($61.26).
3. **Tenure Dynamics:** The first **12 months** represent the highest risk window for customer drop-off.
4. **Payment Method Friction:** Electronic check users exhibit the highest churn probability among all payment channels.

---

## 🛠️ Tech Stack & Tools
* **Language:** Python 3.x
* **Data Manipulation:** Pandas, NumPy
* **Database Engine:** SQLite (`sqlite3`)
* **Visualization:** Seaborn, Matplotlib

---

## 📂 Repository Structure
```text
├── analysis.py              # Main script for Data Cleaning, SQL Querying & EDA
├── requirements.txt         # Project dependencies
├── churn_analysis_grid.png  # Generated high-res charts (Auto-saved)
└── README.md                # Project documentation