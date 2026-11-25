"""Compare topologies for n offices: links, ports and single-link failures."""
from collections import deque
from itertools import combinations


def links(kind, n):
    nodes = list(range(n))
    if kind == "bus":
        return [(i, i + 1) for i in range(n - 1)]       # segments of one backbone
    if kind == "ring":
        return [(i, (i + 1) % n) for i in range(n)]
    if kind == "star":
        return [("hub", i) for i in nodes]
    if kind == "mesh":
        return list(combinations(nodes, 2))
    raise ValueError(kind)


def connected_after_failure(edges, n, broken):
    # TODO 1: Remove the broken link, then use a breadth-first search from office 0
    # (following the remaining links in both directions, through the hub if there is
    # one) and return True if all n offices are still reached
    adj = {}
    for a, b in edges:
        if (a, b) == broken:
            continue
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
    seen = {0}
    q = deque([0])
    while q:
        u = q.popleft()
        for v in adj.get(u, []):
            if v not in seen:
                seen.add(v)
                q.append(v)
    return all(i in seen for i in range(n))


n = 6
for kind in ("bus", "ring", "star", "mesh"):
    e = links(kind, n)
    ports = max(sum(1 for a, b in e if x in (a, b)) for x in set(sum(e, ())))
    ok = sum(connected_after_failure(e, n, b) for b in e)
    print(f"{kind:<5} links {len(e):2d}  max ports on one device {ports}  "
          f"single-link failures survived {ok}/{len(e)}")

# --- Follow-up: n=20 Scaling + Hospital 5-Block Cost & Hybrid Design ---
print("\n--- Scaling Comparison at n = 20 Offices ---")
e_star_20 = links("star", 20)
e_mesh_20 = links("mesh", 20)
print(f"  Star (n=20)      : {len(e_star_20):3d} links (O(n) linear growth)")
print(f"  Full Mesh (n=20) : {len(e_mesh_20):3d} links (O(n^2) = n*(n-1)/2 -> {len(e_mesh_20)/len(e_star_20):.1f}x more links!)")

print("\n--- Hospital 5-Block Cost & Failure Analysis (Rs 60,000/fibre + 2 x Rs 18,000/port = Rs 96,000/link) ---")
link_cost = 60_000 + 2 * 18_000
for name, n_links, n_ports, fails in [
    ("Bus (5 blocks)", 4, 8, "Any cut isolates Emergency or OT"),
    ("Ring (5 blocks)", 5, 10, "Survives ANY single cut (0 disconnected)"),
    ("Star (centred on DC)", 5, 10, "Cut to Emergency or OT isolates it immediately"),
    ("Full Mesh (5 blocks)", 10, 20, "Survives up to 3 cuts"),
    ("Hybrid Core (DC-Emerg-OT ring + 2/3 radials)", 6, 12, "Emerg & OT survive any 1 cut (connected to DC)"),
]:
    cost = n_links * link_cost
    print(f"  {name:<45}: {n_links:2d} links | {n_ports:2d} ports | Rs {cost:>7,} | {fails}")

print("\n--- Alternative Concept Analysis: 5-Block Fibre Ring vs Hybrid ---")
print("  - 5-Block Ring (5 links = Rs 480,000, 10 ports) is actually CHEAPER than 6-link hybrid (Rs 576,000)")
print("    and survives ANY 1 cable cut (including Outpatient/Lab/Admin!), while failing on 2 cuts that bracket a block.")
print("  - Hybrid (DC-Emerg-OT triangle + radials = 6 links, Rs 576,000) adds extra hops=1 direct paths to DC,")
print("    and survives 2 cuts if 1 cut is on a radial + 1 on the triangle, whereas 5-block ring has longer worst-case hop count (2 vs 1).")
