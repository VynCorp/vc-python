from __future__ import annotations

from vynco.types.shared import VyncoModel


class WebhookSubscription(VyncoModel):
    """A webhook subscription."""

    id: str
    url: str = ""
    description: str = ""
    event_filters: list[str] = []
    company_filters: list[str] = []
    status: str = ""
    created_at: str = ""
    updated_at: str = ""


class CreateWebhookResponse(VyncoModel):
    """Response from creating a webhook (includes signing secret)."""

    webhook: WebhookSubscription
    signing_secret: str = ""


class TestDeliveryResponse(VyncoModel):
    """Response from testing a webhook delivery."""

    success: bool = False
    http_status: int | None = None
    error: str | None = None


class WebhookDelivery(VyncoModel):
    """A webhook delivery record."""

    id: str
    event_id: str = ""
    status: str = ""
    attempt: int = 0
    http_status: int | None = None
    error_message: str | None = None
    delivered_at: str | None = None
    created_at: str = ""
