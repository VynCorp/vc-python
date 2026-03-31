from __future__ import annotations

import builtins
from typing import TYPE_CHECKING, Any

from vynco._response import Response, ResponseMeta
from vynco.types.api_keys import ApiKey, ApiKeyCreated

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client

_list = builtins.list


class AsyncApiKeys:
    """Async API key operations."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def create(
        self,
        *,
        name: str | None = None,
        environment: str | None = None,
        scopes: _list[str] | None = None,
    ) -> Response[ApiKeyCreated]:
        """Create a new API key. The full key is only returned once."""
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if environment is not None:
            body["environment"] = environment
        if scopes is not None:
            body["scopes"] = scopes
        return await self._client._request_model(
            "POST",
            "/v1/api-keys",
            json=body,
            response_type=ApiKeyCreated,
        )

    async def list(self) -> Response[_list[ApiKey]]:
        """List all API keys."""
        return await self._client._request_model(
            "GET",
            "/v1/api-keys",
            response_type=list[ApiKey],
        )

    async def revoke(self, id: str) -> ResponseMeta:
        """Revoke an API key."""
        return await self._client._request_empty("DELETE", f"/v1/api-keys/{id}")


class ApiKeys:
    """Sync API key operations."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def create(
        self,
        *,
        name: str | None = None,
        environment: str | None = None,
        scopes: _list[str] | None = None,
    ) -> Response[ApiKeyCreated]:
        """Create a new API key. The full key is only returned once."""
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if environment is not None:
            body["environment"] = environment
        if scopes is not None:
            body["scopes"] = scopes
        return self._client._request_model(
            "POST",
            "/v1/api-keys",
            json=body,
            response_type=ApiKeyCreated,
        )

    def list(self) -> Response[_list[ApiKey]]:
        """List all API keys."""
        return self._client._request_model(
            "GET",
            "/v1/api-keys",
            response_type=list[ApiKey],
        )

    def revoke(self, id: str) -> ResponseMeta:
        """Revoke an API key."""
        return self._client._request_empty("DELETE", f"/v1/api-keys/{id}")
