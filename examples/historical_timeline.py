"""Historical Timeline — Reconstruct a company's evolution over time.

Shows how to pull a chronological timeline of all changes on a company (capital
moves, board changes, name changes, address updates) plus an AI-generated
narrative summary. The AI summary requires the Professional tier and is skipped
with a note on lower tiers.

Usage:
    export VYNCO_API_KEY=vc_live_...
    python examples/historical_timeline.py
"""

from __future__ import annotations

from _common import get_client, section


def main() -> None:
    client = get_client()

    # Pick a target company
    results = client.companies.list(query="UBS", page_size=1)
    if not results.data.items:
        print("No company found for the search; try a different query.")
        return
    target_uid = results.data.items[0].uid
    company_name = results.data.items[0].name
    print(f"=== Historical Timeline: {company_name} ({target_uid}) ===\n")

    # --- Full timeline (no date filter) ---
    with section("Full timeline"):
        t = client.companies.timeline(target_uid).data
        print(f"Total events: {t.total_events}\n")

        by_category: dict[str, int] = {}
        for event in t.events:
            by_category[event.category] = by_category.get(event.category, 0) + 1
        print("Events by category:")
        for cat, count in sorted(by_category.items(), key=lambda x: -x[1]):
            print(f"  {cat:<30} {count}")
        print("\nMost recent events:")
        for event in t.events[:10]:
            severity = f"[{event.severity}] " if event.severity else ""
            change = ""
            if event.old_value or event.new_value:
                change = f"  {event.old_value or '—'} → {event.new_value or '—'}"
            print(
                f"  {event.date[:10]}  {severity}{event.category}: {event.field_name or ''}{change}"
            )
            if event.summary:
                print(f"                   {event.summary}")
    print()

    # --- Filtered timeline: capital changes only ---
    with section("Capital changes only"):
        capital_timeline = client.companies.timeline(target_uid, change_type="capital_change")
        print(f"{capital_timeline.data.total_events} events")
        for event in capital_timeline.data.events[:5]:
            print(f"  {event.date[:10]}  {event.old_value or '—'} → {event.new_value or '—'}")
    print()

    # --- AI-generated narrative summary (Professional) ---
    with section("AI Narrative Summary\n" + "-" * 60):
        summary = client.companies.timeline_summary(target_uid)
        print(summary.data.summary)
        print(
            f"\n({summary.data.event_count} events analyzed, "
            f"generated at {summary.data.generated_at})"
        )


if __name__ == "__main__":
    main()
