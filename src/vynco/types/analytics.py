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
    auditor_name: str | None = None
    auditor_category: str | None = None
