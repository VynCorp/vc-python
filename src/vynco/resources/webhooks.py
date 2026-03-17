from __future__ import annotations

from typing import TYPE_CHECKING

from vynco._response import Response, ResponseMeta
from vynco.types.webhooks import Webhook, WebhookCreated

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client


class AsyncWebhooks:
    """Async webhook operations."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def list(self) -> Response[list[Webhook]]:
        """List all webhooks."""
        return await self._client._request_model(
            "GET", "/webhooks", response_type=list[Webhook],
        )

    async def create(
        self, *, url: str, events: list[str]
    ) -> Response[WebhookCreated]:
        """Create a new webhook subscription."""
        return await self._client._request_model(
            "POST", "/webhooks",
            json={"url": url, "events": events},
            response_type=WebhookCreated,
        )

    async def get(self, id: str) -> Response[Webhook]:
        """Get a webhook by ID."""
        return await self._client._request_model(
            "GET", f"/webhooks/{id}", response_type=Webhook,
        )

    async def update(
        self,
        id: str,
        *,
        url: str | None = None,
        events: list[str] | None = None,
        status: str | None = None,
    ) -> Response[Webhook]:
        """Update a webhook."""
        body: dict = {}
        if url is not None:
            body["url"] = url
        if events is not None:
            body["events"] = events
        if status is not None:
            body["status"] = status
        return await self._client._request_model(
            "PUT", f"/webhooks/{id}", json=body,
            response_type=Webhook,
        )

    async def delete(self, id: str) -> ResponseMeta:
        """Delete a webhook."""
        return await self._client._request_empty("DELETE", f"/webhooks/{id}")

    async def test(self, id: str) -> ResponseMeta:
        """Send a test event to a webhook."""
        return await self._client._request_empty("POST", f"/webhooks/{id}/test")


class Webhooks:
    """Sync webhook operations."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def list(self) -> Response[list[Webhook]]:
        """List all webhooks."""
        return self._client._request_model(
            "GET", "/webhooks", response_type=list[Webhook],
        )

    def create(
        self, *, url: str, events: list[str]
    ) -> Response[WebhookCreated]:
        """Create a new webhook subscription."""
        return self._client._request_model(
            "POST", "/webhooks",
            json={"url": url, "events": events},
            response_type=WebhookCreated,
        )

    def get(self, id: str) -> Response[Webhook]:
        """Get a webhook by ID."""
        return self._client._request_model(
            "GET", f"/webhooks/{id}", response_type=Webhook,
        )

    def update(
        self,
        id: str,
        *,
        url: str | None = None,
        events: list[str] | None = None,
        status: str | None = None,
    ) -> Response[Webhook]:
        """Update a webhook."""
        body: dict = {}
        if url is not None:
            body["url"] = url
        if events is not None:
            body["events"] = events
        if status is not None:
            body["status"] = status
        return self._client._request_model(
            "PUT", f"/webhooks/{id}", json=body,
            response_type=Webhook,
        )

    def delete(self, id: str) -> ResponseMeta:
        """Delete a webhook."""
        return self._client._request_empty("DELETE", f"/webhooks/{id}")

    def test(self, id: str) -> ResponseMeta:
        """Send a test event to a webhook."""
        return self._client._request_empty("POST", f"/webhooks/{id}/test")
