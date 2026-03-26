from __future__ import annotations

from datetime import datetime
from statistics import mean
from typing import Any

from app.agents.types import AgentTrace, RiskResult


DISEASE_KEYS = ["diabetes", "hypertension", "cardiovascular", "obesity", "sleep_disorder"]


def _clamp_int(x: float, lo: int = 0, hi: int = 100) -> int:
    return int(max(lo, min(hi, round(x))))


def _bmi(height_cm: float | None, weight_kg: float | None) -> float | None:
    if not height_cm or not weight_kg:
        return None
    h_m = height_cm / 100.0
    if h_m <= 0:
        return None
    return weight_kg / (h_m * h_m)


def risk_prediction_agent(
    *,
    profile: dict[str, Any],
    recent_logs: list[dict[str, Any]],
) -> AgentTrace:
    """
    Deterministic scoring for the demo.
    Replace with ML models + calibration later.
    """
    age = profile.get("age") or 35
    height_cm = profile.get("height_cm")
    weight_kg = profile.get("weight_kg")
    bmi = _bmi(height_cm, weight_kg)

    steps = [l.get("steps") for l in recent_logs if l.get("steps") is not None]
    sleep = [l.get("sleep_hours") for l in recent_logs if l.get("sleep_hours") is not None]
    exercise = [l.get("exercise_minutes") for l in recent_logs if l.get("exercise_minutes") is not None]
    stress = [l.get("stress_level") for l in recent_logs if l.get("stress_level") is not None]
    sugar = [l.get("sugar_servings") for l in recent_logs if l.get("sugar_servings") is not None]
    upp = [l.get("ultra_processed_servings") for l in recent_logs if l.get("ultra_processed_servings") is not None]

    avg_steps = mean(steps) if steps else 6000
    avg_sleep = mean(sleep) if sleep else 7.0
    avg_ex = mean(exercise) if exercise else 20
    avg_stress = mean(stress) if stress else 4
    avg_sugar = mean(sugar) if sugar else 2.0
    avg_upp = mean(upp) if upp else 1.5

    age_factor = max(0, (age - 35) * 0.6)
    sed_factor = max(0, (8000 - avg_steps) / 200)
    low_ex_factor = max(0, (150 - (avg_ex * 7)) / 15)  # weekly minutes target
    poor_sleep_factor = max(0, (7.0 - avg_sleep) * 8) + max(0, (avg_sleep - 9.0) * 4)
    stress_factor = max(0, (avg_stress - 4) * 4)
    sugar_factor = max(0, (avg_sugar - 2.0) * 6)
    upp_factor = max(0, (avg_upp - 1.5) * 6)

    bmi_factor = 0.0
    if bmi is not None:
        if bmi >= 30:
            bmi_factor = 22
        elif bmi >= 27:
            bmi_factor = 14
        elif bmi >= 25:
            bmi_factor = 8

    diabetes = 18 + age_factor * 0.6 + bmi_factor * 0.8 + sugar_factor * 1.0 + sed_factor * 0.7
    hypertension = 16 + age_factor * 0.7 + stress_factor * 0.9 + poor_sleep_factor * 0.6 + sed_factor * 0.5
    cardiovascular = 15 + age_factor * 0.8 + bmi_factor * 0.7 + sed_factor * 0.7 + upp_factor * 0.8 + poor_sleep_factor * 0.3
    obesity = 14 + bmi_factor * 1.4 + sed_factor * 0.8 + upp_factor * 0.7 + sugar_factor * 0.4
    sleep_disorder = 12 + poor_sleep_factor * 1.4 + stress_factor * 0.7

    scores = {
        "diabetes": _clamp_int(diabetes),
        "hypertension": _clamp_int(hypertension),
        "cardiovascular": _clamp_int(cardiovascular),
        "obesity": _clamp_int(obesity),
        "sleep_disorder": _clamp_int(sleep_disorder),
    }

    drivers = {
        "inputs": {
            "avg_steps": round(avg_steps, 0),
            "avg_sleep_hours": round(avg_sleep, 1),
            "avg_exercise_minutes": round(avg_ex, 0),
            "avg_stress_level": round(avg_stress, 1),
            "avg_sugar_servings": round(avg_sugar, 1),
            "avg_ultra_processed_servings": round(avg_upp, 1),
            "bmi": round(bmi, 1) if bmi is not None else None,
            "age": age,
        },
        "key_drivers": [
            {"driver": "activity", "signal": "low_steps" if avg_steps < 7000 else "ok"},
            {"driver": "sleep", "signal": "poor_sleep" if avg_sleep < 7 else "ok"},
            {"driver": "diet", "signal": "high_sugar" if avg_sugar > 3 else "ok"},
            {"driver": "stress", "signal": "high_stress" if avg_stress >= 6 else "ok"},
            {"driver": "weight", "signal": "high_bmi" if (bmi is not None and bmi >= 25) else "unknown" if bmi is None else "ok"},
        ],
    }

    confidence = 0.55
    if recent_logs:
        confidence += min(0.35, len(recent_logs) * 0.03)
    if bmi is not None:
        confidence += 0.05
    confidence = max(0.0, min(1.0, confidence))

    rec = {
        "daily": [
            "Walk 20–30 minutes after meals (target 8–10k steps/day).",
            "Aim for 7–8 hours sleep; keep consistent sleep/wake times.",
            "Reduce added sugar and ultra-processed foods; add protein + fiber to meals.",
            "Do 150 min/week moderate exercise + 2 strength sessions.",
        ],
        "next_actions": [
            "Log meals for the next 3 days.",
            "Add a 10-minute evening wind-down (no screens) before bed.",
        ],
    }

    return AgentTrace(
        agent_name="risk_prediction_agent",
        ts=datetime.utcnow(),
        output={"scores": scores, "confidence": confidence, "drivers": drivers, "recommendations": rec},
    )


