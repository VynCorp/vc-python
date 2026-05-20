"""Tests for client configuration, authentication, error mapping, and retry logic."""

from __future__ import annotations

import httpx
import pytest
import respx

import vynco

BASE_URL = "https://vynco.ch/api"


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


def test_empty_api_key_raises_config_error(monkeypatch):
    # An empty key falls back to the env var, so null it to keep this hermetic
    # even when VYNCO_API_KEY is exported (e.g. for the live suite).
    monkeypatch.delenv("VYNCO_API_KEY", raising=False)
    with pytest.raises(vynco.ConfigError, match="empty"):
        vynco.Client("")


def test_none_api_key_without_env_raises_config_error(monkeypatch):
    monkeypatch.delenv("VYNCO_API_KEY", raising=False)
    with pytest.raises(vynco.ConfigError, match="empty"):
        vynco.Client(None)


def test_api_key_from_env(monkeypatch):
    monkeypatch.setenv("VYNCO_API_KEY", "vc_test_from_env")
    client = vynco.Client()
    assert client.api_key == "vc_test_from_env"


def test_custom_base_url():
    client = vynco.Client("vc_test_key", base_url="https://custom.api.com/v2/")
    assert client.base_url == "https://custom.api.com/v2"


def test_default_base_url():
    client = vynco.Client("vc_test_key")
    assert client.base_url == "https://vynco.ch/api"


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------


async def test_authorization_header_is_set():
    with respx.mock(base_url=BASE_URL) as mock:
        route = mock.get("/v1/usage/current").mock(
            return_value=httpx.Response(
                200,
                json={"tier": "basic", "groups": []},
            )
        )

        client = vynco.AsyncClient("vc_test_123", base_url=BASE_URL, max_retries=0)
        await client.usage.current()

        assert route.called
        request = route.calls[0].request
        assert request.headers["Authorization"] == "Bearer vc_test_123"
        assert "vynco-python/" in request.headers["User-Agent"]


# ---------------------------------------------------------------------------
# Error mapping
# ---------------------------------------------------------------------------


async def test_not_found_error():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/v1/companies/CHE-000.000.000").mock(
            return_value=httpx.Response(
                404,
                json={"detail": "Company not found", "status": 404},
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        with pytest.raises(vynco.NotFoundError) as exc_info:
            await client.companies.get("CHE-000.000.000")
        assert exc_info.value.detail == "Company not found"
        assert exc_info.value.status == 404


async def test_authentication_error():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/v1/usage/current").mock(
            return_value=httpx.Response(
                401,
                json={"detail": "Invalid API key", "status": 401},
            )
        )

        client = vynco.AsyncClient("vc_test_bad", base_url=BASE_URL, max_retries=0)
        with pytest.raises(vynco.AuthenticationError) as exc_info:
            await client.usage.current()
        assert exc_info.value.detail == "Invalid API key"


