"""
train_anomaly_detector.py

Trains an Isolation Forest to flag unusual pay records -- e.g. someone
whose overtime_pay is wildly out of line with others in the same job
title, or a total_pay that looks like a data entry error. This is an
unsupervised model (no "correct answer" labels needed).

Intended for the ADMIN side of the dashboard as an "AI insight" --
NOT shown to individual employees.

Run manually (with venv active, from project root):
    python ml_training/train_anomaly_detector.py
"""

import os
import sys
import joblib
from sklearn.ensemble import IsolationForest

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(THIS_DIR)
sys.path.insert(0, THIS_DIR)
sys.path.insert(0, PROJECT_ROOT)

from prepare_data import get_clean_dataframe  # noqa: E402

MODEL_OUTPUT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "ml", "anomaly_detector.pkl"
)


def main():
    df, freq_map = get_clean_dataframe()

    feature_cols = ["job_title_freq", "base_pay", "overtime_pay", "other_pay", "total_pay", "year"]
    X = df[feature_cols]

    # contamination = expected proportion of outliers in the data.
    # 0.02 = assume ~2% of records are genuinely unusual. Adjust after
    # reviewing flagged results -- if too many/few are flagged, tune this.
    model = IsolationForest(
        n_estimators=200,
        contamination=0.02,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X)

    # -1 = anomaly, 1 = normal (sklearn's convention)
    df["anomaly_flag"] = model.predict(X)
    num_flagged = (df["anomaly_flag"] == -1).sum()
    print(f"Flagged {num_flagged} out of {len(df)} records as anomalies "
          f"({num_flagged/len(df)*100:.2f}%).")

    print("\nSample flagged records:")
    print(df[df["anomaly_flag"] == -1][
        ["employee_name", "job_title", "base_pay", "overtime_pay", "total_pay", "year"]
    ].head(10))

    joblib.dump({
        "model": model,
        "feature_cols": feature_cols,
        "job_title_freq_map": freq_map,
    }, MODEL_OUTPUT_PATH)

    print(f"\nModel saved to {MODEL_OUTPUT_PATH}")


if __name__ == "__main__":
    main()
