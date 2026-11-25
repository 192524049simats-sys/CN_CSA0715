"""Nyquist and Shannon limits for the transmission media proposed for a campus."""
import math


def nyquist(bandwidth_hz, levels):
    # TODO 1: Return the Nyquist maximum bit rate for a noiseless channel: 2 x bandwidth
    # x log2(levels)
    return 2 * bandwidth_hz * math.log2(levels)


def shannon(bandwidth_hz, snr_db):
    # TODO 2: Convert the SNR from decibels to a ratio (10 ** (dB / 10)) and return the
    # Shannon capacity: bandwidth x log2(1 + SNR)
    snr = 10 ** (snr_db / 10)
    return bandwidth_hz * math.log2(1 + snr)


media = [("Telephone line", 3_100, 30), ("Cat6 pair", 250e6, 40),
         ("Wi-Fi 6 channel", 160e6, 25)]
for name, bw, snr in media:
    print(f"{name:<16} Shannon limit {shannon(bw, snr) / 1e6:10.2f} Mbps")
print(f"Nyquist, 3,100 Hz with 4 levels: {nyquist(3_100, 4) / 1e3:.1f} kbps")

# --- Follow-up Calculations ---
print("\n--- Follow-up: SNR needed on 3,100 Hz telephone line for 56 kbps ---")
req_snr_ratio = 2 ** (56_000 / 3_100) - 1
req_snr_db = 10 * math.log10(req_snr_ratio)
print(f"  Required SNR ratio : {req_snr_ratio:,.2f}")
print(f"  Required SNR (dB)  : {req_snr_db:.2f} dB (Unrealistic for analog POTS loop; typically ~30-35 dB)")

print("\n--- Plant Cable Runs & Trap Analysis ---")
print("  (a) Robot cell near welders (85 m)  -> Cat6A S/FTP (shielded; <100 m limit; blocks arc-welding EMI)")
print("  (b) Office to shop-floor (140 m)   -> Multimode Fibre OM3/OM4 (TRAP: 140 m > 100 m Cat6/Cat6A limit!)")
print("  (c) Shop floor to DC (550 m)       -> Single-mode Fibre (OS2; 550 m exceeds 10G OM3/OM4 300-400 m limit)")
print("  (d) Plant to head office (400 km)  -> Leased Line / Carrier MPLS over Single-mode Fibre")

c_40db = shannon(250e6, 40) / 1e6
c_15db = shannon(250e6, 15) / 1e6
print(f"\n  250 MHz cable @ 40 dB SNR (clean)  : {c_40db:.2f} Mbps")
print(f"  250 MHz cable @ 15 dB SNR (welders): {c_15db:.2f} Mbps (-{(1 - c_15db/c_40db)*100:.1f}% capacity drop)")
print("  Why real speed < Shannon limit     : Protocol headers, guard bands, attenuation, ISI, finite modulation/FEC.")

# Alternative Concept Analysis: Wi-Fi 6 @ 15 dB on 160 MHz channel
wifi_15db = shannon(160e6, 15) / 1e6
print("\n--- Alternative Concept: Wi-Fi 6 (160 MHz, 15 dB SNR near welders) ---")
print(f"  Shannon capacity @ 15 dB           : {wifi_15db:.2f} Mbps (theoretical ceiling)")
print("  Verdict: NOT acceptable for 10 ms robot commands — CSMA/CA contention + arc-welding EMI")
print("           induce retries and non-deterministic latency > 10 ms.")
