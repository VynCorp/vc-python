from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import AliasChoices, BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

T = TypeVar("T")


class VyncoModel(BaseModel):
    """Base for all VynCo API models."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="ignore",
    )


class PaginatedResponse(VyncoModel, Generic[T]):
    """Paginated response wrapper used by list endpoints."""

    items: list[T]
    total: int = Field(0, validation_alias=AliasChoices("total", "totalCount"))
    page: int = 0
    page_size: int = 0
