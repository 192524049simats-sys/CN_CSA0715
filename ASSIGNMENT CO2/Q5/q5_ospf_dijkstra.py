"""CO2 Q5: OSPF Reference Bandwidth Problem, Dijkstra SPF on 6-Router ISP & EIGRP/IS-IS Comparison."""
import heapq
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def ospf_cost(bw_mbps, ref_mbps):
    return max(1, int(ref_mbps // bw_mbps))


def dijkstra(graph, start):
    dist = {node: float("inf") for node in graph}
    prev = {node: None for node in graph}
    dist[start] = 0
    pq = [(0, start)]
    order = []
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        order.append((u, d, prev[u]))
        for v, w in graph[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))
    return dist, prev, order


def draw_isp_spt(out_png, prev_new, dist_new):
    fig, ax = plt.subplots(figsize=(11, 5.8), dpi=160)
    ax.set_facecolor("#0F172A")
    fig.patch.set_facecolor("#0F172A")
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6)
    ax.axis("off")

    ax.text(5.5, 5.6, "CO2 Q5: 6-Router ISP Topology & Dijkstra SPT from R1 (Ref BW = 100,000 Mbps)",
            ha="center", color="#F8FAFC", fontsize=11.5, fontweight="bold")

    pos = {
        "R1": (1.5, 3.0),
        "R2": (4.2, 4.5),
        "R3": (4.2, 1.5),
        "R4": (7.0, 4.5),
        "R5": (7.0, 1.5),
        "R6": (9.6, 3.0),
    }
    edges = [
        ("R1", "R2", "1G (100)"),
        ("R1", "R3", "10G (10)"),
        ("R2", "R4", "1G (100)"),
        ("R3", "R5", "10G (10)"),
        ("R3", "R2", "100M (1000)"),
        ("R4", "R6", "10G (10)"),
        ("R5", "R6", "10G (10)"),
        ("R2", "R5", "1G (100)"),
        ("R4", "R5", "100M (1000)"),
    ]
    spt_edges = set()
    for node, p in prev_new.items():
        if p is not None:
            spt_edges.add(tuple(sorted((node, p))))

    for u, v, lbl in edges:
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        is_spt = tuple(sorted((u, v))) in spt_edges
        ax.plot([x1, x2], [y1, y2], color="#22C55E" if is_spt else "#475569",
                lw=3.0 if is_spt else 1.5, ls="-" if is_spt else "--", zorder=1)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx, my + 0.16, lbl, ha="center", color="#86EFAC" if is_spt else "#94A3B8", fontsize=8)

    for r, (x, y) in pos.items():
        ax.add_patch(mpatches.Circle((x, y), 0.48, fc="#2563EB" if r != "R1" else "#EA580C", ec="#E2E8F0", lw=1.8, zorder=3))
        ax.text(x, y + 0.06, r, ha="center", va="center", color="white", fontsize=10, fontweight="bold", zorder=4)
        ax.text(x, y - 0.22, f"c={dist_new[r]}", ha="center", va="center", color="#FEF08A", fontsize=8, zorder=4)

    ax.text(5.5, 0.28, "Green solid edges = Shortest-Path Tree from R1 (chooses 10G path R1->R3->R5->R6 cost 30 over 1G path cost 210)",
            ha="center", color="#34D399", fontsize=9, fontweight="bold")
    plt.tight_layout()
    plt.savefig(out_png, facecolor=fig.get_facecolor())
    plt.close(fig)


def main():
    print("=== CO2 Q5: OSPF REFERENCE BANDWIDTH & DIJKSTRA SPT ===")
    speeds = [("10 Mbps", 10), ("100 Mbps", 100), ("1 Gbps", 1_000), ("10 Gbps", 10_000)]
    print("1. OSPF Cost Comparison (Default 100 Mbps vs Recommended 100,000 Mbps):")
    for label, bw in speeds:
        c_def = ospf_cost(bw, 100)
        c_new = ospf_cost(bw, 100_000)
        print(f"   - {label:<10}: default cost = {c_def:<3d} | new cost (ref 100G) = {c_new}")
    print("   Problem with default 100 Mbps: floor(100/1000) and floor(100/10000) both clamp to 1,")
    print("   making 100M, 1G and 10G indistinguishable; ECMP or fewer-hop 1G paths beat 10G paths!")

    # 6-router ISP graph
    # Links: (u, v, bw_mbps)
    raw_links = [
        ("R1", "R2", 1_000), ("R1", "R3", 10_000),
        ("R2", "R4", 1_000), ("R3", "R2", 100),
        ("R3", "R5", 10_000), ("R2", "R5", 1_000),
        ("R4", "R6", 10_000), ("R5", "R6", 10_000),
        ("R4", "R5", 100),
    ]
    g_def = {f"R{i}": [] for i in range(1, 7)}
    g_new = {f"R{i}": [] for i in range(1, 7)}
    for u, v, bw in raw_links:
        g_def[u].append((v, ospf_cost(bw, 100)))
        g_def[v].append((u, ospf_cost(bw, 100)))
        g_new[u].append((v, ospf_cost(bw, 100_000)))
        g_new[v].append((u, ospf_cost(bw, 100_000)))

    d_def, p_def, _ = dijkstra(g_def, "R1")
    d_new, p_new, order_new = dijkstra(g_new, "R1")

    print("\n2. Dijkstra SPF Trace from R1 (Ref BW = 100,000 Mbps):")
    for u, d, parent in order_new:
        print(f"   - Pop {u}: total cost = {d:<3d}, parent = {parent}")

    def path_str(prev, target):
        cur, p = target, []
        while cur:
            p.append(cur)
            cur = prev[cur]
        return " -> ".join(reversed(p))

    print(f"\n   Path R1 -> R6 (Default 100M ref): {path_str(p_def, 'R6')} (cost {d_def['R6']})")
    print(f"   Path R1 -> R6 (New 100G ref)   : {path_str(p_new, 'R6')} (cost {d_new['R6']}, purely 10G links!)")

    print("\n3. Single vs Multi-Area OSPF for State ISP:")
    print("   - Use MULTIPLE areas (Area 0 core backbone + regional stub/NSSA areas) to isolate LSA flooding,")
    print("     keep LSDB small, enable area-border route summarisation, and contain regional link-flap SPF runs.")

    print("\n--- Alternative Concept Analysis: EIGRP vs IS-IS ---")
    # EIGRP classic metric: 256 * (10^7 / min_bw_kbps + sum_delay_10us)
    # 1 Gbps: bw_kbps = 1_000_000, delay = 10 us -> 1 -> 256*(10 + 1) = 2816
    # 10 Gbps: bw_kbps = 10_000_000, delay = 10 us -> 1 -> 256*(1 + 1) = 512 (note: wide metrics needed beyond 10G)
    eigrp_1g = 256 * (10_000_000 // 1_000_000 + 1)
    eigrp_10g = 256 * (10_000_000 // 10_000_000 + 1)
    print(f"  - EIGRP classic metric : 1G = {eigrp_1g}, 10G = {eigrp_10g} (distinguishes 1G vs 10G by default, though Wide Metrics needed >10G)")
    print("  - IS-IS default metric : Fixed cost 10 per interface regardless of speed (requires 'metric-style wide' + auto-cost/manual tuning)")
    print("  - Winner without ref-BW change: EIGRP natively differentiates 1G and 10G out of the box.")

    out_png = os.path.join(os.path.dirname(__file__), "q5_ospf_spt.png")
    draw_isp_spt(out_png, p_new, d_new)
    print(f"\nSaved SPT diagram: {out_png}")


if __name__ == "__main__":
    main()
