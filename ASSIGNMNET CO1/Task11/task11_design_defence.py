"""CO1 Task 11: Comprehensive Network Design Defence (Synthesizing Tasks 1-10)."""


def main():
    print("=== CO1 TASK 11: PLANT NETWORK DESIGN DEFENCE (SYNTHESIS OF TASKS 1-10) ===")
    areas = [
        ("Shop-floor robot cells (85m)", "Cat6A S/FTP", "1000BASE-T Full-Duplex Auto-Neg",
         "CRC-32 + Private 5G URLLC/wired redundancy", "Shielded against 15 dB welder EMI (Task 4); eliminates 412 late collisions (Task 6)."),
        ("Office to shop-floor (140m)", "OM4 Multimode Fibre", "10GBASE-SR Full-Duplex",
         "CRC-32 + 802.1Q VLAN + DiffServ EF/AF", "Resolves 140m > 100m copper TIA trap (Task 4)."),
        ("Shop-floor to DC (550m)", "OS2 Single-mode Fibre", "10GBASE-LR (2x10G LACP)",
         "CRC-32 + LACP + Jumbo Frames (9000B CCTV)", "1-plant = 1,265.92 Mbps > 1G uplink (Task 1); 550m needs SMF (Task 4)."),
        ("Office users & IP phones", "Cat6 UTP + Wi-Fi 6", "1000BASE-T Full-Duplex",
         "Replaced 3 hubs -> L2 VLAN switches", "Raises CDs from 17 to 41, eliminates half-duplex collisions (Task 2)."),
        ("Plant to HQ (400 km WAN)", "Carrier MPLS / SMF", "10G WAN + Selective Repeat",
         "CRC-32 + SR ARQ (W >= 335 frames)", "a=166.67 makes Stop-and-Wait 0.30% (2.99 Mbps); W=335 achieves 100% (Task 9)."),
    ]
    for area, med, eth, ctrl, just in areas:
        print(f"  * {area:<28}: {med} | {eth} | {ctrl}")
        print(f"      -> Justification: {just}")

    print("\nError Control & Flow Control Justification:")
    print("  - Vibration radio sensors: Hamming(21,16) FEC (5 check bits, 23.81% overhead) avoids 40 ms ARQ stalls (Task 8).")
    print("  - 400 km WAN: Selective Repeat ARQ with W >= 335 (10-bit seq) sustains 1 Gbps vs 2.99 Mbps Stop-and-Wait (Task 9).")
    print("  - Frames: IEEE 802.3 CRC-32 + DiffServ EF priority queue protects 32 Mbps/line robot traffic (<10 ms) from 96 Mbps/line CCTV (Task 1).")

    print("\nTwo Biggest Remaining Risks:")
    print("  1. Single-point-of-failure on 400 km WAN leased line -> Mitigate with dual-carrier MPLS + 5G/IPsec backup.")
    print("  2. Broadcast storms / security breach if L2 flat network -> Mitigate with VLAN segmentation + 802.1X + firewall ACLs.")

    print("\nScaling to 5 Plants (5 x 1,500 = 7,500 devices):")
    print("  - 5 plants x 1.266 Gbps raw = 6.33 Gbps aggregate; edge NVR recording cuts CCTV by 95% -> ~536 Mbps/plant -> 2.68 Gbps total.")
    print("  - 10 Gbps core + dual 1 Gbps/10 Gbps MPLS WAN scales cleanly across all 5 plants.")

    print("\n--- Alternative Concept: All-Private 5G Plant vs Wired Backbone + Wi-Fi ---")
    print("  - Private 5G carries: AGVs (URLLC), mobile robotics, and 600+ sensors (mMTC) cleanly.")
    print("  - Must stay on cable : 8x24=192 CCTV cameras (768 Mbps continuous saturates 5G uplink TDD slots) & DC storage (9000B jumbo).")
