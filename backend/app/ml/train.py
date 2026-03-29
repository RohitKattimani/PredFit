import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import joblib
import os
import random

DATA_DIR = os.path.join(os.path.dirname(__file__))
MODELS_DIR = os.path.join(DATA_DIR)


def generate_training_data(n=2000):
    """Generate a synthetic health dataset for demonstration."""
    random.seed(42)
    np.random.seed(42)

    records = []
    for _ in range(n):
        age = random.randint(18, 75)
        bmi = random.uniform(16, 42)
        sugar = random.uniform(0, 120)
        sleep = random.uniform(3, 10)
        stress = random.randint(1, 10)
        exercise = random.randint(0, 120)
        bp_sys = random.randint(90, 180)
        bp_dia = random.randint(60, 120)
        hr = random.randint(50, 110)
        smoking = random.randint(0, 20)
        alcohol = random.uniform(0, 10)
        family_diabetes = random.randint(0, 1)
        family_htn = random.randint(0, 1)
        calories = random.uniform(1200, 3500)
        water = random.uniform(500, 3000)
        fiber = random.uniform(5, 40)

        # Diabetes risk (0-1)
        diab_score = (
            0.3 * (bmi > 25) +
            0.2 * (sugar > 50) +
            0.15 * family_diabetes +
            0.1 * (age > 45) +
            0.1 * (exercise < 30) +
            0.05 * (stress > 7) +
            0.05 * (fiber < 15) +
            0.05 * (calories > 2500)
        )
        diabetes = 1 if diab_score + random.uniform(-0.1, 0.1) > 0.4 else 0

        # Hypertension risk
        htn_score = (
            0.25 * (bp_sys > 130) +
            0.2 * (bmi > 28) +
            0.15 * (age > 50) +
            0.1 * (stress > 7) +
            0.1 * (smoking > 5) +
            0.1 * family_htn +
            0.05 * (alcohol > 3) +
            0.05 * (exercise < 20)
        )
        hypertension = 1 if htn_score + random.uniform(-0.1, 0.1) > 0.35 else 0

        # CVD risk
        cvd_score = (
            0.2 * (hr > 90) +
            0.2 * (bp_sys > 140) +
            0.15 * (bmi > 30) +
            0.15 * (smoking > 0) +
            0.1 * (age > 55) +
            0.1 * (exercise < 15) +
            0.1 * (stress > 8)
        )
        cvd = 1 if cvd_score + random.uniform(-0.1, 0.1) > 0.35 else 0

        # Obesity risk
        obesity = 1 if (bmi > 30 and calories > 2500 and exercise < 30) else 0

        # Sleep disorder
        sleep_dis = 1 if (sleep < 6 and stress > 6) or (sleep < 5) else 0

        records.append({
            "age": age, "bmi": bmi, "sugar_intake_g": sugar,
            "sleep_hours": sleep, "stress_level": stress,
            "exercise_minutes": exercise, "bp_systolic": bp_sys,
            "bp_diastolic": bp_dia, "heart_rate": hr,
            "smoking": smoking, "alcohol_units": alcohol,
            "family_diabetes": family_diabetes, "family_htn": family_htn,
            "calories": calories, "water_ml": water, "fiber_g": fiber,
            "diabetes": diabetes, "hypertension": hypertension,
            "cvd": cvd, "obesity": obesity, "sleep_disorder": sleep_dis
        })

    return pd.DataFrame(records)


FEATURES = [
    "age", "bmi", "sugar_intake_g", "sleep_hours", "stress_level",
    "exercise_minutes", "bp_systolic", "bp_diastolic", "heart_rate",
    "smoking", "alcohol_units", "family_diabetes", "family_htn",
    "calories", "water_ml", "fiber_g"
]

TARGETS = ["diabetes", "hypertension", "cvd", "obesity", "sleep_disorder"]


def train_models():
    print("Generating synthetic training data...")
    df = generate_training_data(3000)

    # Save sample data
    df.to_csv(os.path.join(DATA_DIR, "sample_data.csv"), index=False)
    print(f"Saved sample_data.csv with {len(df)} records")

    X = df[FEATURES]
    models = {}

    for target in TARGETS:
        y = df[target]
        pipeline = Pipeline([
            ("scaler", StandardScaler()),
            ("clf", GradientBoostingClassifier(n_estimators=100, random_state=42))
        ])
        pipeline.fit(X, y)
        models[target] = pipeline
        acc = pipeline.score(X, y)
        print(f"  Trained {target} model — train accuracy: {acc:.2f}")

    return models


def save_models(models):
    for target, model in models.items():
        path = os.path.join(MODELS_DIR, f"{target}_model.pkl")
        joblib.dump(model, path)
        print(f"  Saved: {path}")


if __name__ == "__main__":
    print("=== Training ML Risk Models ===")
    models = train_models()
    save_models(models)
    print("=== Training Complete ===")
