from __future__ import annotations

from typing import TYPE_CHECKING

from vynco._response import Response
from vynco.types.health import HealthResponse

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client


class AsyncHealth:
    """Async health operations."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def check(self) -> Response[HealthResponse]:
        """Check API health status."""
        return await self._client._request_model(
            "GET",
            "/health",
            response_type=HealthResponse,
        )


class Health:
    """Sync health operations."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def check(self) -> Response[HealthResponse]:
        """Check API health status."""
        return self._client._request_model(
            "GET",
            "/health",
            response_type=HealthResponse,
        )
