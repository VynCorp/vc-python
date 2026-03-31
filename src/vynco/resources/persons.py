from __future__ import annotations

import builtins
from typing import TYPE_CHECKING

from vynco._response import Response
from vynco.types.persons import BoardMember

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client

_list = builtins.list


class AsyncPersons:
    """Async person operations."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def board_members(self, uid: str) -> Response[_list[BoardMember]]:
        """Get board members of a company."""
        return await self._client._request_model(
            "GET",
            f"/v1/persons/board-members/{uid}",
            response_type=list[BoardMember],
        )


class Persons:
    """Sync person operations."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def board_members(self, uid: str) -> Response[_list[BoardMember]]:
        """Get board members of a company."""
        return self._client._request_model(
            "GET",
            f"/v1/persons/board-members/{uid}",
            response_type=list[BoardMember],
        )
