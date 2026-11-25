"""CO2 Q3: Longest-Prefix Match Routing Table Lookup & Static vs OSPF Evaluation."""
import ipaddress

ROUTES = [
    ("10.0.0.0/8", "192.0.2.1"),
    ("10.1.0.0/16", "192.0.2.5"),
    ("10.1.2.0/24", "192.0.2.9"),
    ("10.1.2.128/25", "192.0.2.13"),
    ("0.0.0.0/0", "198.51.100.1"),
]


def longest_prefix_match(dst_ip):
    ip = ipaddress.IPv4Address(dst_ip)
    matches = []
    for prefix, nh in ROUTES:
        net = ipaddress.IPv4Network(prefix)
        if ip in net:
            matches.append((net.prefixlen, prefix, nh))
    matches.sort(reverse=True)
    return matches[0], matches


def main():
    print("=== CO2 Q3: LONGEST-PREFIX MATCH & STATIC/FLOATING FAILOVER ===")
    targets = ["10.1.2.200", "10.1.2.100", "10.1.9.9", "10.7.7.7", "8.8.8.8"]
    for t in targets:
        best, all_m = longest_prefix_match(t)
        all_str = ", ".join(p for _, p, _ in all_m)
        print(f"  Dst {t:<12} -> Next Hop {best[2]:<13} (via {best[1]:<15}) | All matches: [{all_str}]")

    print("\nDCE Clock-Rate Removal Check (Packet Tracer Serial0/0/0):")
    print("  - Removing 'clock rate 64000' on R1 (DCE) stops clocking pulses -> Serial0/0/0 status becomes 'up/down' (line protocol down),")
    print("    causing the primary static route to be withdrawn and traffic to fail over to the AD 200 floating static route.")

    print("\n--- Alternative Concept Analysis: Static Routes vs OSPF ---")
    print("  - 2 Campuses  : Static+Floating = ~4 route lines; OSPF = ~6 lines (comparable).")
    print("  - 5 Campuses  : Full-mesh static routes need ~5 x 4 x 2 (primary+backup) = 40+ manual lines;")
    print("                  OSPF needs ~5 lines/router regardless of remote prefixes.")
    print("  - Failover    : Floating static fails over instantly ONLY if link-down detected; fails to detect mid-path failure without IP SLA.")
    print("                  OSPF detects link-down (<1 s carrier) or Hello dead timer (40 s default, <200 ms with BFD) end-to-end.")


if __name__ == "__main__":
    main()
