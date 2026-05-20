from __future__ import annotations

from vynco.types.shared import VyncoModel


class Notification(VyncoModel):
    """A single in-app notification."""

    id: str = ""
    title: str = ""
    body: str = ""
    category: str = ""
    is_read: bool = False
    link: str | None = None
    created_at: str = ""


class NotificationListResponse(VyncoModel):
    """A page of notifications with unread count."""

    items: list[Notification] = []
    total: int = 0
    unread_count: int = 0


class MarkReadResponse(VyncoModel):
    """Result of marking notifications read."""

    updated: int = 0


class NotificationPreferences(VyncoModel):
    """A user's notification delivery preferences."""

    id: str = ""
    user_id: str = ""
    is_enabled: bool = True
    delivery_mode: str = "Immediate"
    channel: str = "InApp"
    email_address: str | None = None
    digest_time: str = "08:00:00"
    watched_change_types: list[str] = []
    created_at: str = ""
    updated_at: str = ""


class TestNotificationResponse(VyncoModel):
    """Result of sending a test notification."""

    message: str = ""
