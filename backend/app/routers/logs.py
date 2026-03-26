from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.agents.risk_scoring import run_agent_workflow
from app.deps import get_current_user
from app.models import DailyLog, RiskSnapshot, User
from app.realtime import manager
from app.schemas import DailyLogIn, DailyLogOut, RiskSnapshotOut
from app.db import get_session
import json


router = APIRouter(prefix="/logs", tags=["logs"])


def _recent_logs(session: Session, user_id: int, limit: int = 30) -> list[DailyLog]:
    return list(
        session.exec(
            select(DailyLog).where(DailyLog.user_id == user_id).order_by(DailyLog.ts.desc()).limit(limit)
        ).all()
    )


def _compute_and_store_snapshot(session: Session, user: User) -> RiskSnapshot:
    logs = _recent_logs(session, user.id, limit=30)
    recent = [
        {
            "ts": l.ts,
            "steps": l.steps,
            "sleep_hours": l.sleep_hours,
            "exercise_minutes": l.exercise_minutes,
            "stress_level": l.stress_level,
            "water_liters": l.water_liters,
            "sugar_servings": l.sugar_servings,
            "ultra_processed_servings": l.ultra_processed_servings,
            "source": l.source,
        }
        for l in logs
    ]
    profile = {
        "age": user.age,
        "gender": user.gender,
        "height_cm": user.height_cm,
        "weight_kg": user.weight_kg,
    }
    result = run_agent_workflow(profile=profile, recent_logs=recent)

    snap = RiskSnapshot(
        user_id=user.id,
        ts=datetime.utcnow(),
        diabetes=result.scores["diabetes"],
        hypertension=result.scores["hypertension"],
        cardiovascular=result.scores["cardiovascular"],
        obesity=result.scores["obesity"],
        sleep_disorder=result.scores["sleep_disorder"],
        confidence=result.confidence,
        drivers_json=json.dumps(result.drivers),
        recommendations_json=json.dumps(result.recommendations),
    )
    session.add(snap)
    session.commit()
    session.refresh(snap)
    return snap


@router.post("", response_model=DailyLogOut)
async def create_log(
    payload: DailyLogIn,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    log = DailyLog(
        user_id=user.id,
        ts=payload.ts or datetime.utcnow(),
        steps=payload.steps,
        sleep_hours=payload.sleep_hours,
        exercise_minutes=payload.exercise_minutes,
        stress_level=payload.stress_level,
        water_liters=payload.water_liters,
        sugar_servings=payload.sugar_servings,
        ultra_processed_servings=payload.ultra_processed_servings,
        source=payload.source,
    )
    session.add(log)
    session.commit()
    session.refresh(log)

    snap = _compute_and_store_snapshot(session, user)
    message = {
        "type": "risk_update",
        "ts": snap.ts.isoformat(),
        "scores": {
            "diabetes": snap.diabetes,
            "hypertension": snap.hypertension,
            "cardiovascular": snap.cardiovascular,
            "obesity": snap.obesity,
            "sleep_disorder": snap.sleep_disorder,
        },
        "confidence": snap.confidence,
    }
    await manager.broadcast_user(user.id, message)

    return DailyLogOut(
        id=log.id,
        ts=log.ts,
        steps=log.steps,
        sleep_hours=log.sleep_hours,
        exercise_minutes=log.exercise_minutes,
        stress_level=log.stress_level,
        water_liters=log.water_liters,
        sugar_servings=log.sugar_servings,
        ultra_processed_servings=log.ultra_processed_servings,
        source=log.source,
    )


@router.get("", response_model=list[DailyLogOut])
def list_logs(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    limit: int = 50,
):
    logs = session.exec(select(DailyLog).where(DailyLog.user_id == user.id).order_by(DailyLog.ts.desc()).limit(limit)).all()
    return [
        DailyLogOut(
            id=l.id,
            ts=l.ts,
            steps=l.steps,
            sleep_hours=l.sleep_hours,
            exercise_minutes=l.exercise_minutes,
            stress_level=l.stress_level,
            water_liters=l.water_liters,
            sugar_servings=l.sugar_servings,
            ultra_processed_servings=l.ultra_processed_servings,
            source=l.source,
        )
        for l in logs
    ]


@router.post("/recompute", response_model=RiskSnapshotOut)
async def recompute_risk(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    snap = _compute_and_store_snapshot(session, user)
    import json as _json

    message = {
        "type": "risk_update",
        "ts": snap.ts.isoformat(),
        "scores": {
            "diabetes": snap.diabetes,
            "hypertension": snap.hypertension,
            "cardiovascular": snap.cardiovascular,
            "obesity": snap.obesity,
            "sleep_disorder": snap.sleep_disorder,
        },
        "confidence": snap.confidence,
    }
    await manager.broadcast_user(user.id, message)

    return RiskSnapshotOut(
        ts=snap.ts,
        diabetes=snap.diabetes,
        hypertension=snap.hypertension,
        cardiovascular=snap.cardiovascular,
        obesity=snap.obesity,
        sleep_disorder=snap.sleep_disorder,
        confidence=snap.confidence,
        drivers=_json.loads(snap.drivers_json),
        recommendations=_json.loads(snap.recommendations_json),
    )

