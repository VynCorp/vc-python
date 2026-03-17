from __future__ import annotations

from typing import TYPE_CHECKING

from vynco._response import Response
from vynco.types.persons import Person

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client


class AsyncPersons:
    """Async person operations."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def get(self, id: str) -> Response[Person]:
        """Get a person by ID."""
        return await self._client._request_model(
            "GET", f"/persons/{id}", response_type=Person,
        )

    async def search(self, *, name: str) -> Response[list[Person]]:
        """Search persons by name."""
        return await self._client._request_model(
            "POST", "/persons/search", json={"name": name},
            response_type=list[Person],
        )


class Persons:
    """Sync person operations."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def get(self, id: str) -> Response[Person]:
        """Get a person by ID."""
        return self._client._request_model(
            "GET", f"/persons/{id}", response_type=Person,
        )

    def search(self, *, name: str) -> Response[list[Person]]:
        """Search persons by name."""
        return self._client._request_model(
            "POST", "/persons/search", json={"name": name},
            response_type=list[Person],
        )
