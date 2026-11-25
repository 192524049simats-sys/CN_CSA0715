"""CO1 Task 12: Day-4 Design Challenge — 50 AGVs + Private 5G Adaptation."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def draw_revised_topology(out_png):
    fig, ax = plt.subplots(figsize=(12, 6.4), dpi=160)
    ax.set_facecolor("#0F172A")
    fig.patch.set_facecolor("#0F172A")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.6)
    ax.axis("off")

    ax.text(6.0, 6.25, "CO1 Task 12: Revised Smart Plant Topology (Private 5G URLLC + 10G Fibre Core)",
            ha="center", va="center", color="#F8FAFC", fontsize=12, fontweight="bold")

    nodes = [
        (6.0, 5.1, 2.8, 0.75, "#EA580C", "Core L3 Switches (Dual 10G)\nDiffServ QoS (EF/AF/BE)"),
        (2.1, 3.2, 2.6, 0.85, "#7C3AED", "Private 5G UPF / gNodeB\nURLLC Slice (<1-5ms)\n50 AGVs + Mobile Robots"),
        (6.0, 3.2, 2.5, 0.85, "#2563EB", "Shop-Floor Dist Switch\nCat6A S/FTP (85m Welders)\nFixed Robots + 192 CCTV"),
        (9.9, 3.2, 2.5, 0.85, "#059669", "Office & Data Centre\nWi-Fi 6 + L2 VLAN Switches\nLocal NVR + 10G SMF"),
        (6.0, 1.1, 3.2, 0.8, "#0284C7", "Dual 10G MPLS WAN (400 km to HQ)\nSelective Repeat W >= 335 | CRC-32"),
    ]
    for x, y, w, h, col, txt in nodes:
        ax.add_patch(mpatches.FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.08", fc=col, ec="#E2E8F0", lw=1.4))
        ax.text(x, y, txt, ha="center", va="center", color="white", fontsize=8.5, fontweight="bold")

    edges = [
        ((6.0, 4.72), (2.1, 3.63), "10G OS2 SMF"),
        ((6.0, 4.72), (6.0, 3.63), "2x10G LACP OM4/OS2"),
        ((6.0, 4.72), (9.9, 3.63), "10G OS2 SMF (550m)"),
        ((2.1, 2.77), (6.0, 1.5), "URLLC Failover"),
        ((6.0, 2.77), (6.0, 1.5), "10G Core -> WAN"),
        ((9.9, 2.77), (6.0, 1.5), "Edge NVR (5% clip)"),
    ]
    for (x1, y1), (x2, y2), lbl in edges:
        ax.plot([x1, x2], [y1, y2], color="#38BDF8", lw=2.0)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx, my + 0.14, lbl, ha="center", color="#BAE6FD", fontsize=7.8)

    ax.text(6.0, 0.25, "Decision: REDESIGN wireless/access + MODIFY core QoS (Private 5G URLLC + 10G LACP + Edge NVR -> 576 Mbps/plant avg)",
            ha="center", color="#34D399", fontsize=9.2, fontweight="bold")
    plt.tight_layout()
    plt.savefig(out_png, facecolor=fig.get_facecolor())
    plt.close(fig)


def main():
    print("=== CO1 TASK 12: DAY-4 DESIGN CHALLENGE (50 AGVs + PRIVATE 5G) ===")
    agv_bps = 50 * (200 * 8) / 0.002       # 50 AGVs @ 200B every 2 ms = 40 Mbps
    orig_line_bps = 158.24e6
    orig_plant_bps = 1265.92e6
    new_plant_raw = orig_plant_bps + agv_bps
    # With local NVR motion-triggered CCTV (5% = 38.4 Mbps across 8 lines instead of 768 Mbps)
    new_plant_nvr = (orig_plant_bps - 768e6 * 0.95) + agv_bps

    print("A. Impact Analysis:")
    print(f"   - Added AGV control traffic : 50 x 200B / 2ms = {agv_bps / 1e6:.2f} Mbps (strict <= 10 ms deadline, 0 missed frames)")
    print(f"   - Raw plant traffic (8 lines + 50 AGVs): {new_plant_raw / 1e6:.2f} Mbps (exceeds single 1G uplink by {(new_plant_raw-1e9)/1e6:.2f} Mbps)")
    print(f"   - With edge NVR (5% CCTV) + 50 AGVs    : {new_plant_nvr / 1e6:.2f} Mbps")
    print("   - Impacted subsystems: Shop-floor wireless (Wi-Fi -> 5G URLLC), Core uplink (1G -> 2x10G LACP), Error control (HARQ+CRC+DAPS).")

    print("\nB. Testing the Original Design Against 50 Moving AGVs:")
    print("   - Wi-Fi handover (150 ms, 39 HOs/1.2km) = 5,850 ms total blackout -> FAILS 10 ms AGV deadline by 15x per HO.")
    print("   - Even 802.11r fast roaming (20-50 ms) + CSMA/CA contention + 15 dB welder EMI drops control packets.")
    print("   - Verdict: Original Wi-Fi office design CANNOT serve 50 moving AGVs -> REDESIGN required.")

    print("\nC. Adapted / Redesigned Architecture:")
    print("   - AGVs & mobile robots : Private 5G SA URLLC slice (300m cells, DAPS < 1 ms HO, < 5 ms air latency, HARQ FEC).")
    print("   - Fixed welding robots : Cat6A S/FTP wired 1000BASE-T Full-Duplex (blocks EMI).")
    print("   - Office & diagnostics : Wi-Fi 6 (802.11ax) on non-overlapping channels + VLANs.")
    print("   - Backbone & WAN       : Dual 10G OS2 SMF LACP core + DiffServ EF priority + 400 km MPLS WAN (SR W>=335).")

    print("\nD. Evidence-Based Defence:")
    print("   - Eliminates 5.85 s Wi-Fi roaming outage -> < 1 ms DAPS handover, guaranteeing 10 ms AGV control loop.")
    print("   - 2x10G LACP core provides 20 Gbps vs 1.31 Gbps worst-case raw load (6.5% utilisation, zero queueing).")

    out_png = os.path.join(os.path.dirname(__file__), "task12_revised_topology.png")
    draw_revised_topology(out_png)
    print(f"\nSaved revised topology diagram: {out_png}")


if __name__ == "__main__":
    main()
