"""Distance-vector routing (Bellman-Ford exchange) among five campus routers."""

INF = 99
names = "ABCDE"
cost = {("A", "B"): 2, ("A", "C"): 7, ("B", "C"): 3, ("B", "D"): 8,
        ("C", "D"): 1, ("D", "E"): 4}
link = {}
for (u, v), c in cost.items():
    link[u, v] = link[v, u] = c

table = {u: {v: (0 if u == v else link.get((u, v), INF)) for v in names} for u in names}

rounds = 0
changed = True
while changed:
    changed = False
    rounds += 1
    old = {u: dict(table[u]) for u in names}    # vectors received this round
    for u in names:
        for n in names:
            if (u, n) not in link:
                continue
            for dest in names:
                # TODO 1: Bellman-Ford update: if going through neighbour n (link cost +
                # n's old distance to dest) is cheaper than table[u][dest], update it
                # and set changed = True
                new_cost = link[u, n] + old[n][dest]
                if new_cost < table[u][dest]:
                    table[u][dest] = new_cost
                    changed = True

print(f"converged after {rounds} rounds")
for u in names:
    print(u, " ".join(f"{table[u][v]:2d}" for v in names))

# --- Follow-up: Round-by-round explanation, C-D link failure, Count-to-Infinity ---
print("\n--- Why A's best route to C is NOT direct ---")
print("  Direct link A-C = 7, whereas A-B-C = 2 + 3 = 5 (lower cumulative cost).")

print("\n--- Rerun with link C-D failed (cost = 99) ---")
cost_fail = dict(cost)
cost_fail[("C", "D")] = INF
link_fail = {}
for (u, v), c in cost_fail.items():
    link_fail[u, v] = link_fail[v, u] = c
t2 = {u: {v: (0 if u == v else link_fail.get((u, v), INF)) for v in names} for u in names}
r2, ch = 0, True
while ch:
    ch = False
    r2 += 1
    old2 = {u: dict(t2[u]) for u in names}
    for u in names:
        for n in names:
            if (u, n) not in link_fail:
                continue
            for dest in names:
                nc = link_fail[u, n] + old2[n][dest]
                if nc < t2[u][dest]:
                    t2[u][dest] = nc
                    ch = True
print(f"converged after {r2} rounds (C-D failed)")
for u in names:
    print(u, " ".join(f"{t2[u][v]:2d}" for v in names))

print("\n--- Count-to-Infinity on X-Y-Z (cost=1 each, Y-Z fails) ---")
dx, dy = 2, 1
for rnd in range(1, 7):
    # Without split horizon: Y hears dx from X and sets dy = 1 + dx; X hears dy from Y and sets dx = 1 + dy
    new_dy = 1 + dx
    new_dx = 1 + dy
    dy, dx = new_dy, new_dx
    print(f"  Round {rnd}: Y->Z = {dy:2d}, X->Z = {dx:2d} (counting to infinity!)")
print("  With Split Horizon + Poison Reverse: X advertises Z=INF (16 in RIP) back to Y -> Y immediately sets Y->Z=INF in Round 1!")

print("\n--- Alternative Concept Analysis: Link-State (OSPF) vs Distance-Vector on C-D Failure ---")
print("  - Link-State: C and D flood 1 LSA each across 6 links (~12 LSA messages), every router recomputes SPF in 1 flood + 1 Dijkstra (~ms).")
print("  - Distance-Vector: Exchanges full vectors with neighbours over multiple rounds (and risks count-to-infinity without poison reverse).")
