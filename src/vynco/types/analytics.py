from __future__ import annotations

from typing import Any

from vynco.types.shared import VyncoModel


class CantonDistribution(VyncoModel):
    """Analytics by Swiss canton."""

    canton: str = ""
    count: int = 0
    percentage: float = 0.0


class AuditorMarketShare(VyncoModel):
    """Analytics by auditor firm."""

    auditor_name: str = ""
    company_count: int = 0
    percentage: float = 0.0


class ClusterResult(VyncoModel):
    """A single cluster result."""

    id: int = 0
    centroid: Any = None
    company_count: int = 0
    sample_companies: list[str] = []


class ClusterResponse(VyncoModel):
    """Clustering response."""

    clusters: list[ClusterResult] = []


class AnomalyResponse(VyncoModel):
    """Anomaly detection response."""

    anomalies: list[Any] = []
    total_scanned: int = 0
    threshold: float = 0.0


class RfmSegment(VyncoModel):
    """An RFM segment."""

    name: str = ""
    count: int = 0
    description: str = ""


class RfmSegmentsResponse(VyncoModel):
    """RFM segmentation results."""

    segments: list[RfmSegment] = []


class CohortEntry(VyncoModel):
    """A single cohort entry."""

    group: str = ""
    count: int = 0
    metric: str = ""


class CohortResponse(VyncoModel):
    """Cohort analytics response."""

    cohorts: list[CohortEntry] = []
    group_by: str = ""
    metric: str = ""


class AuditCandidate(VyncoModel):
    """An audit candidate company."""

    uid: str
    name: str
    canton: str | None = None
    legal_form: str | None = None
    share_capital: float | None = None
    currency: str | None = None
    auditor_name: str | None = None
    auditor_category: str | None = None
    change_count: int = 0
    score: int = 0
    risk_indicators: list[str] = []
    auditor_tenure_years: float | None = None


class FlowDataPoint(VyncoModel):
    """A single period of company registration/dissolution flow."""

    period: str = ""
    group: str = ""
    registrations: int = 0
    dissolutions: int = 0
    net: int = 0


class FlowsResponse(VyncoModel):
    """Market flow analytics — registrations and dissolutions over time.

    ``data_coverage_note`` surfaces known asymmetries in the underlying data
    (e.g. dissolution detection started later than registration detection,
    so earlier periods may under-report net formation rate).
    """

    flows: list[FlowDataPoint] = []
    data_coverage_note: str | None = None


class MigrationFlow(VyncoModel):
    """A single canton-to-canton migration flow."""

    from_canton: str = ""
    to_canton: str = ""
    count: int = 0


class MigrationResponse(VyncoModel):
    """Canton migration analytics — tracking legal seat changes between cantons."""

    flows: list[MigrationFlow] = []
    top_flows: list[MigrationFlow] = []
    data_coverage_note: str | None = None


class BenchmarkDimension(VyncoModel):
    """A single benchmarking dimension comparing a company to its industry peers.

    ``industry_median`` and ``percentile`` are null when too few peers have
    data; ``company_value`` and ``peers_with_data`` are always present.
    """

    name: str = ""
    company_value: float = 0.0
    industry_median: float | None = None
    percentile: float | None = None
    peers_with_data: int = 0


class BenchmarkResponse(VyncoModel):
    """Industry benchmarking response — how a company compares to its peers."""

    uid: str = ""
    company_name: str = ""
    industry: str | None = None
    peer_count: int = 0
    dimensions: list[BenchmarkDimension] = []


class ProspectItem(VyncoModel):
    """An audit-mandate prospect (company likely to switch auditor)."""

    company_uid: str = ""
    company_name: str = ""
    canton: str | None = None
    auditor_name: str | None = None
    auditor_category: str | None = None
    tenure_years: float | None = None
    opportunity_score: int = 0
    pitch_readiness: str = ""
    estimated_mandate_value: float | None = None
    tenure_risk: str = ""
    share_capital: float | None = None
    currency: str | None = None
