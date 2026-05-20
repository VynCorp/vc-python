from __future__ import annotations

from typing import Any

from pydantic import ConfigDict
from pydantic.alias_generators import to_camel

from vynco.types.shared import VyncoModel


class Preferences(VyncoModel):
    """User UI/notification preferences (free-form blob).

    The API stores and returns an arbitrary JSON object; the fields below are
    the known defaults. Any additional keys are preserved (``extra="allow"``).
    """

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="allow",
    )

    theme: str | None = None
    language: str | None = None
    notifications: dict[str, Any] | None = None
