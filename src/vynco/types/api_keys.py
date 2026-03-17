from __future__ import annotations

from vynco.types.shared import VyncoModel


class ApiKeyInfo(VyncoModel):
    """An existing API key (secret is redacted)."""

    id: str
    name: str = ""
    key_prefix: str = ""
    key_hint: str = ""
    permissions: list[str] = []
    is_active: bool = False
    last_used_at: str | None = None
    created_at: str = ""
    expires_at: str | None = None


class ApiKeyCreated(VyncoModel):
    """A newly created API key (includes the full secret, shown only once)."""

    id: str
    name: str = ""
    raw_key: str = ""
    key_prefix: str = ""
    permissions: list[str] = []
    created_at: str = ""
    expires_at: str | None = None
