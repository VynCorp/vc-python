from __future__ import annotations

import builtins
from typing import TYPE_CHECKING, Any

from vynco._response import Response, ResponseMeta
from vynco.types.saved_searches import SavedSearch

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client

_list = builtins.list


class AsyncSavedSearches:
    """Async saved search operations."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def list(self) -> Response[_list[SavedSearch]]:
        """List all saved searches."""
        return await self._client._request_model(
            "GET", "/v1/saved-searches", response_type=list[SavedSearch]
        )

    async def create(
        self,
        *,
        name: str,
        search_params: dict[str, Any],
        description: str | None = None,
        is_scheduled: bool = False,
        schedule_frequency: str | None = None,
    ) -> Response[SavedSearch]:
        """Create a new saved search."""
        body: dict[str, Any] = {
            "name": name,
            "searchParams": search_params,
            "isScheduled": is_scheduled,
        }
        if description is not None:
            body["description"] = description
        if schedule_frequency is not None:
            body["scheduleFrequency"] = schedule_frequency
        return await self._client._request_model(
            "POST", "/v1/saved-searches", json=body, response_type=SavedSearch
        )

    async def get(self, id: str) -> Response[SavedSearch]:
        """Get a saved search by ID."""
        return await self._client._request_model(
            "GET", f"/v1/saved-searches/{id}", response_type=SavedSearch
        )

    async def update(
        self,
        id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        search_params: dict[str, Any] | None = None,
        is_scheduled: bool | None = None,
        schedule_frequency: str | None = None,
    ) -> Response[SavedSearch]:
        """Update a saved search."""
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if description is not None:
            body["description"] = description
        if search_params is not None:
            body["searchParams"] = search_params
        if is_scheduled is not None:
            body["isScheduled"] = is_scheduled
        if schedule_frequency is not None:
            body["scheduleFrequency"] = schedule_frequency
        return await self._client._request_model(
            "PUT", f"/v1/saved-searches/{id}", json=body, response_type=SavedSearch
        )

    async def delete(self, id: str) -> ResponseMeta:
        """Delete a saved search."""
        return await self._client._request_empty("DELETE", f"/v1/saved-searches/{id}")


class SavedSearches:
    """Sync saved search operations."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def list(self) -> Response[_list[SavedSearch]]:
        """List all saved searches."""
        return self._client._request_model(
            "GET", "/v1/saved-searches", response_type=list[SavedSearch]
        )

    def create(
        self,
        *,
        name: str,
        search_params: dict[str, Any],
        description: str | None = None,
        is_scheduled: bool = False,
        schedule_frequency: str | None = None,
    ) -> Response[SavedSearch]:
        """Create a new saved search."""
        body: dict[str, Any] = {
            "name": name,
            "searchParams": search_params,
            "isScheduled": is_scheduled,
        }
        if description is not None:
            body["description"] = description
        if schedule_frequency is not None:
            body["scheduleFrequency"] = schedule_frequency
        return self._client._request_model(
            "POST", "/v1/saved-searches", json=body, response_type=SavedSearch
        )

    def get(self, id: str) -> Response[SavedSearch]:
        """Get a saved search by ID."""
        return self._client._request_model(
            "GET", f"/v1/saved-searches/{id}", response_type=SavedSearch
        )

    def update(
        self,
        id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        search_params: dict[str, Any] | None = None,
        is_scheduled: bool | None = None,
        schedule_frequency: str | None = None,
    ) -> Response[SavedSearch]:
        """Update a saved search."""
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if description is not None:
            body["description"] = description
        if search_params is not None:
            body["searchParams"] = search_params
        if is_scheduled is not None:
            body["isScheduled"] = is_scheduled
        if schedule_frequency is not None:
            body["scheduleFrequency"] = schedule_frequency
        return self._client._request_model(
            "PUT", f"/v1/saved-searches/{id}", json=body, response_type=SavedSearch
        )

    def delete(self, id: str) -> ResponseMeta:
        """Delete a saved search."""
        return self._client._request_empty("DELETE", f"/v1/saved-searches/{id}")
