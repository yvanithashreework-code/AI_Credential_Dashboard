# Backend branch created

import pandas as pd

# ✅ Direct absolute path (safe for Windows)
file_in = "data/employee_records.csv"
file_out = "data/clean_employee_records.csv"

# ✅ Read raw dataset
df = pd.read_csv(file_in)

# ✅ Convert JoiningDate to datetime with dayfirst
df["JoiningDate"] = pd.to_datetime(df["JoiningDate"], errors="coerce", dayfirst=True)

# ✅ Standardize format to ISO (YYYY-MM-DD)
df["JoiningDate"] = df["JoiningDate"].dt.strftime("%Y-%m-%d")

# ✅ Save cleaned dataset
df.to_csv(file_out, index=False)

print("Cleaned dataset saved to:", file_out)
