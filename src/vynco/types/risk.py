from __future__ import annotations

from vynco.types.dossiers import Citation
from vynco.types.shared import VyncoModel


class FactorBreakdown(VyncoModel):
    """A single Bayesian risk factor with its posterior parameters."""

    factor: str = ""
    category: str = ""
    weight: float = 0.0
    posterior_alpha: float = 0.0
    posterior_beta: float = 0.0
    posterior_mean: float = 0.0
    rationale: str = ""
    obligation_refs: list[str] = []
    citations: list[Citation] = []
    evidence_applied: bool = False
    evidence_note: str | None = None


class RiskScoreV2Response(VyncoModel):
    """Bayesian (v2) risk score for a company.

    ``risk_level`` is one of ``low``, ``medium``, ``high``, ``critical``.
    """

    uid: str = ""
    company_name: str = ""
    score: float = 0.0
    risk_level: str = ""
    factors: list[FactorBreakdown] = []
    priors_schema_version: str = ""
    assessed_at: str = ""
