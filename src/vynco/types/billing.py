from __future__ import annotations

from vynco.types.shared import VyncoModel


class SessionUrl(VyncoModel):
    """Stripe session URL response."""

    url: str
