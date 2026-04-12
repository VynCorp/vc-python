"""Company Network — Explore corporate relationships, hierarchy, and graph data.

Demonstrates how to map the corporate network around a company: who are the
board members, what other companies are they connected to, and how does the
ownership hierarchy look.

Usage:
    export VYNCO_API_KEY=vc_live_...
    python examples/company_network.py
"""

from __future__ import annotations

import vynco


def main() -> None:
    client = vynco.Client()

    # Find target company (UBS has rich network data)
    results = client.companies.list(query="UBS", page_size=1)
    target_uid = results.data.items[0].uid
    company = client.companies.get(target_uid).data
    print(f"=== Corporate Network: {company.name} ===\n")

    # --- Board members ---
    print("1. Board Members")
    members = client.persons.board_members(target_uid)
    for m in members.data[:15]:
        authority = f" [{m.signing_authority}]" if m.signing_authority else ""
        since = f" (since {m.since})" if m.since else ""
        print(f"   {m.first_name} {m.last_name} — {m.role}{authority}{since}")
    if len(members.data) > 15:
        print(f"   ... and {len(members.data) - 15} more ({len(members.data)} total)")
    print()

    # --- Corporate relationships ---
    print("2. Corporate Relationships")
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
    print("3. Corporate Hierarchy")
    hierarchy = client.companies.hierarchy(target_uid)
    h = hierarchy.data
    if h.parent:
        print(f"   Parent: {h.parent.name} ({h.parent.uid})")
    print(f"   Subsidiaries: {len(h.subsidiaries)}")
    for sub in h.subsidiaries[:5]:
        conf = f" [confidence: {sub.confidence}]" if sub.confidence else ""
        shared = f" — {sub.shared_person_count} shared persons" if sub.shared_person_count else ""
        print(f"     - {sub.name} ({sub.uid}){conf}{shared}")
    if len(h.subsidiaries) > 5:
        print(f"     ... and {len(h.subsidiaries) - 5} more")
    if h.siblings:
        print(f"   Siblings: {len(h.siblings)}")
    print()

    # --- Corporate structure ---
    print("4. Corporate Structure")
    structure = client.companies.structure(target_uid)
    st = structure.data
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
    print("5. Network Graph")
    graph = client.graph.get(target_uid)
    g = graph.data
    company_nodes = [n for n in g.nodes if n.node_type in ("company", "root")]
    person_nodes = [n for n in g.nodes if n.node_type == "person"]
    print(f"   Nodes: {len(g.nodes)} ({len(company_nodes)} companies, {len(person_nodes)} persons)")
    print(f"   Links: {len(g.links)}")
    link_types: dict[str, int] = {}
    for link in g.links:
        link_types[link.link_type] = link_types.get(link.link_type, 0) + 1
    for lt, count in sorted(link_types.items(), key=lambda x: -x[1]):
        print(f"     {lt}: {count}")
    print()

    # --- Multi-company network analysis ---
    print("6. Multi-Company Network Analysis")
    # Find a second company for the analysis
    abb = client.companies.list(query="ABB", canton="ZH", page_size=1).data.items[0]
    analysis = client.graph.analyze(uids=[target_uid, abb.uid], overlay="persons")
    a = analysis.data
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
