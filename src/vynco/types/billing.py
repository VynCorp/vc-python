from __future__ import annotations

from vynco.types.shared import VyncoModel


class CheckoutSessionResponse(VyncoModel):
    """Response containing a Stripe checkout session URL."""

    url: str


class PortalSessionResponse(VyncoModel):
    """Response containing a Stripe billing portal URL."""

    url: str
