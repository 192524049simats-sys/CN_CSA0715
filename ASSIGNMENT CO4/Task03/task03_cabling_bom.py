"""CO4 Task 3: Outpatient Cabling Audit, Device Domains, Bill of Materials & T568B."""


def main():
    print("=== CO4 TASK 3: OUTPATIENT CABLING AUDIT, DEVICES & BILL OF MATERIALS ===")
    print("3.1 TIA/EIA-568 Audit (Max 90 m Permanent Link, 100 m Channel):")
    runs = [
        ("Consulting rooms (35-80 m)", 80, "PASS (<90m)", "Cat6 UTP (or Cat6A for 10G future)"),
        ("Pharmacy (96 m)", 96, "FAIL (>90m perm link!)", "Multimode Fibre OM3/OM4 (zero distance margin left on copper)"),
        ("Waiting-hall APs (60 m)", 60, "PASS (<90m)", "Cat6A UTP (supports PoE+ & multi-gig Wi-Fi 6)"),
        ("Link to main building (420 m)", 420, "FAIL (4.2x > 100m!)", "OS2 Single-mode Fibre (420m > 10G OM3/OM4 300-400m limit)"),
    ]
    for name, dist, status, fix in runs:
        print(f"  - {name:<30} | {dist:3d} m | {status:<21} | Use: {fix}")

    print("\nMixed T568A/T568B Patch Cables:")
    print("  - Created: Crossover cables (TX pairs 1-2 & 3-6 swapped).")
    print("  - Modern switches: Still work seamlessly due to Auto-MDIX (IEEE 802.3ab), though standardising on T568B is best.")

    print("\n3.2 Device Selection & Domain Counts (Outpatient Block):")
    print("  - Chosen: L2 PoE+ Access Switches + Wi-Fi 6 APs + L3 Core Switch/Router + Stateful Firewall (NO hubs).")
    print("  - Collision Domains : 1 per active switch port + 1 per wireless cell (eliminates shared hub collisions).")
    print("  - Broadcast Domains : 4 VLANs (Consulting, Pharmacy, Guest Wi-Fi, Management) terminated at L3 Switch/Router.")

    print("\n3.3 Bill of Materials (Outpatient Block, with 10% spare cable):")
    # Example room count: 10 consulting rooms avg 57.5m (~575m), pharmacy 96m MMF, 4 APs @ 60m (240m), main link 420m SMF
    bom = [
        ("L2 Managed PoE+ 24-port Switch", 2, "48 access + 4 SFP+ ports", "Telecom rack"),
        ("Wi-Fi 6 Ceiling Access Points", 4, "802.11ax dual-band", "Waiting hall"),
        ("Cat6 / Cat6A UTP Cable (incl. 10% spare)", "900 m (815 m + 10%)", "RJ45 Cat6 plugs + keystone jacks", "Consulting + APs"),
        ("OM4 Multimode Fibre (incl. 10% spare)", "106 m (96 m + 10%)", "LC-LC duplex connectors", "Pharmacy"),
        ("OS2 Single-mode Fibre (incl. 10% spare)", "462 m (420 m + 10%)", "LC-LC + SFP-10G-LR transceivers", "To Main Bldg"),
        ("12U Wall/Floor Telecom Rack + Patch Panel + UPS", 1, "24-port Cat6 patch panel + LIU", "Telecom room"),
    ]
    for item, qty, spec, loc in bom:
        print(f"  - {item:<44} | Qty: {str(qty):<18} | {spec}")

    print("\n3.4 T568B Pinout Colour Order (Pins 1 to 8):")
    t568b = ["1: White-Orange", "2: Orange", "3: White-Green", "4: Blue",
             "5: White-Blue", "6: Green", "7: White-Brown", "8: Brown"]
    print("  " + " | ".join(t568b))

    print("\n--- Alternative Concept Analysis: 420 m Multimode Fibre vs Cat6A + Mid-Span Switch ---")
    print("  - Multimode/Single-mode Fibre : Single passive dielectric run (up to 550m-10km), zero mid-span power, immune to lightning/EMI.")
    print("  - Cat6A + Mid-span Switch     : Needs 4-5 segments/switches (<100m each) or 1 switch at 210m STILL exceeds 100m on each side!")
    print("    (To bridge 420m with 100m copper segments actually requires FOUR active mid-span switches + UPS + outdoor enclosures + surge arrestors!)")


if __name__ == "__main__":
    main()
