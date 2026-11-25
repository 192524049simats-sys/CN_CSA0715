"""CO1 Task 10: Traceroute Analysis + Live Windows Ping, Tracert & Socket Header Capture."""
import re
import socket
import subprocess
import time


def main():
    print("=== CO1 TASK 10: DELAY ANALYSIS & REAL NETWORK MEASUREMENT ===")
    # 1. Given 400 km traceroute analysis
    prop_one_way_ms = (400_000 / 2e8) * 1000
    prop_rtt_ms = 2 * prop_one_way_ms
    measured_avg_ms = (12.6 + 12.4 + 12.9) / 3.0
    print(f"1. Given 400 km Head-Office Traceroute Analysis:")
    print(f"   - Expected propagation delay : {prop_one_way_ms:.2f} ms one-way | {prop_rtt_ms:.2f} ms RTT")
    print(f"   - Measured RTT to 10.200.0.10: {measured_avg_ms:.2f} ms avg (min 12.4 ms)")
    print(f"   - Propagation share of RTT   : {prop_rtt_ms / measured_avg_ms * 100:.1f}% (remaining {measured_avg_ms - prop_rtt_ms:.2f} ms = routing/queuing/tx)")
    print("   - Hop 3 (38.2 ms spike)      : Control-plane ICMP TTL-exceeded rate-limiting/CPU delay (NOT a data-plane fault; Hop 4 is 11.5 ms).")
    print("   - Hop 5 (* * *)              : Router drops ICMP probes/ACL blocks TTL-exceeded (NOT a fault; Hop 6 responds cleanly).")
    print("   - Largest delay jump         : Hop 4 (103.21.8.17), jumping from ~4.1 ms (Hop 3) to ~11.8 ms (+7.7 ms, long-haul WAN segment).")

    # 2. Real Live Ping & Tracert from this Windows host
    print("\n2. Live Ping Measurement (ping -n 4 1.1.1.1):")
    ping_out = subprocess.check_output(["ping", "-n", "4", "1.1.1.1"], text=True, timeout=15)
    print(ping_out.strip())

    print("\n3. Live Traceroute Measurement (tracert -d -h 10 -w 1000 1.1.1.1):")
    tracert_out = subprocess.check_output(["tracert", "-d", "-h", "10", "-w", "1000", "1.1.1.1"], text=True, timeout=30)
    print(tracert_out.strip())

    # 4. Real HTTP/TCP header inspection over live connection
    print("\n4. Real TCP+HTTP Probe to example.com (port 80) — Layer Headers Dissected:")
    t0 = time.perf_counter()
    ip = socket.gethostbyname("example.com")
    t_dns = (time.perf_counter() - t0) * 1000
    t1 = time.perf_counter()
    with socket.create_connection((ip, 80), timeout=8) as s:
        t_tcp = (time.perf_counter() - t1) * 1000
        local_ip, local_port = s.getsockname()
        s.sendall(b"HEAD / HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\n\r\n")
        resp = s.recv(512).decode(errors="replace").splitlines()[0:4]
    print(f"   - DNS lookup time   : {t_dns:.2f} ms -> example.com = {ip}")
    print(f"   - TCP 3-way HS RTT  : {t_tcp:.2f} ms ({local_ip}:{local_port} -> {ip}:80)")
    print(f"   - L2 Ethernet II    : 14B hdr + 4B FCS (Src Host NIC -> Default Gateway MAC)")
    print(f"   - L3 IPv4           : 20B hdr (Src {local_ip} -> Dst {ip}, Proto=6 TCP, TTL=128 Win)")
    print(f"   - L4 TCP            : 20B hdr (SrcPort={local_port} -> DstPort=80, SYN/SYN-ACK/ACK)")
    print(f"   - L7 HTTP response  : {' | '.join(resp)}")

    # 5. Alternative Concept: SNMP/NetFlow vs Occasional Ping/Traceroute
    print("\n5. Alternative Concept Analysis: Continuous SNMP/NetFlow vs Occasional Ping/Traceroute:")
    print("   - SNMP/NetFlow detects interface utilisation, queue drops, and asymmetric congestion within 10-60 s,")
    print("     distinguishing true packet loss from Hop 5 ICMP filtering (* * *). Occasional ping only sees instantaneous RTT.")


if __name__ == "__main__":
    main()
