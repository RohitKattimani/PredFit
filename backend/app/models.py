from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    password_hash: str
    role: str = Field(default="user", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Basic profile fields (extend freely)
    age: Optional[int] = None
    gender: Optional[str] = None  # "male" | "female" | "other"
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    medical_history_json: Optional[str] = None
    family_history_json: Optional[str] = None
    lifestyle_baseline_json: Optional[str] = None


class DailyLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    ts: datetime = Field(default_factory=datetime.utcnow, index=True)

    # Manual / wearable normalized fields (subset for demo)
    steps: Optional[int] = None
    sleep_hours: Optional[float] = None
    exercise_minutes: Optional[int] = None
    stress_level: Optional[int] = Field(default=None, ge=0, le=10)
    water_liters: Optional[float] = None

    # Simple dietary proxies (demo)
    sugar_servings: Optional[float] = None
    ultra_processed_servings: Optional[float] = None

    source: str = Field(default="manual", index=True)  # manual|wearable|chat|call


class RiskSnapshot(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    ts: datetime = Field(default_factory=datetime.utcnow, index=True)

    # Scores 0-100
    diabetes: int
    hypertension: int
    cardiovascular: int
    obesity: int
    sleep_disorder: int

    # Explainability (JSON string for demo; swap to JSONB in Postgres)
    drivers_json: str
    recommendations_json: str
    confidence: float = Field(default=0.65, ge=0.0, le=1.0)

