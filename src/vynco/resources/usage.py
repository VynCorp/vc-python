from __future__ import annotations

from typing import TYPE_CHECKING

from vynco._response import Response
from vynco.types.usage import UsageSnapshot

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client


class AsyncUsage:
    """Async usage operations."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def current(self) -> Response[UsageSnapshot]:
        """Get current usage snapshot (rate-limit groups and tier)."""
        return await self._client._request_model(
            "GET",
            "/v1/usage/current",
            response_type=UsageSnapshot,
        )


class Usage:
    """Sync usage operations."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def current(self) -> Response[UsageSnapshot]:
        """Get current usage snapshot (rate-limit groups and tier)."""
        return self._client._request_model(
            "GET",
            "/v1/usage/current",
            response_type=UsageSnapshot,
        )
