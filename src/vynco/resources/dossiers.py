from __future__ import annotations

from typing import TYPE_CHECKING

from vynco._response import Response
from vynco.types.dossiers import Dossier

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client


class AsyncDossiers:
    """Async dossier operations."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def generate(
        self, uid: str, *, level: str = "standard"
    ) -> Response[Dossier]:
        """Generate an AI dossier for a company.

        Args:
            uid: Company Swiss UID.
            level: Dossier detail level — "summary", "standard", or "comprehensive".
        """
        return await self._client._request_model(
            "POST", "/dossiers",
            json={"companyUid": uid, "level": level},
            response_type=Dossier,
        )


class Dossiers:
    """Sync dossier operations."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def generate(
        self, uid: str, *, level: str = "standard"
    ) -> Response[Dossier]:
        """Generate an AI dossier for a company.

        Args:
            uid: Company Swiss UID.
            level: Dossier detail level — "summary", "standard", or "comprehensive".
        """
        return self._client._request_model(
            "POST", "/dossiers",
            json={"companyUid": uid, "level": level},
            response_type=Dossier,
        )
