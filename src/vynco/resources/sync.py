from __future__ import annotations

from typing import TYPE_CHECKING

from vynco._response import Response
from vynco.types.sync import SyncStatusListResponse

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client


class AsyncSync:
    """Async data-pipeline freshness/status."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def status(self) -> Response[SyncStatusListResponse]:
        """Get freshness/health status for every tracked data pipeline."""
        return await self._client._request_model(
            "GET", "/v1/sync/status", response_type=SyncStatusListResponse
        )


class Sync:
    """Sync data-pipeline freshness/status."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def status(self) -> Response[SyncStatusListResponse]:
        """Get freshness/health status for every tracked data pipeline."""
        return self._client._request_model(
            "GET", "/v1/sync/status", response_type=SyncStatusListResponse
        )
