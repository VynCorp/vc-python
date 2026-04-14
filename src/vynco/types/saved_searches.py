from __future__ import annotations

from typing import Any

from vynco.types.shared import VyncoModel


class SavedSearch(VyncoModel):
    """A saved search query that can be scheduled or linked to alerts."""

    id: str = ""
    name: str = ""
    description: str | None = None
    search_params: Any = None
    is_scheduled: bool = False
    schedule_frequency: str | None = None
    last_run_at: str | None = None
    last_result_count: int | None = None
    created_at: str = ""
    updated_at: str = ""
