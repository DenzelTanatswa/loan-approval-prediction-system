import streamlit as st
import pandas as pd
import joblib 
model = joblib.load("models/loan_approval_model.pkl") 
encoder = joblib.load("models/label_encoder.pkl")
st.title("🏦 Loan Approval Prediction System")

st.write("Enter the applicant details below.")