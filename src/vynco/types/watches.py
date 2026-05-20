from __future__ import annotations

from vynco.types.shared import VyncoModel


class WatchItem(VyncoModel):
    """A lightweight per-company watch entry."""

    company_uid: str = ""
    added_at: str = ""
