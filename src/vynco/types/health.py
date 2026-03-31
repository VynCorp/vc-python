from __future__ import annotations

from vynco.types.shared import VyncoModel


class HealthResponse(VyncoModel):
    """API health status response."""

    status: str = ""
    database: str = ""
    redis: str = ""
    version: str = ""
