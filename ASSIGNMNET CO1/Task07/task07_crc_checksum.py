"""CRC error detection for frames sent between two switches."""


def mod2_div(dividend, divisor):
    """Return the remainder of modulo-2 (XOR) division of two bit strings."""
    rem = list(dividend)
    for i in range(len(dividend) - len(divisor) + 1):
        # TODO 1: If the current leading bit rem[i] is 1, XOR the divisor into rem
        # starting at position i
        if rem[i] == "1":
            for j in range(len(divisor)):
                rem[i + j] = "0" if rem[i + j] == divisor[j] else "1"
    return "".join(rem[-(len(divisor) - 1):])


def encode(data, gen):
    crc = mod2_div(data + "0" * (len(gen) - 1), gen)
    return data + crc


def check(frame, gen):
    return set(mod2_div(frame, gen)) == {"0"}


GEN = "1011"                                # x^3 + x + 1
frame = encode("1101011011", GEN)
print("transmitted:", frame)
print("no error   :", check(frame, GEN))
bad = frame[:4] + ("1" if frame[4] == "0" else "0") + frame[5:]
print("1-bit error:", check(bad, GEN))
burst = frame[:2] + "".join("1" if b == "0" else "0" for b in frame[2:5]) + frame[5:]
print("3-bit burst:", check(burst, GEN))

# --- Follow-up Verification & Error Analysis ---
print("\n--- Follow-up: Received frame 1101011011101 ---")
rx_test = "1101011011101"
rem_test = mod2_div(rx_test, GEN)
print(f"  Remainder of {rx_test} / {GEN} = {rem_test} -> {'ACCEPTED' if check(rx_test, GEN) else 'REJECTED'}")

# Undetected error pattern (any multiple of generator 1011, e.g., 1011000000000)
err_pattern = "1011" + "0" * (len(frame) - 4)
undetected = "".join("1" if a != b else "0" for a, b in zip(frame, err_pattern))
print(f"  Undetectable error E(x)=x^3+x+1 ({err_pattern}) -> check={check(undetected, GEN)} (MISSED!)")
print("  Max guaranteed burst detection for degree-3 CRC: <= 3 bits.")

# 2D Parity (4x4 block) and missed 4-bit corner error
block = ["1010", "0110", "1100", "0011"]
row_p = [str(r.count("1") % 2) for r in block]
col_p = [str(sum(int(block[r][c]) for r in range(4)) % 2) for c in range(4)]
print(f"\n--- 2D Even Parity (4x4 block {block}) ---")
print(f"  Row parities: {''.join(row_p)} | Col parities: {''.join(col_p)}")
print("  Missed 4-bit error: flipping bits (0,0), (0,3), (3,0), (3,3) keeps all row/col parities even.")

# Internet Checksum of 4500, 0073, 0000, 4000
words = [0x4500, 0x0073, 0x0000, 0x4000]
s = sum(words)
while s >> 16:
    s = (s & 0xFFFF) + (s >> 16)
chk = (~s) & 0xFFFF
print(f"\n--- Internet Checksum (4500, 0073, 0000, 4000) ---")
print(f"  Sum = 0x{sum(words):04X} | 1's Complement Checksum = 0x{chk:04X}")

# Alternative Concept Analysis: Even Parity vs CRC-3
print("\n--- Alternative Concept: Even Parity vs CRC-3 (1011) ---")
# 2-bit error E = 1011? No, 1011 has weight 3 (even parity catches odd weights!).
# Parity catches 3-bit error 1011000000000 (which CRC-3 misses!), whereas CRC-3 catches
# adjacent 2-bit error 1100000000000 (which even parity misses!).
e_2bit = "11" + "0" * (len(frame) - 2)
f_2bit = "".join("1" if a != b else "0" for a, b in zip(frame, e_2bit))
e_4bit_crc_miss = "1011" + "0" * (len(frame) - 4)  # 3-bit weight; 4-bit multiple: 1011 XOR 01011 = 11101 (weight 4)
e_4bit_mult = "11101" + "0" * (len(frame) - 5)     # (x+1)*(x^3+x+1) = x^4+x^3+x^2+1 -> 11101 (weight 4, divisible by 1011!)
f_4bit_mult = "".join("1" if a != b else "0" for a, b in zip(frame, e_4bit_mult))
print(f"  2-bit burst (110...0): CRC-3 check={check(f_2bit, GEN)} (CATCHES), Even-parity catches={e_2bit.count('1')%2==1} (MISSES)")
print(f"  4-bit mult (11101...): CRC-3 check={check(f_4bit_mult, GEN)} (MISSES), Even-parity catches={e_4bit_mult.count('1')%2==1} (MISSES)")
print(f"  3-bit mult (10110...): CRC-3 check={check(undetected, GEN)} (MISSES), Even-parity catches={err_pattern.count('1')%2==1} (CATCHES)")
