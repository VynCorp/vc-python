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
