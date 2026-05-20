"""UBO Resolution — Identify ultimate beneficial owners for AML compliance.

Walks the ownership chain upward from a company to identify the natural
person(s) who ultimately control it. Combines the UBO endpoint with the
lower-level ownership trace and batch sanctions screening to produce a
compliance-ready report. These endpoints require the Professional tier and are
skipped with a note on lower tiers.

Usage:
    export VYNCO_API_KEY=vc_live_...
    python examples/ubo_resolution.py
"""

from __future__ import annotations

from _common import get_client, section


def main() -> None:
    client = get_client()

    # Pick a target company (Free tier)
    results = client.companies.list(query="UBS", page_size=1)
    if not results.data.items:
        print("No company found for the search; try a different query.")
        return
    target_uid = results.data.items[0].uid
    company_name = results.data.items[0].name
    print(f"=== UBO Resolution: {company_name} ({target_uid}) ===\n")

    # --- Step 1: Resolve UBOs ---
    with section("1. Ultimate Beneficial Owners"):
        u = client.companies.ubo(target_uid).data
        print(f"   Chain depth:   {u.chain_depth} levels")
        print(f"   UBO persons:   {len(u.ubo_persons)}")
        if u.risk_flags:
            print(f"   Risk flags:    {', '.join(u.risk_flags)}")
        for p in u.ubo_persons[:10]:
            auth = f" [{p.signing_authority}]" if p.signing_authority else ""
            print(f"     - {p.name} ({p.role}){auth}")
            print(f"       via {p.controlling_entity_name} (depth {p.path_length})")
    print()

    # --- Steps 2-4: Ownership chain → screening → key persons (depend on the trace) ---
    with section("2. Ownership Chain, Screening & Key Persons"):
        c = client.ownership.trace(target_uid, max_depth=10).data
        print(f"   Assessed at:   {c.assessed_at}")
        print(f"   Risk level:    {c.risk_level}")
        if c.ultimate_parent:
            print(f"   Ultimate parent: {c.ultimate_parent.name} ({c.ultimate_parent.uid})")
        print(f"   Links in chain: {len(c.ownership_chain)}")
        for link in c.ownership_chain[:5]:
            print(
                f"     [{link.depth}] {link.source_name} → {link.target_name} "
                f"({link.relationship_type})"
            )
        if c.circular_flags:
            print(f"\n   ⚠ Circular ownership detected: {len(c.circular_flags)} loops")
            for flag in c.circular_flags[:3]:
                print(f"     - {flag.description}")

        # Screen all entities in the chain
        chain_uids = list({link.target_uid for link in c.ownership_chain} | {target_uid})[:50]
        screening = client.screening.batch(uids=chain_uids)
        clear = sum(1 for r in screening.data.results if r.total_hits == 0)
        hits = [r for r in screening.data.results if r.total_hits > 0]
        print(
            f"\n   Screened {len(screening.data.results)} chain entities: "
            f"{clear} clear, {len(hits)} with hits"
        )
        for r in hits[:5]:
            print(f"     ⚠ {r.company_name}: {r.total_hits} hits [{r.risk_level}]")

        if c.key_persons:
            print("\n   Key persons (significant roles across chain):")
            for kp in c.key_persons[:5]:
                print(f"     {kp.name} — roles at {len(kp.companies)} companies:")
                for role in kp.companies[:3]:
                    print(f"       - {role.role} at {role.company_name}")


if __name__ == "__main__":
    main()
