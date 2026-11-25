"""CO5 Task A3: P2P vs Client-Server Distribution, G.711 VoIP Bandwidth & CDN/VPN Overlays."""
import math


def main():
    print("=== CO5 TASK A3: P2P, VoIP & OVERLAYS BY THE NUMBERS ===")
    # 4 GB package = 4 * 1024^3 * 8 bits = 34.3597 Gbits (also show 4e9*8 = 32 Gbits)
    F_mb = 4 * 1000 * 8       # 32,000 Mb (decimal)
    F_mib = 4 * 1024 * 8      # 32,768 Mb (4 GiB)
    N = 20
    u_s = 100.0               # Mbps
    d_i = 50.0                # Mbps
    u_i = 20.0                # Mbps

    t_cs = max(N * F_mb / u_s, F_mb / d_i)
    t_p2p = max(F_mb / u_s, F_mb / d_i, (N * F_mb) / (u_s + N * u_i))
    print(f"A3.1 — Distributing 4 GB (32,000 Mb) to N={N} Regional Centres:")
    print(f"  - Client-Server min time : max(20*32000/100, 32000/50) = {t_cs:.0f} s ({t_cs/60:.1f} min)")
    print(f"  - Peer-to-Peer min time  : max(320, 640, 640000/500)  = {t_p2p:.0f} s ({t_p2p/60:.1f} min) -> {t_cs/t_p2p:.1f}x faster!")
    print("  (Note: Using 4 GiB = 32,768 Mb gives CS = 6,553.6 s and P2P = 1,310.7 s, same 5.0x speedup.)")
    print("  Why P2P wins: Each centre contributes 20 Mbps upload (total 500 Mbps vs 100 Mbps server).")
    print("  When P2P would NOT win: Asymmetric residential links with near-zero upload, NAT blocks, or N=1.")

    print("\nA3.2 — G.711 VoIP Call Real Bandwidth (20 ms packets, 40B IP/UDP/RTP):")
    pps = 1.0 / 0.020
    speech_bytes = int(64_000 / 8 * 0.020)
    pkt_bytes = speech_bytes + 40
    real_bps = pps * pkt_bytes * 8
    calls_2m = int(2_000_000 // real_bps)
    print(f"  - Packets/sec      : {pps:.0f} pkt/s | Speech = {speech_bytes} B + 40 B headers = {pkt_bytes} B/pkt")
    print(f"  - Real BW/direction: {real_bps/1000:.1f} kbps (+25% header overhead over 64 kbps codec)")
    print(f"  - Calls on 2 Mbps  : {calls_2m} calls per direction (before L2 Ethernet/PPP headers)")
    print("  - SIP vs RTP       : SIP handles signalling (INVITE/ACK/BYE, session setup & codec negotiation);")
    print("                       RTP carries the actual real-time audio stream with timestamps & seq numbers.")

    print("\nA3.3 — Overlay Networks (CDN & VPN):")
    print("  - CDN caches recorded lectures/packages at regional edge PoPs over the public Internet -> fixes evening congestion/DoS.")
    print("  - VPN builds encrypted IPsec/WireGuard tunnels over public Internet -> secures inter-office/admin traffic.")

    print("\n--- Alternative Concept Analysis: CDN with 1 Gbps Edge Server in Each Region ---")
    t_cdn = F_mb / d_i   # bottlenecked by centre's 50 Mbps download once edge is populated
    print(f"  - Download time from local 1 Gbps CDN edge (limited by centre 50 Mbps down): {t_cdn:.0f} s ({t_cdn/60:.1f} min, 2x faster than P2P!)")
    print("  - Trade-off: Higher recurring CDN cost vs much higher reliability, zero NAT traversal issues, and built-in DDoS absorption.")


if __name__ == "__main__":
    main()
