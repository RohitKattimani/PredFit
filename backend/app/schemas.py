from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    age: Optional[int] = Field(default=None, ge=1, le=120)
    gender: Optional[str] = None
    height_cm: Optional[float] = Field(default=None, ge=50, le=250)
    weight_kg: Optional[float] = Field(default=None, ge=10, le=500)


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    age: Optional[int] = None
    gender: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class DailyLogIn(BaseModel):
    ts: Optional[datetime] = None
    steps: Optional[int] = Field(default=None, ge=0, le=200_000)
    sleep_hours: Optional[float] = Field(default=None, ge=0, le=24)
    exercise_minutes: Optional[int] = Field(default=None, ge=0, le=600)
    stress_level: Optional[int] = Field(default=None, ge=0, le=10)
    water_liters: Optional[float] = Field(default=None, ge=0, le=20)
    sugar_servings: Optional[float] = Field(default=None, ge=0, le=50)
    ultra_processed_servings: Optional[float] = Field(default=None, ge=0, le=50)
    source: str = Field(default="manual")


class DailyLogOut(BaseModel):
    id: int
    ts: datetime
    steps: Optional[int] = None
    sleep_hours: Optional[float] = None
    exercise_minutes: Optional[int] = None
    stress_level: Optional[int] = None
    water_liters: Optional[float] = None
    sugar_servings: Optional[float] = None
    ultra_processed_servings: Optional[float] = None
    source: str


class RiskScores(BaseModel):
    diabetes: int
    hypertension: int
    cardiovascular: int
    obesity: int
    sleep_disorder: int
    confidence: float
    drivers: dict
    recommendations: dict


class RiskSnapshotOut(RiskScores):
    ts: Optional[datetime] = None

