from __future__ import annotations

import builtins
from typing import TYPE_CHECKING, Any

from vynco._base_client import _build_params
from vynco._response import Response
from vynco.types.analytics import (
    AnomalyResponse,
    AuditCandidate,
    AuditorMarketShare,
    CantonDistribution,
    ClusterResponse,
    CohortResponse,
    RfmSegmentsResponse,
)
from vynco.types.shared import PaginatedResponse

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client

_list = builtins.list


class AsyncAnalytics:
    """Async analytics operations."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def cantons(self) -> Response[_list[CantonDistribution]]:
        """Get analytics by Swiss canton."""
        return await self._client._request_model(
            "GET",
            "/v1/analytics/cantons",
            response_type=list[CantonDistribution],
        )

    async def auditors(self) -> Response[_list[AuditorMarketShare]]:
        """Get analytics by auditor firm."""
        return await self._client._request_model(
            "GET",
            "/v1/analytics/auditors",
            response_type=list[AuditorMarketShare],
        )

    async def cluster(
        self,
        *,
        algorithm: str,
        k: int | None = None,
    ) -> Response[ClusterResponse]:
        """Run clustering on companies."""
        body: dict[str, Any] = {"algorithm": algorithm}
        if k is not None:
            body["k"] = k
        return await self._client._request_model(
            "POST",
            "/v1/analytics/cluster",
            json=body,
            response_type=ClusterResponse,
        )

    async def anomalies(
        self,
        *,
        algorithm: str,
        threshold: float | None = None,
    ) -> Response[AnomalyResponse]:
        """Detect anomalies in company data."""
        body: dict[str, Any] = {"algorithm": algorithm}
        if threshold is not None:
            body["threshold"] = threshold
        return await self._client._request_model(
            "POST",
            "/v1/analytics/anomalies",
            json=body,
            response_type=AnomalyResponse,
        )

    async def rfm_segments(self) -> Response[RfmSegmentsResponse]:
        """Get RFM segmentation results."""
        return await self._client._request_model(
            "GET",
            "/v1/analytics/rfm-segments",
            response_type=RfmSegmentsResponse,
        )

    async def cohorts(
        self,
        *,
        group_by: str | None = None,
        metric: str | None = None,
    ) -> Response[CohortResponse]:
        """Get cohort analytics."""
        params = _build_params({k: v for k, v in locals().items() if k != "self"})
        return await self._client._request_model(
            "GET",
            "/v1/analytics/cohorts",
            params=params or None,
            response_type=CohortResponse,
        )

    async def candidates(
        self,
        *,
        sort_by: str | None = None,
        canton: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
    ) -> Response[PaginatedResponse[AuditCandidate]]:
        """Get audit candidate companies."""
        params = _build_params({k: v for k, v in locals().items() if k != "self"})
        return await self._client._request_model(
            "GET",
            "/v1/analytics/candidates",
            params=params or None,
            response_type=PaginatedResponse[AuditCandidate],
        )


class Analytics:
    """Sync analytics operations."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def cantons(self) -> Response[_list[CantonDistribution]]:
        """Get analytics by Swiss canton."""
        return self._client._request_model(
            "GET",
            "/v1/analytics/cantons",
            response_type=list[CantonDistribution],
        )

    def auditors(self) -> Response[_list[AuditorMarketShare]]:
        """Get analytics by auditor firm."""
        return self._client._request_model(
            "GET",
            "/v1/analytics/auditors",
            response_type=list[AuditorMarketShare],
        )

    def cluster(
        self,
        *,
        algorithm: str,
        k: int | None = None,
    ) -> Response[ClusterResponse]:
        """Run clustering on companies."""
        body: dict[str, Any] = {"algorithm": algorithm}
        if k is not None:
            body["k"] = k
        return self._client._request_model(
            "POST",
            "/v1/analytics/cluster",
            json=body,
            response_type=ClusterResponse,
        )

    def anomalies(
        self,
        *,
        algorithm: str,
        threshold: float | None = None,
    ) -> Response[AnomalyResponse]:
        """Detect anomalies in company data."""
        body: dict[str, Any] = {"algorithm": algorithm}
        if threshold is not None:
            body["threshold"] = threshold
        return self._client._request_model(
            "POST",
            "/v1/analytics/anomalies",
            json=body,
            response_type=AnomalyResponse,
        )

    def rfm_segments(self) -> Response[RfmSegmentsResponse]:
        """Get RFM segmentation results."""
        return self._client._request_model(
            "GET",
            "/v1/analytics/rfm-segments",
            response_type=RfmSegmentsResponse,
        )

    def cohorts(
        self,
        *,
        group_by: str | None = None,
        metric: str | None = None,
    ) -> Response[CohortResponse]:
        """Get cohort analytics."""
        params = _build_params({k: v for k, v in locals().items() if k != "self"})
        return self._client._request_model(
            "GET",
            "/v1/analytics/cohorts",
            params=params or None,
            response_type=CohortResponse,
        )

    def candidates(
        self,
        *,
        sort_by: str | None = None,
        canton: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
    ) -> Response[PaginatedResponse[AuditCandidate]]:
        """Get audit candidate companies."""
        params = _build_params({k: v for k, v in locals().items() if k != "self"})
        return self._client._request_model(
            "GET",
            "/v1/analytics/candidates",
            params=params or None,
            response_type=PaginatedResponse[AuditCandidate],
        )
