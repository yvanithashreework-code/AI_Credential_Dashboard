import streamlit as st
import pandas as pd

st.title("AI Credential Dashboard")

st.subheader("Raw Dataset")
raw = pd.read_csv("data/employee_records.csv")
st.dataframe(raw)

st.subheader("Cleaned Dataset")
clean = pd.read_csv("data/clean_employee_records.csv")
st.dataframe(clean)
