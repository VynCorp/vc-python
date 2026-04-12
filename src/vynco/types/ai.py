from __future__ import annotations

from typing import Any

from vynco.types.companies import Company
from vynco.types.shared import VyncoModel


class DossierResponse(VyncoModel):
    """AI dossier response."""

    uid: str = ""
    company_name: str = ""
    dossier: str = ""
    sources: list[str] = []
    generated_at: str = ""


class AiSearchResponse(VyncoModel):
    """AI search response."""

    query: str = ""
    explanation: str = ""
    filters_applied: Any = None
    results: list[Company] = []
    total: int = 0


class RiskFactor(VyncoModel):
    """A single risk factor in a risk score breakdown."""

    factor: str = ""
    score: int = 0
    weight: float = 0.0
    description: str = ""


class RiskScoreResponse(VyncoModel):
    """Risk score response."""

    uid: str = ""
    company_name: str = ""
    overall_score: int = 0
    risk_level: str = ""
    breakdown: list[RiskFactor] = []
    assessed_at: str = ""


class RiskScoreResult(VyncoModel):
    """A summary risk score for a single company in a batch request."""

    uid: str = ""
    company_name: str = ""
    overall_score: int = 0
    risk_level: str = ""


class BatchRiskScoreResponse(VyncoModel):
    """Response from a batch risk scoring request."""

    results: list[RiskScoreResult] = []
