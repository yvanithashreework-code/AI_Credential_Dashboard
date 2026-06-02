import pandas as pd

raw = pd.read_csv("data/employee_records.csv")

# Example: add a Role column with placeholder values
roles = ["Manager", "Analyst", "Developer", "HR"]
raw["Role"] = [roles[i % len(roles)] for i in range(len(raw))]

raw.to_csv("data/employee_records.csv", index=False)
