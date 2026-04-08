from __future__ import annotations

from vynco.types.shared import VyncoModel


class AuditorTenure(VyncoModel):
    """A single auditor tenure record."""

    id: str
    company_uid: str = ""
    company_name: str = ""
    auditor_name: str = ""
    appointed_at: str | None = None
    resigned_at: str | None = None
    tenure_years: float | None = None
    is_current: bool = False
    source: str = ""


class AuditorHistoryResponse(VyncoModel):
    """Auditor history for a company."""

    company_uid: str
    company_name: str
    current_auditor: AuditorTenure | None = None
    history: list[AuditorTenure] = []


class LongestTenure(VyncoModel):
    """The longest current auditor tenure."""

    company_uid: str = ""
    company_name: str = ""
    auditor_name: str = ""
    tenure_years: float = 0.0


class AuditorTenureStats(VyncoModel):
    """Auditor tenure aggregate statistics."""

    total_tracked: int = 0
    current_auditors: int = 0
    tenures_over_10_years: int = 0
    tenures_over_7_years: int = 0
    avg_tenure_years: float = 0.0
    longest_tenure: LongestTenure | None = None
