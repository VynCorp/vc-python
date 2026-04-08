from __future__ import annotations

from vynco.types.auditors import AuditorTenureStats
from vynco.types.shared import VyncoModel


class DataCompleteness(VyncoModel):
    """Data completeness metrics."""

    total_companies: int = 0
    enriched_companies: int = 0
    companies_with_industry: int = 0
    companies_with_geo: int = 0
    total_persons: int = 0
    total_changes: int = 0
    total_sogc_publications: int = 0


class PipelineStatus(VyncoModel):
    """Pipeline run status."""

    id: str
    status: str = ""
    items_processed: int = 0
    last_completed_at: str | None = None


class DashboardResponse(VyncoModel):
    """Admin dashboard response."""

    generated_at: str = ""
    data: DataCompleteness = DataCompleteness()
    pipelines: list[PipelineStatus] = []
    auditor_tenures: AuditorTenureStats = AuditorTenureStats()
