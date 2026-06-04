#Cleansing the data
import pandas as pd

# Load raw dataset
raw = pd.read_csv("data/employee_records.csv")

# Cleaning steps
clean = raw.dropna()
clean["Role"] = clean["Role"].str.strip().str.title()
clean["Department"] = clean["Department"].str.strip().str.title()

# Save cleaned dataset
clean.to_csv("data/clean_employee_records.csv", index=False)
print("Cleaned dataset saved to data/clean_employee_records.csv")
