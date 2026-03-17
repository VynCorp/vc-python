from __future__ import annotations

import os
from typing import Any, TypeVar, get_args, get_origin

import httpx
from pydantic import BaseModel

from vynco._constants import DEFAULT_BASE_URL, DEFAULT_MAX_RETRIES, DEFAULT_TIMEOUT, __version__
from vynco._errors import (
    STATUS_ERROR_MAP,
    ConfigError,
    DeserializationError,
    ServerError,
    VyncoError,
)
from vynco._response import Response, ResponseMeta

T = TypeVar("T")

_PARAM_RENAME = {"query": "search"}


def _build_params(kwargs: dict[str, Any]) -> dict[str, str]:
    """Build query parameters from keyword arguments, dropping None values."""
    params: dict[str, str] = {}
    for key, value in kwargs.items():
        if key == "self" or value is None:
            continue
        wire_key = _PARAM_RENAME.get(key, key)
        # Convert snake_case to camelCase for the wire
        parts = wire_key.split("_")
        camel = parts[0] + "".join(p.capitalize() for p in parts[1:])
        params[camel] = str(value).lower() if isinstance(value, bool) else str(value)
    return params


def _parse_meta(headers: httpx.Headers) -> ResponseMeta:
    """Extract metadata from API response headers."""
    return ResponseMeta(
        request_id=headers.get("X-Request-Id"),
        credits_used=_parse_int(headers.get("X-Credits-Used")),
        credits_remaining=_parse_int(headers.get("X-Credits-Remaining")),
        rate_limit_limit=_parse_int(headers.get("X-Rate-Limit-Limit")),
        data_source=headers.get("X-Data-Source"),
    )


def _parse_int(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def _map_error(status_code: int, body: dict[str, Any]) -> VyncoError:
    """Map an HTTP status code and response body to a typed error."""
    detail = body.get("detail", "")
    message = body.get("message", "")
    status = body.get("status", status_code)

    error_cls = STATUS_ERROR_MAP.get(status_code)
    if error_cls:
        return error_cls(detail=detail, message=message, status=status)
    if status_code >= 500:
        return ServerError(detail=detail, message=message, status=status)
    return ServerError(detail=detail or f"HTTP {status_code}", message=message, status=status)


def _deserialize(data: Any, response_type: type[T]) -> T:
    """Deserialize JSON data into the given type."""
    origin = get_origin(response_type)
    args = get_args(response_type)

    # list[X]
    if origin is list and args:
        item_type = args[0]
        if isinstance(data, list):
            items = data
        elif isinstance(data, dict):
            # Try "data" key, then first array-valued key
            items = data.get("data")
            if not isinstance(items, list):
                for val in data.values():
                    if isinstance(val, list):
                        items = val
                        break
                else:
                    items = [data]
        else:
            items = [data]
        if issubclass(item_type, BaseModel):
            return [item_type.model_validate(item) for item in items]  # type: ignore[return-value]
        return items  # type: ignore[return-value]

    # Pydantic model (including generics like PaginatedResponse[Company])
    if isinstance(response_type, type) and issubclass(response_type, BaseModel):
        return response_type.model_validate(data)
    if origin and args and isinstance(origin, type) and issubclass(origin, BaseModel):
        # Generic model like PaginatedResponse[Company]
        concrete = response_type  # Already parameterized
        if isinstance(concrete, type) and issubclass(concrete, BaseModel):
            return concrete.model_validate(data)
        # For runtime generics, we need the origin class
        return origin.model_validate(data)

    # dict or other simple types
    return data  # type: ignore[return-value]


class BaseClientConfig:
    """Shared configuration for async and sync clients."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ) -> None:
        self.api_key = api_key or os.environ.get("VYNCO_API_KEY", "")
        if not self.api_key:
            raise ConfigError("API key must not be empty. Pass api_key or set VYNCO_API_KEY.")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": f"vynco-python/{__version__}",
        }

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def _retry_delay(self, attempt: int, headers: httpx.Headers | None = None) -> float:
        """Compute retry delay with exponential backoff, respecting Retry-After."""
        if headers:
            retry_after = headers.get("Retry-After")
            if retry_after:
                try:
                    return float(retry_after)
                except ValueError:
                    pass
        return 0.5 * (2**attempt)

    def _should_retry(self, status_code: int) -> bool:
        return status_code == 429 or status_code >= 500

    def _handle_response(
        self, resp: httpx.Response, response_type: type[T]
    ) -> Response[T]:
        meta = _parse_meta(resp.headers)

        if not resp.is_success:
            try:
                body = resp.json()
            except Exception:
                body = {"detail": resp.text, "status": resp.status_code}
            raise _map_error(resp.status_code, body)

        if resp.status_code == 204 or not resp.content:
            return Response(data=None, meta=meta)  # type: ignore[arg-type]

        try:
            data = resp.json()
        except Exception as e:
            raise DeserializationError(detail=f"Failed to parse JSON: {e}") from e

        try:
            parsed = _deserialize(data, response_type)
        except Exception as e:
            raise DeserializationError(detail=f"Failed to deserialize response: {e}") from e

        return Response(data=parsed, meta=meta)

    def _handle_empty_response(self, resp: httpx.Response) -> ResponseMeta:
        meta = _parse_meta(resp.headers)
        if not resp.is_success:
            try:
                body = resp.json()
            except Exception:
                body = {"detail": resp.text, "status": resp.status_code}
            raise _map_error(resp.status_code, body)
        return meta
