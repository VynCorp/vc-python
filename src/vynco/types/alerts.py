from __future__ import annotations

from typing import Any

from vynco.types.shared import VyncoModel


class Alert(VyncoModel):
    """A saved alert that triggers on matching query results."""

    id: str
    name: str
    query_params: Any = None
    webhook_url: str | None = None
    frequency: str = ""
    is_active: bool = False
    saved_search_id: str | None = None
    last_triggered_at: str | None = None
    last_result_count: int | None = None
    trigger_count: int = 0
    created_at: str = ""
    updated_at: str = ""
