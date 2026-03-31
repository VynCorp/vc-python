from __future__ import annotations

from typing import TYPE_CHECKING

from vynco._response import Response
from vynco.types.dashboard import DashboardResponse

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client


class AsyncDashboard:
    """Async dashboard operations."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def get(self) -> Response[DashboardResponse]:
        """Get admin dashboard data."""
        return await self._client._request_model(
            "GET",
            "/v1/dashboard",
            response_type=DashboardResponse,
        )


class Dashboard:
    """Sync dashboard operations."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def get(self) -> Response[DashboardResponse]:
        """Get admin dashboard data."""
        return self._client._request_model(
            "GET",
            "/v1/dashboard",
            response_type=DashboardResponse,
        )
