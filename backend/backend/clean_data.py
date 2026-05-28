import pandas as pd

# Load raw dataset
df = pd.read_csv("../data/employee_records.csv")

# -----------------------------
# Fix Age
# -----------------------------
df['Age'] = df['Age'].replace("twenty four", 24)   # replace text with number
df['Age'] = pd.to_numeric(df['Age'], errors='coerce')  # convert to numeric, invalid → NaN
df['Age'].fillna(df['Age'].median(), inplace=True)     # fill missing with median

# -----------------------------
# Fix Department
# -----------------------------
df['Department'].fillna("Unknown", inplace=True)   # replace NaN with "Unknown"

# -----------------------------
# Fix Salary
# -----------------------------
df['Salary'] = pd.to_numeric(df['Salary'], errors='coerce')  # convert to numeric
df['Salary'].fillna(df['Salary'].mean(), inplace=True)       # fill missing with mean

# -----------------------------
# Fix JoiningDate
# -----------------------------
df['JoiningDate'] = pd.to_datetime(df['JoiningDate'], errors='coerce')  # convert to datetime
df['JoiningDate'] = df['JoiningDate'].dt.strftime("%Y-%m-%d")           # standardize format

# -----------------------------
# Remove duplicates
# -----------------------------
df = df.drop_duplicates()

# -----------------------------
# Save cleaned dataset
# -----------------------------
df.to_csv("../data/clean_employee_records.csv", index=False)
print("✅ Clean dataset saved at data/clean_employee_records.csv")
