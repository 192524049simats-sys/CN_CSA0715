"""CO4 Task 1: Office Bus-to-Star Redesign, Bandwidth Calculations & Topology Diagram."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def draw_redesign_diagram(out_png):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.6), dpi=160)
    for ax in (ax1, ax2):
        ax.set_facecolor("#0F172A")
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 6)
        ax.axis("off")
    fig.patch.set_facecolor("#0F172A")

    # Left: Legacy Coax Bus + Hub
    ax1.set_title("BEFORE: Legacy Coax Bus + Hub (10 Mbps Shared)", color="#FCA5A5", fontsize=11, fontweight="bold")
    ax1.plot([0.8, 9.2], [3.5, 3.5], color="#EF4444", lw=4)
    ax1.text(0.5, 3.5, "50\u03a9", color="#F87171", fontsize=9, va="center", fontweight="bold")
    ax1.text(9.4, 3.5, "50\u03a9", color="#F87171", fontsize=9, va="center", fontweight="bold")
    for idx, x in enumerate([1.6, 3.0, 4.4], 1):
        ax1.plot([x, x], [3.5, 2.3], color="#F87171", lw=1.5)
        ax1.add_patch(mpatches.FancyBboxPatch((x - 0.55, 1.5), 1.1, 0.75, boxstyle="round,pad=0.05", fc="#334155", ec="#94A3B8"))
        ax1.text(x, 1.87, f"F1 PCs\nGroup {idx}", ha="center", va="center", color="white", fontsize=7.5)
    # Hub Floor 2
    ax1.plot([6.0, 6.0], [3.5, 2.4], color="#F87171", lw=1.8)
    ax1.add_patch(mpatches.FancyBboxPatch((5.1, 1.7), 1.8, 0.7, boxstyle="round,pad=0.05", fc="#DC2626", ec="#FCA5A5"))
    ax1.text(6.0, 2.05, "Floor-2 Hub\n(15 PCs, Half-Dup)", ha="center", va="center", color="white", fontsize=7.5, fontweight="bold")
    # Server + Printer + Home Router
    ax1.plot([7.8, 7.8], [3.5, 4.4], color="#F87171", lw=1.5)
    ax1.add_patch(mpatches.FancyBboxPatch((7.0, 4.4), 1.6, 0.75, boxstyle="round,pad=0.05", fc="#475569", ec="#94A3B8"))
    ax1.text(7.8, 4.77, "Server + Printer\n(Far End)", ha="center", va="center", color="white", fontsize=7.5)
    ax1.plot([2.2, 2.2], [3.5, 4.4], color="#F87171", lw=1.5)
    ax1.add_patch(mpatches.FancyBboxPatch((1.3, 4.4), 1.8, 0.75, boxstyle="round,pad=0.05", fc="#B45309", ec="#FCD34D"))
    ax1.text(2.2, 4.77, "Home Router\n(SPOF)", ha="center", va="center", color="white", fontsize=7.5)
    ax1.text(5.0, 0.45, "1 Collision Domain | 1 Broadcast Domain\n~0.33 Mbps effective/PC at peak", ha="center", color="#FCA5A5", fontsize=9, fontweight="bold")

    # Right: Redesigned Extended Star
    ax2.set_title("AFTER: Extended Star (1 Gbps Switched + Firewall)", color="#86EFAC", fontsize=11, fontweight="bold")
    ax2.add_patch(mpatches.FancyBboxPatch((3.6, 4.7), 2.8, 0.85, boxstyle="round,pad=0.06", fc="#EA580C", ec="#FDBA74"))
    ax2.text(5.0, 5.12, "Business Router + Firewall\n(VLANs + NAT + Dual WAN)", ha="center", va="center", color="white", fontsize=8, fontweight="bold")

    ax2.add_patch(mpatches.FancyBboxPatch((1.1, 2.9), 2.8, 0.85, boxstyle="round,pad=0.06", fc="#2563EB", ec="#93C5FD"))
    ax2.text(2.5, 3.32, "Floor-1 GbE Switch\n(15 PCs + Server + Printer)", ha="center", va="center", color="white", fontsize=8, fontweight="bold")
    ax2.add_patch(mpatches.FancyBboxPatch((6.1, 2.9), 2.8, 0.85, boxstyle="round,pad=0.06", fc="#2563EB", ec="#93C5FD"))
    ax2.text(7.5, 3.32, "Floor-2 GbE Switch\n(15 PCs, Full-Duplex)", ha="center", va="center", color="white", fontsize=8, fontweight="bold")

    ax2.plot([5.0, 2.5], [4.7, 3.75], color="#38BDF8", lw=2.2)
    ax2.plot([5.0, 7.5], [4.7, 3.75], color="#38BDF8", lw=2.2)
    ax2.plot([3.9, 6.1], [3.32, 3.32], color="#22C55E", lw=2.0, ls="--")
    ax2.text(5.0, 3.55, "1G Cat6 Trunk", ha="center", color="#86EFAC", fontsize=7.5)

    for cx, lbl in [(1.5, "F1 PCs (x15)\n1 Gbps each"), (3.4, "Server/Printer\n1 Gbps GbE"), (7.5, "F2 PCs (x15)\n1 Gbps each")]:
        src_x = 2.5 if cx < 5 else 7.5
        ax2.plot([src_x, cx], [2.9, 1.9], color="#34D399", lw=1.6)
        ax2.add_patch(mpatches.FancyBboxPatch((cx - 0.9, 1.15), 1.8, 0.75, boxstyle="round,pad=0.05", fc="#059669", ec="#6EE7B7"))
        ax2.text(cx, 1.52, lbl, ha="center", va="center", color="white", fontsize=7.8)

    ax2.text(5.0, 0.45, "33 Collision Domains | Isolated VLAN Broadcast Domains\n1,000 Mbps dedicated full-duplex per PC (3,000x boost!)", ha="center", color="#86EFAC", fontsize=9, fontweight="bold")

    plt.tight_layout()
    plt.savefig(out_png, facecolor=fig.get_facecolor())
    plt.close(fig)


def main():
    print("=== CO4 TASK 1: INVESTIGATING & REDESIGNING THE CA OFFICE NETWORK ===")
    print("1.1 Cause of Each Staff Complaint:")
    print("  - 'Moving a desk kills whole network': Coax bus breaks/unterminates when a BNC T-connector is unplugged ->")
    print("    open impedance causes signal reflections across the entire shared backbone.")
    print("  - 'Saving a file takes a minute at month-end': 30 PCs share one 10 Mbps half-duplex collision domain")
    print("    (coax + Floor-2 hub); CSMA/CD collisions crush per-PC throughput to < 0.33 Mbps.")
    print("  - 'Internet stops on router restart': Single consumer home router is a SPOF for NAT/DHCP/routing.")
    print("  - Unnoticed weaknesses: (1) Single broadcast & collision domain; (2) Zero VLAN/security isolation;")
    print("    (3) 10BASE2 185 m length limit & brittle troubleshooting.")

    print("\n1.2 Bandwidth Per Computer (Before vs After):")
    before_mbps = 10.0 / 30.0
    after_mbps = 1000.0
    print(f"  - Before (10 Mbps shared coax/hub, 30 PCs) : <= {before_mbps:.2f} Mbps/PC (less with collisions)")
    print(f"  - After  (1 Gbps Cat6 switched extended star): {after_mbps:.0f} Mbps dedicated full-duplex/PC ({after_mbps/before_mbps:.0f}x improvement)")

    print("\n1.3 Concise Defence (<= 100 words):")
    defence = (
        "Replacing the coaxial bus and Floor-2 hub with a Cat6 extended-star topology and Gigabit switches "
        "gives each desk an isolated point-to-point link, eliminating desk-move outages and CSMA/CD collisions. "
        "Dedicated 1 Gbps full-duplex ports raise peak per-PC bandwidth from 0.33 Mbps to 1,000 Mbps, ending "
        "month-end server delays. Adding a business router with stateful firewall, dual-WAN failover, and UPS "
        "removes the home-router single point of failure and isolates accounting traffic cleanly."
    )
    print(f"  ({len(defence.split())} words) {defence}")

    print("\n--- Alternative Concept Analysis: Single Wi-Fi 6 AP vs Switched Star ---")
    print("  - 1 Wi-Fi 6 AP (1.2 Gbps PHY ~ 600 Mbps net shared half-duplex across 30 PCs) -> ~20 Mbps/PC with CSMA/CA contention.")
    print("  - Switched Cat6 Star -> 1,000 Mbps full-duplex/PC (50x faster, zero airtime collisions) -> wins for month-end file saves.")

    out_png = os.path.join(os.path.dirname(__file__), "task01_office_redesign.png")
    draw_redesign_diagram(out_png)
    print(f"\nSaved topology diagram: {out_png}")


if __name__ == "__main__":
    main()
