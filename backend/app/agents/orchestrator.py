"""
Multi-Agent Orchestrator
Coordinates all health agents and runs the full analysis pipeline.
"""
import asyncio
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from models.user import User
from models.health_log import HealthLog
from models.risk_score import RiskScore, Recommendation, AgentInsight
from ml.predict import predict_risks
from websocket_manager import ws_manager

from agents.cardiologist import CardiologistAgent
from agents.diabetologist import DiabetologistAgent
from agents.nutritionist import NutritionistAgent
from agents.lifestyle_coach import LifestyleCoachAgent
from agents.sleep_specialist import SleepSpecialistAgent
from agents.consensus import ConsensusAgent
from agents.behavioral_insight import BehavioralInsightAgent
from agents.recommendation import RecommendationAgent
from agents.nudge_alert import NudgeAlertAgent


class AgentOrchestrator:
    def __init__(self):
        self.cardiologist = CardiologistAgent()
        self.diabetologist = DiabetologistAgent()
        self.nutritionist = NutritionistAgent()
        self.lifestyle_coach = LifestyleCoachAgent()
        self.sleep_specialist = SleepSpecialistAgent()
        self.consensus = ConsensusAgent()
        self.behavioral = BehavioralInsightAgent()
        self.recommender = RecommendationAgent()
        self.nudge_alert = NudgeAlertAgent()

    def _build_user_data(self, user: User, logs: list) -> dict:
        """Merge user profile + recent health logs into feature dict."""
        height_m = (user.height_cm or 170) / 100
        weight_kg = user.weight_kg or 70
        bmi = round(weight_kg / (height_m ** 2), 1)

        family_diabetes = 1 if user.family_history and "diabetes" in user.family_history.lower() else 0
        family_htn = 1 if user.family_history and ("hypertension" in user.family_history.lower() or "htn" in user.family_history.lower() or "blood pressure" in user.family_history.lower()) else 0

        if logs:
            latest = logs[0]
            return {
                "user_id": user.id,
                "age": user.age or 35,
                "bmi": bmi,
                "sugar_intake_g": latest.sugar_intake_g or 30,
                "sleep_hours": latest.sleep_hours or 7,
                "stress_level": latest.stress_level or 5,
                "exercise_minutes": latest.exercise_minutes or 30,
                "bp_systolic": latest.blood_pressure_systolic or 120,
                "bp_diastolic": latest.blood_pressure_diastolic or 80,
                "heart_rate": latest.heart_rate_avg or 72,
                "smoking": latest.smoking or 0,
                "alcohol_units": latest.alcohol_units or 0,
                "family_diabetes": family_diabetes,
                "family_htn": family_htn,
                "calories": latest.calories_intake or 2000,
                "water_ml": latest.water_intake_ml or 2000,
                "fiber_g": latest.fiber_intake_g or 20,
                # Extra context for agents
                "steps_count": latest.steps_count or 0,
                "mood": latest.mood or "neutral",
                "meal_description": latest.meal_description or "",
            }
        else:
            return {
                "user_id": user.id,
                "age": user.age or 35,
                "bmi": bmi,
                "sugar_intake_g": 30,
                "sleep_hours": 7,
                "stress_level": 5,
                "exercise_minutes": 30,
                "bp_systolic": 120,
                "bp_diastolic": 80,
                "heart_rate": 72,
                "smoking": 0,
                "alcohol_units": 0,
                "family_diabetes": family_diabetes,
                "family_htn": family_htn,
                "calories": 2000,
                "water_ml": 2000,
                "fiber_g": 20,
                "steps_count": 0,
                "mood": "neutral",
                "meal_description": "",
            }

    async def run_pipeline(self, user: User, db: Session) -> dict:
        """Run the full multi-agent analysis pipeline for a user."""
        # Fetch recent logs
        logs = (
            db.query(HealthLog)
            .filter(HealthLog.user_id == user.id)
            .order_by(HealthLog.logged_at.desc())
            .limit(14)
            .all()
        )

        user_data = self._build_user_data(user, logs)

        # Notify frontend: agents starting
        await ws_manager.send_to_user(user.id, {
            "type": "agents_started",
            "message": "AI health agents are analyzing your data...",
            "agents": ["Cardiologist", "Diabetologist", "Nutritionist",
                       "Lifestyle Coach", "Sleep Specialist"]
        })

        # Run all specialist agents in parallel
        cardio_result = self.cardiologist.analyze(user_data)
        diab_result = self.diabetologist.analyze(user_data)
        nutr_result = self.nutritionist.analyze(user_data)
        coach_result = self.lifestyle_coach.analyze(user_data)
        sleep_result = self.sleep_specialist.analyze(user_data)

        agent_results = {
            "cardiologist": cardio_result,
            "diabetologist": diab_result,
            "nutritionist": nutr_result,
            "lifestyle_coach": coach_result,
            "sleep_specialist": sleep_result,
        }

        # Save insights
        for agent_name, result in agent_results.items():
            for insight in result.get("insights", []):
                db_insight = AgentInsight(
                    user_id=user.id,
                    agent_name=agent_name,
                    insight_type=insight.get("type", "recommendation"),
                    title=insight.get("title", ""),
                    content=insight.get("content", ""),
                    severity=insight.get("severity", "info"),
                )
                db.add(db_insight)

        # Consensus agent aggregates all doctors
        consensus_result = self.consensus.aggregate(user_data, agent_results)

        # ML Risk prediction
        risk_scores = predict_risks(user_data)

        # Save risk score
        existing = db.query(RiskScore).filter(RiskScore.user_id == user.id).order_by(RiskScore.id.desc()).first()
        risk_entry = RiskScore(
            user_id=user.id,
            diabetes_risk=risk_scores.get("diabetes", 0),
            hypertension_risk=risk_scores.get("hypertension", 0),
            cvd_risk=risk_scores.get("cvd", 0),
            obesity_risk=risk_scores.get("obesity", 0),
            sleep_disorder_risk=risk_scores.get("sleep_disorder", 0),
            overall_risk=risk_scores.get("overall", 0),
            risk_level=risk_scores.get("risk_level", "low"),
            confidence=risk_scores.get("confidence", 0.8),
            key_factors=consensus_result.get("key_factors", ""),
        )
        db.add(risk_entry)

        # Generate recommendations
        recommendations = self.recommender.generate(user_data, risk_scores, consensus_result)
        for rec in recommendations:
            db_rec = Recommendation(
                user_id=user.id,
                category=rec.get("category", "general"),
                title=rec.get("title", ""),
                description=rec.get("description", ""),
                priority=rec.get("priority", "medium"),
                agent_source=rec.get("agent_source", "consensus"),
            )
            db.add(db_rec)

        # Behavioral insights
        behavioral_result = self.behavioral.analyze(logs, user_data)

        # Nudge/Alert check
        alerts = self.nudge_alert.check(user_data, risk_scores)

        db.commit()

        # Push real-time update to frontend
        await ws_manager.send_to_user(user.id, {
            "type": "risk_updated",
            "risk_scores": risk_scores,
            "consensus": consensus_result.get("summary", ""),
            "alerts": alerts,
            "agent_insights": {k: v.get("summary", "") for k, v in agent_results.items()},
            "recommendations_count": len(recommendations),
        })

        return {
            "risk_scores": risk_scores,
            "agent_results": agent_results,
            "consensus": consensus_result,
            "behavioral": behavioral_result,
            "recommendations": recommendations,
            "alerts": alerts,
        }


orchestrator = AgentOrchestrator()