async def test_rate_limit_error():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/v1/usage/current").mock(
            return_value=httpx.Response(
                429,
                json={"detail": "Rate limit exceeded", "status": 429},
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        with pytest.raises(vynco.RateLimitError) as exc_info:
            await client.usage.current()
        assert exc_info.value.detail == "Rate limit exceeded"


async def test_server_error():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/v1/usage/current").mock(
            return_value=httpx.Response(
                500,
                json={"detail": "Internal server error", "status": 500},
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        with pytest.raises(vynco.ServerError) as exc_info:
            await client.usage.current()
        assert exc_info.value.detail == "Internal server error"


async def test_insufficient_credits_error():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/v1/dossiers").mock(
            return_value=httpx.Response(
                402,
                json={"detail": "Insufficient credits", "status": 402},
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        with pytest.raises(vynco.InsufficientCreditsError) as exc_info:
            await client.dossiers.create(uid="CHE-100.000.000", level="detailed")
        assert exc_info.value.detail == "Insufficient credits"


async def test_validation_error():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/v1/companies").mock(
            return_value=httpx.Response(
                422,
                json={"detail": "Invalid canton code", "status": 422},
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        with pytest.raises(vynco.ValidationError) as exc_info:
            await client.companies.list(canton="INVALID")
        assert exc_info.value.detail == "Invalid canton code"


async def test_forbidden_error():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/v1/api-keys").mock(
            return_value=httpx.Response(
                403,
                json={"detail": "Insufficient permissions", "status": 403},
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        with pytest.raises(vynco.ForbiddenError) as exc_info:
            await client.api_keys.list()
        assert exc_info.value.detail == "Insufficient permissions"


async def test_conflict_error():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/v1/watchlists").mock(
            return_value=httpx.Response(
                409,
                json={"detail": "Watchlist already exists", "status": 409},
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        with pytest.raises(vynco.ConflictError) as exc_info:
            await client.watchlists.create(name="Test")
        assert exc_info.value.detail == "Watchlist already exists"


async def test_service_unavailable_error():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/v1/usage/current").mock(
            return_value=httpx.Response(
                503,
                json={"detail": "Service temporarily unavailable", "status": 503},
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        with pytest.raises(vynco.ServiceUnavailableError) as exc_info:
            await client.usage.current()
        assert exc_info.value.detail == "Service temporarily unavailable"


# ---------------------------------------------------------------------------
# Response metadata
# ---------------------------------------------------------------------------


async def test_response_meta_from_headers():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/v1/teams/me").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "team_001",
                    "name": "Acme Corp",
                    "slug": "acme-corp",
                    "tier": "enterprise",
                    "creditBalance": 10000,
                    "monthlyCredits": 10000,
                },
                headers={
                    "X-Request-Id": "req-xyz-789",
                    "X-RateLimit-Group": "standard",
                    "X-RateLimit-Window": "hour",
                    "X-RateLimit-Limit": "300",
                    "X-RateLimit-Remaining": "299",
                    "X-RateLimit-Reset": "1711800000",
                    "X-Data-Source": "LINDAS",
                },
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.teams.me()

        assert resp.meta.request_id == "req-xyz-789"
        assert resp.meta.rate_limit_group == "standard"
        assert resp.meta.rate_limit_window == "hour"
        assert resp.meta.rate_limit_limit == 300
        assert resp.meta.rate_limit_remaining == 299
        assert resp.meta.rate_limit_reset == 1711800000
        assert resp.meta.data_source == "LINDAS"
        assert resp.data.name == "Acme Corp"
        assert resp.data.tier == "enterprise"


# ---------------------------------------------------------------------------
# Retry logic
# ---------------------------------------------------------------------------


async def test_retry_on_429():
    with respx.mock(base_url=BASE_URL) as mock:
        route = mock.get("/v1/usage/current").mock(
            side_effect=[
                httpx.Response(429, json={"detail": "Rate limited", "status": 429}),
                httpx.Response(
                    200,
                    json={"tier": "free", "groups": []},
                ),
            ]
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=1)
        resp = await client.usage.current()

        assert resp.data.tier == "free"
        assert route.call_count == 2


async def test_retry_on_500():
    with respx.mock(base_url=BASE_URL) as mock:
        route = mock.get("/v1/usage/current").mock(
            side_effect=[
                httpx.Response(500, json={"detail": "Server error", "status": 500}),
                httpx.Response(
                    200,
                    json={"tier": "free", "groups": []},
                ),
            ]
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=1)
        resp = await client.usage.current()

        assert resp.data.tier == "free"
        assert route.call_count == 2


async def test_no_retry_on_404():
    with respx.mock(base_url=BASE_URL) as mock:
        route = mock.get("/v1/companies/CHE-000.000.000").mock(
            return_value=httpx.Response(
                404,
                json={"detail": "Not found", "status": 404},
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=2)
        with pytest.raises(vynco.NotFoundError):
            await client.companies.get("CHE-000.000.000")

        assert route.call_count == 1


# ---------------------------------------------------------------------------
# Sync client
# ---------------------------------------------------------------------------


def test_sync_client_works():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/v1/usage/current").mock(
            return_value=httpx.Response(
                200,
                json={"tier": "professional", "groups": []},
            )
        )

        client = vynco.Client("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = client.usage.current()

        assert resp.data.tier == "professional"


def test_sync_context_manager():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/v1/usage/current").mock(
            return_value=httpx.Response(
                200,
                json={"tier": "free", "groups": []},
            )
        )

        with vynco.Client("vc_test_key", base_url=BASE_URL, max_retries=0) as client:
            resp = client.usage.current()
            assert resp.data.tier == "free"
