##-------------PAGE SETUP --------------##
import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="AI Credential Dashboard", layout="wide")
st.title("AI Credential Dashboard")

# Load datasets
st.subheader("Raw Dataset")
raw = pd.read_csv("data/employee_records.csv")
st.dataframe(raw)

st.subheader("Cleaned Dataset")
clean = pd.read_csv("data/clean_employee_records.csv")
st.dataframe(clean)
