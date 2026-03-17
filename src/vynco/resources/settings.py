from __future__ import annotations

from typing import TYPE_CHECKING, Any

from vynco._response import Response

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client


class AsyncSettings:
    """Async settings operations."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def get(self) -> Response[dict[str, Any]]:
        """Get user preferences."""
        return await self._client._request_model(
            "GET", "/settings", response_type=dict,
        )

    async def update(self, preferences: dict[str, Any]) -> Response[dict[str, Any]]:
        """Update user preferences."""
        return await self._client._request_model(
            "PUT", "/settings", json=preferences,
            response_type=dict,
        )


class Settings:
    """Sync settings operations."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def get(self) -> Response[dict[str, Any]]:
        """Get user preferences."""
        return self._client._request_model(
            "GET", "/settings", response_type=dict,
        )

    def update(self, preferences: dict[str, Any]) -> Response[dict[str, Any]]:
        """Update user preferences."""
        return self._client._request_model(
            "PUT", "/settings", json=preferences,
            response_type=dict,
        )
