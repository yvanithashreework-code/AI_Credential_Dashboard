"""
prepare_data.py

Pulls salary data from the RDS database (via Django ORM), cleans it,
and returns a model-ready DataFrame. This is imported by the training
scripts (train_salary_regressor.py, train_salary_band_classifier.py,
train_anomaly_detector.py) -- it is NOT run directly against the web app.

Run manually to sanity-check output:
    python manage.py shell < ml_training/prepare_data.py
or import get_clean_dataframe() from another script.
"""

import os
import sys
import django
import pandas as pd
import numpy as np

# ---------------------------------------------------------
# Allow this script to use Django models standalone.
# Add the project root (one level up from this file) to sys.path
# so Python can find the "backend" settings package.
# ---------------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings.dev")
django.setup()

from api.models import VanpreSalary  # noqa: E402


RARE_JOB_TITLE_THRESHOLD = 10  # titles appearing fewer times than this get grouped


def load_raw_dataframe() -> pd.DataFrame:
    """Pull all salary rows from the DB into a DataFrame."""
    queryset = VanpreSalary.objects.all().values(
        "employee_id",
        "employee_name",
        "job_title",
        "base_pay",
        "overtime_pay",
        "other_pay",
        "benefits",
        "total_pay",
        "total_pay_benefits",
        "year",
        "status",
    )
    df = pd.DataFrame.from_records(queryset)
    return df


def clean_dataframe(df: pd.DataFrame):
    """
    Apply all cleaning steps and return (clean_df, job_title_freq_map).

    job_title_freq_map is returned because it must be saved alongside
    each trained model -- at prediction time, a brand-new job title string
    coming from the frontend needs to be converted into the same numeric
    encoding the model was trained on. Without saving this map, predictions
    would be inconsistent with training.
    """

    df = df.copy()

    # 1. Drop rows with no job_title or negative/zero total_pay (bad data)
    df = df[df["job_title"].notna()]
    df = df[df["total_pay"] > 0]

    # 2. Fill any remaining numeric nulls with 0 (import already zero-fills,
    #    this is a safety net in case data was loaded another way)
    numeric_cols = [
        "base_pay", "overtime_pay", "other_pay",
        "benefits", "total_pay", "total_pay_benefits"
    ]
    df[numeric_cols] = df[numeric_cols].fillna(0.0)

    # 3. Normalize job_title text (strip whitespace, uppercase for consistency)
    df["job_title"] = df["job_title"].str.strip().str.upper()

    # 4. Group rare job titles into "OTHER" to avoid high-cardinality blowup
    #    (dataset has 2,159 unique titles -- most appear only a handful of times)
    title_counts = df["job_title"].value_counts()
    rare_titles = title_counts[title_counts < RARE_JOB_TITLE_THRESHOLD].index
    df["job_title_grouped"] = df["job_title"].where(
        ~df["job_title"].isin(rare_titles), "OTHER"
    )

    # 5. Frequency-encode job_title_grouped (simple, robust for tree models)
    freq_map = df["job_title_grouped"].value_counts(normalize=True).to_dict()
    df["job_title_freq"] = df["job_title_grouped"].map(freq_map)

    # 6. Drop columns that are constant or unusable for modeling
    #    (agency dropped upstream -- it's constant "San Francisco" in this dataset;
    #     status is mostly null so we keep it only as a filled categorical flag)
    df["status"] = df["status"].fillna("UNKNOWN")
    df["status"] = df["status"].replace("", "UNKNOWN")

    # 7. Remove extreme outliers that are almost certainly data errors
    #    (e.g., total_pay above $1M is implausible for this dataset's job types)
    df = df[df["total_pay"] < 1_000_000]

    return df.reset_index(drop=True), freq_map


def get_clean_dataframe():
    """Main entry point: load + clean in one call. Returns (df, freq_map)."""
    raw = load_raw_dataframe()
    print(f"Loaded {len(raw)} raw rows from database.")
    clean, freq_map = clean_dataframe(raw)
    print(f"Returning {len(clean)} clean rows after filtering.")
    return clean, freq_map


if __name__ == "__main__":
    df, freq_map = get_clean_dataframe()
    print(df.head(10))
    print(df.describe())
    print(f"Number of job title buckets (incl. OTHER): {len(freq_map)}")
