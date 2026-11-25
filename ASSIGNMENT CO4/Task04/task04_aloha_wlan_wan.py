"""CO4 Task 4: ALOHA, CSMA/CD Min Frame, Wi-Fi 6 Channel Plan & ATM/MPLS WAN Calculations."""
import math


def main():
    print("=== CO4 TASK 4: SHARED MEDIA, WIRELESS LANs & WANs BY THE NUMBERS ===")
    # 4.1 Multiple Access
    pure_aloha = 1.0 / (2.0 * math.e)
    slotted_aloha = 1.0 / math.e
    dist_m = 2500.0
    speed = 2e8
    rate = 10e6
    prop_s = dist_m / speed
    rtt_s = 2.0 * prop_s
    min_bits = rate * rtt_s
    print("4.1 Multiple Access:")
    print(f"  - Pure ALOHA max throughput    : 1/(2e) = {pure_aloha*100:.2f}% (0.184)")
    print(f"  - Slotted ALOHA max throughput : 1/e    = {slotted_aloha*100:.2f}% (0.368)")
    print(f"  - 10 Mbps, 2,500 m, v=2e8 m/s  : prop = {prop_s*1e6:.2f} us, 2*prop = {rtt_s*1e6:.2f} us")
    print(f"  - Min CSMA/CD frame size       : {min_bits:.0f} bits ({min_bits/8:.2f} B; IEEE 802.3 pads to 512 bits / 64 B for repeaters)")
    print("  - Full-duplex switched Ethernet: Dedicated TX/RX wire pairs -> zero collisions -> CSMA/CD disabled.")
    print("  - Wi-Fi (802.11): Shared half-duplex RF medium -> cannot hear collisions while transmitting -> uses CSMA/CA.")

    # 4.2 Wireless LANs (300 phones in waiting hall)
    print("\n4.2 Waiting Hall Wireless Plan (300 Phones):")
    print("  - Deploy 6 Wi-Fi 6 (802.11ax) ceiling APs (~50 phones/AP).")
    print("  - 2.4 GHz non-overlapping reuse: Channels 1, 6, 11 alternating across adjacent cells.")
    print("  - 5 GHz non-overlapping (20/40 MHz): Channels 36, 40, 44, 48, 149, 153 (zero co-channel overlap).")
    print("  - Wi-Fi 6 features: OFDMA (sub-channel RUs serve multiple phones/TXOP), MU-MIMO (spatial streams), BSS Colouring (spatial reuse).")
    print("  - Bluetooth (BLE): Suits bedside pulse-oximeters/wearables (<10 m, low power); unsuitable for waiting-hall WAN/high-rate imaging.")

    # 4.3 Backbone & WAN
    atm_ov = 5.0 / 53.0 * 100
    eth_ov = 18.0 / 1518.0 * 100
    print("\n4.3 ATM vs Ethernet Overhead & Virtual Circuits:")
    print(f"  - ATM cell (5B hdr / 53B total)     : {atm_ov:.2f}% header overhead")
    print(f"  - Ethernet (18B hdr+FCS / 1518B)    : {eth_ov:.2f}% header overhead")
    print("  - Virtual circuit IDs: Frame Relay = DLCI | ATM = VPI/VCI | MPLS = 20-bit Label.")
    print("  - Clinic WAN choice: MPLS for predictable SLA latency/jitter & DiffServ QoS for live tele-consultations.")

    print("\n--- Alternative Concept Analysis: Internet VPN vs MPLS for 3 Branch Clinics ---")
    print("  - Internet IPsec VPN : Best-effort public internet (no BW/delay SLA, cannot enforce end-to-end QoS priority for video).")
    print("  - Carrier MPLS       : Committed Information Rate (CIR), <20-30 ms SLA delay, honours EF/AF CoS queues.")
    print("  - Acceptable premium : ~2x-3x monthly link cost justified when clinical video consultations cannot tolerate public jitter.")


if __name__ == "__main__":
    main()
