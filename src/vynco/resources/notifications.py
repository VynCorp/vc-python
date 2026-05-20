from __future__ import annotations

import builtins
from typing import TYPE_CHECKING, Any

from vynco._base_client import _build_params
from vynco._response import Response
from vynco.types.notifications import (
    MarkReadResponse,
    NotificationListResponse,
    NotificationPreferences,
    TestNotificationResponse,
)

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client

_list = builtins.list


def _prefs_body(
    is_enabled: bool | None,
    delivery_mode: str | None,
    channel: str | None,
    email_address: str | None,
    digest_time: str | None,
    watched_change_types: _list[str] | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {}
    if is_enabled is not None:
        body["isEnabled"] = is_enabled
    if delivery_mode is not None:
        body["deliveryMode"] = delivery_mode
    if channel is not None:
        body["channel"] = channel
    if email_address is not None:
        body["emailAddress"] = email_address
    if digest_time is not None:
        body["digestTime"] = digest_time
    if watched_change_types is not None:
        body["watchedChangeTypes"] = watched_change_types
    return body


class AsyncNotifications:
    """Async in-app notifications and delivery preferences."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def list(
        self,
        *,
        unread: bool | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Response[NotificationListResponse]:
        """List notifications for the authenticated user."""
        params = _build_params({"unread": unread, "limit": limit, "offset": offset})
        return await self._client._request_model(
            "GET",
            "/v1/notifications",
            params=params or None,
            response_type=NotificationListResponse,
        )

    async def mark_read(
        self, *, ids: _list[str] | None = None, mark_all: bool = False
    ) -> Response[MarkReadResponse]:
        """Mark notifications read. Pass ``ids`` or ``mark_all=True``."""
        body: dict[str, Any] = {"all": True} if mark_all else {"ids": ids or []}
        return await self._client._request_model(
            "POST", "/v1/notifications/read", json=body, response_type=MarkReadResponse
        )

    async def get_preferences(self) -> Response[NotificationPreferences]:
        """Get notification delivery preferences."""
        return await self._client._request_model(
            "GET", "/v1/notifications/preferences", response_type=NotificationPreferences
        )

    async def update_preferences(
        self,
        *,
        is_enabled: bool | None = None,
        delivery_mode: str | None = None,
        channel: str | None = None,
        email_address: str | None = None,
        digest_time: str | None = None,
        watched_change_types: _list[str] | None = None,
    ) -> Response[NotificationPreferences]:
        """Update notification delivery preferences."""
        body = _prefs_body(
            is_enabled, delivery_mode, channel, email_address, digest_time, watched_change_types
        )
        return await self._client._request_model(
            "PUT",
            "/v1/notifications/preferences",
            json=body,
            response_type=NotificationPreferences,
        )

    async def test(self) -> Response[TestNotificationResponse]:
        """Send a test notification to the authenticated user."""
        return await self._client._request_model(
            "POST", "/v1/notifications/test", response_type=TestNotificationResponse
        )


class Notifications:
    """Sync in-app notifications and delivery preferences."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        *,
        unread: bool | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Response[NotificationListResponse]:
        """List notifications for the authenticated user."""
        params = _build_params({"unread": unread, "limit": limit, "offset": offset})
        return self._client._request_model(
            "GET",
            "/v1/notifications",
            params=params or None,
            response_type=NotificationListResponse,
        )

    def mark_read(
        self, *, ids: _list[str] | None = None, mark_all: bool = False
    ) -> Response[MarkReadResponse]:
        """Mark notifications read. Pass ``ids`` or ``mark_all=True``."""
        body: dict[str, Any] = {"all": True} if mark_all else {"ids": ids or []}
        return self._client._request_model(
            "POST", "/v1/notifications/read", json=body, response_type=MarkReadResponse
        )

    def get_preferences(self) -> Response[NotificationPreferences]:
        """Get notification delivery preferences."""
        return self._client._request_model(
            "GET", "/v1/notifications/preferences", response_type=NotificationPreferences
        )

    def update_preferences(
        self,
        *,
        is_enabled: bool | None = None,
        delivery_mode: str | None = None,
        channel: str | None = None,
        email_address: str | None = None,
        digest_time: str | None = None,
        watched_change_types: _list[str] | None = None,
    ) -> Response[NotificationPreferences]:
        """Update notification delivery preferences."""
        body = _prefs_body(
            is_enabled, delivery_mode, channel, email_address, digest_time, watched_change_types
        )
        return self._client._request_model(
            "PUT",
            "/v1/notifications/preferences",
            json=body,
            response_type=NotificationPreferences,
        )

    def test(self) -> Response[TestNotificationResponse]:
        """Send a test notification to the authenticated user."""
        return self._client._request_model(
            "POST", "/v1/notifications/test", response_type=TestNotificationResponse
        )
