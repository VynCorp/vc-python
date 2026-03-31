from __future__ import annotations

import builtins
from typing import TYPE_CHECKING, Any

from vynco._base_client import _build_params
from vynco._response import Response, ResponseMeta
from vynco.types.webhooks import (
    CreateWebhookResponse,
    TestDeliveryResponse,
    WebhookDelivery,
    WebhookSubscription,
)

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client

_list = builtins.list


class AsyncWebhooks:
    """Async webhook operations."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def list(self) -> Response[_list[WebhookSubscription]]:
        """List all webhook subscriptions."""
        return await self._client._request_model(
            "GET",
            "/v1/webhooks",
            response_type=list[WebhookSubscription],
        )

    async def create(
        self,
        *,
        url: str,
        description: str | None = None,
        event_filters: _list[str] | None = None,
        company_filters: _list[str] | None = None,
    ) -> Response[CreateWebhookResponse]:
        """Create a webhook subscription."""
        body: dict[str, Any] = {"url": url}
        if description is not None:
            body["description"] = description
        if event_filters is not None:
            body["eventFilters"] = event_filters
        if company_filters is not None:
            body["companyFilters"] = company_filters
        return await self._client._request_model(
            "POST",
            "/v1/webhooks",
            json=body,
            response_type=CreateWebhookResponse,
        )

    async def update(
        self,
        id: str,
        *,
        url: str | None = None,
        description: str | None = None,
        event_filters: _list[str] | None = None,
        company_filters: _list[str] | None = None,
        status: str | None = None,
    ) -> Response[WebhookSubscription]:
        """Update a webhook subscription."""
        body: dict[str, Any] = {}
        if url is not None:
            body["url"] = url
        if description is not None:
            body["description"] = description
        if event_filters is not None:
            body["eventFilters"] = event_filters
        if company_filters is not None:
            body["companyFilters"] = company_filters
        if status is not None:
            body["status"] = status
        return await self._client._request_model(
            "PUT",
            f"/v1/webhooks/{id}",
            json=body,
            response_type=WebhookSubscription,
        )

    async def delete(self, id: str) -> ResponseMeta:
        """Delete a webhook subscription."""
        return await self._client._request_empty("DELETE", f"/v1/webhooks/{id}")

    async def test(self, id: str) -> Response[TestDeliveryResponse]:
        """Send a test delivery to a webhook."""
        return await self._client._request_model(
            "POST",
            f"/v1/webhooks/{id}/test",
            json={},
            response_type=TestDeliveryResponse,
        )

    async def deliveries(
        self, id: str, *, limit: int | None = None
    ) -> Response[_list[WebhookDelivery]]:
        """Get delivery history for a webhook."""
        params = _build_params({"limit": limit})
        return await self._client._request_model(
            "GET",
            f"/v1/webhooks/{id}/deliveries",
            params=params or None,
            response_type=list[WebhookDelivery],
        )


class Webhooks:
    """Sync webhook operations."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def list(self) -> Response[_list[WebhookSubscription]]:
        """List all webhook subscriptions."""
        return self._client._request_model(
            "GET",
            "/v1/webhooks",
            response_type=list[WebhookSubscription],
        )

    def create(
        self,
        *,
        url: str,
        description: str | None = None,
        event_filters: _list[str] | None = None,
        company_filters: _list[str] | None = None,
    ) -> Response[CreateWebhookResponse]:
        """Create a webhook subscription."""
        body: dict[str, Any] = {"url": url}
        if description is not None:
            body["description"] = description
        if event_filters is not None:
            body["eventFilters"] = event_filters
        if company_filters is not None:
            body["companyFilters"] = company_filters
        return self._client._request_model(
            "POST",
            "/v1/webhooks",
            json=body,
            response_type=CreateWebhookResponse,
        )

    def update(
        self,
        id: str,
        *,
        url: str | None = None,
        description: str | None = None,
        event_filters: _list[str] | None = None,
        company_filters: _list[str] | None = None,
        status: str | None = None,
    ) -> Response[WebhookSubscription]:
        """Update a webhook subscription."""
        body: dict[str, Any] = {}
        if url is not None:
            body["url"] = url
        if description is not None:
            body["description"] = description
        if event_filters is not None:
            body["eventFilters"] = event_filters
        if company_filters is not None:
            body["companyFilters"] = company_filters
        if status is not None:
            body["status"] = status
        return self._client._request_model(
            "PUT",
            f"/v1/webhooks/{id}",
            json=body,
            response_type=WebhookSubscription,
        )

    def delete(self, id: str) -> ResponseMeta:
        """Delete a webhook subscription."""
        return self._client._request_empty("DELETE", f"/v1/webhooks/{id}")

    def test(self, id: str) -> Response[TestDeliveryResponse]:
        """Send a test delivery to a webhook."""
        return self._client._request_model(
            "POST",
            f"/v1/webhooks/{id}/test",
            json={},
            response_type=TestDeliveryResponse,
        )

    def deliveries(self, id: str, *, limit: int | None = None) -> Response[_list[WebhookDelivery]]:
        """Get delivery history for a webhook."""
        params = _build_params({"limit": limit})
        return self._client._request_model(
            "GET",
            f"/v1/webhooks/{id}/deliveries",
            params=params or None,
            response_type=list[WebhookDelivery],
        )