def _doctor_agent(name: str, focus: str, scores: dict[str, int], drivers: dict[str, Any]) -> AgentTrace:
    key = focus
    score = scores.get(key, 0)
    risk_band = "low" if score < 30 else "moderate" if score < 60 else "high"
    out = {
        "focus": key,
        "risk_band": risk_band,
        "note": f"{name} sees {key} risk as {risk_band}.",
        "top_driver": drivers.get("key_drivers", [None])[0],
        "actions": [],
    }
    if key == "sleep_disorder":
        out["actions"] = ["Keep a fixed bedtime/wake time for 7 days.", "Avoid caffeine after 2pm."]
    if key == "diabetes":
        out["actions"] = ["Swap refined carbs for whole grains/legumes.", "Post-meal 10–15 min walk."]
    if key == "hypertension":
        out["actions"] = ["Practice 5-min breathing twice daily.", "Limit high-sodium packaged foods."]
    if key == "cardiovascular":
        out["actions"] = ["Add 2 strength sessions/week.", "Increase omega-3 rich foods (fish/flax/chia)."]
    if key == "obesity":
        out["actions"] = ["Prioritize protein at breakfast.", "Track late-night snacking triggers."]

    return AgentTrace(agent_name=name, ts=datetime.utcnow(), output=out)


def consensus_agent(traces: list[AgentTrace]) -> AgentTrace:
    doctor_traces = [t for t in traces if t.agent_name.endswith("_agent") and t.agent_name != "risk_prediction_agent"]
    actions: list[str] = []
    for t in doctor_traces:
        actions.extend(t.output.get("actions") or [])
    # de-dupe while preserving order
    seen: set[str] = set()
    actions = [a for a in actions if not (a in seen or seen.add(a))]
    return AgentTrace(
        agent_name="consensus_agent",
        ts=datetime.utcnow(),
        output={"summary": "Combined specialist recommendations.", "actions": actions[:8]},
    )


def run_agent_workflow(*, profile: dict[str, Any], recent_logs: list[dict[str, Any]]) -> RiskResult:
    traces: list[AgentTrace] = []
    base = risk_prediction_agent(profile=profile, recent_logs=recent_logs)
    traces.append(base)
    scores = base.output["scores"]
    drivers = base.output["drivers"]

    traces.extend(
        [
            _doctor_agent("cardiologist_agent", "cardiovascular", scores, drivers),
            _doctor_agent("diabetologist_agent", "diabetes", scores, drivers),
            _doctor_agent("nutritionist_agent", "obesity", scores, drivers),
            _doctor_agent("sleep_specialist_agent", "sleep_disorder", scores, drivers),
            _doctor_agent("lifestyle_coach_agent", "hypertension", scores, drivers),
        ]
    )
    cons = consensus_agent(traces)
    traces.append(cons)

    recommendations = base.output["recommendations"]
    recommendations["specialist_actions"] = cons.output["actions"]

    return RiskResult(
        scores=scores,
        confidence=base.output["confidence"],
        drivers=drivers,
        recommendations=recommendations,
        traces=traces,
    )

