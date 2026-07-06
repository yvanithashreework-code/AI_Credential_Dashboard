"""
train_salary_regressor.py

Trains a regression model to predict TotalPay from job title, base pay,
overtime pay, other pay, and year. Saves the trained model + supporting
encoders to ml/salary_regressor.pkl.

Run manually (with venv active, from project root):
    python ml_training/train_salary_regressor.py
"""

import os
import sys
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# Allow importing prepare_data.py from this same folder, and ensure the
# project root is on sys.path so prepare_data.py's Django setup succeeds
# when this script is run directly (python ml_training/train_salary_regressor.py)
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(THIS_DIR)
sys.path.insert(0, THIS_DIR)
sys.path.insert(0, PROJECT_ROOT)

from prepare_data import get_clean_dataframe  # noqa: E402

MODEL_OUTPUT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "ml", "salary_regressor.pkl"
)


def main():
    df, freq_map = get_clean_dataframe()

    # Features: ONLY job_title_freq and year.
    # IMPORTANT: base_pay, overtime_pay, and other_pay are deliberately
    # EXCLUDED. In this dataset, total_pay = base_pay + overtime_pay + other_pay
    # almost exactly, so including them causes data leakage -- the model
    # would just learn addition (R^2 ~0.999) instead of a genuine prediction
    # from role/year. This version predicts what pay to *expect* for a given
    # job title and year, without already knowing the pay breakdown.
    feature_cols = ["job_title_freq", "year"]
    X = df[feature_cols]
    y = df["total_pay"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=15,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    print(f"Mean Absolute Error: ${mae:,.2f}")
    print(f"R^2 Score: {r2:.4f}")

    # Save model + feature column order + job_title freq map.
    # The freq map MUST travel with the model: at prediction time, the API
    # will receive a raw job_title string and needs to convert it into the
    # same job_title_freq number the model was trained on.
    joblib.dump({
        "model": model,
        "feature_cols": feature_cols,
        "job_title_freq_map": freq_map,
    }, MODEL_OUTPUT_PATH)

    print(f"Model saved to {MODEL_OUTPUT_PATH}")


if __name__ == "__main__":
    main()
