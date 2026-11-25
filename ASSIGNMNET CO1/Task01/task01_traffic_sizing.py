"""CO1 Task 1: Smart Manufacturing Plant Traffic Sizing & Bottleneck Analysis."""


def main():
    print("=== CO1 TASK 1: SMART MANUFACTURING PLANT TRAFFIC SIZING ===")
    # Traffic per production line
    robot_bps = 40 * (200 * 8) / 0.002       # 40 controllers, 200 B every 2 ms
    sensor_bps = 600 * (50 * 8) / 1.0        # 600 sensors, 50 B/s
    cctv_bps = 24 * 4_000_000                # 24 cameras @ 4 Mbps continuous
    office_bps = 150 * 0.10 * 2_000_000      # 150 users, 10% active @ 2 Mbps

    sources = [
        ("Robot controllers (40 x 200B / 2ms)", robot_bps, "<= 10 ms (strict)"),
        ("Vibration sensors (600 x 50B / s)", sensor_bps, "~1 s (tolerant)"),
        ("CCTV cameras (24 x 4 Mbps)", cctv_bps, "~100-200 ms (buffered)"),
        ("Office users (150 x 10% x 2 Mbps)", office_bps, "~200-500 ms (elastic)"),
    ]

    total_1_line = sum(s[1] for s in sources)
    total_8_lines = total_1_line * 8

    for name, bps, req in sources:
        print(f"  {name:<38}: {bps / 1e6:8.2f} Mbps | Delay req: {req}")

    print(f"\nTotal traffic (1 production line)     : {total_1_line / 1e6:.2f} Mbps")
    print(f"Total traffic (8 production lines)    : {total_8_lines / 1e6:.2f} Mbps ({total_8_lines / 1e9:.4f} Gbps)")
    print(f"Single 1 Gbps uplink sufficient?      : {'YES' if total_8_lines <= 1e9 else 'NO (oversubscribed by ' + f'{(total_8_lines - 1e9)/1e6:.2f} Mbps)'}")

    # Queueing impact if CCTV and robot commands share a FIFO queue on 1 Gbps
    # One 1500B CCTV MTU frame at 1 Gbps = 12 us; at 100 Mbps = 120 us; bursty queue buildup
    # Under congestion (>1.266 Gbps on 1 Gbps link), queue fills to buffer limit (e.g. 10-50 MB -> 80-400 ms)
    print("\nDelay vs Volume Finding:")
    print("  - Highest data volume   : CCTV cameras (96.00 Mbps/line = 60.67% of line traffic)")
    print("  - Strictest delay req   : Robot controllers (<= 10 ms deadline, only 32.00 Mbps/line)")
    print("  - Shared FIFO queue risk: Continuous 768 Mbps CCTV + 518.4 Mbps other saturates 1 Gbps,")
    print("    causing tail drops and >100 ms queueing delay that violates the 10 ms robot deadline.")

    print("\n100 ms Delay Harm Ranking (Most to Least Harmful):")
    print("  1. Robot controllers  -> Safety/collision risk; 50 control cycles missed (deadline 10 ms).")
    print("  2. Vibration sensors  -> Delayed fault/anomaly alert; slight buffer risk on high-rate bursts.")
    print("  3. CCTV cameras       -> Live monitoring lag/jitter; tolerable via short playback buffer.")
    print("  4. Office users       -> Mild ERP/email sluggishness; fully elastic TCP traffic.")

    # Alternative Concept Analysis: Motion-triggered CCTV (5% duty cycle)
    cctv_alt_bps = cctv_bps * 0.05
    line_alt_bps = robot_bps + sensor_bps + cctv_alt_bps + office_bps
    plant_alt_bps = line_alt_bps * 8
    print("\n--- Alternative Concept Analysis: Motion-Triggered CCTV (5% active) ---")
    print(f"  CCTV traffic (5% of 96 Mbps)        : {cctv_alt_bps / 1e6:.2f} Mbps/line")
    print(f"  Revised 1-line total                : {line_alt_bps / 1e6:.2f} Mbps")
    print(f"  Revised 8-line total                : {plant_alt_bps / 1e6:.2f} Mbps (53.6% of 1 Gbps)")
    print("  Verdict: 1 Gbps uplink is NO LONGER the continuous average bottleneck, though QoS")
    print("           (DiffServ EF) is still required so simultaneous motion bursts do not delay robots.")


if __name__ == "__main__":
    main()
