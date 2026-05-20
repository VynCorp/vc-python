from __future__ import annotations

from vynco.types.shared import VyncoModel


class BulkScreeningMatch(VyncoModel):
    """A single sanctions match within a bulk screening result."""

    source: str = ""
    matched_name: str = ""
    score: float = 0.0


class BulkScreeningResult(VyncoModel):
    """Screening outcome for a single submitted entity."""

    name: str = ""
    entity_type: str = ""
    risk_level: str = ""
    hit_count: int = 0
    top_matches: list[BulkScreeningMatch] = []


class BulkScreeningResponse(VyncoModel):
    """Response from a bulk sanctions screening request."""

    total: int = 0
    hits_found: int = 0
    results: list[BulkScreeningResult] = []
    screened_at: str = ""


class BulkWatchlistResponse(VyncoModel):
    """Result of bulk-adding companies to a watchlist from a CSV upload."""

    added: int = 0
    skipped: int = 0
    skipped_uids: list[str] = []
