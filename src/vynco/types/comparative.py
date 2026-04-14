from __future__ import annotations

from vynco.types.shared import VyncoModel


class OverlapCompanyRole(VyncoModel):
    """A company-role entry within a board overlap."""

    uid: str = ""
    company_name: str = ""
    role: str = ""


class BoardOverlap(VyncoModel):
    """A board member appearing in multiple compared companies."""

    person_name: str = ""
    companies: list[OverlapCompanyRole] = []


class AuditorEntry(VyncoModel):
    """An auditor serving one or more compared companies."""

    auditor_name: str = ""
    company_count: int = 0
    company_uids: list[str] = []
    group_share: float = 0.0


class AuditorAnalysis(VyncoModel):
    """Auditor analysis across compared companies."""

    auditor_distribution: list[AuditorEntry] = []
    unique_auditor_count: int = 0
    concentration_flag: bool = False


class GovernanceFactor(VyncoModel):
    """A single governance score factor."""

    factor: str = ""
    score: int = 0
    description: str = ""


class GovernanceScore(VyncoModel):
    """Per-company governance score."""

    uid: str = ""
    company_name: str = ""
    score: int = 0
    factors: list[GovernanceFactor] = []


class ComparativeResponse(VyncoModel):
    """AI-generated comparative dossier for multiple companies."""

    uids: list[str] = []
    focus: str = ""
    report: str = ""
    board_overlaps: list[BoardOverlap] = []
    auditor_analysis: AuditorAnalysis | None = None
    governance_scores: list[GovernanceScore] = []
    generated_at: str = ""
