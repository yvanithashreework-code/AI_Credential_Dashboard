# --------------------1
import pandas as pd
from datetime import datetime
from word2number import w2n
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

# --------------------
# File paths
file_in = "data/employee_records.csv"
file_out = "data/clean_employee_records.csv"

# Load raw dataset
df = pd.read_csv(file_in)

# --------------------
# Step 1: Drop rows with all missing values
df = df.dropna(how="all")

# --------------------
# Step 2: Standardize text columns
df["Name"] = df["Name"].astype(str).str.strip().str.title()
df["Role"] = df["Role"].astype(str).str.strip().str.title()
df["Department"] = df["Department"].astype(str).str.strip().str.title()

# --------------------
# Step 3: Convert Age (words → number)
def convert_age_to_number(age_str):
    try:
        return w2n.word_to_num(str(age_str))
    except:
        try:
            return int(age_str)
        except:
            return None

df["Age"] = df["Age"].apply(convert_age_to_number)

# --------------------
# Step 4: Ensure Salary is numeric
df["Salary"] = pd.to_numeric(df["Salary"], errors="coerce")

# --------------------
# Step 5: Convert JoiningDate to datetime
df["JoiningDate"] = pd.to_datetime(df["JoiningDate"], errors="coerce", dayfirst=True)

# --------------------
# Step 6: Derived feature - ExperienceYears
current_date = datetime.now()
df["ExperienceYears"] = (current_date - df["JoiningDate"]).dt.days // 365

# --------------------
# Step 7: Derived feature - SalaryBand
def categorize_salary(salary):
    if pd.isnull(salary):
        return None
    if salary < 40000:
        return "Low"
    elif salary < 80000:
        return "Medium"
    else:
        return "High"

df["SalaryBand"] = df["Salary"].apply(categorize_salary)

# --------------------
# Step 8: Drop rows with missing SalaryBand
df = df.dropna(subset=["SalaryBand"])

# --------------------
# Step 9: Encode categorical columns
label_encoder = LabelEncoder()
df["DepartmentEncoded"] = label_encoder.fit_transform(df["Department"].astype(str))

# --------------------
# Step 10: Encode SalaryBand
salaryband_encoder = LabelEncoder()
df["SalaryBandEncoded"] = salaryband_encoder.fit_transform(df["SalaryBand"].astype(str))

# --------------------
# Step 11: Normalize numeric values
scaler = MinMaxScaler()
df[["SalaryNorm", "ExperienceNorm"]] = scaler.fit_transform(
    df[["Salary", "ExperienceYears"]].fillna(0)
)

# --------------------
# Save cleaned dataset
df.to_csv(file_out, index=False)

print("✅ Cleaned and engineered dataset saved to:", file_out)