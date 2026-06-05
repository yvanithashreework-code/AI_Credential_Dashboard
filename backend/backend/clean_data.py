import pandas as pd

file_in = "data/employee_records.csv"
file_out = "data/clean_employee_records.csv"

# Read raw dataset
df = pd.read_csv(file_in)

# Cleaning steps
df = df.dropna()
df["Role"] = df["Role"].str.strip().str.title()
df["Department"] = df["Department"].str.strip().str.title()

# Convert JoiningDate to datetime
df["JoiningDate"] = pd.to_datetime(df["JoiningDate"], errors="coerce", dayfirst=True)

# Save cleaned dataset
df.to_csv(file_out, index=False)
print("Cleaned dataset saved to", file_out)
