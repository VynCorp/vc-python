from __future__ import annotations

import builtins
from typing import TYPE_CHECKING

from vynco._base_client import _build_params
from vynco._response import Response
from vynco.types.persons import (
    BoardMember,
    PersonDetail,
    PersonNetworkResponse,
    PersonSearchResult,
)
from vynco.types.shared import PaginatedResponse

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client

_list = builtins.list


class AsyncPersons:
    """Async person operations."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def board_members(
        self,
        uid: str,
        *,
        page: int | None = None,
        page_size: int | None = None,
    ) -> Response[_list[BoardMember]]:
        """Get board members of a company.

        Supports pagination via ``page`` (1-indexed) and ``page_size`` (max 500,
        default 100). For companies with large boards like UBS, paginating is
        essential to keep payloads manageable.
        """
        params = _build_params({"page": page, "pageSize": page_size})
        return await self._client._request_model(
            "GET",
            f"/v1/persons/board-members/{uid}",
            params=params or None,
            response_type=list[BoardMember],
        )

    async def search(
        self,
        *,
        q: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
    ) -> Response[PaginatedResponse[PersonSearchResult]]:
        """Search persons by name."""
        params = _build_params({k: v for k, v in locals().items() if k != "self"})
        return await self._client._request_model(
            "GET",
            "/v1/persons/search",
            params=params or None,
            response_type=PaginatedResponse[PersonSearchResult],
        )

    async def get(self, id: str) -> Response[PersonDetail]:
        """Get a person by ID with all their roles."""
        return await self._client._request_model(
            "GET",
            f"/v1/persons/{id}",
            response_type=PersonDetail,
        )

    async def network(self, id: str) -> Response[PersonNetworkResponse]:
        """Get a person-centric network view.

        Returns the person's companies, co-directors (persons they share
        directorships with), and summary statistics. Useful for compliance
        investigations where you start from a person rather than a company.
        """
        return await self._client._request_model(
            "GET",
            f"/v1/persons/{id}/network",
            response_type=PersonNetworkResponse,
        )


class Persons:
    """Sync person operations."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def board_members(
        self,
        uid: str,
        *,
        page: int | None = None,
        page_size: int | None = None,
    ) -> Response[_list[BoardMember]]:
        """Get board members of a company.

        Supports pagination via ``page`` (1-indexed) and ``page_size`` (max 500,
        default 100). For companies with large boards like UBS, paginating is
        essential to keep payloads manageable.
        """
        params = _build_params({"page": page, "pageSize": page_size})
        return self._client._request_model(
            "GET",
            f"/v1/persons/board-members/{uid}",
            params=params or None,
            response_type=list[BoardMember],
        )

    def search(
        self,
        *,
        q: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
    ) -> Response[PaginatedResponse[PersonSearchResult]]:
        """Search persons by name."""
        params = _build_params({k: v for k, v in locals().items() if k != "self"})
        return self._client._request_model(
            "GET",
            "/v1/persons/search",
            params=params or None,
            response_type=PaginatedResponse[PersonSearchResult],
        )

    def get(self, id: str) -> Response[PersonDetail]:
        """Get a person by ID with all their roles."""
        return self._client._request_model(
            "GET",
            f"/v1/persons/{id}",
            response_type=PersonDetail,
        )

    def network(self, id: str) -> Response[PersonNetworkResponse]:
        """Get a person-centric network view.

        Returns the person's companies, co-directors (persons they share
        directorships with), and summary statistics. Useful for compliance
        investigations where you start from a person rather than a company.
        """
        return self._client._request_model(
            "GET",
            f"/v1/persons/{id}/network",
            response_type=PersonNetworkResponse,
        )
