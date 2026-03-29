from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from database import Base


class HealthLog(Base):
    __tablename__ = "health_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Nutrition
    calories_intake = Column(Float, default=0)
    water_intake_ml = Column(Float, default=0)
    sugar_intake_g = Column(Float, default=0)
    fiber_intake_g = Column(Float, default=0)
    protein_intake_g = Column(Float, default=0)
    carbs_intake_g = Column(Float, default=0)
    fat_intake_g = Column(Float, default=0)
    meal_description = Column(Text, default="")

    # Activity
    steps_count = Column(Integer, default=0)
    exercise_minutes = Column(Integer, default=0)
    exercise_type = Column(String, default="")

    # Sleep
    sleep_hours = Column(Float, default=0)
    sleep_quality = Column(Integer, default=5)  # 1–10

    # Vitals (from wearables or manual)
    heart_rate_avg = Column(Float, nullable=True)
    blood_pressure_systolic = Column(Integer, nullable=True)
    blood_pressure_diastolic = Column(Integer, nullable=True)

    # Mental
    stress_level = Column(Integer, default=5)  # 1–10
    mood = Column(String, default="neutral")

    # Substance
    smoking = Column(Integer, default=0)  # cigarettes
    alcohol_units = Column(Float, default=0)

    # Metadata
    log_source = Column(String, default="manual")  # manual/wearable/chat/call
    raw_input = Column(Text, default="")
    logged_at = Column(DateTime(timezone=True), server_default=func.now())
