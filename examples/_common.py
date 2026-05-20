"""Shared helpers for the VynCo SDK examples.

Run any example with:

    export VYNCO_API_KEY=vc_live_...
    python examples/<name>.py

The ``section`` context manager makes every example *tier-resilient*: a call
that the current API key's tier doesn't unlock returns 403, and instead of
crashing the script we print a short note and move on. So the same example runs
end-to-end on Free, Professional, or Enterprise keys.
"""

from __future__ import annotations

import contextlib
import os
import sys
from collections.abc import Iterator

import vynco


def get_client() -> vynco.Client:
    """Construct a client, exiting with a friendly hint if the key is missing."""
    if not os.environ.get("VYNCO_API_KEY"):
        sys.exit("Set your API key first:  export VYNCO_API_KEY=vc_live_...")
    return vynco.Client()


@contextlib.contextmanager
def section(title: str) -> Iterator[None]:
    """Print ``title``, run the block, and degrade gracefully on expected errors.

    - ``ForbiddenError`` (403) → the key's tier doesn't unlock this endpoint;
      print the upgrade hint and skip the rest of the block.
    - ``ServiceUnavailableError`` / ``ServerError`` → a transient/LLM outage;
      skip with a note rather than aborting the whole example.
    """
    print(title)
    try:
        yield
    except vynco.ForbiddenError as exc:
        print(f"   [skipped — {exc}]")
    except vynco.RateLimitError as exc:
        print(f"   [skipped — rate limited (try again later): {exc}]")
    except (vynco.ServiceUnavailableError, vynco.ServerError) as exc:
        print(f"   [skipped — service unavailable: {type(exc).__name__}]")
