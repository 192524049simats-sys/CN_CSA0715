"""Hamming(7,4) code: correct a single-bit error in a 4-bit sensor reading."""
import math


def encode(d):                              # d = [d1, d2, d3, d4]
    p1 = d[0] ^ d[1] ^ d[3]
    p2 = d[0] ^ d[2] ^ d[3]
    p3 = d[1] ^ d[2] ^ d[3]
    return [p1, p2, d[0], p3, d[1], d[2], d[3]]     # positions 1..7


def decode(c):
    # TODO 1: Compute the syndrome bits s1 (positions 1,3,5,7), s2 (2,3,6,7) and s3
    # (4,5,6,7); pos = s1 + 2*s2 + 4*s3. If pos is not 0, flip bit pos (index pos-1).
    # Return pos and the data bits at positions 3, 5, 6, 7
    s1 = c[0] ^ c[2] ^ c[4] ^ c[6]
    s2 = c[1] ^ c[2] ^ c[5] ^ c[6]
    s3 = c[3] ^ c[4] ^ c[5] ^ c[6]
    pos = s1 + 2 * s2 + 4 * s3
    corrected = c[:]
    if pos != 0:
        corrected[pos - 1] ^= 1
    data = [corrected[2], corrected[4], corrected[5], corrected[6]]
    return pos, data


word = encode([1, 0, 1, 1])
print("codeword :", "".join(map(str, word)))
for flip in (None, 5):
    rx = word[:]
    if flip:
        rx[flip - 1] ^= 1
    pos, data = decode(rx)
    print(f"error at {str(flip):<4}: syndrome {pos}, data {''.join(map(str, data))}")

# --- Follow-up: 2-bit error miscorrection & 16-bit Hamming calculations ---
print("\n--- Follow-up: Double-bit flip (positions 3 and 5) ---")
rx2 = word[:]
rx2[2] ^= 1
rx2[4] ^= 1
pos2, data2 = decode(rx2)
print(f"  Corrupted rx={''.join(map(str, rx2))} -> syndrome {pos2}, miscorrected data={''.join(map(str, data2))} (WRONG; expected 1011!)")

# 16-bit word Hamming check bits
m = 16
r = 1
while (2 ** r) < (m + r + 1):
    r += 1
overhead_pct = r / (m + r) * 100
print(f"\n--- 16-bit Sensor Word Hamming Sizing ---")
print(f"  m = {m} bits -> smallest r with 2^r >= m+r+1 is r = {r} (2^{r}={2**r} >= {m+r+1})")
print(f"  Codeword = {m+r} bits | Overhead = {r}/{m+r} = {overhead_pct:.2f}%")

# Minimum Hamming distance of {00000, 01011, 10101, 11110}
codebook = ["00000", "01011", "10101", "11110"]
d_min = min(sum(a != b for a, b in zip(codebook[i], codebook[j]))
            for i in range(len(codebook)) for j in range(i + 1, len(codebook)))
print(f"  Min Hamming distance d_min = {d_min} -> detects {d_min - 1} errors, corrects {(d_min - 1) // 2} error")

# Received 0110111
pos_rx, data_rx = decode([int(x) for x in "0110111"])
print(f"  Received 0110111 -> syndrome {pos_rx} (bit 5 flipped), corrected data = {''.join(map(str, data_rx))}")

# Alternative Concept Analysis: BER = 1e-3, FEC vs ARQ (40 ms retransmission)
print("\n--- Alternative Concept: BER = 1e-3 (Hamming FEC vs 40 ms ARQ) ---")
ber = 1e-3
p_err_16 = 1 - (1 - ber) ** 16
p_err_21 = 1 - (1 - ber) ** 21
p_gt1_21 = 1 - ((1 - ber) ** 21 + 21 * ber * ((1 - ber) ** 20))
arq_bits_avg = (16 + 1) / (1 - p_err_16)     # assuming 1 parity bit or 16+CRC; with 1-bit parity = 17 bits
arq_delay_avg = (p_err_16 / (1 - p_err_16)) * 40.0
fec_delay_avg = (p_gt1_21 / (1 - p_gt1_21)) * 40.0
print(f"  Hamming(21,16) FEC : 21 bits/reading | >=2-bit fail prob = {p_gt1_21*100:.4f}% | avg extra delay = {fec_delay_avg:.4f} ms")
print(f"  ARQ (16b + parity) : {arq_bits_avg:.2f} bits/reading | frame error prob = {p_err_16*100:.2f}% | avg extra delay = {arq_delay_avg:.3f} ms (tail = 40 ms)")
print("  Verdict: FEC suits noisy real-time radio/video/5G links because it eliminates 40 ms retransmission stalls.")
