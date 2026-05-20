"""Company Network — Explore corporate relationships, hierarchy, and graph data.

Demonstrates how to map the corporate network around a company: who are the
board members, what other companies are they connected to, and how does the
ownership hierarchy look. Multi-company graph analysis requires the Professional
tier and is skipped with a note on lower tiers.

Usage:
    export VYNCO_API_KEY=vc_live_...
    python examples/company_network.py
"""

from __future__ import annotations

from _common import get_client, section


def main() -> None:
    client = get_client()

    # Find target company (UBS has rich network data)
    results = client.companies.list(query="UBS", page_size=1)
    if not results.data.items:
        print("No company found for the search; try a different query.")
        return
    target_uid = results.data.items[0].uid
    company = client.companies.get(target_uid).data
    print(f"=== Corporate Network: {company.name} ===\n")

    # --- Board members ---
    with section("1. Board Members"):
        members = client.persons.board_members(target_uid)
        for m in members.data[:15]:
            authority = f" [{m.signing_authority}]" if m.signing_authority else ""
            since = f" (since {m.since})" if m.since else ""
            print(f"   {m.first_name} {m.last_name} — {m.role}{authority}{since}")
        if len(members.data) > 15:
            print(f"   ... and {len(members.data) - 15} more ({len(members.data)} total)")
    print()

    # --- Corporate relationships ---
    with section("2. Corporate Relationships"):
        rels = client.companies.relationships(target_uid)
        by_type: dict[str, list[str]] = {}
        for rel in rels.data:
            by_type.setdefault(rel.relationship_type, []).append(rel.related_name)
        for rel_type, names in by_type.items():
            print(f"   {rel_type}:")
            for name in names[:5]:
                print(f"     - {name}")
            if len(names) > 5:
                print(f"     ... and {len(names) - 5} more")
    print()

    # --- Hierarchy ---
    with section("3. Corporate Hierarchy"):
        h = client.companies.hierarchy(target_uid).data
        if h.parent:
            print(f"   Parent: {h.parent.name} ({h.parent.uid})")
        print(f"   Subsidiaries: {len(h.subsidiaries)}")
        for sub in h.subsidiaries[:5]:
            conf = f" [confidence: {sub.confidence}]" if sub.confidence else ""
            shared = (
                f" — {sub.shared_person_count} shared persons" if sub.shared_person_count else ""
            )
            print(f"     - {sub.name} ({sub.uid}){conf}{shared}")
        if len(h.subsidiaries) > 5:
            print(f"     ... and {len(h.subsidiaries) - 5} more")
        if h.siblings:
            print(f"   Siblings: {len(h.siblings)}")
    print()

    # --- Corporate structure ---
    with section("4. Corporate Structure"):
        st = client.companies.structure(target_uid).data
        if st.head_offices:
            print(f"   Head offices: {len(st.head_offices)}")
            for ho in st.head_offices[:3]:
                print(f"     - {ho.name} ({ho.uid})")
        if st.branch_offices:
            print(f"   Branch offices: {len(st.branch_offices)}")
            for bo in st.branch_offices[:3]:
                print(f"     - {bo.name} ({bo.uid})")
    print()

    # --- Network graph ---
    with section("5. Network Graph"):
        g = client.graph.get(target_uid).data
        company_nodes = [n for n in g.nodes if n.node_type in ("company", "root")]
        person_nodes = [n for n in g.nodes if n.node_type == "person"]
        print(
            f"   Nodes: {len(g.nodes)} "
            f"({len(company_nodes)} companies, {len(person_nodes)} persons)"
        )
        print(f"   Links: {len(g.links)}")
        link_types: dict[str, int] = {}
        for link in g.links:
            link_types[link.link_type] = link_types.get(link.link_type, 0) + 1
        for lt, count in sorted(link_types.items(), key=lambda x: -x[1]):
            print(f"     {lt}: {count}")
    print()

    # --- Multi-company network analysis (Professional) ---
    with section("6. Multi-Company Network Analysis"):
        abb = client.companies.list(query="ABB", canton="ZH", page_size=1).data.items[0]
        a = client.graph.analyze(uids=[target_uid, abb.uid], overlay="persons").data
        print(f"   Nodes: {len(a.nodes)}, Links: {len(a.links)}")
        print(f"   Clusters found: {len(a.clusters)}")
        for cluster in a.clusters:
            print(
                f"     Cluster {cluster.id}: "
                f"{len(cluster.company_uids)} companies, "
                f"{len(cluster.shared_persons)} shared persons"
            )


if __name__ == "__main__":
    main()
