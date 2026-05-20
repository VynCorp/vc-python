from __future__ import annotations

from typing import TYPE_CHECKING, Any

from vynco._response import Response
from vynco.types.settings import Preferences

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client


class AsyncSettings:
    """Async user settings / preferences."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def get_preferences(self) -> Response[Preferences]:
        """Get the authenticated user's preferences."""
        return await self._client._request_model(
            "GET", "/v1/settings/preferences", response_type=Preferences
        )

    async def update_preferences(self, preferences: dict[str, Any]) -> Response[Preferences]:
        """Replace the authenticated user's preferences with ``preferences``."""
        return await self._client._request_model(
            "PUT", "/v1/settings/preferences", json=preferences, response_type=Preferences
        )


class Settings:
    """Sync user settings / preferences."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def get_preferences(self) -> Response[Preferences]:
        """Get the authenticated user's preferences."""
        return self._client._request_model(
            "GET", "/v1/settings/preferences", response_type=Preferences
        )

    def update_preferences(self, preferences: dict[str, Any]) -> Response[Preferences]:
        """Replace the authenticated user's preferences with ``preferences``."""
        return self._client._request_model(
            "PUT", "/v1/settings/preferences", json=preferences, response_type=Preferences
        )
