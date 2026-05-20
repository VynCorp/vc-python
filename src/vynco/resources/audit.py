from __future__ import annotations

from typing import TYPE_CHECKING

from vynco._base_client import _build_params
from vynco._response import Response
from vynco.types.audit import AuditPlaybook

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client


class AsyncAudit:
    """Async audit-methodology playbooks."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def playbook(
        self, uid: str, *, tiers: str | None = None, overlays: str | None = None
    ) -> Response[AuditPlaybook]:
        """Get a tailored audit playbook for a company.

        ``tiers`` and ``overlays`` are optional comma-separated overrides
        (e.g. ``tiers="complex,core"``).
        """
        params = _build_params({"tiers": tiers, "overlays": overlays})
        return await self._client._request_model(
            "GET",
            f"/v1/audit/playbook/{uid}",
            params=params or None,
            response_type=AuditPlaybook,
        )


class Audit:
    """Sync audit-methodology playbooks."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def playbook(
        self, uid: str, *, tiers: str | None = None, overlays: str | None = None
    ) -> Response[AuditPlaybook]:
        """Get a tailored audit playbook for a company.

        ``tiers`` and ``overlays`` are optional comma-separated overrides
        (e.g. ``tiers="complex,core"``).
        """
        params = _build_params({"tiers": tiers, "overlays": overlays})
        return self._client._request_model(
            "GET",
            f"/v1/audit/playbook/{uid}",
            params=params or None,
            response_type=AuditPlaybook,
        )
