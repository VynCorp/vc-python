from __future__ import annotations

import builtins
from typing import TYPE_CHECKING, Any

from vynco._response import Response, ResponseMeta
from vynco.types.pipelines import (
    Pipeline,
    PipelineEntry,
    PipelineStats,
    PipelineWithEntries,
)

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client

_list = builtins.list


class AsyncPipelines:
    """Async pipeline operations for sales/prospect tracking."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def list(self) -> Response[_list[Pipeline]]:
        """List all pipelines."""
        return await self._client._request_model(
            "GET", "/v1/pipelines", response_type=list[Pipeline]
        )

    async def create(self, *, name: str, stages: _list[str] | None = None) -> Response[Pipeline]:
        """Create a new pipeline with optional custom stages."""
        body: dict[str, Any] = {"name": name}
        if stages is not None:
            body["stages"] = stages
        return await self._client._request_model(
            "POST", "/v1/pipelines", json=body, response_type=Pipeline
        )

    async def get(self, id: str) -> Response[PipelineWithEntries]:
        """Get a pipeline with all its entries."""
        return await self._client._request_model(
            "GET", f"/v1/pipelines/{id}", response_type=PipelineWithEntries
        )

    async def delete(self, id: str) -> ResponseMeta:
        """Delete a pipeline."""
        return await self._client._request_empty("DELETE", f"/v1/pipelines/{id}")

    async def add_entry(
        self,
        id: str,
        *,
        company_uid: str,
        stage: str | None = None,
        tier: int | None = None,
        assigned_to_user_id: str | None = None,
    ) -> Response[PipelineEntry]:
        """Add a company to a pipeline."""
        body: dict[str, Any] = {"companyUid": company_uid}
        if stage is not None:
            body["stage"] = stage
        if tier is not None:
            body["tier"] = tier
        if assigned_to_user_id is not None:
            body["assignedToUserId"] = assigned_to_user_id
        return await self._client._request_model(
            "POST",
            f"/v1/pipelines/{id}/entries",
            json=body,
            response_type=PipelineEntry,
        )

    async def update_entry(
        self,
        id: str,
        entry_id: str,
        *,
        stage: str | None = None,
        tier: int | None = None,
        assigned_to_user_id: str | None = None,
        notes: str | None = None,
    ) -> Response[PipelineEntry]:
        """Update a pipeline entry."""
        body: dict[str, Any] = {}
        if stage is not None:
            body["stage"] = stage
        if tier is not None:
            body["tier"] = tier
        if assigned_to_user_id is not None:
            body["assignedToUserId"] = assigned_to_user_id
        if notes is not None:
            body["notes"] = notes
        return await self._client._request_model(
            "PUT",
            f"/v1/pipelines/{id}/entries/{entry_id}",
            json=body,
            response_type=PipelineEntry,
        )

    async def remove_entry(self, id: str, entry_id: str) -> ResponseMeta:
        """Remove an entry from a pipeline."""
        return await self._client._request_empty("DELETE", f"/v1/pipelines/{id}/entries/{entry_id}")

    async def stats(self, id: str) -> Response[PipelineStats]:
        """Get aggregate statistics for a pipeline."""
        return await self._client._request_model(
            "GET", f"/v1/pipelines/{id}/stats", response_type=PipelineStats
        )


class Pipelines:
    """Sync pipeline operations for sales/prospect tracking."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def list(self) -> Response[_list[Pipeline]]:
        """List all pipelines."""
        return self._client._request_model("GET", "/v1/pipelines", response_type=list[Pipeline])

    def create(self, *, name: str, stages: _list[str] | None = None) -> Response[Pipeline]:
        """Create a new pipeline with optional custom stages."""
        body: dict[str, Any] = {"name": name}
        if stages is not None:
            body["stages"] = stages
        return self._client._request_model(
            "POST", "/v1/pipelines", json=body, response_type=Pipeline
        )

    def get(self, id: str) -> Response[PipelineWithEntries]:
        """Get a pipeline with all its entries."""
        return self._client._request_model(
            "GET", f"/v1/pipelines/{id}", response_type=PipelineWithEntries
        )

    def delete(self, id: str) -> ResponseMeta:
        """Delete a pipeline."""
        return self._client._request_empty("DELETE", f"/v1/pipelines/{id}")

    def add_entry(
        self,
        id: str,
        *,
        company_uid: str,
        stage: str | None = None,
        tier: int | None = None,
        assigned_to_user_id: str | None = None,
    ) -> Response[PipelineEntry]:
        """Add a company to a pipeline."""
        body: dict[str, Any] = {"companyUid": company_uid}
        if stage is not None:
            body["stage"] = stage
        if tier is not None:
            body["tier"] = tier
        if assigned_to_user_id is not None:
            body["assignedToUserId"] = assigned_to_user_id
        return self._client._request_model(
            "POST",
            f"/v1/pipelines/{id}/entries",
            json=body,
            response_type=PipelineEntry,
        )

    def update_entry(
        self,
        id: str,
        entry_id: str,
        *,
        stage: str | None = None,
        tier: int | None = None,
        assigned_to_user_id: str | None = None,
        notes: str | None = None,
    ) -> Response[PipelineEntry]:
        """Update a pipeline entry."""
        body: dict[str, Any] = {}
        if stage is not None:
            body["stage"] = stage
        if tier is not None:
            body["tier"] = tier
        if assigned_to_user_id is not None:
            body["assignedToUserId"] = assigned_to_user_id
        if notes is not None:
            body["notes"] = notes
        return self._client._request_model(
            "PUT",
            f"/v1/pipelines/{id}/entries/{entry_id}",
            json=body,
            response_type=PipelineEntry,
        )

    def remove_entry(self, id: str, entry_id: str) -> ResponseMeta:
        """Remove an entry from a pipeline."""
        return self._client._request_empty("DELETE", f"/v1/pipelines/{id}/entries/{entry_id}")

    def stats(self, id: str) -> Response[PipelineStats]:
        """Get aggregate statistics for a pipeline."""
        return self._client._request_model(
            "GET", f"/v1/pipelines/{id}/stats", response_type=PipelineStats
        )
