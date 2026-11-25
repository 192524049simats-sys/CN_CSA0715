"""CO5 Task A5: SYN-Flood Sizing, SYN Cookies, DNS Amplification & DDoS Protection Plan."""


def main():
    print("=== CO5 TASK A5: HOW EASY IS IT TO TAKE THE SITE DOWN? ===")
    backlog = 1024
    timeout_s = 60
    syn_per_s = backlog / timeout_s

    print("A5.1 — SYN Flood & DNS Amplification:")
    print(f"  - Backlog = {backlog} half-open connections | Hold time = {timeout_s} s")
    print(f"  - Attack rate to exhaust server = {backlog} / {timeout_s} = {syn_per_s:.2f} SYN packets/sec (~18 SYN/s!)")
    print("  - How SYN cookies fix it: Server computes cryptographic ISN = hash(5-tuple, secret, MSS) and drops half-open")
    print("    state; TCB memory is allocated ONLY when client returns a valid ACK (so queue never fills).")
    print("  - Why DNS amplification is hard to block at victim: Attackers spoof victim's IP to open resolvers ->")
    print("    50-byte queries reflect 3,000+ byte ANY/TXT replies (50-70x amplification) that saturate the victim's")
    print("    access pipe BEFORE packets even reach the victim's firewall.")

    print("\nA5.2 — Layered Protection Plan:")
    print("  - SYN Flood         -> Enable TCP SYN Cookies on OS/load balancer + SYN proxy.")
    print("  - DNS Amplification -> Upstream Anycast Scrubbing Service / ISP BGP FlowSpec (drops junk before access link).")
    print("  - L7 HTTP Flood     -> CDN (offloads static/recorded video) + WAF / IP rate limiting.")

    print("\n--- Alternative Concept Analysis: Buying 4x Server Capacity ---")
    cap_4x = 4 * syn_per_s
    print(f"  - 4x servers absorb only 4 x {syn_per_s:.2f} = {cap_4x:.2f} SYN packets/sec (~69 SYN/s).")
    print("  - Verdict: NOT realistic — a single laptop or small botnet easily exceeds 100,000+ SYN/s and saturates the WAN link.")


if __name__ == "__main__":
    main()
