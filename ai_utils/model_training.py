# --------------------
# Model Training Script (Final Fixed)
# --------------------

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib

# --------------------
# File paths
file_in = "data/clean_employee_records.csv"
model_out = "models/salaryband_model.pkl"

# Load cleaned dataset
df = pd.read_csv(file_in)

# --------------------
# Step 1: Drop rows with NaN in critical columns
df = df.dropna(subset=[
    "ExperienceYears",
    "DepartmentEncoded",
    "SalaryNorm",
    "ExperienceNorm",
    "SalaryBandEncoded"
])

# --------------------
# Step 2: Feature selection
X = df[["ExperienceYears", "DepartmentEncoded", "SalaryNorm", "ExperienceNorm"]]
y = df["SalaryBandEncoded"]

# --------------------
# Step 3: Train/Test split (stratified to keep class balance)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# --------------------
# Step 4: Train baseline model
model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)

# --------------------
# Step 5: Evaluate model
y_pred = model.predict(X_test)
print("✅ Model Training Complete")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# --------------------
# Step 6: Save model
joblib.dump(model, model_out)
print("✅ Model saved to:", model_out)
