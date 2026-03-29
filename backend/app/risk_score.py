from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from database import Base


class RiskScore(Base):
    __tablename__ = "risk_scores"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    diabetes_risk = Column(Float, default=0.0)
    hypertension_risk = Column(Float, default=0.0)
    cvd_risk = Column(Float, default=0.0)
    obesity_risk = Column(Float, default=0.0)
    sleep_disorder_risk = Column(Float, default=0.0)
    overall_risk = Column(Float, default=0.0)

    risk_level = Column(String, default="low")  # low/moderate/high/critical
    confidence = Column(Float, default=0.0)
    key_factors = Column(Text, default="")
    computed_at = Column(DateTime(timezone=True), server_default=func.now())


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    category = Column(String, default="general")  # diet/exercise/sleep/lifestyle/medical
    title = Column(String, default="")
    description = Column(Text, default="")
    priority = Column(String, default="medium")  # low/medium/high/urgent
    agent_source = Column(String, default="consensus")
    is_read = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AgentInsight(Base):
    __tablename__ = "agent_insights"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    agent_name = Column(String, default="")
    insight_type = Column(String, default="")  # risk/recommendation/alert/trend
    title = Column(String, default="")
    content = Column(Text, default="")
    severity = Column(String, default="info")  # info/warning/critical
    created_at = Column(DateTime(timezone=True), server_default=func.now())
