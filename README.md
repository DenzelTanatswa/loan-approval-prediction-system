# 🏦 Loan Approval Prediction System

A complete end-to-end Machine Learning project that predicts whether a loan application will be **Approved** or **Rejected** based on an applicant's financial profile. The project includes data analysis, machine learning model development, a Streamlit web application, and an interactive Power BI dashboard.

---

## 📌 Project Overview

Financial institutions process thousands of loan applications every day. This project demonstrates how Machine Learning can assist in evaluating loan applications by analyzing applicant information such as income, CIBIL score, assets, education, employment status, and loan amount.

The project was developed as part of my Data Analytics and Machine Learning portfolio.

---

## 🚀 Features

- 📊 Exploratory Data Analysis (EDA)
- 🤖 Machine Learning Model Training
- 🌲 Random Forest Classifier
- 🌐 Streamlit Web Application
- 📈 Interactive Power BI Dashboard
- 📥 Download Prediction Report (CSV)
- 📋 Applicant Summary
- 📊 Prediction Confidence Score

---
```

---

# 📊 Dataset Information

**Source:** Kaggle

The dataset contains **4,269 loan applications** with **13 features**.

### Features

| Feature | Description |
|----------|-------------|
| loan_id | Unique Loan ID |
| no_of_dependents | Number of Dependents |
| education | Graduate / Not Graduate |
| self_employed | Self Employed Status |
| income_annum | Annual Income |
| loan_amount | Requested Loan Amount |
| loan_term | Loan Duration |
| cibil_score | Applicant Credit Score |
| residential_assets_value | Residential Asset Value |
| commercial_assets_value | Commercial Asset Value |
| luxury_assets_value | Luxury Asset Value |
| bank_asset_value | Bank Asset Value |
| loan_status | Approved / Rejected |

---

# 📈 Exploratory Data Analysis

During EDA the following tasks were completed:

- Data inspection
- Missing value analysis
- Duplicate detection
- Distribution analysis
- Correlation analysis
- Loan approval trends
- Income analysis
- CIBIL score analysis
- Asset analysis

### Visualizations

- Loan Approval by Education
- CIBIL Score Distribution
- Income vs Loan Amount
- Correlation Heatmap
- CIBIL Score by Loan Status

---

# 🤖 Machine Learning

Three machine learning models were trained and evaluated.

| Model | Accuracy |
|---------|---------:|
| Logistic Regression | 79.86% |
| Decision Tree | 97.78% |
| Random Forest | **97.78%** ✅ |

The Random Forest Classifier was selected as the final production model.

---

# 📊 Model Performance

### Random Forest

**Accuracy**

```
97.78%
```

### Confusion Matrix

```
[[529   7]
 [ 12 306]]
```

### Classification Report

| Metric | Class 0 | Class 1 |
|----------|---------:|---------:|
| Precision | 0.98 | 0.98 |
| Recall | 0.99 | 0.96 |
| F1 Score | 0.98 | 0.97 |

---

# 🌐 Streamlit Application

The application allows users to:

- Enter applicant information
- Predict loan approval
- View prediction confidence
- Download prediction report
- Review applicant summary

### Technologies Used

- Streamlit
- Scikit-learn
- Pandas
- Plotly
- Joblib

---

# 📊 Power BI Dashboard

The Power BI dashboard provides business insights into the loan approval process.

### Dashboard Features

- Total Applications
- Approved Loans
- Rejected Loans
- Approval Rate
- Average Income
- Average CIBIL Score
- Loan Status Analysis
- Approval by Education
- Interactive Filters

---

# 📈 Key Insights

- Overall loan approval rate is **62.22%**.
- Applicants with higher CIBIL scores are significantly more likely to receive loan approval.
- Annual income has a strong positive relationship with loan amount.
- Graduates and non-graduates show similar approval trends in this dataset.
- Asset values positively correlate with higher loan amounts.

---

# 🛠 Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Plotly
- Scikit-learn
- Joblib
- Streamlit
- Power BI

---

# ▶️ Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/loan-approval-prediction-system.git
```

Navigate into the project

```bash
cd loan-approval-prediction-system
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the Streamlit application

```bash
streamlit run "Approval App/AppBuild.py"
```

---

# 👨‍💻 Author

**Denzel Chidzikwe**



---


**LinkedIn:** https://www.linkedin.com/in/denzel-chidzikwe-0a6965288/


---

# ⭐ If you found this project useful, please consider giving it a star!
