from __future__ import annotations

from typing import TYPE_CHECKING

from vynco._response import Response
from vynco.types.billing import SessionUrl

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client


class AsyncBilling:
    """Async billing operations."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def create_checkout(self, *, tier: str) -> Response[SessionUrl]:
        """Create a Stripe checkout session for a plan upgrade."""
        return await self._client._request_model(
            "POST",
            "/v1/billing/checkout-session",
            json={"tier": tier},
            response_type=SessionUrl,
        )

    async def create_portal(self) -> Response[SessionUrl]:
        """Create a Stripe billing portal session."""
        return await self._client._request_model(
            "POST",
            "/v1/billing/portal-session",
            json={},
            response_type=SessionUrl,
        )


class Billing:
    """Sync billing operations."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def create_checkout(self, *, tier: str) -> Response[SessionUrl]:
        """Create a Stripe checkout session for a plan upgrade."""
        return self._client._request_model(
            "POST",
            "/v1/billing/checkout-session",
            json={"tier": tier},
            response_type=SessionUrl,
        )

    def create_portal(self) -> Response[SessionUrl]:
        """Create a Stripe billing portal session."""
        return self._client._request_model(
            "POST",
            "/v1/billing/portal-session",
            json={},
            response_type=SessionUrl,
        )
