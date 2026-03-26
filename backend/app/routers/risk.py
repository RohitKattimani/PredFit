from __future__ import annotations

import json

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.db import get_session
from app.deps import get_current_user
from app.models import RiskSnapshot, User
from app.schemas import RiskSnapshotOut


router = APIRouter(prefix="/risk", tags=["risk"])


@router.get("/latest", response_model=RiskSnapshotOut)
def latest_risk(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    snap = session.exec(
        select(RiskSnapshot).where(RiskSnapshot.user_id == user.id).order_by(RiskSnapshot.ts.desc()).limit(1)
    ).first()
    if not snap:
        return RiskSnapshotOut(
            ts=None,  # type: ignore[arg-type]
            diabetes=0,
            hypertension=0,
            cardiovascular=0,
            obesity=0,
            sleep_disorder=0,
            confidence=0.0,
            drivers={},
            recommendations={},
        )
    return RiskSnapshotOut(
        ts=snap.ts,
        diabetes=snap.diabetes,
        hypertension=snap.hypertension,
        cardiovascular=snap.cardiovascular,
        obesity=snap.obesity,
        sleep_disorder=snap.sleep_disorder,
        confidence=snap.confidence,
        drivers=json.loads(snap.drivers_json),
        recommendations=json.loads(snap.recommendations_json),
    )


@router.get("/history", response_model=list[RiskSnapshotOut])
def risk_history(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    limit: int = 30,
):
    snaps = session.exec(
        select(RiskSnapshot).where(RiskSnapshot.user_id == user.id).order_by(RiskSnapshot.ts.desc()).limit(limit)
    ).all()
    return [
        RiskSnapshotOut(
            ts=s.ts,
            diabetes=s.diabetes,
            hypertension=s.hypertension,
            cardiovascular=s.cardiovascular,
            obesity=s.obesity,
            sleep_disorder=s.sleep_disorder,
            confidence=s.confidence,
            drivers=json.loads(s.drivers_json),
            recommendations=json.loads(s.recommendations_json),
        )
        for s in snaps
    ]

