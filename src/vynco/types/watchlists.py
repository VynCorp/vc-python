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


class WatchlistCompanyEntry(VyncoModel):
    """An enriched company entry in a watchlist response."""

    uid: str
    name: str | None = None
    status: str | None = None
    canton: str | None = None


class WatchlistCompaniesResponse(VyncoModel):
    """Response containing companies in a watchlist.

    The ``uids`` field contains the bare UIDs for backwards compatibility.
    The ``companies`` field (added in v3.1) contains enriched entries with
    name, status, and canton.
    """

    uids: list[str] = []
    companies: list[WatchlistCompanyEntry] = []


class AddCompaniesResponse(VyncoModel):
    """Response from adding companies to a watchlist."""

    added: int = 0
