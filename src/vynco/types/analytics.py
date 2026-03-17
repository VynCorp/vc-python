from __future__ import annotations

from vynco.types.shared import VyncoModel


class CantonAnalytics(VyncoModel):
    """Analytics data for a Swiss canton."""

    canton: str
    company_count: int = 0
    active_count: int = 0
    change_count: int = 0


class AuditorAnalytics(VyncoModel):
    """Analytics data for an auditor firm."""

    auditor_name: str
    client_count: int = 0
    change_count: int = 0


class RfmSegment(VyncoModel):
    """Recency/Frequency/Monetary segmentation result."""

    segment: str = ""
    count: int = 0
    avg_recency: float = 0.0
    avg_frequency: float = 0.0
    avg_monetary: float = 0.0
