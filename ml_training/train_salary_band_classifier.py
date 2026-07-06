"""
train_salary_band_classifier.py

Trains a classifier that predicts a salary "band" (Low / Mid / High) for
a given job title + pay profile. Bands are derived from total_pay
percentiles within the dataset itself (not hardcoded dollar amounts),
so this stays meaningful even if pay levels shift over time.

Run manually (with venv active, from project root):
    python ml_training/train_salary_band_classifier.py
"""

import os
import sys
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(THIS_DIR)
sys.path.insert(0, THIS_DIR)
sys.path.insert(0, PROJECT_ROOT)

from prepare_data import get_clean_dataframe  # noqa: E402

MODEL_OUTPUT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "ml", "salary_band_classifier.pkl"
)


def assign_bands(df: pd.DataFrame) -> pd.DataFrame:
    """
    Split total_pay into 3 bands using percentiles:
    Low = bottom 33%, Mid = middle 33%, High = top 33%.
    """
    df = df.copy()
    low_cutoff = df["total_pay"].quantile(0.33)
    high_cutoff = df["total_pay"].quantile(0.66)

    def band(pay):
        if pay <= low_cutoff:
            return "Low"
        elif pay <= high_cutoff:
            return "Mid"
        else:
            return "High"

    df["salary_band"] = df["total_pay"].apply(band)
    return df, low_cutoff, high_cutoff


def main():
    df, freq_map = get_clean_dataframe()
    df, low_cutoff, high_cutoff = assign_bands(df)

    # Same leakage fix as train_salary_regressor.py: exclude base_pay,
    # overtime_pay, other_pay since they sum directly to total_pay, which
    # is what the band label is derived from. Only job_title_freq and year
    # are used, so the model genuinely predicts from role/year context.
    feature_cols = ["job_title_freq", "year"]
    X = df[feature_cols]
    y = df["salary_band"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=12,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    print(classification_report(y_test, preds))

    joblib.dump({
        "model": model,
        "feature_cols": feature_cols,
        "job_title_freq_map": freq_map,
        "band_cutoffs": {"low": low_cutoff, "high": high_cutoff},
    }, MODEL_OUTPUT_PATH)

    print(f"Model saved to {MODEL_OUTPUT_PATH}")
    print(f"Band cutoffs -- Low <= ${low_cutoff:,.2f} < Mid <= ${high_cutoff:,.2f} < High")


if __name__ == "__main__":
    main()
