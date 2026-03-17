from __future__ import annotations

from typing import TYPE_CHECKING

from vynco._response import Response
from vynco.types.users import UserProfile

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client


class AsyncUsers:
    """Async user operations."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def me(self) -> Response[UserProfile]:
        """Get the authenticated user's profile."""
        return await self._client._request_model(
            "GET", "/users/me", response_type=UserProfile,
        )

    async def update_profile(
        self,
        *,
        name: str | None = None,
        email: str | None = None,
    ) -> Response[UserProfile]:
        """Update the authenticated user's profile."""
        body: dict = {}
        if name is not None:
            body["name"] = name
        if email is not None:
            body["email"] = email
        return await self._client._request_model(
            "PUT", "/users/me", json=body,
            response_type=UserProfile,
        )


class Users:
    """Sync user operations."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def me(self) -> Response[UserProfile]:
        """Get the authenticated user's profile."""
        return self._client._request_model(
            "GET", "/users/me", response_type=UserProfile,
        )

    def update_profile(
        self,
        *,
        name: str | None = None,
        email: str | None = None,
    ) -> Response[UserProfile]:
        """Update the authenticated user's profile."""
        body: dict = {}
        if name is not None:
            body["name"] = name
        if email is not None:
            body["email"] = email
        return self._client._request_model(
            "PUT", "/users/me", json=body,
            response_type=UserProfile,
        )
