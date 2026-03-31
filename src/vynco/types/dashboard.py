from __future__ import annotations

from vynco.types.auditors import AuditorTenureStats
from vynco.types.shared import VyncoModel


class DataCompleteness(VyncoModel):
    """Data completeness metrics."""

    total_companies: int = 0
    with_canton: int = 0
    with_status: int = 0
    with_legal_form: int = 0
    with_capital: int = 0
    with_industry: int = 0
    with_auditor: int = 0
    completeness_pct: float = 0.0


class PipelineStatus(VyncoModel):
    """Pipeline run status."""

    name: str
    last_run: str | None = None
    status: str = ""
    records_processed: int | None = None
    duration_seconds: float | None = None


class DashboardResponse(VyncoModel):
    """Admin dashboard response."""

    generated_at: str = ""
    data: DataCompleteness = DataCompleteness()
    pipelines: list[PipelineStatus] = []
    auditor_tenures: AuditorTenureStats = AuditorTenureStats()
