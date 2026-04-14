from __future__ import annotations

from vynco.types.shared import VyncoModel


class Pipeline(VyncoModel):
    """A sales/tracking pipeline."""

    id: str = ""
    team_id: str = ""
    name: str = ""
    stages: list[str] = []
    created_at: int = 0


class PipelineEntry(VyncoModel):
    """An entry (company) within a pipeline stage."""

    id: str = ""
    pipeline_id: str = ""
    company_uid: str = ""
    company_name: str = ""
    canton: str | None = None
    stage: str = ""
    assigned_to_user_id: str | None = None
    assigned_to_name: str | None = None
    tier: int = 3
    score: float | None = None
    notes: str | None = None
    created_at: int = 0
    updated_at: int = 0


class PipelineWithEntries(VyncoModel):
    """A pipeline with its entries loaded."""

    id: str = ""
    team_id: str = ""
    name: str = ""
    stages: list[str] = []
    created_at: int = 0
    entries: list[PipelineEntry] = []
    total_entries: int = 0


class PipelineStats(VyncoModel):
    """Aggregate statistics for a pipeline."""

    by_stage: dict[str, int] = {}
    by_tier: dict[str, int] = {}
    total: int = 0
