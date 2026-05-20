from __future__ import annotations

from vynco.types.shared import VyncoModel


class SyncStatus(VyncoModel):
    """Freshness/health status of a single data pipeline."""

    pipeline: str = ""
    status: str = ""
    items_processed: int = 0
    items_total: int = 0
    last_completed_at: str | None = None
    last_started_at: str | None = None
    health: str | None = None
    expected_run_interval_minutes: int | None = None
    alert_threshold_minutes: int | None = None
    depends_on: list[str] | None = None
    minutes_since_completion: float | None = None


class SyncStatusListResponse(VyncoModel):
    """Status of every tracked pipeline."""

    pipelines: list[SyncStatus] = []
