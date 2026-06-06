import pandas as pd
from word2number import w2n

file_in = "data/employee_records.csv"
file_out = "data/clean_employee_records.csv"

# Load raw dataset
df = pd.read_csv(file_in)

# 1. Drop rows with all missing values
df = df.dropna(how="all")

# 2. Standardize text columns
df["Name"] = df["Name"].astype(str).str.strip().str.title()
df["Role"] = df["Role"].astype(str).str.strip().str.title()
df["Department"] = df["Department"].astype(str).str.strip().str.title()

# 3. Convert Age to numeric (handle words + digits)
def convert_age(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        try:
            return w2n.word_to_num(str(value))
        except:
            return None

df["Age"] = df["Age"].apply(convert_age)

# 4. Convert Salary to numeric
df["Salary"] = pd.to_numeric(df["Salary"], errors="coerce")

# 5. Convert JoiningDate to datetime
df["JoiningDate"] = pd.to_datetime(df["JoiningDate"], errors="coerce", dayfirst=True)

# 6. Remove duplicates
df = df.drop_duplicates()

# 7. Handle remaining missing values (optional: fill with defaults)
df = df.fillna({
    "Age": 0,
    "Salary": 0,
    "Department": "Unknown",
    "Role": "Unknown"
})

# Save cleaned dataset
df.to_csv(file_out, index=False)
print("✅ Cleaned dataset saved to", file_out)