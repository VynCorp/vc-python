from __future__ import annotations

import builtins
from typing import TYPE_CHECKING, Any

from vynco._response import Response, ResponseMeta
from vynco.types.alerts import Alert

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client

_list = builtins.list


class AsyncAlerts:
    """Async alert operations.

    Alerts are persistent saved queries that trigger notifications (optionally
    via webhook) when matching companies or events appear.
    """

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def list(self) -> Response[_list[Alert]]:
        """List all alerts for the authenticated user."""
        return await self._client._request_model(
            "GET",
            "/v1/alerts",
            response_type=list[Alert],
        )

    async def create(
        self,
        *,
        name: str,
        query_params: dict[str, Any],
        webhook_url: str | None = None,
        frequency: str | None = None,
        saved_search_id: str | None = None,
    ) -> Response[Alert]:
        """Create a new alert.

        ``frequency`` accepts ``hourly``, ``daily``, or ``weekly`` (default
        ``daily`` on the server). ``query_params`` is an arbitrary JSON filter
        describing the saved query (e.g. ``{"canton": "ZH", "capital_min":
        1000000}``).
        """
        body: dict[str, Any] = {"name": name, "queryParams": query_params}
        if webhook_url is not None:
            body["webhookUrl"] = webhook_url
        if frequency is not None:
            body["frequency"] = frequency
        if saved_search_id is not None:
            body["savedSearchId"] = saved_search_id
        return await self._client._request_model(
            "POST",
            "/v1/alerts",
            json=body,
            response_type=Alert,
        )

    async def delete(self, id: str) -> ResponseMeta:
        """Delete an alert."""
        return await self._client._request_empty("DELETE", f"/v1/alerts/{id}")


class Alerts:
    """Sync alert operations."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def list(self) -> Response[_list[Alert]]:
        """List all alerts for the authenticated user."""
        return self._client._request_model(
            "GET",
            "/v1/alerts",
            response_type=list[Alert],
        )

    def create(
        self,
        *,
        name: str,
        query_params: dict[str, Any],
        webhook_url: str | None = None,
        frequency: str | None = None,
        saved_search_id: str | None = None,
    ) -> Response[Alert]:
        """Create a new alert.

        ``frequency`` accepts ``hourly``, ``daily``, or ``weekly`` (default
        ``daily`` on the server). ``query_params`` is an arbitrary JSON filter
        describing the saved query.
        """
        body: dict[str, Any] = {"name": name, "queryParams": query_params}
        if webhook_url is not None:
            body["webhookUrl"] = webhook_url
        if frequency is not None:
            body["frequency"] = frequency
        if saved_search_id is not None:
            body["savedSearchId"] = saved_search_id
        return self._client._request_model(
            "POST",
            "/v1/alerts",
            json=body,
            response_type=Alert,
        )

    def delete(self, id: str) -> ResponseMeta:
        """Delete an alert."""
        return self._client._request_empty("DELETE", f"/v1/alerts/{id}")
