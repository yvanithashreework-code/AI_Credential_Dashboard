import pandas as pd

file_in = "data/employee_records.csv"
file_out = "data/clean_employee_records.csv"

# Load raw dataset
df = pd.read_csv(file_in)

# Cleaning steps
df = df.dropna()

# Standardize text columns
df["Name"] = df["Name"].str.strip().str.title()
df["Role"] = df["Role"].str.strip().str.title()
df["Department"] = df["Department"].str.strip().str.title()

# Convert Age to numeric (handle words)
def convert_age(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        words_to_numbers = {
            "twenty four": 24,
            "twenty five": 25,
            "thirty": 30
        }
        return words_to_numbers.get(str(value).lower(), None)

df["Age"] = df["Age"].apply(convert_age)

# Convert Salary to numeric
df["Salary"] = pd.to_numeric(df["Salary"], errors="coerce")

# Convert JoiningDate to datetime
df["JoiningDate"] = pd.to_datetime(df["JoiningDate"], errors="coerce", dayfirst=True)

# Remove duplicates
df = df.drop_duplicates()

# Save cleaned dataset
df.to_csv(file_out, index=False)
print("Cleaned dataset saved to", file_out)
