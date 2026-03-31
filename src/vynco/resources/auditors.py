from __future__ import annotations

from typing import TYPE_CHECKING

from vynco._response import Response
from vynco.types.auditors import AuditorHistoryResponse, AuditorTenure
from vynco.types.shared import PaginatedResponse

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client


def _tenure_params(
    min_years: float | None,
    canton: str | None,
    page: int | None,
    page_size: int | None,
) -> dict[str, str] | None:
    """Build query params for auditor tenures.

    The API expects ``min_years`` (snake_case), not camelCase, so we cannot
    use the generic ``_build_params`` helper for that key.
    """
    params: dict[str, str] = {}
    if min_years is not None:
        params["min_years"] = str(min_years)
    if canton is not None:
        params["canton"] = canton
    if page is not None:
        params["page"] = str(page)
    if page_size is not None:
        params["pageSize"] = str(page_size)
    return params or None


class AsyncAuditors:
    """Async auditor operations."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def history(self, uid: str) -> Response[AuditorHistoryResponse]:
        """Get auditor history for a company."""
        return await self._client._request_model(
            "GET",
            f"/v1/companies/{uid}/auditor-history",
            response_type=AuditorHistoryResponse,
        )

    async def tenures(
        self,
        *,
        min_years: float | None = None,
        canton: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
    ) -> Response[PaginatedResponse[AuditorTenure]]:
        """List auditor tenures with optional filtering."""
        return await self._client._request_model(
            "GET",
            "/v1/auditor-tenures",
            params=_tenure_params(min_years, canton, page, page_size),
            response_type=PaginatedResponse[AuditorTenure],
        )


class Auditors:
    """Sync auditor operations."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def history(self, uid: str) -> Response[AuditorHistoryResponse]:
        """Get auditor history for a company."""
        return self._client._request_model(
            "GET",
            f"/v1/companies/{uid}/auditor-history",
            response_type=AuditorHistoryResponse,
        )

    def tenures(
        self,
        *,
        min_years: float | None = None,
        canton: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
    ) -> Response[PaginatedResponse[AuditorTenure]]:
        """List auditor tenures with optional filtering."""
        return self._client._request_model(
            "GET",
            "/v1/auditor-tenures",
            params=_tenure_params(min_years, canton, page, page_size),
            response_type=PaginatedResponse[AuditorTenure],
        )
