from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, default="")
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)  # male/female/other
    height_cm = Column(Float, nullable=True)
    weight_kg = Column(Float, nullable=True)
    medical_history = Column(Text, default="")
    family_history = Column(Text, default="")
    activity_level = Column(String, default="moderate")  # sedentary/moderate/active
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
