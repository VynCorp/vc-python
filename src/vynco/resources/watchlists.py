from __future__ import annotations

import builtins
from typing import TYPE_CHECKING, Any

from vynco._base_client import _build_params
from vynco._response import Response, ResponseMeta
from vynco.types.companies import EventListResponse
from vynco.types.watchlists import (
    AddCompaniesResponse,
    Watchlist,
    WatchlistCompaniesResponse,
    WatchlistSummary,
)

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client

_list = builtins.list


class AsyncWatchlists:
    """Async watchlist operations."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def list(self) -> Response[_list[WatchlistSummary]]:
        """List all watchlists."""
        return await self._client._request_model(
            "GET",
            "/v1/watchlists",
            response_type=list[WatchlistSummary],
        )

    async def create(
        self,
        *,
        name: str,
        description: str | None = None,
    ) -> Response[Watchlist]:
        """Create a new watchlist."""
        body: dict[str, Any] = {"name": name}
        if description is not None:
            body["description"] = description
        return await self._client._request_model(
            "POST",
            "/v1/watchlists",
            json=body,
            response_type=Watchlist,
        )

    async def delete(self, id: str) -> ResponseMeta:
        """Delete a watchlist."""
        return await self._client._request_empty("DELETE", f"/v1/watchlists/{id}")

    async def companies(self, id: str) -> Response[WatchlistCompaniesResponse]:
        """Get companies in a watchlist."""
        return await self._client._request_model(
            "GET",
            f"/v1/watchlists/{id}/companies",
            response_type=WatchlistCompaniesResponse,
        )

    async def add_companies(self, id: str, *, uids: _list[str]) -> Response[AddCompaniesResponse]:
        """Add companies to a watchlist."""
        return await self._client._request_model(
            "POST",
            f"/v1/watchlists/{id}/companies",
            json={"uids": uids},
            response_type=AddCompaniesResponse,
        )

    async def remove_company(self, id: str, uid: str) -> ResponseMeta:
        """Remove a company from a watchlist."""
        return await self._client._request_empty(
            "DELETE",
            f"/v1/watchlists/{id}/companies/{uid}",
        )

    async def events(self, id: str, *, limit: int | None = None) -> Response[EventListResponse]:
        """Get events for a watchlist."""
        params = _build_params({"limit": limit})
        return await self._client._request_model(
            "GET",
            f"/v1/watchlists/{id}/events",
            params=params or None,
            response_type=EventListResponse,
        )


class Watchlists:
    """Sync watchlist operations."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def list(self) -> Response[_list[WatchlistSummary]]:
        """List all watchlists."""
        return self._client._request_model(
            "GET",
            "/v1/watchlists",
            response_type=list[WatchlistSummary],
        )

    def create(
        self,
        *,
        name: str,
        description: str | None = None,
    ) -> Response[Watchlist]:
        """Create a new watchlist."""
        body: dict[str, Any] = {"name": name}
        if description is not None:
            body["description"] = description
        return self._client._request_model(
            "POST",
            "/v1/watchlists",
            json=body,
            response_type=Watchlist,
        )

    def delete(self, id: str) -> ResponseMeta:
        """Delete a watchlist."""
        return self._client._request_empty("DELETE", f"/v1/watchlists/{id}")

    def companies(self, id: str) -> Response[WatchlistCompaniesResponse]:
        """Get companies in a watchlist."""
        return self._client._request_model(
            "GET",
            f"/v1/watchlists/{id}/companies",
            response_type=WatchlistCompaniesResponse,
        )

    def add_companies(self, id: str, *, uids: _list[str]) -> Response[AddCompaniesResponse]:
        """Add companies to a watchlist."""
        return self._client._request_model(
            "POST",
            f"/v1/watchlists/{id}/companies",
            json={"uids": uids},
            response_type=AddCompaniesResponse,
        )

    def remove_company(self, id: str, uid: str) -> ResponseMeta:
        """Remove a company from a watchlist."""
        return self._client._request_empty(
            "DELETE",
            f"/v1/watchlists/{id}/companies/{uid}",
        )

    def events(self, id: str, *, limit: int | None = None) -> Response[EventListResponse]:
        """Get events for a watchlist."""
        params = _build_params({"limit": limit})
        return self._client._request_model(
            "GET",
            f"/v1/watchlists/{id}/events",
            params=params or None,
            response_type=EventListResponse,
        )
