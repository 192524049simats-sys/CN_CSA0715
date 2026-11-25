"""CO2 Q1: IPv4 Addressing Traps, NAT Table Simulation & Datagram vs Virtual-Circuit Analysis."""
import ipaddress


def analyze_device(name, cidr, gw):
    iface = ipaddress.IPv4Interface(cidr)
    net = iface.network
    ip = iface.ip
    first_host = net.network_address + 1
    last_host = net.broadcast_address - 1
    is_net = (ip == net.network_address)
    is_bcast = (ip == net.broadcast_address)
    valid = not (is_net or is_bcast)
    reason = "VALID host address"
    if is_net:
        reason = "INVALID TRAP: configured IP equals the NETWORK address!"
    elif is_bcast:
        reason = "INVALID TRAP: configured IP equals the BROADCAST address!"
    print(f"  {name:<15} | IP: {str(ip):<14} /{net.prefixlen:<2} | GW: {gw:<13}")
    print(f"    Network: {net.network_address} | Broadcast: {net.broadcast_address} | Usable: {first_host} - {last_host}")
    print(f"    Verdict: {reason}\n")


def main():
    print("=== CO2 Q1: SPOT THE INVALID ADDRESSES IN HOSPITAL GROUP ===")
    devices = [
        ("Admission PC", "172.16.45.200/20", "172.16.32.1"),
        ("Lab printer", "10.0.15.255/21", "10.0.8.1"),
        ("X-ray server", "192.168.4.0/23", "192.168.4.1"),
        ("Clinic router", "203.0.113.10/29", "Public ISP"),
    ]
    for d in devices:
        analyze_device(*d)

    print("Clinic /29 Exhaustion & PAT (NAT Overload) Table Example:")
    print("  203.0.113.8/29 provides only 6 usable public IPs (203.0.113.9 - 203.0.113.14) for 18 devices.")
    print("  With PAT/NAPT, two internal PCs both using source port 50000 get unique external ports:")
    nat_table = [
        ("192.168.1.10:50000", "203.0.113.10:50000", "93.184.216.34:443"),
        ("192.168.1.11:50000", "203.0.113.10:50001", "93.184.216.34:443"),
    ]
    print("  +------------------------+------------------------+------------------------+")
    print("  | Inside Local           | Inside Global (NAT)    | Outside Global         |")
    print("  +------------------------+------------------------+------------------------+")
    for il, ig, og in nat_table:
        print(f"  | {il:<22} | {ig:<22} | {og:<22} |")
    print("  +------------------------+------------------------+------------------------+")

    print("\nDatagram vs Virtual-Circuit Switching:")
    print("  - Datagram (IP)     : Each packet routed independently; multipath/rerouting causes out-of-order arrival.")
    print("  - Virtual Circuit   : Fixed pre-established path/label (MPLS/ATM); packets follow identical path in order.")

    print("\n--- Alternative Concept Analysis: Public /27 vs /29 + NAT ---")
    n_27 = ipaddress.IPv4Network("203.0.113.0/27")
    print(f"  Public /27 usable IPs : {n_27.num_addresses - 2} hosts (fits 18 devices directly with 12 spares)")
    print("  Cost & Exposure       : Higher monthly IP lease cost; all 18 devices directly reachable/scannable on internet (needs strict stateful firewall).")
    print("  NAT Problems Removed  : Fixes inbound P2P/VoIP/SIP ALG breakage, port-forwarding conflicts, and end-to-end IPsec/checksum issues.")


if __name__ == "__main__":
    main()
