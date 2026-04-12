"""Quickstart — Search Swiss companies, fetch details, and check your credits.

Usage:
    export VYNCO_API_KEY=vc_live_...
    python examples/quickstart.py
"""

from __future__ import annotations

import vynco


def main() -> None:
    client = vynco.Client()

    # --- Check API health ---
    health = client.health.check()
    print(f"API status: {health.data.status}\n")

    # --- Database overview ---
    count = client.companies.count()
    print(f"Total companies in database: {count.data.count:,}\n")

    # --- Search for companies ---
    results = client.companies.list(query="Nestlé", page_size=5)
    print(f"Search 'Nestlé': {results.data.total} results")
    for company in results.data.items:
        canton = company.canton or ""
        status = company.status or ""
        print(f"  {company.uid}  {company.name:<50} {canton:<4} {status}")

    # --- Get a single company by UID ---
    uid = results.data.items[0].uid
    detail = client.companies.get(uid)
    c = detail.data
    print(f"\n--- {c.name} ---")
    print(f"  UID:          {c.uid}")
    print(f"  Legal form:   {c.legal_form}")
    print(f"  Status:       {c.status}")
    print(f"  Canton:       {c.canton}")
    if c.share_capital:
        print(f"  Capital:      {c.share_capital:,.0f} {c.currency}")
    print(f"  Purpose:      {(c.purpose or '')[:120]}...")
    print(
        f"  Address:      {c.address_street} {c.address_house_number or ''}, "
        f"{c.address_zip_code} {c.address_city}"
    )

    # --- Get full company profile (persons + changes + relationships) ---
    full = client.companies.get_full(uid)
    print(f"\n  Board members: {len(full.data.persons)}")
    for p in full.data.persons[:5]:
        print(f"    - {p.first_name} {p.last_name} ({p.role})")
    print(f"  Recent changes: {len(full.data.recent_changes)}")
    print(f"  Relationships:  {len(full.data.relationships)}")

    # --- Response metadata (every call includes this) ---
    print(
        f"\n[Request {detail.meta.request_id} | "
        f"Credits used: {detail.meta.credits_used} | "
        f"Remaining: {detail.meta.credits_remaining}]"
    )


if __name__ == "__main__":
    main()
