"""CO1 Task 5: Wi-Fi 6 vs Private 5G Handover & Service Slice Analysis for AGVs."""


def main():
    print("=== CO1 TASK 5: WI-FI 6 vs PRIVATE 5G FOR MOVING AGVs ===")
    route_m = 1200
    speed_ms = 2.0
    trip_time_s = route_m / speed_ms

    # Handovers along 1.2 km route (30 m AP spacing -> 39 transitions; 300 m 5G cell -> 3 transitions)
    wifi_handovers = (route_m // 30) - 1
    fiveg_handovers = (route_m // 300) - 1
    wifi_down_s = wifi_handovers * 0.150
    fiveg_down_s = fiveg_handovers * 0.020

    print(f"Route length: {route_m} m | AGV speed: {speed_ms} m/s | Trip duration: {trip_time_s:.0f} s")
    print(f"  Wi-Fi (30 m AP spacing, 150 ms HO) : {wifi_handovers:2d} handovers | Unreachable = {wifi_down_s:.2f} s ({wifi_down_s/trip_time_s*100:.2f}%)")
    print(f"  5G    (300 m cell, 20 ms HO)       : {fiveg_handovers:2d} handovers | Unreachable = {fiveg_down_s:.2f} s ({fiveg_down_s/trip_time_s*100:.4f}%)")
    print("  10 ms deadline check: Both 150 ms Wi-Fi HO and 20 ms break-before-make 5G HO exceed 10 ms;")
    print("  5G Dual Active Protocol Stack (DAPS / make-before-break) achieves ~0 ms interruption.")

    print("\n5G Service Class Mapping:")
    print("  - AGVs & Robot controllers -> URLLC (Ultra-Reliable Low-Latency Communications, <1-10 ms, 99.999%)")
    print("  - CCTV video streams       -> eMBB  (Enhanced Mobile Broadband, high throughput ~96 Mbps/line)")
    print("  - Temperature/Vib sensors  -> mMTC  (Massive Machine-Type Communications, high connection density)")

    print("\nShort-Range / LPWAN Technologies in the Plant:")
    print("  - Bluetooth (BLE): Wearable/handheld technician diagnostics (<10-30 m).")
    print("  - Zigbee         : Low-power mesh ambient temperature/lighting sensors.")
    print("  - LoRa / LoRaWAN : Yard/warehouse environmental sensors over kilometres (battery life in years).")

    print("\nWi-Fi 6 + 802.11r (Fast BSS Transition):")
    print("  - Cuts handover from ~150 ms to ~20-50 ms, still risky for strict 10 ms AGV deadline")
    print("    due to unlicensed 2.4/5 GHz contention, welding EMI, and roaming misses.")

    # Alternative Concept Analysis: LoRaWAN for 600 sensors @ 50 B/s
    sensor_rate_bps = 600 * 50 * 8
    lora_cap_bps = 5_000
    print("\n--- Alternative Concept: LoRaWAN (5 kbps) for 600 Sensors ---")
    print(f"  Required sensor throughput : {sensor_rate_bps / 1000:.1f} kbps (600 x 50 B/s)")
    print(f"  Single LoRa gateway cap    : {lora_cap_bps / 1000:.1f} kbps (oversubscribed {sensor_rate_bps/lora_cap_bps:.0f}x!)")
    print("  Decision: High-rate vibration sensors (50 B/s) MUST stay on Wi-Fi/wired/5G mMTC;")
    print("            only slow telemetry (e.g. temperature every 60 s) suits LoRaWAN.")


if __name__ == "__main__":
    main()
