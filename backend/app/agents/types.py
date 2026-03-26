from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class AgentTrace:
    agent_name: str
    ts: datetime
    output: dict[str, Any]


@dataclass(frozen=True)
class RiskResult:
    scores: dict[str, int]  # 0-100 per disease key
    confidence: float
    drivers: dict[str, Any]
    recommendations: dict[str, Any]
    traces: list[AgentTrace]

