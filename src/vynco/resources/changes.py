from __future__ import annotations

from typing import TYPE_CHECKING

from vynco._base_client import _build_params
from vynco._response import Response
from vynco.types.changes import ChangeStatistics, CompanyChange
from vynco.types.shared import PaginatedResponse

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client


class AsyncChanges:
    """Async change feed operations."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def list(
        self,
        *,
        page: int | None = None,
        page_size: int | None = None,
    ) -> Response[PaginatedResponse[CompanyChange]]:
        """List recent changes across all companies."""
        params = _build_params(
            {k: v for k, v in locals().items() if k != "self"}
        )
        return await self._client._request_model(
            "GET", "/changes", params=params or None,
            response_type=PaginatedResponse[CompanyChange],
        )

    async def by_company(self, uid: str) -> Response[list[CompanyChange]]:
        """Get changes for a specific company."""
        return await self._client._request_model(
            "GET", f"/changes/company/{uid}",
            response_type=list[CompanyChange],
        )

    async def statistics(self) -> Response[ChangeStatistics]:
        """Get aggregate change statistics."""
        return await self._client._request_model(
            "GET", "/changes/statistics",
            response_type=ChangeStatistics,
        )


class Changes:
    """Sync change feed operations."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        *,
        page: int | None = None,
        page_size: int | None = None,
    ) -> Response[PaginatedResponse[CompanyChange]]:
        """List recent changes across all companies."""
        params = _build_params(
            {k: v for k, v in locals().items() if k != "self"}
        )
        return self._client._request_model(
            "GET", "/changes", params=params or None,
            response_type=PaginatedResponse[CompanyChange],
        )

    def by_company(self, uid: str) -> Response[list[CompanyChange]]:
        """Get changes for a specific company."""
        return self._client._request_model(
            "GET", f"/changes/company/{uid}",
            response_type=list[CompanyChange],
        )

    def statistics(self) -> Response[ChangeStatistics]:
        """Get aggregate change statistics."""
        return self._client._request_model(
            "GET", "/changes/statistics",
            response_type=ChangeStatistics,
        )
