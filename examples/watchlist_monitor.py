"""Watchlist Monitor — Create a watchlist, add companies, and monitor for changes.

Demonstrates portfolio monitoring: set up a watchlist of companies you care about,
then poll for events and recent corporate changes. Tier-gated steps are skipped
with a note rather than failing.

Usage:
    export VYNCO_API_KEY=vc_live_...
    python examples/watchlist_monitor.py
"""

from __future__ import annotations

from _common import get_client, section

import vynco


def main() -> None:
    client = get_client()

    # --- Find companies to monitor (Free tier) ---
    print("=== Portfolio Monitoring ===\n")
    target_uids = []
    for query in ["ABB", "UBS", "Novartis"]:
        results = client.companies.list(query=query, page_size=1)
        if results.data.items:
            co = results.data.items[0]
            target_uids.append(co.uid)
            print(f"  Found: {co.name} ({co.uid})")

    # --- Create and populate a watchlist ---
    wl_id: str | None = None
    with section("\nCreate & populate watchlist"):
        wl = client.watchlists.create(
            name="Swiss Blue Chips",
            description="Top Swiss companies to monitor for regulatory changes",
        ).data
        wl_id = wl.id
        print(f"  Created watchlist: {wl.name} (id: {wl.id})")
        added = client.watchlists.add_companies(wl.id, uids=target_uids)
        print(f"  Added {added.data.added} companies")

        wl_companies = client.watchlists.companies(wl.id)
        print("  Companies in watchlist:")
        if wl_companies.data.companies:
            for entry in wl_companies.data.companies:
                canton = f" [{entry.canton}]" if entry.canton else ""
                status = f" {entry.status}" if entry.status else ""
                print(f"    - {entry.name or entry.uid} ({entry.uid}){canton}{status}")
        else:
            for uid in wl_companies.data.uids:
                print(f"    - {uid}")
    print()

    if wl_id is not None:
        with section("Recent watchlist events"):
            events = client.watchlists.events(wl_id, limit=10)
            print(f"  {events.data.count} total")
            for evt in events.data.events[:5]:
                print(f"    [{evt.severity}] {evt.company_name}: {evt.summary} ({evt.ce_time})")
        print()

    # --- Recent corporate changes (Free tier) ---
    with section("Recent corporate changes across Switzerland"):
        changes = client.changes.list(page_size=10)
        for ch in changes.data.items[:5]:
            print(
                f"  {ch.company_name or ch.company_uid}: "
                f"{ch.change_type} — {ch.field_name}: {ch.old_value} → {ch.new_value}"
            )
    print()

    # --- Change statistics ---
    with section("Change statistics"):
        s = client.changes.statistics().data
        print(f"  Total changes:    {s.total_changes:,}")
        print(f"  This week:        {s.changes_this_week:,}")
        print(f"  This month:       {s.changes_this_month:,}")

    # --- Clean up (best-effort) ---
    if wl_id is not None:
        try:
            client.watchlists.delete(wl_id)
            print("\nWatchlist deleted.")
        except vynco.VyncoError as exc:
            print(f"\n[cleanup skipped — {type(exc).__name__}]")


if __name__ == "__main__":
    main()
