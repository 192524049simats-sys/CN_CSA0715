"""Link utilisation of stop-and-wait and sliding-window protocols on different links."""
import math


def utilisation(frame_bits, rate_bps, distance_m, window, speed=2e8):
    tx = frame_bits / rate_bps              # transmission time
    prop = distance_m / speed               # propagation time
    # TODO 1: a = prop / tx. Utilisation is window / (1 + 2a), but never more than 1.
    # Return the utilisation and a
    a = prop / tx
    u = min(1.0, window / (1.0 + 2.0 * a))
    return u, a


links = [("Campus LAN, 200 m, 1 Gbps", 1e9, 200),
         ("City fibre, 50 km, 1 Gbps", 1e9, 50_000),
         ("Satellite, 36,000 km, 10 Mbps", 10e6, 36_000_000)]
for name, rate, dist in links:
    u1, a = utilisation(12_000, rate, dist, 1)
    u7, _ = utilisation(12_000, rate, dist, 7)
    u127, _ = utilisation(12_000, rate, dist, 127)
    print(f"{name:<31} a = {a:7.2f} stop-and-wait {u1:6.1%} "
          f"W=7 {u7:6.1%} W=127 {u127:6.1%}")

# --- Follow-up: Satellite 100% window & Head-Office 400 km 1 Gbps Link ---
_, a_sat = utilisation(12_000, 10e6, 36_000_000, 1)
w_sat_100 = math.ceil(1 + 2 * a_sat)
print(f"\n--- Follow-up: Satellite 100% Utilisation Window ---")
print(f"  a = {a_sat:.2f} -> smallest integer window W >= 1 + 2a = {w_sat_100}")

print("\n--- Head-Office Link: 400 km Fibre @ 1 Gbps, 1,500 B frames ---")
u_ho_sw, a_ho = utilisation(12_000, 1e9, 400_000, 1)
tx_ho = 12_000 / 1e9
prop_ho = 400_000 / 2e8
w_ho = math.ceil(1 + 2 * a_ho)
gbn_bits = math.ceil(math.log2(w_ho + 1))
sr_bits = math.ceil(math.log2(2 * w_ho))
print(f"  Tx time = {tx_ho*1e6:.2f} us | Prop time = {prop_ho*1e3:.2f} ms | a = {a_ho:.2f}")
print(f"  Stop-and-Wait U = {u_ho_sw*100:.3f}% ({u_ho_sw*1000:.2f} Mbps)")
print(f"  Min window for 100% U = {w_ho} frames (1 + 2a = {1 + 2*a_ho:.2f})")
print(f"  Seq-number bits: Go-Back-N >= {gbn_bits} bits (2^k - 1 >= {w_ho}) | Selective Repeat >= {sr_bits} bits (2^(k-1) >= {w_ho})")
print("  SR vs GBN: Selective Repeat resends only lost frames (1 vs up to W), costing W frames of out-of-order RX buffer.")
print("  HDLC/PPP framing: Uses 0x7E (01111110) start/end flags with bit stuffing (HDLC) or byte stuffing 0x7D (PPP).")

# Alternative Concept Analysis: Selective Repeat W=64 on 400 km link
u_sr64, _ = utilisation(12_000, 1e9, 400_000, 64)
print("\n--- Alternative Concept: Selective Repeat W=64 on 400 km Link ---")
print(f"  Utilisation = {u_sr64*100:.2f}% | Effective throughput = {u_sr64*1000:.2f} Mbps")
print(f"  Receiver buffer required = 64 x 1,500 B = {64 * 1500:,} bytes ({64 * 1500 / 1024:.2f} KB)")
