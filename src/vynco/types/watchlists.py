from __future__ import annotations

from vynco.types.shared import VyncoModel


class Watchlist(VyncoModel):
    """A watchlist."""

    id: str
    name: str
    description: str = ""
    created_at: str = ""
    updated_at: str = ""


class WatchlistSummary(VyncoModel):
    """Watchlist summary (used in list responses)."""

    id: str
    name: str
    description: str = ""
    company_count: int = 0
    created_at: str = ""


class WatchlistCompaniesResponse(VyncoModel):
    """Response containing UIDs of companies in a watchlist."""

    uids: list[str] = []


class AddCompaniesResponse(VyncoModel):
    """Response from adding companies to a watchlist."""

    added: int = 0
