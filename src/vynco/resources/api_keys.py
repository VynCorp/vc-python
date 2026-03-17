from __future__ import annotations

from typing import TYPE_CHECKING

from vynco._response import Response, ResponseMeta
from vynco.types.api_keys import ApiKeyCreated, ApiKeyInfo

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client


class AsyncApiKeys:
    """Async API key operations."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def list(self) -> Response[list[ApiKeyInfo]]:
        """List all API keys."""
        return await self._client._request_model(
            "GET", "/api-keys", response_type=list[ApiKeyInfo],
        )

    async def create(
        self,
        *,
        name: str,
        is_test: bool = False,
        permissions: list[str] | None = None,
    ) -> Response[ApiKeyCreated]:
        """Create a new API key."""
        body = {
            "name": name,
            "isTest": is_test,
            "permissions": permissions or ["read"],
        }
        return await self._client._request_model(
            "POST", "/api-keys", json=body,
            response_type=ApiKeyCreated,
        )

    async def revoke(self, id: str) -> ResponseMeta:
        """Revoke an API key."""
        return await self._client._request_empty("DELETE", f"/api-keys/{id}")


class ApiKeys:
    """Sync API key operations."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def list(self) -> Response[list[ApiKeyInfo]]:
        """List all API keys."""
        return self._client._request_model(
            "GET", "/api-keys", response_type=list[ApiKeyInfo],
        )

    def create(
        self,
        *,
        name: str,
        is_test: bool = False,
        permissions: list[str] | None = None,
    ) -> Response[ApiKeyCreated]:
        """Create a new API key."""
        body = {
            "name": name,
            "isTest": is_test,
            "permissions": permissions or ["read"],
        }
        return self._client._request_model(
            "POST", "/api-keys", json=body,
            response_type=ApiKeyCreated,
        )

    def revoke(self, id: str) -> ResponseMeta:
        """Revoke an API key."""
        return self._client._request_empty("DELETE", f"/api-keys/{id}")
