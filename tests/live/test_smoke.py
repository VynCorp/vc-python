"""Live smoke tests against the real VynCo API.

Run with: ``VYNCO_API_KEY=vc_live_... uv run pytest -m live -v``

Rules:
- Read-only / idempotent endpoints only (no resource mutation against prod).
- A ``ForbiddenError`` (403) means the key's tier doesn't unlock that group;
  treat it as a skip, not a failure.
- Respect that quotas are finite — keep the surface small.
"""

from __future__ import annotations

import pytest

import vynco

pytestmark = pytest.mark.live

# A stable, well-known Swiss UID (Novartis AG) for detail lookups.
KNOWN_UID = "CHE-105.805.080"


def _skip_if_tier_gated(exc: vynco.VyncoError) -> None:
    """Re-raise unless the failure is a tier gate (403), which becomes a skip."""
    if isinstance(exc, vynco.ForbiddenError):
        pytest.skip(f"tier-gated endpoint: {exc}")
    raise exc


def test_health(client: vynco.Client) -> None:
    resp = client.health.check()
    assert resp.data.status


def test_usage_current(client: vynco.Client) -> None:
    try:
        resp = client.usage.current()
    except vynco.VyncoError as exc:
        _skip_if_tier_gated(exc)
    assert resp.data.tier


def test_company_search(client: vynco.Client) -> None:
    try:
        resp = client.companies.list(query="bank", page_size=3)
    except vynco.VyncoError as exc:
        _skip_if_tier_gated(exc)
    assert resp.data.items, "expected at least one company for query='bank'"
    # The rate-limit metadata should round-trip from real headers.
    assert resp.meta.rate_limit_limit is None or resp.meta.rate_limit_limit >= 0


def test_company_get(client: vynco.Client) -> None:
    try:
        resp = client.companies.get(KNOWN_UID)
    except vynco.VyncoError as exc:
        _skip_if_tier_gated(exc)
    assert resp.data.uid == KNOWN_UID
    assert resp.data.name


def test_company_count(client: vynco.Client) -> None:
    try:
        resp = client.companies.count()
    except vynco.VyncoError as exc:
        _skip_if_tier_gated(exc)
    assert resp.data.count > 0


def test_changes_list(client: vynco.Client) -> None:
    try:
        resp = client.changes.list(page_size=3)
    except vynco.VyncoError as exc:
        _skip_if_tier_gated(exc)
    assert resp.data.items is not None
