from __future__ import annotations

from typing import TYPE_CHECKING

from vynco._response import Response
from vynco.types.teams import Team

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client


class AsyncTeams:
    """Async team operations."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def me(self) -> Response[Team]:
        """Get the current team."""
        return await self._client._request_model(
            "GET", "/teams/me", response_type=Team,
        )

    async def create(self, *, name: str, slug: str) -> Response[Team]:
        """Create a new team."""
        return await self._client._request_model(
            "POST", "/teams", json={"name": name, "slug": slug},
            response_type=Team,
        )


class Teams:
    """Sync team operations."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def me(self) -> Response[Team]:
        """Get the current team."""
        return self._client._request_model(
            "GET", "/teams/me", response_type=Team,
        )

    def create(self, *, name: str, slug: str) -> Response[Team]:
        """Create a new team."""
        return self._client._request_model(
            "POST", "/teams", json={"name": name, "slug": slug},
            response_type=Team,
        )
