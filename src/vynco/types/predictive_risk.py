from __future__ import annotations

from vynco.types.shared import VyncoModel


class RiskIndicator(VyncoModel):
    """A pre-dissolution risk indicator."""

    signal: str = ""
    triggered: bool = False
    weight: float = 0.0
    contribution: float = 0.0
    severity: str = ""
    description: str = ""


class PredictiveRiskResponse(VyncoModel):
    """Predictive risk scoring response with dissolution probability."""

    uid: str = ""
    company_name: str = ""
    dissolution_probability: float = 0.0
    risk_level: str = ""
    pre_dissolution_indicators: list[RiskIndicator] = []
    credit_risk_score: int = 0
    recommendation: str = ""
    assessed_at: str = ""
