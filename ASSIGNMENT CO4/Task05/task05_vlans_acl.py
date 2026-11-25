"""CO4 Task 5: VLAN Segmentation, 802.1Q Tag Overhead, ACL Verification & Broadcast Domains."""


def acl_check(src_vlan, dst_net):
    # Simulates R-Admin GUEST_INTERNET_ONLY ACL on VLAN 30 inbound
    if src_vlan == 30:
        if dst_net in ("VLAN10-Office", "VLAN20-CCTV"):
            return "DENY (blocked by GUEST_INTERNET_ONLY ACL)"
        return "PERMIT (Internet / external only)"
    if src_vlan in (10, 20):
        return "PERMIT (Inter-VLAN routing enabled)"
    return "DENY"


def main():
    print("=== CO4 TASK 5: SEPARATE THE GUESTS FROM THE OFFICE (VLANs & ACL) ===")
    print("5.1 IEEE 802.1Q Trunk Tag Overhead:")
    print("  - 802.1Q inserts a 4-byte tag (2B TPID 0x8100 + 2B TCI: 3b PCP, 1b DEI, 12b VID) into the Ethernet header.")
    print("  - Standard max frame increases from 1,518 B to 1,522 B (0.26% overhead at 1500 B MTU).")

    print("\n5.2 Switch & Router Config Summary (see sw_admin_vlans.cfg & r_admin_roas_acl.cfg):")
    print("  - SW-Admin: VLAN 10 (Office: Fa0/1-12), VLAN 20 (CCTV: Fa0/13-20), VLAN 30 (Guest-WiFi: Fa0/21-24).")
    print("  - Trunk Gi0/1: switchport mode trunk; switchport trunk allowed vlan 10,20,30.")
    print("  - R-Admin: Router-on-a-stick subinterfaces G0/0.10, .20, .30 + ACL GUEST_INTERNET_ONLY on .30 inbound.")

    print("\n5.3 Reachability Matrix & Broadcast Domain Counts:")
    tests = [
        ("PC-Guest (VLAN 30)", 30, "PC-Office (VLAN 10)", "VLAN10-Office", "L2 Pre-ROAS: FAIL (isolated) | Post-ROAS+ACL: " + acl_check(30, "VLAN10-Office")),
        ("PC-Guest (VLAN 30)", 30, "CCTV (VLAN 20)", "VLAN20-CCTV", "Post-ROAS+ACL: " + acl_check(30, "VLAN20-CCTV")),
        ("PC-Guest (VLAN 30)", 30, "Internet (8.8.8.8)", "Internet", "Post-ROAS+ACL: " + acl_check(30, "Internet")),
        ("PC-Office (VLAN 10)", 10, "CCTV (VLAN 20)", "VLAN20-CCTV", "Post-ROAS+ACL: " + acl_check(10, "VLAN20-CCTV")),
    ]
    for src, _, dst, _, res in tests:
        print(f"  - {src:<20} -> {dst:<20}: {res}")
    print("  - Broadcast domains BEFORE VLANs: 1 | AFTER VLANs (10, 20, 30): 3 independent broadcast domains.")

    print("\n--- Alternative Concept Analysis: Separate Physical Switch + ISP Line for Guests ---")
    print("  - Cost: Requires extra switch, cabling, router, and second ISP subscription (~2x hardware/ISP opex).")
    print("  - Isolation: Complete physical air-gap (eliminates VLAN-hopping / misconfiguration risks).")
    print("  - Worth it when: High-compliance banking/defence/R&D networks mandate zero shared hardware with public guests.")


if __name__ == "__main__":
    main()
