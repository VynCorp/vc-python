from __future__ import annotations

from vynco.types.shared import VyncoModel


class SanctionEntry(VyncoModel):
    """A single sanctions list entry."""

    seco_id: str = ""
    entity_type: str = ""
    name: str = ""
    aliases: list[str] = []
    nationality: str | None = None
    date_of_birth: str | None = None
    address: str | None = None
    program: str = ""
    listed_since: str | None = None
    source_url: str = ""


class SanctionsListResponse(VyncoModel):
    """Paginated sanctions browse response."""

    items: list[SanctionEntry] = []
    total: int = 0
    page: int = 0
    page_size: int = 0
