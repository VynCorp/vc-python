from __future__ import annotations

import builtins
from typing import TYPE_CHECKING, Any

from vynco._base_client import _build_params
from vynco._response import ExportFile, Response, ResponseMeta
from vynco.types.companies import (
    Acquisition,
    Classification,
    Company,
    CompanyCount,
    CompanyFullResponse,
    CompanyReport,
    CompanyStatistics,
    CompareResponse,
    CorporateStructure,
    EventListResponse,
    Fingerprint,
    HierarchyResponse,
    NearbyCompany,
    NewsItem,
    Note,
    Relationship,
    Tag,
    TagSummary,
)
from vynco.types.shared import PaginatedResponse

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client

_list = builtins.list


class AsyncCompanies:
    """Async company operations."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def list(
        self,
        *,
        query: str | None = None,
        canton: str | None = None,
        changed_since: str | None = None,
        status: str | None = None,
        legal_form: str | None = None,
        capital_min: float | None = None,
        capital_max: float | None = None,
        auditor_category: str | None = None,
        sort_by: str | None = None,
        sort_desc: bool | None = None,
        page: int | None = None,
        page_size: int | None = None,
    ) -> Response[PaginatedResponse[Company]]:
        """List companies with optional filtering and pagination."""
        params = _build_params({k: v for k, v in locals().items() if k != "self"})
        return await self._client._request_model(
            "GET",
            "/v1/companies",
            params=params or None,
            response_type=PaginatedResponse[Company],
        )

    async def get(self, uid: str) -> Response[Company]:
        """Get a company by its Swiss UID (e.g. 'CHE-105.805.080')."""
        return await self._client._request_model(
            "GET",
            f"/v1/companies/{uid}",
            response_type=Company,
        )

    async def get_full(self, uid: str) -> Response[CompanyFullResponse]:
        """Get full company details with persons, changes, and relationships."""
        return await self._client._request_model(
            "GET",
            f"/v1/companies/{uid}/full",
            response_type=CompanyFullResponse,
        )

    async def count(self) -> Response[CompanyCount]:
        """Get the total count of companies."""
        return await self._client._request_model(
            "GET",
            "/v1/companies/count",
            response_type=CompanyCount,
        )

    async def events(self, uid: str, *, limit: int | None = None) -> Response[EventListResponse]:
        """Get events for a company."""
        params = _build_params({"limit": limit})
        return await self._client._request_model(
            "GET",
            f"/v1/companies/{uid}/events",
            params=params or None,
            response_type=EventListResponse,
        )

    async def statistics(self) -> Response[CompanyStatistics]:
        """Get aggregate statistics about companies."""
        return await self._client._request_model(
            "GET",
            "/v1/companies/statistics",
            response_type=CompanyStatistics,
        )

    async def compare(self, uids: _list[str]) -> Response[CompareResponse]:
        """Compare multiple companies side-by-side."""
        return await self._client._request_model(
            "POST",
            "/v1/companies/compare",
            json={"uids": uids},
            response_type=CompareResponse,
        )

    async def news(self, uid: str) -> Response[_list[NewsItem]]:
        """Get news articles related to a company."""
        return await self._client._request_model(
            "GET",
            f"/v1/companies/{uid}/news",
            response_type=list[NewsItem],
        )

    async def reports(self, uid: str) -> Response[_list[CompanyReport]]:
        """Get financial reports for a company."""
        return await self._client._request_model(
            "GET",
            f"/v1/companies/{uid}/reports",
            response_type=list[CompanyReport],
        )

    async def relationships(self, uid: str) -> Response[_list[Relationship]]:
        """Get company relationships."""
        return await self._client._request_model(
            "GET",
            f"/v1/companies/{uid}/relationships",
            response_type=list[Relationship],
        )

    async def hierarchy(self, uid: str) -> Response[HierarchyResponse]:
        """Get parent/subsidiary hierarchy."""
        return await self._client._request_model(
            "GET",
            f"/v1/companies/{uid}/hierarchy",
            response_type=HierarchyResponse,
        )

    async def classification(self, uid: str) -> Response[Classification]:
        """Get industry classification for a company."""
        return await self._client._request_model(
            "GET",
            f"/v1/companies/{uid}/classification",
            response_type=Classification,
        )

    async def fingerprint(self, uid: str) -> Response[Fingerprint]:
        """Get data fingerprint for a company."""
        return await self._client._request_model(
            "GET",
            f"/v1/companies/{uid}/fingerprint",
            response_type=Fingerprint,
        )

    async def structure(self, uid: str) -> Response[CorporateStructure]:
        """Get corporate structure (head offices, branches, acquisitions)."""
        return await self._client._request_model(
            "GET",
            f"/v1/companies/{uid}/structure",
            response_type=CorporateStructure,
        )

    async def acquisitions(self, uid: str) -> Response[_list[Acquisition]]:
        """Get M&A relationships for a company."""
        return await self._client._request_model(
            "GET",
            f"/v1/companies/{uid}/acquisitions",
            response_type=list[Acquisition],
        )

    async def nearby(
        self,
        *,
        lat: float,
        lng: float,
        radius_km: float | None = None,
        limit: int | None = None,
    ) -> Response[_list[NearbyCompany]]:
        """Find companies near a geographic point."""
        params = _build_params({k: v for k, v in locals().items() if k != "self"})
        return await self._client._request_model(
            "GET",
            "/v1/companies/nearby",
            params=params or None,
            response_type=list[NearbyCompany],
        )

    # -- Notes --

    async def notes(self, uid: str) -> Response[_list[Note]]:
        """Get notes for a company."""
        return await self._client._request_model(
            "GET",
            f"/v1/companies/{uid}/notes",
            response_type=list[Note],
        )

    async def create_note(
        self,
        uid: str,
        *,
        content: str,
        note_type: str | None = None,
        rating: int | None = None,
        is_private: bool | None = None,
    ) -> Response[Note]:
        """Create a note on a company."""
        body: dict[str, Any] = {"content": content}
        if note_type is not None:
            body["noteType"] = note_type
        if rating is not None:
            body["rating"] = rating
        if is_private is not None:
            body["isPrivate"] = is_private
        return await self._client._request_model(
            "POST",
            f"/v1/companies/{uid}/notes",
            json=body,
            response_type=Note,
        )

    async def update_note(
        self,
        uid: str,
        note_id: str,
        *,
        content: str | None = None,
        note_type: str | None = None,
        rating: int | None = None,
        is_private: bool | None = None,
    ) -> Response[Note]:
        """Update a note on a company."""
        body: dict[str, Any] = {}
        if content is not None:
            body["content"] = content
        if note_type is not None:
            body["noteType"] = note_type
        if rating is not None:
            body["rating"] = rating
        if is_private is not None:
            body["isPrivate"] = is_private
        return await self._client._request_model(
            "PUT",
            f"/v1/companies/{uid}/notes/{note_id}",
            json=body,
            response_type=Note,
        )

    async def delete_note(self, uid: str, note_id: str) -> ResponseMeta:
        """Delete a note from a company."""
        return await self._client._request_empty(
            "DELETE",
            f"/v1/companies/{uid}/notes/{note_id}",
        )

    # -- Tags --

    async def tags(self, uid: str) -> Response[_list[Tag]]:
        """Get tags for a company."""
        return await self._client._request_model(
            "GET",
            f"/v1/companies/{uid}/tags",
            response_type=list[Tag],
        )

    async def create_tag(
        self,
        uid: str,
        *,
        tag_name: str,
        color: str | None = None,
    ) -> Response[Tag]:
        """Create a tag on a company."""
        body: dict[str, Any] = {"tagName": tag_name}
        if color is not None:
            body["color"] = color
        return await self._client._request_model(
            "POST",
            f"/v1/companies/{uid}/tags",
            json=body,
            response_type=Tag,
        )

    async def delete_tag(self, uid: str, tag_id: str) -> ResponseMeta:
        """Delete a tag from a company."""
        return await self._client._request_empty(
            "DELETE",
            f"/v1/companies/{uid}/tags/{tag_id}",
        )

    async def all_tags(self) -> Response[_list[TagSummary]]:
        """Get all tags with usage counts."""
        return await self._client._request_model(
            "GET",
            "/v1/tags",
            response_type=list[TagSummary],
        )

    # -- Excel export --

    async def export_excel(
        self,
        *,
        uids: _list[str] | None = None,
        filter: dict[str, Any] | None = None,
        fields: _list[str] | None = None,
    ) -> ExportFile:
        """Export companies as Excel/CSV."""
        body: dict[str, Any] = {}
        if uids is not None:
            body["uids"] = uids
        if filter is not None:
            body["filter"] = filter
        if fields is not None:
            body["fields"] = fields
        return await self._client._request_bytes(
            "POST",
            "/v1/companies/export/excel",
            json=body,
        )


class Companies:
    """Sync company operations."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        *,
        query: str | None = None,
        canton: str | None = None,
        changed_since: str | None = None,
        status: str | None = None,
        legal_form: str | None = None,
        capital_min: float | None = None,
        capital_max: float | None = None,
        auditor_category: str | None = None,
        sort_by: str | None = None,
        sort_desc: bool | None = None,
        page: int | None = None,
        page_size: int | None = None,
    ) -> Response[PaginatedResponse[Company]]:
        """List companies with optional filtering and pagination."""
        params = _build_params({k: v for k, v in locals().items() if k != "self"})
        return self._client._request_model(
            "GET",
            "/v1/companies",
            params=params or None,
            response_type=PaginatedResponse[Company],
        )

    def get(self, uid: str) -> Response[Company]:
        """Get a company by its Swiss UID (e.g. 'CHE-105.805.080')."""
        return self._client._request_model(
            "GET",
            f"/v1/companies/{uid}",
            response_type=Company,
        )

    def get_full(self, uid: str) -> Response[CompanyFullResponse]:
        """Get full company details with persons, changes, and relationships."""
        return self._client._request_model(
            "GET",
            f"/v1/companies/{uid}/full",
            response_type=CompanyFullResponse,
        )

    def count(self) -> Response[CompanyCount]:
        """Get the total count of companies."""
        return self._client._request_model(
            "GET",
            "/v1/companies/count",
            response_type=CompanyCount,
        )

    def events(self, uid: str, *, limit: int | None = None) -> Response[EventListResponse]:
        """Get events for a company."""
        params = _build_params({"limit": limit})
        return self._client._request_model(
            "GET",
            f"/v1/companies/{uid}/events",
            params=params or None,
            response_type=EventListResponse,
        )

    def statistics(self) -> Response[CompanyStatistics]:
        """Get aggregate statistics about companies."""
        return self._client._request_model(
            "GET",
            "/v1/companies/statistics",
            response_type=CompanyStatistics,
        )

    def compare(self, uids: _list[str]) -> Response[CompareResponse]:
        """Compare multiple companies side-by-side."""
        return self._client._request_model(
            "POST",
            "/v1/companies/compare",
            json={"uids": uids},
            response_type=CompareResponse,
        )

    def news(self, uid: str) -> Response[_list[NewsItem]]:
        """Get news articles related to a company."""
        return self._client._request_model(
            "GET",
            f"/v1/companies/{uid}/news",
            response_type=list[NewsItem],
        )

    def reports(self, uid: str) -> Response[_list[CompanyReport]]:
        """Get financial reports for a company."""
        return self._client._request_model(
            "GET",
            f"/v1/companies/{uid}/reports",
            response_type=list[CompanyReport],
        )

    def relationships(self, uid: str) -> Response[_list[Relationship]]:
        """Get company relationships."""
        return self._client._request_model(
            "GET",
            f"/v1/companies/{uid}/relationships",
            response_type=list[Relationship],
        )

    def hierarchy(self, uid: str) -> Response[HierarchyResponse]:
        """Get parent/subsidiary hierarchy."""
        return self._client._request_model(
            "GET",
            f"/v1/companies/{uid}/hierarchy",
            response_type=HierarchyResponse,
        )

    def classification(self, uid: str) -> Response[Classification]:
        """Get industry classification for a company."""
        return self._client._request_model(
            "GET",
            f"/v1/companies/{uid}/classification",
            response_type=Classification,
        )

    def fingerprint(self, uid: str) -> Response[Fingerprint]:
        """Get data fingerprint for a company."""
        return self._client._request_model(
            "GET",
            f"/v1/companies/{uid}/fingerprint",
            response_type=Fingerprint,
        )

    def structure(self, uid: str) -> Response[CorporateStructure]:
        """Get corporate structure (head offices, branches, acquisitions)."""
        return self._client._request_model(
            "GET",
            f"/v1/companies/{uid}/structure",
            response_type=CorporateStructure,
        )

    def acquisitions(self, uid: str) -> Response[_list[Acquisition]]:
        """Get M&A relationships for a company."""
        return self._client._request_model(
            "GET",
            f"/v1/companies/{uid}/acquisitions",
            response_type=list[Acquisition],
        )

    def nearby(
        self,
        *,
        lat: float,
        lng: float,
        radius_km: float | None = None,
        limit: int | None = None,
    ) -> Response[_list[NearbyCompany]]:
        """Find companies near a geographic point."""
        params = _build_params({k: v for k, v in locals().items() if k != "self"})
        return self._client._request_model(
            "GET",
            "/v1/companies/nearby",
            params=params or None,
            response_type=list[NearbyCompany],
        )

    # -- Notes --

    def notes(self, uid: str) -> Response[_list[Note]]:
        """Get notes for a company."""
        return self._client._request_model(
            "GET",
            f"/v1/companies/{uid}/notes",
            response_type=list[Note],
        )

    def create_note(
        self,
        uid: str,
        *,
        content: str,
        note_type: str | None = None,
        rating: int | None = None,
        is_private: bool | None = None,
    ) -> Response[Note]:
        """Create a note on a company."""
        body: dict[str, Any] = {"content": content}
        if note_type is not None:
            body["noteType"] = note_type
        if rating is not None:
            body["rating"] = rating
        if is_private is not None:
            body["isPrivate"] = is_private
        return self._client._request_model(
            "POST",
            f"/v1/companies/{uid}/notes",
            json=body,
            response_type=Note,
        )

    def update_note(
        self,
        uid: str,
        note_id: str,
        *,
        content: str | None = None,
        note_type: str | None = None,
        rating: int | None = None,
        is_private: bool | None = None,
    ) -> Response[Note]:
        """Update a note on a company."""
        body: dict[str, Any] = {}
        if content is not None:
            body["content"] = content
        if note_type is not None:
            body["noteType"] = note_type
        if rating is not None:
            body["rating"] = rating
        if is_private is not None:
            body["isPrivate"] = is_private
        return self._client._request_model(
            "PUT",
            f"/v1/companies/{uid}/notes/{note_id}",
            json=body,
            response_type=Note,
        )

    def delete_note(self, uid: str, note_id: str) -> ResponseMeta:
        """Delete a note from a company."""
        return self._client._request_empty(
            "DELETE",
            f"/v1/companies/{uid}/notes/{note_id}",
        )

    # -- Tags --

    def tags(self, uid: str) -> Response[_list[Tag]]:
        """Get tags for a company."""
        return self._client._request_model(
            "GET",
            f"/v1/companies/{uid}/tags",
            response_type=list[Tag],
        )

    def create_tag(
        self,
        uid: str,
        *,
        tag_name: str,
        color: str | None = None,
    ) -> Response[Tag]:
        """Create a tag on a company."""
        body: dict[str, Any] = {"tagName": tag_name}
        if color is not None:
            body["color"] = color
        return self._client._request_model(
            "POST",
            f"/v1/companies/{uid}/tags",
            json=body,
            response_type=Tag,
        )

    def delete_tag(self, uid: str, tag_id: str) -> ResponseMeta:
        """Delete a tag from a company."""
        return self._client._request_empty(
            "DELETE",
            f"/v1/companies/{uid}/tags/{tag_id}",
        )

    def all_tags(self) -> Response[_list[TagSummary]]:
        """Get all tags with usage counts."""
        return self._client._request_model(
            "GET",
            "/v1/tags",
            response_type=list[TagSummary],
        )

    # -- Excel export --

    def export_excel(
        self,
        *,
        uids: _list[str] | None = None,
        filter: dict[str, Any] | None = None,
        fields: _list[str] | None = None,
    ) -> ExportFile:
        """Export companies as Excel/CSV."""
        body: dict[str, Any] = {}
        if uids is not None:
            body["uids"] = uids
        if filter is not None:
            body["filter"] = filter
        if fields is not None:
            body["fields"] = fields
        return self._client._request_bytes(
            "POST",
            "/v1/companies/export/excel",
            json=body,
        )
