from __future__ import annotations

from typing import TYPE_CHECKING, Any

from vynco._response import Response
from vynco.types.screening import BatchScreeningResponse, ScreeningResponse

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client


class AsyncScreening:
    """Async screening operations."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def screen(
        self,
        *,
        name: str,
        uid: str | None = None,
        sources: list[str] | None = None,
    ) -> Response[ScreeningResponse]:
        """Run compliance screening against sanctions lists."""
        body: dict[str, Any] = {"name": name}
        if uid is not None:
            body["uid"] = uid
        if sources is not None:
            body["sources"] = sources
        return await self._client._request_model(
            "POST",
            "/v1/screening",
            json=body,
            response_type=ScreeningResponse,
        )

    async def batch(self, *, uids: list[str]) -> Response[BatchScreeningResponse]:
        """Screen up to 100 companies against sanctions lists in a single call."""
        return await self._client._request_model(
            "POST",
            "/v1/screening/batch",
            json={"uids": uids},
            response_type=BatchScreeningResponse,
        )


class Screening:
    """Sync screening operations."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def screen(
        self,
        *,
        name: str,
        uid: str | None = None,
        sources: list[str] | None = None,
    ) -> Response[ScreeningResponse]:
        """Run compliance screening against sanctions lists."""
        body: dict[str, Any] = {"name": name}
        if uid is not None:
            body["uid"] = uid
        if sources is not None:
            body["sources"] = sources
        return self._client._request_model(
            "POST",
            "/v1/screening",
            json=body,
            response_type=ScreeningResponse,
        )

    def batch(self, *, uids: list[str]) -> Response[BatchScreeningResponse]:
        """Screen up to 100 companies against sanctions lists in a single call."""
        return self._client._request_model(
            "POST",
            "/v1/screening/batch",
            json={"uids": uids},
            response_type=BatchScreeningResponse,
        )
