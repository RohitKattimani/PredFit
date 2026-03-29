import os
import numpy as np
import joblib
from typing import Dict, Optional

ML_DIR = os.path.join(os.path.dirname(__file__))

FEATURES = [
    "age", "bmi", "sugar_intake_g", "sleep_hours", "stress_level",
    "exercise_minutes", "bp_systolic", "bp_diastolic", "heart_rate",
    "smoking", "alcohol_units", "family_diabetes", "family_htn",
    "calories", "water_ml", "fiber_g"
]

TARGETS = ["diabetes", "hypertension", "cvd", "obesity", "sleep_disorder"]

_models: Dict[str, object] = {}


def load_models():
    global _models
    for target in TARGETS:
        path = os.path.join(ML_DIR, f"{target}_model.pkl")
        if os.path.exists(path):
            _models[target] = joblib.load(path)
    return _models


def predict_risks(user_data: dict) -> dict:
    """
    Predict risk scores (0-100) for all diseases.
    user_data should contain all FEATURES, using user profile + latest health log.
    """
    if not _models:
        load_models()

    if not _models:
        # Fallback: rule-based estimation if models not trained yet
        return _rule_based_estimate(user_data)

    feature_vec = np.array([[
        user_data.get("age", 35),
        user_data.get("bmi", 22.0),
        user_data.get("sugar_intake_g", 30),
        user_data.get("sleep_hours", 7),
        user_data.get("stress_level", 5),
        user_data.get("exercise_minutes", 30),
        user_data.get("bp_systolic", 120),
        user_data.get("bp_diastolic", 80),
        user_data.get("heart_rate", 72),
        user_data.get("smoking", 0),
        user_data.get("alcohol_units", 0),
        user_data.get("family_diabetes", 0),
        user_data.get("family_htn", 0),
        user_data.get("calories", 2000),
        user_data.get("water_ml", 2000),
        user_data.get("fiber_g", 20),
    ]])

    scores = {}
    for target, model in _models.items():
        prob = model.predict_proba(feature_vec)[0][1]
        scores[target] = round(prob * 100, 1)

    overall = round(np.mean(list(scores.values())), 1)
    scores["overall"] = overall
    scores["risk_level"] = _get_risk_level(overall)
    scores["confidence"] = 0.85

    return scores


def get_feature_importance(target: str = "diabetes") -> dict:
    if not _models:
        load_models()
    model = _models.get(target)
    if not model:
        return {}
    clf = model.named_steps["clf"]
    importances = clf.feature_importances_
    return dict(sorted(zip(FEATURES, importances), key=lambda x: -x[1]))


def _get_risk_level(score: float) -> str:
    if score < 25: return "low"
    if score < 50: return "moderate"
    if score < 75: return "high"
    return "critical"


def _rule_based_estimate(data: dict) -> dict:
    """Fallback rule-based scoring when ML models aren't available."""
    age = data.get("age", 35)
    bmi = data.get("bmi", 22)
    sugar = data.get("sugar_intake_g", 30)
    sleep = data.get("sleep_hours", 7)
    stress = data.get("stress_level", 5)
    exercise = data.get("exercise_minutes", 30)
    bp_sys = data.get("bp_systolic", 120)
    smoking = data.get("smoking", 0)
    fam_diab = data.get("family_diabetes", 0)
    fam_htn = data.get("family_htn", 0)

    diabetes = min(100, max(0,
        (bmi - 18) * 1.5 + (sugar * 0.4) + (fam_diab * 20) +
        (max(0, age - 40) * 0.5) + (max(0, 30 - exercise) * 0.3)
    ))
    hypertension = min(100, max(0,
        (max(0, bp_sys - 110) * 0.8) + (bmi * 0.8) + (stress * 3) +
        (smoking * 1.5) + (fam_htn * 20) + (max(0, age - 40))
    ))
    cvd = min(100, max(0,
        (max(0, bp_sys - 120) * 0.7) + (bmi * 0.5) + (smoking * 2) +
        (stress * 2) + (max(0, age - 45) * 0.8)
    ))
    obesity = min(100, max(0, (bmi - 18) * 3))
    sleep_disorder = min(100, max(0,
        (max(0, 7 - sleep) * 12) + (stress * 4)
    ))

    overall = round((diabetes + hypertension + cvd + obesity + sleep_disorder) / 5, 1)
    return {
        "diabetes": round(diabetes, 1),
        "hypertension": round(hypertension, 1),
        "cvd": round(cvd, 1),
        "obesity": round(obesity, 1),
        "sleep_disorder": round(sleep_disorder, 1),
        "overall": overall,
        "risk_level": _get_risk_level(overall),
        "confidence": 0.70
    }
