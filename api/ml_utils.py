"""
ml_utils.py

Loads the three trained models (once, at import time) and provides
helper functions to run predictions against them. Used by the
prediction views in predictions.py.
"""

import os
import joblib

ML_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ml")

_salary_regressor_bundle = None
_salary_band_bundle = None
_anomaly_bundle = None


def _load_bundle(filename):
    path = os.path.join(ML_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Model file not found at {path}. Run the corresponding "
            f"training script in ml_training/ first."
        )
    return joblib.load(path)


def get_salary_regressor():
    global _salary_regressor_bundle
    if _salary_regressor_bundle is None:
        _salary_regressor_bundle = _load_bundle("salary_regressor.pkl")
    return _salary_regressor_bundle


def get_salary_band_classifier():
    global _salary_band_bundle
    if _salary_band_bundle is None:
        _salary_band_bundle = _load_bundle("salary_band_classifier.pkl")
    return _salary_band_bundle


def get_anomaly_detector():
    global _anomaly_bundle
    if _anomaly_bundle is None:
        _anomaly_bundle = _load_bundle("anomaly_detector.pkl")
    return _anomaly_bundle


def encode_job_title(job_title: str, freq_map: dict) -> float:
    """
    Convert a raw job title string into the same frequency-encoded number
    used during training. Falls back to the "OTHER" bucket's frequency if
    this exact title wasn't in the training data -- this WILL happen for
    job titles that didn't exist in the 2011-2014 dataset (e.g. modern
    role names), so it's expected, not an error.
    """
    normalized = job_title.strip().upper()
    if normalized in freq_map:
        return freq_map[normalized]
    return freq_map.get("OTHER", min(freq_map.values()) if freq_map else 0.0)


def predict_salary(job_title: str, year: int) -> dict:
    bundle = get_salary_regressor()
    model = bundle["model"]
    freq_map = bundle["job_title_freq_map"]

    job_title_freq = encode_job_title(job_title, freq_map)
    features = [[job_title_freq, year]]

    prediction = model.predict(features)[0]

    return {
        "predicted_total_pay": round(float(prediction), 2),
        "job_title_used": job_title.strip().upper(),
        "year": year,
    }


def predict_salary_band(job_title: str, year: int) -> dict:
    bundle = get_salary_band_classifier()
    model = bundle["model"]
    freq_map = bundle["job_title_freq_map"]
    cutoffs = bundle["band_cutoffs"]

    job_title_freq = encode_job_title(job_title, freq_map)
    features = [[job_title_freq, year]]

    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]
    class_labels = model.classes_

    confidence = {
        label: round(float(prob), 4)
        for label, prob in zip(class_labels, probabilities)
    }

    return {
        "predicted_band": prediction,
        "confidence": confidence,
        "band_cutoffs": {
            "low_max": round(float(cutoffs["low"]), 2),
            "high_min": round(float(cutoffs["high"]), 2),
        },
        "job_title_used": job_title.strip().upper(),
        "year": year,
    }


def predict_anomaly(job_title: str, base_pay: float, overtime_pay: float,
                     other_pay: float, total_pay: float, year: int) -> dict:
    bundle = get_anomaly_detector()
    model = bundle["model"]
    freq_map = bundle["job_title_freq_map"]

    job_title_freq = encode_job_title(job_title, freq_map)
    features = [[job_title_freq, base_pay, overtime_pay, other_pay, total_pay, year]]

    raw_prediction = model.predict(features)[0]  # -1 = anomaly, 1 = normal
    anomaly_score = model.decision_function(features)[0]  # lower = more anomalous

    return {
        "is_anomaly": bool(raw_prediction == -1),
        "anomaly_score": round(float(anomaly_score), 4),
        "job_title_used": job_title.strip().upper(),
    }
