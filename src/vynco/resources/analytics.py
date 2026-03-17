from __future__ import annotations

from typing import TYPE_CHECKING, Any

from vynco._response import Response
from vynco.types.analytics import AuditorAnalytics, CantonAnalytics, RfmSegment

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client


class AsyncAnalytics:
    """Async analytics operations."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def cantons(self) -> Response[list[CantonAnalytics]]:
        """Get analytics by Swiss canton."""
        return await self._client._request_model(
            "GET", "/analytics/cantons",
            response_type=list[CantonAnalytics],
        )

    async def auditors(self) -> Response[list[AuditorAnalytics]]:
        """Get analytics by auditor firm."""
        return await self._client._request_model(
            "GET", "/analytics/auditors",
            response_type=list[AuditorAnalytics],
        )

    async def rfm_segments(self) -> Response[list[RfmSegment]]:
        """Get RFM (Recency/Frequency/Monetary) segmentation results."""
        return await self._client._request_model(
            "GET", "/analytics/rfm-segments",
            response_type=list[RfmSegment],
        )

    async def velocity(self) -> Response[dict[str, Any]]:
        """Get change velocity analytics."""
        return await self._client._request_model(
            "GET", "/analytics/velocity",
            response_type=dict,
        )


class Analytics:
    """Sync analytics operations."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def cantons(self) -> Response[list[CantonAnalytics]]:
        """Get analytics by Swiss canton."""
        return self._client._request_model(
            "GET", "/analytics/cantons",
            response_type=list[CantonAnalytics],
        )

    def auditors(self) -> Response[list[AuditorAnalytics]]:
        """Get analytics by auditor firm."""
        return self._client._request_model(
            "GET", "/analytics/auditors",
            response_type=list[AuditorAnalytics],
        )

    def rfm_segments(self) -> Response[list[RfmSegment]]:
        """Get RFM (Recency/Frequency/Monetary) segmentation results."""
        return self._client._request_model(
            "GET", "/analytics/rfm-segments",
            response_type=list[RfmSegment],
        )

    def velocity(self) -> Response[dict[str, Any]]:
        """Get change velocity analytics."""
        return self._client._request_model(
            "GET", "/analytics/velocity",
            response_type=dict,
        )
