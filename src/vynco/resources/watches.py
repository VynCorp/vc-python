from __future__ import annotations

import builtins
from typing import TYPE_CHECKING

from vynco._response import Response, ResponseMeta
from vynco.types.watches import WatchItem

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client

_list = builtins.list


class AsyncWatches:
    """Async lightweight per-company watches (distinct from watchlists)."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def list(self) -> Response[_list[WatchItem]]:
        """List the authenticated user's watched companies."""
        return await self._client._request_model(
            "GET", "/v1/watches", response_type=list[WatchItem]
        )

    async def add(self, *, company_uid: str) -> ResponseMeta:
        """Start watching a company."""
        return await self._client._request_empty(
            "POST", "/v1/watches", json={"companyUid": company_uid}
        )

    async def remove(self, company_uid: str) -> ResponseMeta:
        """Stop watching a company."""
        return await self._client._request_empty("DELETE", f"/v1/watches/{company_uid}")


class Watches:
    """Sync lightweight per-company watches (distinct from watchlists)."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def list(self) -> Response[_list[WatchItem]]:
        """List the authenticated user's watched companies."""
        return self._client._request_model("GET", "/v1/watches", response_type=list[WatchItem])

    def add(self, *, company_uid: str) -> ResponseMeta:
        """Start watching a company."""
        return self._client._request_empty("POST", "/v1/watches", json={"companyUid": company_uid})

    def remove(self, company_uid: str) -> ResponseMeta:
        """Stop watching a company."""
        return self._client._request_empty("DELETE", f"/v1/watches/{company_uid}")
