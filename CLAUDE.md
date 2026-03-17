# CLAUDE.md

## Project

VynCo Python SDK (`vynco`) — Python client for the VynCo Swiss Corporate Intelligence API.

## Build & Test

```bash
uv sync                    # Install all dependencies
uv run pytest              # Run all tests
uv run pytest -x           # Stop on first failure
uv run pytest -k "test_company"  # Run specific tests
uv run ruff check src/     # Lint
uv run ruff format src/    # Format
uv run mypy src/           # Type check
```

## Architecture

- `src/vynco/` — Package source (src layout)
- `_constants.py` — Default base URL, timeout, version
- `_errors.py` — Exception hierarchy (VyncoError → AuthenticationError, etc.)
- `_response.py` — Response[T] and ResponseMeta dataclasses
- `_base_client.py` — Shared HTTP logic, retry, error mapping
- `_client.py` — AsyncClient + Client (sync)
- `types/` — Pydantic v2 models (one file per domain)
- `resources/` — Resource classes (async + sync variants per file)
- `tests/` — pytest + respx tests

## Conventions

- All API models use `VyncoModel` base (Pydantic with camelCase alias)
- Resource methods use keyword-only arguments (not param objects)
- Both sync and async resource classes live in the same file
- The `query` Python parameter maps to `search` on the wire
- Use `from __future__ import annotations` in all modules
