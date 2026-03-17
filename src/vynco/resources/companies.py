from __future__ import annotations

from typing import TYPE_CHECKING, Any

from vynco._base_client import _build_params
from vynco._response import Response
from vynco.types.changes import CompanyChange
from vynco.types.companies import Company, CompanyComparison, CompanyCount, CompanyNews
from vynco.types.dossiers import Dossier
from vynco.types.persons import PersonRole
from vynco.types.relationships import RelationshipsResponse
from vynco.types.shared import PaginatedResponse

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client


class AsyncCompanies:
    """Async company operations."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def search(
        self,
        *,
        query: str | None = None,
        canton: str | None = None,
        legal_form: str | None = None,
        status: str | None = None,
        sort_by: str | None = None,
        sort_desc: bool | None = None,
        page: int | None = None,
        page_size: int | None = None,
    ) -> Response[PaginatedResponse[Company]]:
        """Search companies with filters and pagination."""
        params = _build_params(
            {k: v for k, v in locals().items() if k != "self"}
        )
        return await self._client._request_model(
            "GET", "/companies", params=params or None,
            response_type=PaginatedResponse[Company],
        )

    async def get(self, uid: str) -> Response[Company]:
        """Get a company by its Swiss UID (e.g. 'CHE-100.023.968')."""
        return await self._client._request_model(
            "GET", f"/companies/{uid}", response_type=Company,
        )

    async def count(
        self,
        *,
        query: str | None = None,
        canton: str | None = None,
        legal_form: str | None = None,
        status: str | None = None,
    ) -> Response[CompanyCount]:
        """Get the total count of companies matching optional filters."""
        params = _build_params(
            {k: v for k, v in locals().items() if k != "self"}
        )
        return await self._client._request_model(
            "GET", "/companies/count", params=params or None,
            response_type=CompanyCount,
        )

    async def statistics(self) -> Response[dict[str, Any]]:
        """Get aggregate statistics about companies."""
        return await self._client._request_model(
            "GET", "/companies/statistics", response_type=dict,
        )

    async def compare(self, uids: list[str]) -> Response[CompanyComparison]:
        """Compare multiple companies (up to 5)."""
        return await self._client._request_model(
            "POST", "/companies/compare", json={"uids": uids},
            response_type=CompanyComparison,
        )

    async def persons(self, uid: str) -> Response[list[PersonRole]]:
        """Get the board members / persons for a company."""
        return await self._client._request_model(
            "GET", f"/companies/{uid}/persons", response_type=list[PersonRole],
        )

    async def dossier(self, uid: str) -> Response[Dossier]:
        """Get the AI-generated dossier for a company (if available)."""
        return await self._client._request_model(
            "GET", f"/companies/{uid}/dossier", response_type=Dossier,
        )

    async def relationships(self, uid: str) -> Response[RelationshipsResponse]:
        """Get company relationships."""
        return await self._client._request_model(
            "GET", f"/companies/{uid}/relationships",
            response_type=RelationshipsResponse,
        )

    async def hierarchy(self, uid: str) -> Response[RelationshipsResponse]:
        """Get parent/subsidiary hierarchy."""
        return await self._client._request_model(
            "GET", f"/companies/{uid}/hierarchy",
            response_type=RelationshipsResponse,
        )

    async def changes(self, uid: str) -> Response[list[CompanyChange]]:
        """Get the change history for a specific company."""
        return await self._client._request_model(
            "GET", f"/companies/{uid}/changes",
            response_type=list[CompanyChange],
        )

    async def batch_get(self, uids: list[str]) -> Response[list[Company]]:
        """Get multiple companies by UIDs."""
        return await self._client._request_model(
            "POST", "/companies/batch", json={"uids": uids},
            response_type=list[Company],
        )

    async def news(self, uid: str) -> Response[list[CompanyNews]]:
        """Get news articles related to a company."""
        return await self._client._request_model(
            "GET", f"/companies/{uid}/news",
            response_type=list[CompanyNews],
        )


class Companies:
    """Sync company operations."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def search(
        self,
        *,
        query: str | None = None,
        canton: str | None = None,
        legal_form: str | None = None,
        status: str | None = None,
        sort_by: str | None = None,
        sort_desc: bool | None = None,
        page: int | None = None,
        page_size: int | None = None,
    ) -> Response[PaginatedResponse[Company]]:
        """Search companies with filters and pagination."""
        params = _build_params(
            {k: v for k, v in locals().items() if k != "self"}
        )
        return self._client._request_model(
            "GET", "/companies", params=params or None,
            response_type=PaginatedResponse[Company],
        )

    def get(self, uid: str) -> Response[Company]:
        """Get a company by its Swiss UID (e.g. 'CHE-100.023.968')."""
        return self._client._request_model(
            "GET", f"/companies/{uid}", response_type=Company,
        )

    def count(
        self,
        *,
        query: str | None = None,
        canton: str | None = None,
        legal_form: str | None = None,
        status: str | None = None,
    ) -> Response[CompanyCount]:
        """Get the total count of companies matching optional filters."""
        params = _build_params(
            {k: v for k, v in locals().items() if k != "self"}
        )
        return self._client._request_model(
            "GET", "/companies/count", params=params or None,
            response_type=CompanyCount,
        )

    def statistics(self) -> Response[dict[str, Any]]:
        """Get aggregate statistics about companies."""
        return self._client._request_model(
            "GET", "/companies/statistics", response_type=dict,
        )

    def compare(self, uids: list[str]) -> Response[CompanyComparison]:
        """Compare multiple companies (up to 5)."""
        return self._client._request_model(
            "POST", "/companies/compare", json={"uids": uids},
            response_type=CompanyComparison,
        )

    def persons(self, uid: str) -> Response[list[PersonRole]]:
        """Get the board members / persons for a company."""
        return self._client._request_model(
            "GET", f"/companies/{uid}/persons", response_type=list[PersonRole],
        )

    def dossier(self, uid: str) -> Response[Dossier]:
        """Get the AI-generated dossier for a company (if available)."""
        return self._client._request_model(
            "GET", f"/companies/{uid}/dossier", response_type=Dossier,
        )

    def relationships(self, uid: str) -> Response[RelationshipsResponse]:
        """Get company relationships."""
        return self._client._request_model(
            "GET", f"/companies/{uid}/relationships",
            response_type=RelationshipsResponse,
        )

    def hierarchy(self, uid: str) -> Response[RelationshipsResponse]:
        """Get parent/subsidiary hierarchy."""
        return self._client._request_model(
            "GET", f"/companies/{uid}/hierarchy",
            response_type=RelationshipsResponse,
        )

    def changes(self, uid: str) -> Response[list[CompanyChange]]:
        """Get the change history for a specific company."""
        return self._client._request_model(
            "GET", f"/companies/{uid}/changes",
            response_type=list[CompanyChange],
        )

    def batch_get(self, uids: list[str]) -> Response[list[Company]]:
        """Get multiple companies by UIDs."""
        return self._client._request_model(
            "POST", "/companies/batch", json={"uids": uids},
            response_type=list[Company],
        )

    def news(self, uid: str) -> Response[list[CompanyNews]]:
        """Get news articles related to a company."""
        return self._client._request_model(
            "GET", f"/companies/{uid}/news",
            response_type=list[CompanyNews],
        )
