from __future__ import annotations

from vynco.types.shared import VyncoModel


class IndustrySummary(VyncoModel):
    """Summary of an industry with company count."""

    industry: str = ""
    company_count: int = 0


class IndustryListResponse(VyncoModel):
    """List of available industries."""

    industries: list[IndustrySummary] = []
    total: int = 0


class IndustryCompanyEntry(VyncoModel):
    """A company entry within an industry report."""

    uid: str = ""
    name: str = ""
    canton: str | None = None
    share_capital: float | None = None
    status: str | None = None


class CantonCount(VyncoModel):
    """Canton distribution entry."""

    canton: str = ""
    count: int = 0


class AuditorCount(VyncoModel):
    """Auditor concentration entry."""

    auditor_name: str = ""
    count: int = 0


class StatusCount(VyncoModel):
    """Status distribution entry."""

    status: str = ""
    count: int = 0


class IndustryReportResponse(VyncoModel):
    """Detailed industry report with analytics."""

    industry: str = ""
    company_count: int = 0
    avg_capital: float | None = None
    median_capital: float | None = None
    top_companies: list[IndustryCompanyEntry] = []
    canton_distribution: list[CantonCount] = []
    recent_changes: int = 0
    auditor_concentration: list[AuditorCount] = []
    status_distribution: list[StatusCount] = []
    generated_at: str = ""


class GeneratedIndustryReport(VyncoModel):
    """AI-generated industry narrative report."""

    industry: str = ""
    report: str = ""
    sources: list[str] = []
    generated_at: str = ""
