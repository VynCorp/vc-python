"""api_gap.py — diff VynCo axum router routes against SDK resource wire paths.

Usage:
    python scripts/api_gap.py [api_repo_root]

    api_repo_root defaults to /home/michael/DEV/Repos/VyncCorpApi/VynCorpApi

Prints two buckets:
  - SDK-only (phantom)  : SDK paths with no matching API route
  - API-only (missing)  : in-scope API routes with no matching SDK path
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DEFAULT_API_ROOT = Path("/home/michael/DEV/Repos/VyncCorpApi/VynCorpApi")

ROUTER_REL = Path("src/routes/mod.rs")

SDK_RESOURCES_REL = Path("src/vynco/resources")

# Prefixes (WITHOUT /v1) — API paths that start with any of these are excluded
# from the "missing" bucket.  We normalise API paths by stripping a leading
# /v1 before this check.
OUT_OF_SCOPE_PREFIXES: tuple[str, ...] = (
    "/auth",
    "/blog",
    "/widget",
    "/public",
    "/webhooks/stripe",
    "/monitoring",
    "/sync/trigger",
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# Match any path segment that looks like a named parameter: {uid}, {id}, etc.
_PARAM_RE = re.compile(r"\{[^}]+\}")


def normalise(path: str) -> str:
    """Canonicalise a path for comparison.

    1. Strip a leading ``/v1`` prefix (SDK paths have it, router paths don't).
    2. Collapse all ``{param}`` placeholders to ``{}``.
    """
    p = path
    if p.startswith("/v1"):
        p = p[3:]  # strip exactly "/v1" (3 chars)
    p = _PARAM_RE.sub("{}", p)
    return p


def is_out_of_scope(normalised_api_path: str) -> bool:
    """Return True if this (already-normalised) API path should be excluded."""
    for prefix in OUT_OF_SCOPE_PREFIXES:
        # Normalise the prefix itself (no-op here since prefixes have no /v1,
        # but collapse params just in case).
        norm_prefix = _PARAM_RE.sub("{}", prefix)
        if normalised_api_path == norm_prefix or normalised_api_path.startswith(
            norm_prefix + "/"
        ):
            return True
    return False


# ---------------------------------------------------------------------------
# API route extraction  (axum router)
# ---------------------------------------------------------------------------

# Matches:  .route("/some/path", …)
# Captures the raw path string.
_ROUTE_RE = re.compile(r'\.route\(\s*"(/[^"]*)"')


def extract_api_paths(router_file: Path) -> set[str]:
    """Return the set of normalised paths registered in the axum router.

    Paths inside ``api_routes`` are already WITHOUT the ``/v1`` prefix (it is
    added by ``.nest("/v1", api_routes(state))``).  The only path that lives
    outside that nest and starts directly from root is ``/health`` in
    ``router()``.  We want to capture everything in ``api_routes``.

    Strategy: parse the whole file and treat every ``.route(...)`` line as a
    candidate; strip the ``/v1`` prefix from any that happen to carry it
    (none should, but defensive) and normalise.
    """
    text = router_file.read_text()
    paths: set[str] = set()
    for m in _ROUTE_RE.finditer(text):
        raw = m.group(1)
        paths.add(normalise(raw))
    return paths


# ---------------------------------------------------------------------------
# SDK path extraction  (Python resource files)
# ---------------------------------------------------------------------------

# Match plain string literals:   "/v1/something"
_SDK_STR_RE = re.compile(r'"/v1(/[^"]*)"')

# Match f-string literals:        f"/v1/companies/{uid}/events"
# We capture everything after /v1 up to the closing quote.
_SDK_FSTR_RE = re.compile(r'f"/v1(/[^"]*)"')


def extract_sdk_paths(resources_dir: Path) -> set[str]:
    """Return the set of normalised wire paths found in all resource .py files."""
    paths: set[str] = set()
    for py_file in resources_dir.glob("*.py"):
        if py_file.name.startswith("_"):
            continue  # skip __init__.py etc.
        text = py_file.read_text()
        for m in _SDK_STR_RE.finditer(text):
            raw = "/v1" + m.group(1)
            paths.add(normalise(raw))
        for m in _SDK_FSTR_RE.finditer(text):
            raw = "/v1" + m.group(1)
            paths.add(normalise(raw))
    return paths


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    api_root = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_API_ROOT
    router_file = api_root / ROUTER_REL

    # Resolve SDK resources relative to this script's parent directory.
    sdk_root = Path(__file__).parent.parent
    resources_dir = sdk_root / SDK_RESOURCES_REL

    if not router_file.exists():
        print(f"ERROR: router file not found: {router_file}", file=sys.stderr)
        sys.exit(1)
    if not resources_dir.is_dir():
        print(f"ERROR: resources dir not found: {resources_dir}", file=sys.stderr)
        sys.exit(1)

    api_paths = extract_api_paths(router_file)
    sdk_paths = extract_sdk_paths(resources_dir)

    # Phantom: SDK has it, API doesn't
    phantom = sorted(sdk_paths - api_paths)

    # Missing: API has it, SDK doesn't, and it's in-scope
    missing = sorted(
        p for p in (api_paths - sdk_paths) if not is_out_of_scope(p)
    )

    print("=" * 60)
    print("SDK-only (phantom — fix or remove)")
    print("=" * 60)
    if phantom:
        for p in phantom:
            print(f"  {p}")
    else:
        print("  (none)")

    print()
    print("=" * 60)
    print("API-only & in-scope (missing from SDK)")
    print("=" * 60)
    if missing:
        for p in missing:
            print(f"  {p}")
    else:
        print("  (none)")

    print()
    print(
        f"Totals: {len(phantom)} phantom, {len(missing)} missing"
        f"  (API routes: {len(api_paths)}, SDK paths: {len(sdk_paths)})"
    )


if __name__ == "__main__":
    main()
