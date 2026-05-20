from __future__ import annotations

from typing import TYPE_CHECKING

from vynco._response import Response
from vynco.types.risk import RiskScoreV2Response

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client


class AsyncRisk:
    """Async Bayesian (v2) risk scoring."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def v2(self, uid: str) -> Response[RiskScoreV2Response]:
        """Get the Bayesian (v2) risk score for a company."""
        return await self._client._request_model(
            "GET", f"/v1/risk/v2/{uid}", response_type=RiskScoreV2Response
        )


class Risk:
    """Sync Bayesian (v2) risk scoring."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def v2(self, uid: str) -> Response[RiskScoreV2Response]:
        """Get the Bayesian (v2) risk score for a company."""
        return self._client._request_model(
            "GET", f"/v1/risk/v2/{uid}", response_type=RiskScoreV2Response
        )
