from __future__ import annotations

import builtins
from typing import TYPE_CHECKING

from vynco._base_client import _build_params
from vynco._response import Response
from vynco.types.changes import ChangeStatistics, CompanyChange
from vynco.types.shared import PaginatedResponse

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client

_list = builtins.list


class AsyncChanges:
    """Async change feed operations."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def list(
        self,
        *,
        change_type: str | None = None,
        since: str | None = None,
        until: str | None = None,
        company_search: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
    ) -> Response[PaginatedResponse[CompanyChange]]:
        """List recent changes across all companies."""
        params = _build_params({k: v for k, v in locals().items() if k != "self"})
        return await self._client._request_model(
            "GET",
            "/v1/changes",
            params=params or None,
            response_type=PaginatedResponse[CompanyChange],
        )

    async def by_company(self, uid: str) -> Response[_list[CompanyChange]]:
        """Get changes for a specific company."""
        return await self._client._request_model(
            "GET",
            f"/v1/changes/{uid}",
            response_type=list[CompanyChange],
        )

    async def statistics(self) -> Response[ChangeStatistics]:
        """Get aggregate change statistics."""
        return await self._client._request_model(
            "GET",
            "/v1/changes/statistics",
            response_type=ChangeStatistics,
        )


class Changes:
    """Sync change feed operations."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        *,
        change_type: str | None = None,
        since: str | None = None,
        until: str | None = None,
        company_search: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
    ) -> Response[PaginatedResponse[CompanyChange]]:
        """List recent changes across all companies."""
        params = _build_params({k: v for k, v in locals().items() if k != "self"})
        return self._client._request_model(
            "GET",
            "/v1/changes",
            params=params or None,
            response_type=PaginatedResponse[CompanyChange],
        )

    def by_company(self, uid: str) -> Response[_list[CompanyChange]]:
        """Get changes for a specific company."""
        return self._client._request_model(
            "GET",
            f"/v1/changes/{uid}",
            response_type=list[CompanyChange],
        )

    def statistics(self) -> Response[ChangeStatistics]:
        """Get aggregate change statistics."""
        return self._client._request_model(
            "GET",
            "/v1/changes/statistics",
            response_type=ChangeStatistics,
        )
