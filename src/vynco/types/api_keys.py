from __future__ import annotations

from vynco.types.shared import VyncoModel


class ApiKey(VyncoModel):
    """An API key (metadata only)."""

    id: str
    name: str = ""
    prefix: str = ""
    environment: str = ""
    scopes: list[str] = []
    status: str = ""
    expires_at: str | None = None
    created_at: str = ""
    last_used_at: str | None = None


class ApiKeyCreated(VyncoModel):
    """Response from creating an API key (includes the secret key)."""

    key: str
    id: str
    name: str = ""
    prefix: str = ""
    environment: str = ""
    scopes: list[str] = []
    expires_at: str | None = None
    created_at: str = ""
    warning: str = ""
