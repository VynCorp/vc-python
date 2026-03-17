from __future__ import annotations

import asyncio
from typing import Any, TypeVar

import httpx

from vynco._base_client import BaseClientConfig
from vynco._constants import DEFAULT_BASE_URL, DEFAULT_MAX_RETRIES, DEFAULT_TIMEOUT
from vynco._response import Response, ResponseMeta
from vynco.resources.analytics import Analytics, AsyncAnalytics
from vynco.resources.api_keys import ApiKeys, AsyncApiKeys
from vynco.resources.billing import AsyncBilling, Billing
from vynco.resources.changes import AsyncChanges, Changes
from vynco.resources.companies import AsyncCompanies, Companies
from vynco.resources.credits import AsyncCredits, Credits
from vynco.resources.dossiers import AsyncDossiers, Dossiers
from vynco.resources.persons import AsyncPersons, Persons
from vynco.resources.settings import AsyncSettings, Settings
from vynco.resources.teams import AsyncTeams, Teams
from vynco.resources.users import AsyncUsers, Users
from vynco.resources.webhooks import AsyncWebhooks, Webhooks

T = TypeVar("T")


class AsyncClient(BaseClientConfig):
    """Async client for the VynCo API.

    Uses httpx.AsyncClient under the hood. Supports ``async with`` for
    automatic cleanup.

    Example::

        async with vynco.AsyncClient("vc_live_xxx") as client:
            result = await client.companies.search(query="Novartis")
    """

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ) -> None:
        super().__init__(
            api_key=api_key, base_url=base_url, timeout=timeout, max_retries=max_retries,
        )
        self._http = httpx.AsyncClient(
            headers=self._headers(),
            timeout=self.timeout,
        )
        self.companies = AsyncCompanies(self)
        self.persons = AsyncPersons(self)
        self.dossiers = AsyncDossiers(self)
        self.changes = AsyncChanges(self)
        self.credits = AsyncCredits(self)
        self.billing = AsyncBilling(self)
        self.api_keys = AsyncApiKeys(self)
        self.webhooks = AsyncWebhooks(self)
        self.teams = AsyncTeams(self)
        self.users = AsyncUsers(self)
        self.settings = AsyncSettings(self)
        self.analytics = AsyncAnalytics(self)

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, str] | None = None,
        json: Any = None,
    ) -> httpx.Response:
        """Execute an HTTP request with retry logic."""
        url = self._url(path)
        last_exc: Exception | None = None

        for attempt in range(self.max_retries + 1):
            try:
                resp = await self._http.request(
                    method, url, params=params, json=json,
                )
            except httpx.HTTPError as e:
                last_exc = e
                if attempt < self.max_retries:
                    await asyncio.sleep(self._retry_delay(attempt))
                    continue
                raise

            if self._should_retry(resp.status_code) and attempt < self.max_retries:
                delay = self._retry_delay(attempt, resp.headers)
                await asyncio.sleep(delay)
                continue

            return resp

        raise last_exc  # type: ignore[misc]

    async def _request_model(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, str] | None = None,
        json: Any = None,
        response_type: type[T],
    ) -> Response[T]:
        resp = await self._request(method, path, params=params, json=json)
        return self._handle_response(resp, response_type)

    async def _request_empty(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, str] | None = None,
        json: Any = None,
    ) -> ResponseMeta:
        resp = await self._request(method, path, params=params, json=json)
        return self._handle_empty_response(resp)

    async def close(self) -> None:
        await self._http.aclose()

    async def __aenter__(self) -> AsyncClient:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()


class Client(BaseClientConfig):
    """Sync client for the VynCo API.

    Uses httpx.Client under the hood. Supports ``with`` for automatic cleanup.

    Example::

        with vynco.Client("vc_live_xxx") as client:
            result = client.companies.search(query="Novartis")
    """

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ) -> None:
        super().__init__(
            api_key=api_key, base_url=base_url, timeout=timeout, max_retries=max_retries,
        )
        self._http = httpx.Client(
            headers=self._headers(),
            timeout=self.timeout,
        )
        self.companies = Companies(self)
        self.persons = Persons(self)
        self.dossiers = Dossiers(self)
        self.changes = Changes(self)
        self.credits = Credits(self)
        self.billing = Billing(self)
        self.api_keys = ApiKeys(self)
        self.webhooks = Webhooks(self)
        self.teams = Teams(self)
        self.users = Users(self)
        self.settings = Settings(self)
        self.analytics = Analytics(self)

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, str] | None = None,
        json: Any = None,
    ) -> httpx.Response:
        """Execute an HTTP request with retry logic."""
        import time

        url = self._url(path)
        last_exc: Exception | None = None

        for attempt in range(self.max_retries + 1):
            try:
                resp = self._http.request(
                    method, url, params=params, json=json,
                )
            except httpx.HTTPError as e:
                last_exc = e
                if attempt < self.max_retries:
                    time.sleep(self._retry_delay(attempt))
                    continue
                raise

            if self._should_retry(resp.status_code) and attempt < self.max_retries:
                delay = self._retry_delay(attempt, resp.headers)
                time.sleep(delay)
                continue

            return resp

        raise last_exc  # type: ignore[misc]

    def _request_model(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, str] | None = None,
        json: Any = None,
        response_type: type[T],
    ) -> Response[T]:
        resp = self._request(method, path, params=params, json=json)
        return self._handle_response(resp, response_type)

    def _request_empty(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, str] | None = None,
        json: Any = None,
    ) -> ResponseMeta:
        resp = self._request(method, path, params=params, json=json)
        return self._handle_empty_response(resp)

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> Client:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
