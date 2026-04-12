from __future__ import annotations

from typing import Any

from vynco.types.shared import VyncoModel


class ScreeningHit(VyncoModel):
    """A single screening hit."""

    source: str = ""
    matched_name: str = ""
    entity_type: str = ""
    score: float = 0.0
    datasets: list[str] = []
    details: Any = None


class ScreeningResponse(VyncoModel):
    """Screening result response."""

    query_name: str = ""
    query_uid: str | None = None
    screened_at: str = ""
    hit_count: int = 0
    risk_level: str = ""
    hits: list[ScreeningHit] = []
    sources_checked: list[str] = []


class BatchScreeningHitSummary(VyncoModel):
    """A summary of a single screening hit within a batch result."""

    source: str = ""
    matched_name: str = ""
    score: float = 0.0


class BatchScreeningResultByUid(VyncoModel):
    """Screening result for a single company in a batch screening request."""

    uid: str = ""
    company_name: str = ""
    risk_level: str = ""
    total_hits: int = 0
    sources_checked: list[str] = []
    hits: list[BatchScreeningHitSummary] = []


class BatchScreeningResponse(VyncoModel):
    """Response from a batch screening request."""

    results: list[BatchScreeningResultByUid] = []
