"""CO1 Task 2: Collision & Broadcast Domains, Standards Table, and Diagram Generator."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def draw_office_topology(out_png):
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=160)
    ax.set_facecolor("#0F172A")
    fig.patch.set_facecolor("#0F172A")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.5)
    ax.axis("off")

    ax.text(6.0, 6.15, "CO1 Task 2: Contractor Office Topology — Collision (CD) & Broadcast Domains (BD)",
            ha="center", va="center", color="#F8FAFC", fontsize=12, fontweight="bold")

    # Broadcast Domain 1 dashed box
    bd1 = mpatches.FancyBboxPatch((0.3, 0.4), 6.9, 5.1, boxstyle="round,pad=0.15",
                                  ec="#38BDF8", fc="#1E293B", lw=1.8, ls="--", alpha=0.55)
    ax.add_patch(bd1)
    ax.text(3.75, 5.25, "Broadcast Domain 1 (Router G0/0 LAN)", ha="center", color="#38BDF8", fontsize=10, fontweight="bold")

    # Broadcast Domain 2 dashed box
    bd2 = mpatches.FancyBboxPatch((7.6, 0.4), 4.1, 5.1, boxstyle="round,pad=0.15",
                                  ec="#A78BFA", fc="#1E293B", lw=1.8, ls="--", alpha=0.55)
    ax.add_patch(bd2)
    ax.text(9.65, 5.25, "Broadcast Domain 2 (Router G0/1 Voice)", ha="center", color="#A78BFA", fontsize=10, fontweight="bold")

    # Router
    ax.add_patch(mpatches.FancyBboxPatch((6.4, 3.8), 1.9, 0.85, boxstyle="round,pad=0.08", fc="#EA580C", ec="#FDBA74", lw=1.5))
    ax.text(7.35, 4.22, "Router R1 (L3)\nG0/0  |  G0/1", ha="center", va="center", color="white", fontsize=9, fontweight="bold")

    # Switch 1 (24-port)
    ax.add_patch(mpatches.FancyBboxPatch((2.6, 3.65), 2.3, 0.8, boxstyle="round,pad=0.08", fc="#2563EB", ec="#93C5FD", lw=1.5))
    ax.text(3.75, 4.05, "24-Port Switch 1 (L2)\n4 active ports", ha="center", va="center", color="white", fontsize=9, fontweight="bold")

    # Switch 2 (IP phones)
    ax.add_patch(mpatches.FancyBboxPatch((8.5, 3.65), 2.3, 0.8, boxstyle="round,pad=0.08", fc="#2563EB", ec="#93C5FD", lw=1.5))
    ax.text(9.65, 4.05, "Switch 2 (L2)\n12 ports -> 12 Phones", ha="center", va="center", color="white", fontsize=9, fontweight="bold")

    # Links from Router to Switches
    ax.plot([6.4, 4.9], [4.15, 4.05], color="#FACC15", lw=2.2)
    ax.text(5.65, 4.35, "CD #4 (P2P)", ha="center", color="#FACC15", fontsize=8)
    ax.plot([8.3, 8.5], [4.15, 4.05], color="#FACC15", lw=2.2)
    ax.text(8.4, 4.45, "CD #5 (P2P)", ha="center", color="#FACC15", fontsize=8)

    # 3 Hubs + 8 PCs each
    hub_xs = [1.3, 3.75, 6.1]
    for idx, hx in enumerate(hub_xs, 1):
        ax.plot([3.75, hx], [3.65, 2.55], color="#F87171", lw=1.8)
        hub_box = mpatches.FancyBboxPatch((hx - 0.85, 1.8), 1.7, 0.72, boxstyle="round,pad=0.06", fc="#DC2626", ec="#FCA5A5", lw=1.4)
        ax.add_patch(hub_box)
        ax.text(hx, 2.16, f"Hub {idx} (L1)\n8 PCs (CD #{idx})", ha="center", va="center", color="white", fontsize=8.5, fontweight="bold")
        # PC cluster
        ax.add_patch(mpatches.FancyBboxPatch((hx - 0.85, 0.7), 1.7, 0.65, boxstyle="round,pad=0.05", fc="#334155", ec="#94A3B8", lw=1.0))
        ax.text(hx, 1.02, f"8 PCs\n(Multipoint Bus/Star)", ha="center", va="center", color="#E2E8F0", fontsize=8)
        ax.plot([hx, hx], [1.8, 1.35], color="#F87171", lw=1.5)

    # 12 IP Phones under Switch 2
    for i in range(4):
        px = 8.2 + i * 0.95
        ax.plot([9.65, px], [3.65, 2.25], color="#34D399", lw=1.4)
        ax.add_patch(mpatches.FancyBboxPatch((px - 0.38, 1.55), 0.76, 0.65, boxstyle="round,pad=0.04", fc="#059669", ec="#6EE7B7", lw=1.1))
        ax.text(px, 1.87, f"Phone\n{i*3+1}-{i*3+3}", ha="center", va="center", color="white", fontsize=7.5)

    ax.text(9.65, 0.95, "CD #6 to CD #17\n(12 independent P2P switch ports)", ha="center", color="#34D399", fontsize=8.5, fontweight="bold")

    ax.text(6.0, 0.12, "Total: 17 Collision Domains (3 Hubs + 2 Switch-Router + 12 Phone ports) | 2 Broadcast Domains (G0/0 & G0/1)",
            ha="center", color="#E2E8F0", fontsize=9.5, fontweight="bold")

    plt.tight_layout()
    plt.savefig(out_png, facecolor=fig.get_facecolor())
    plt.close(fig)


def main():
    print("=== CO1 TASK 2: COLLISION & BROADCAST DOMAINS + STANDARDS ===")
    cd_hubs = 3          # Each hub + its 8 PCs forms 1 shared collision domain on 1 Switch1 port
    cd_sw1_r1 = 1        # Switch 1 <-> Router G0/0
    cd_r1_sw2 = 1        # Router G0/1 <-> Switch 2
    cd_phones = 12       # 12 individual switch ports to 12 IP phones
    total_cd = cd_hubs + cd_sw1_r1 + cd_r1_sw2 + cd_phones
    total_bd = 2         # Separated by Router R1 interfaces G0/0 and G0/1

    print(f"Original Contractor Drawing:")
    print(f"  - Collision Domains : {total_cd} (3 Hubs + 1 SW1-R1 + 1 R1-SW2 + 12 Phone ports)")
    print(f"  - Broadcast Domains : {total_bd} (Router G0/0 LAN and Router G0/1 Voice LAN)")

    print("\nOSI Layer & Hub Behaviour:")
    print("  - Hub       : Layer 1 (Physical) - repeats electrical signals to all ports; no MAC filtering/buffering -> cannot isolate collisions.")
    print("  - Switch    : Layer 2 (Data Link) - buffers frames, learns MACs, forwards per port -> 1 collision domain per port.")
    print("  - Router    : Layer 3 (Network) - terminates L2 broadcasts, routes IP packets -> separates broadcast domains.")
    print("  - PCs/Phones: Layers 1-7 (End Hosts).")

    print("\nPoint-to-Point vs Multipoint Links:")
    print("  - Point-to-Point: Hub-to-Switch ports, Switch1-to-G0/0, G0/1-to-Switch2, Switch2-to-each IP Phone.")
    print("  - Multipoint    : Shared repeater bus inside each Hub connecting 8 PCs in half-duplex CSMA/CD.")

    standards = [
        ("Ethernet", "IEEE 802.3", "IEEE (Institute of Electrical and Electronics Engineers)"),
        ("Wi-Fi", "IEEE 802.11", "IEEE"),
        ("IPv4", "RFC 791", "IETF (Internet Engineering Task Force)"),
        ("OSI Model", "ISO/IEC 7498-1", "ISO (International Organization for Standardization)"),
        ("5G NR", "3GPP Rel-15/16/17 / IMT-2020", "3GPP & ITU-R"),
    ]
    print("\nStandards & Governing Bodies:")
    for tech, std, body in standards:
        print(f"  - {tech:<10} | {std:<28} | {body}")

    # Alternative Concept Analysis: Replace 3 hubs with 3 unmanaged switches
    alt_cd = (3 * 8) + 3 + 1 + 1 + 12  # 24 PC ports + 3 switch-to-switch uplinks + 2 router links + 12 phones
    print("\n--- Alternative Concept Analysis: Replace 3 Hubs with 3 Switches ---")
    print(f"  New Collision Domains: {alt_cd} (24 PC ports + 3 SW-to-SW uplinks + 2 router links + 12 phone ports)")
    print(f"  New Broadcast Domains: {total_bd} (unchanged; L2 switches still flood broadcasts across all 24 PCs)")
    print("  Fixes     : Eliminates CSMA/CD collisions on PCs, enables full-duplex 100/1000 Mbps per PC.")
    print("  Does NOT  : Does not isolate broadcast storms or provide VLAN segmentation without managed L2/VLANs.")

    out_png = os.path.join(os.path.dirname(__file__), "task02_domains_diagram.png")
    draw_office_topology(out_png)
    print(f"\nSaved topology diagram: {out_png}")


if __name__ == "__main__":
    main()
