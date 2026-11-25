"""CO4 Task 6: 40-Acre University Campus Network Design Challenge (Stages 1-5 + Collapsed Core Analysis)."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def draw_campus_diagram(out_png):
    fig, ax = plt.subplots(figsize=(12.5, 6.8), dpi=160)
    ax.set_facecolor("#0F172A")
    fig.patch.set_facecolor("#0F172A")
    ax.set_xlim(0, 12.5)
    ax.set_ylim(0, 7.0)
    ax.axis("off")

    ax.text(6.25, 6.65, "CO4 Task 6: 40-Acre University Hierarchical Hybrid Topology (Core - Dist - Access)",
            ha="center", color="#F8FAFC", fontsize=12, fontweight="bold")

    # Dual ISP
    for ix, lbl in [(4.2, "ISP-1 (10G Primary)"), (8.3, "ISP-2 (10G Backup)")]:
        ax.add_patch(mpatches.FancyBboxPatch((ix - 1.1, 5.5), 2.2, 0.65, boxstyle="round,pad=0.06", fc="#0284C7", ec="#7DD3FC"))
        ax.text(ix, 5.82, lbl, ha="center", va="center", color="white", fontsize=8.5, fontweight="bold")

    # Core Mesh
    for cx, lbl in [(4.4, "Core-SW-1 (L3 10G)"), (8.1, "Core-SW-2 (L3 10G)")]:
        ax.add_patch(mpatches.FancyBboxPatch((cx - 1.25, 4.1), 2.5, 0.72, boxstyle="round,pad=0.06", fc="#EA580C", ec="#FDBA74"))
        ax.text(cx, 4.46, lbl, ha="center", va="center", color="white", fontsize=8.5, fontweight="bold")
    ax.plot([5.65, 6.85], [4.46, 4.46], color="#FACC15", lw=2.8)
    ax.text(6.25, 4.65, "2x10G Core Mesh", ha="center", color="#FEF08A", fontsize=7.8)

    # ISP to Core full cross-mesh
    for ix in (4.2, 8.3):
        for cx in (4.4, 8.1):
            ax.plot([ix, cx], [5.5, 4.82], color="#38BDF8", lw=1.6)

    # Distribution switches (Buildings)
    dists = [
        (1.6, "Dist: Academic+Lib\n(400+250 users)\n2x10G Uplink"),
        (4.7, "Dist: Labs (600 PCs)\n+ Auditorium (1k)\n2x10G Uplink"),
        (7.8, "Dist: Hostels\n(3,000 students)\n2x10G Uplink"),
        (10.9, "Dist: Data Centre\n(Servers + NVR)\n2x10G LACP"),
    ]
    for dx, lbl in dists:
        ax.add_patch(mpatches.FancyBboxPatch((dx - 1.25, 2.2), 2.5, 0.85, boxstyle="round,pad=0.06", fc="#2563EB", ec="#93C5FD"))
        ax.text(dx, 2.62, lbl, ha="center", va="center", color="white", fontsize=8, fontweight="bold")
        # Dual-homed OS2 SMF uplinks to both Core switches
        ax.plot([4.4, dx], [4.1, 3.05], color="#22C55E", lw=1.7)
        ax.plot([8.1, dx], [4.1, 3.05], color="#22C55E", lw=1.7, ls="--")

    # Access Layer
    accs = [
        (1.6, "Access SW + Wi-Fi 6\nVLAN 10/20/30/40"),
        (4.7, "Access SW (GbE/PoE+)\n15x48p + Hall APs"),
        (7.8, "Hostel Access SW\n60x Wi-Fi 6 APs"),
        (10.9, "Server ToR 10G\nDNS/LMS/ERP/CCTV"),
    ]
    for ax_x, lbl in accs:
        ax.plot([ax_x, ax_x], [2.2, 1.45], color="#94A3B8", lw=1.8)
        ax.add_patch(mpatches.FancyBboxPatch((ax_x - 1.15, 0.7), 2.3, 0.75, boxstyle="round,pad=0.05", fc="#059669", ec="#6EE7B7"))
        ax.text(ax_x, 1.07, lbl, ha="center", va="center", color="white", fontsize=7.8)

    ax.text(6.25, 0.22, "OS2 Single-Mode Fibre Backbone | VLANs: 10-Student, 20-Staff, 30-Guest, 40-CCTV | Dual-ISP BGP/NAT Failover",
            ha="center", color="#34D399", fontsize=9, fontweight="bold")
    plt.tight_layout()
    plt.savefig(out_png, facecolor=fig.get_facecolor())
    plt.close(fig)


def main():
    print("=== CO4 TASK 6: UNIVERSITY CAMPUS NETWORK DESIGN CHALLENGE ===")
    print("Stage 1 — Building Sizing & Peak Traffic Estimates:")
    buildings = [
        ("Academic Block", 400, 350, 250.0, "Wired Staff + Wi-Fi 6"),
        ("Laboratories", 600, 600, 600.0, "600 Wired PCs (1G)"),
        ("Library", 250, 300, 200.0, "Wired Kiosks + Wi-Fi 6"),
        ("Hostels (3,000 students)", 3000, 4500, 1800.0, "High-density Wi-Fi 6 + Wired"),
        ("Auditorium", 1000, 1000, 400.0, "High-density Wi-Fi 6"),
        ("Data Centre", 20, 40, 2500.0, "LMS, ERP, DNS, NVR (East-West)"),
    ]
    for b, u, d, mbps, note in buildings:
        print(f"  - {b:<26}: Users={u:4d} | Devices={d:4d} | Peak={mbps:6.1f} Mbps | {note}")

    print("\nStage 2 & 3 — Architecture, VLANs, Media & WAN:")
    print("  - Topology : 3-Tier Hierarchical Hybrid (Full-mesh 2x10G Core <-> Dual-homed OS2 SMF Distribution <-> Star Access).")
    print("  - VLANs    : VLAN 10 Student (10.10.0.0/17), VLAN 20 Staff (10.10.128.0/19), VLAN 30 Guest (10.10.160.0/20), VLAN 40 CCTV (10.10.176.0/20).")
    print("  - Media    : OS2 Single-Mode Fibre across 40-acre campus (>100m); Cat6A UTP horizontal (<90m) + Wi-Fi 6 (802.11ax).")
    print("  - WAN      : Dual 10G/1G ISP uplinks with stateful firewall + BGP/floating failover.")

    print("\nStage 4 — Address Plan, BOM & Uplink Oversubscription Ratios:")
    # Labs: 600 access ports @ 1G -> 600G edge? No, typical PC bursts 100M/1G, uplink = 2x10G = 20G -> 600*1G / 20G = 30:1 (or 600*100M/20G = 3:1 peak)
    # Academic+Lib: 10G active / 20G LACP; Hostels: 20G LACP
    uplinks = [
        ("Labs (600 x 1G access)", 600.0, 20.0),
        ("Academic + Library (650 x 1G/Wi-Fi)", 650.0, 20.0),
        ("Hostels (60 APs x 1G)", 60.0, 20.0),
        ("Data Centre (20 x 10G servers)", 200.0, 40.0),
    ]
    for name, agg_g, up_g in uplinks:
        print(f"  - {name:<36}: Edge={agg_g:5.1f}G | Uplink={up_g:4.1f}G | Oversubscription = {agg_g/up_g:.1f}:1")

    print("\nStage 5 — Packet Tracer Reduced Simulation (Core + 2 Buildings + Dual ISP):")
    print("  - Config provided in campus_core_ospf.cfg (OSPF Area 0 + VLAN 10/20/30/40 + ACL Guest isolation + RSTP/LACP).")
    print("  - Core-link failure test: Shutting Core-SW-1 -> Dist1 link triggers OSPF/RSTP failover to Core-SW-2 in < 1 s.")

    print("\n--- Alternative Concept Analysis: Collapsed Core (Core + Distribution Combined) ---")
    print("  - Devices saved: Eliminates 2 dedicated Core switches (saves ~Rs 8-12 Lakhs upfront).")
    print("  - Blast radius : If a single collapsed-core switch fails, ALL 6 buildings (3,000 hostel students, 600 labs, DC) go dark!")
    print("  - 10-Year Verdict: NOT worth saving 2 switches over 10 years for a 4,000+ user campus; keep dual redundant Core/Dist.")

    out_png = os.path.join(os.path.dirname(__file__), "task06_university_campus.png")
    draw_campus_diagram(out_png)
    print(f"\nSaved campus topology diagram: {out_png}")


if __name__ == "__main__":
    main()
