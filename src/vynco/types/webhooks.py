from __future__ import annotations

from vynco.types.shared import VyncoModel


class Webhook(VyncoModel):
    """A webhook subscription."""

    id: str
    url: str = ""
    events: list[str] = []
    status: str = ""
    secret: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class WebhookCreated(VyncoModel):
    """A newly created webhook (includes the signing secret, shown only once)."""

    id: str
    url: str = ""
    events: list[str] = []
    secret: str = ""
    created_at: str | None = None
