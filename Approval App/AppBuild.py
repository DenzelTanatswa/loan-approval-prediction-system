import streamlit as st
import pandas as pd
import joblib
model = joblib.load("C:\\Users\\denze\\OneDrive\\Desktop\\Project\\loan-approval-prediction-system\\loan-approval-prediction-system\\Models\\loan_approval_model.pkl")
encoder = joblib.load("C:\\Users\\denze\\OneDrive\\Desktop\\Project\\loan-approval-prediction-system\\loan-approval-prediction-system\\Models\\label_encoder.pkl")
st.title("🏦 Loan Approval Prediction System")

st.write("Enter the applicant details below.")
dependents = st.number_input("Number of Dependents", 
                             min_value=0,
                               max_value=10,
                                 value=0
                                 )

education = st.selectbox("Education",
                         ["Graduate", "Not Graduate"]
)