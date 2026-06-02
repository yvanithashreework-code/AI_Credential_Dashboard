import streamlit as st
import pandas as pd

st.title("AI Credential Dashboard")

st.subheader("Raw Dataset")
raw = pd.read_csv("data/employee_records.csv")
st.dataframe(raw)

st.subheader("Cleaned Dataset")
clean = pd.read_csv("data/clean_employee_records.csv")
st.dataframe(clean)

# Load cleaned dataset
data = pd.read_csv("data/clean_employee_records.csv")

# Create department dropdown
departments = data["Department"].unique()
selected_dept = st.selectbox("Select Department", departments)

# Filter dataset
filtered_data = data[data["Department"] == selected_dept]
st.write(filtered_data)

# Create role dropdown
roles = data["Role"].unique()
selected_role = st.selectbox("Select Role", roles)

# Filter dataset by department and role
filtered_data = data[
    (data["Department"] == selected_dept) &
    (data["Role"] == selected_role)
]
st.write(filtered_data)
