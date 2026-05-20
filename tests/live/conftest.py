"""Fixtures for the opt-in live smoke suite.

These tests hit the real VynCo API and are deselected by default
(``addopts = -m 'not live'``). Run them explicitly with:

    VYNCO_API_KEY=vc_live_... uv run pytest -m live

Set ``VYNCO_BASE_URL`` to point at a non-production instance.
"""

from __future__ import annotations

import os
from collections.abc import Iterator

import pytest

import vynco

LIVE_BASE_URL = os.environ.get("VYNCO_BASE_URL", "https://vynco.ch/api")


@pytest.fixture(scope="session")
def api_key() -> str:
    key = os.environ.get("VYNCO_API_KEY")
    if not key:
        pytest.skip("VYNCO_API_KEY not set; skipping live tests")
    return key


@pytest.fixture
def client(api_key: str) -> Iterator[vynco.Client]:
    c = vynco.Client(api_key, base_url=LIVE_BASE_URL)
    try:
        yield c
    finally:
        c.close()
