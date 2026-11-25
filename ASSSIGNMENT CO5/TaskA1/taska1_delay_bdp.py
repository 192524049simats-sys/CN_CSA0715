"""CO5 Task A1: Delay Breakdown, Bandwidth-Delay Product, SLA Targets & Passive vs Active Monitoring."""


def main():
    print("=== CO5 TASK A1: WHERE DOES THE DELAY COME FROM? ===")
    pkt_bits = 1500 * 8
    rate_bps = 100e6
    dist_m = 2_000_000
    speed = 2e8
    n_routers = 3
    n_links = n_routers + 1

    tx_1link_ms = (pkt_bits / rate_bps) * 1000
    tx_4links_ms = n_links * tx_1link_ms
    prop_ms = (dist_m / speed) * 1000
    queue_ms = n_routers * 0.5
    proc_ms = n_routers * 0.1
    total_ms = tx_4links_ms + prop_ms + queue_ms + proc_ms

    print("A1.1 — 1,500-byte Packet over 2,000 km, 100 Mbps links, 3 Routers (4 links):")
    print(f"  - Transmission delay (4 links x {tx_1link_ms:.2f} ms) : {tx_4links_ms:6.3f} ms")
    print(f"  - Propagation delay (2,000 km / 2e8 m/s)  : {prop_ms:6.3f} ms  ({prop_ms/total_ms*100:.1f}% -> DOMINANT)")
    print(f"  - Queuing delay (3 routers x 0.5 ms)      : {queue_ms:6.3f} ms")
    print(f"  - Processing delay (3 routers x 0.1 ms)   : {proc_ms:6.3f} ms")
    print(f"  - Total one-way delay                     : {total_ms:6.3f} ms")
    tx_1g_ms = n_links * (pkt_bits / 1e9) * 1000
    print(f"  Upgrading all links to 1 Gbps cuts tx to {tx_1g_ms:.3f} ms -> total {total_ms - tx_4links_ms + tx_1g_ms:.3f} ms (saves only {(tx_4links_ms - tx_1g_ms)/total_ms*100:.1f}%!).")

    print("\nA1.2 — Bandwidth-Delay Product (1 Gbps link, 80 ms RTT):")
    bdp_bits = 1e9 * 0.080
    bdp_mb = bdp_bits / 8 / 1e6
    win_64k_bits = 65_535 * 8
    max_thr_mbps = win_64k_bits / 0.080 / 1e6
    print(f"  - BDP = 1 Gbps x 0.080 s = {bdp_bits/1e6:.0f} Mb = {bdp_mb:.1f} MB in flight")
    print(f"  - 64 KB TCP window sends max 65,535 B per 80 ms RTT -> throughput = {max_thr_mbps:.3f} Mbps ({max_thr_mbps/1000*100:.3f}% of 1 Gbps!)")

    print("\nA1.3 — Application SLA Targets & Measurement Tools:")
    slas = [
        ("Live Video", "<= 150 ms", "<= 30 ms", "<= 1%", ">= 2.5 Mbps", "iperf3 + Wireshark RTP + ping"),
        ("Live Voice", "<= 150 ms", "<= 20 ms", "<= 1%", ">= 80 kbps", "ping + Wireshark RTP + NS-3"),
        ("Recorded Video", "<= 1-2 s", "N/A (buf)", "<= 0.5%", ">= 5 Mbps", "iperf3 + curl/browser DevTools"),
        ("E-mail", "<= 5 s", "N/A", "0% (TCP)", ">= 1 Mbps", "SMTP/IMAP probe + SNMP"),
        ("File Downloads", "Best effort", "N/A", "0% (TCP)", ">= 20 Mbps", "iperf3 (window scaling) + SNMP"),
    ]
    for app, d, j, l, t, tool in slas:
        print(f"  - {app:<15}: Delay {d:<10} | Jitter {j:<9} | Loss {l:<8} | Thr {t:<11} | Tool: {tool}")
    print("  Active vs Passive: Active injects synthetic probes (ping/iperf3) to measure latency/loss anytime;")
    print("                     Passive observes live production traffic (Wireshark/SNMP) with zero overhead.")

    print("\n--- Alternative Concept Analysis: Passive-Only Monitoring ---")
    print("  - Can obtain : Interface utilisation, error/drop counters (SNMP), TCP retransmits & app response times (PCAP).")
    print("  - Would miss : Baseline RTT/jitter during quiet hours, proactive SLA alerts before students log in, and path hop breakdown.")


if __name__ == "__main__":
    main()
