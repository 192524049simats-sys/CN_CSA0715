"""CO2 Q6: IPv6 Compression, EUI-64, ICMP Traceroute, Multicast MAC & OpenFlow SDN."""
import ipaddress


def mac_to_eui64(mac):
    octets = [int(x, 16) for x in mac.split(":")]
    # Flip 7th bit (U/L bit = 0x02) of first byte and insert FF:FE in the middle
    octets[0] ^= 0x02
    eui = octets[:3] + [0xFF, 0xFE] + octets[3:]
    groups = [f"{eui[i]:02x}{eui[i+1]:02x}" for i in range(0, 8, 2)]
    return ":".join(groups)


def ipv4_multicast_to_mac(ip_str):
    octets = [int(x) for x in ip_str.split(".")]
    # Low 23 bits of IPv4 mapped into 01:00:5e:XX:YY:ZZ
    b4 = octets[1] & 0x7F
    b5 = octets[2]
    b6 = octets[3]
    return f"01:00:5e:{b4:02x}:{b5:02x}:{b6:02x}"


def openflow_eval(dst_ip, proto, dport):
    rules = [
        (200, "dst 10.5.0.0/16", lambda ip, p, pt: ipaddress.IPv4Address(ip) in ipaddress.IPv4Network("10.5.0.0/16"), "forward -> port 3"),
        (100, "TCP port 80", lambda ip, p, pt: p == "TCP" and pt == 80, "send -> controller"),
        (0, "default", lambda ip, p, pt: True, "drop"),
    ]
    for prio, desc, cond, action in sorted(rules, reverse=True):
        if cond(dst_ip, proto, dport):
            return prio, desc, action


def main():
    print("=== CO2 Q6: IPv6, ICMP TRACEROUTE, MULTICAST & OPENFLOW SDN ===")
    raw_v6 = "2001:0db8:0000:0000:0000:ff00:0042:8329"
    comp_v6 = str(ipaddress.IPv6Address(raw_v6))
    print(f"1. IPv6 Shortest Form:")
    print(f"   - Full       : {raw_v6}")
    print(f"   - Compressed : {comp_v6}")

    mac = "00:1A:2B:3C:4D:5E"
    eui64 = mac_to_eui64(mac)
    print(f"   - MAC {mac} -> EUI-64 IID = {eui64} (Link-local: fe80::{eui64})")

    print("\n2. How Traceroute Uses TTL & ICMP Time Exceeded:")
    print("   - Probes start with IP TTL=1, then 2, 3... Each router decrements TTL by 1;")
    print("     when TTL hits 0, the router drops the probe and returns ICMP Type 11 Code 0 (Time Exceeded),")
    print("     revealing its IP address and per-hop RTT until the destination replies (ICMP Port Unreachable / Echo Reply).")

    mcast_ip = "239.1.2.3"
    mcast_mac = ipv4_multicast_to_mac(mcast_ip)
    print(f"\n3. Multicast Camera Stream:")
    print(f"   - Group {mcast_ip} -> Multicast MAC = {mcast_mac}")
    print("   - Camera sends ONE stream; switches/routers running IGMP snooping & PIM replicate packets")
    print("     only at branching forks toward subscribed control rooms (saving upstream camera & backbone bandwidth).")

    print("\n4. OpenFlow Switch Rule Evaluation:")
    for pkt in [("HTTP", "10.5.1.1", "TCP", 80), ("SSH", "10.6.1.1", "TCP", 22)]:
        prio, desc, act = openflow_eval(pkt[1], pkt[2], pkt[3])
        print(f"   - {pkt[0]:<4} to {pkt[1]} ({pkt[2]}/{pkt[3]}) -> matched priority {prio} ({desc}) -> {act}")
    print("   - SDN Worth Adopting? YES for smart city: centralised traffic engineering, dynamic camera-stream steering,")
    print("     and programmable QoS/isolation across 2M sensors, provided redundant controllers prevent SPOF.")

    print("\n--- Alternative Concept Analysis: Native IPv6 vs Dual-Stack vs 6in4 Tunnel ---")
    payload = 100
    ip6_hdr = 40
    ip4_hdr = 20
    print(f"  - Native IPv6  : {payload} B payload + 40 B IPv6 = 140 B")
    print(f"  - 6in4 Tunnel  : +20 B outer IPv4 header -> 160 B (+{ip4_hdr/140*100:.2f}% packet size, {ip4_hdr} extra bytes; 20% of 100B sensor payload)")
    print("  - Verdict      : Start with Dual-Stack at gateways + Native IPv6 in new sensor/camera segments to avoid 6in4 MTU/encapsulation overhead.")


if __name__ == "__main__":
    main()
