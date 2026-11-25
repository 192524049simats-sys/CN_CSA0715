"""A stateless packet filter: the first matching rule decides (like iptables)."""

RULES = [   # (action, protocol, destination port or None for any, source prefix or None)
    ("allow", "tcp", 443, None),
    ("allow", "tcp", 22, "10.1."),
    ("deny", "tcp", 22, None),
    ("allow", "udp", 53, None),
]
DEFAULT = "deny"


def decide(proto, port, src):
    for action, p, dport, prefix in RULES:
        # TODO 1: A rule matches when its protocol equals proto, its port is None or
        # equals port, and its prefix is None or src starts with it. Return the action
        # of the first matching rule
        if p == proto and (dport is None or dport == port) and (prefix is None or src.startswith(prefix)):
            return action
    return DEFAULT


packets = [("tcp", 443, "49.37.2.8"), ("tcp", 22, "10.1.4.20"),
           ("tcp", 22, "49.37.2.8"), ("udp", 53, "10.1.4.20"),
           ("tcp", 80, "49.37.2.8"), ("icmp", None, "49.37.2.8")]
for pk in packets:
    print(f"{pk[0]:<5} {str(pk[1]):<5} from {pk[2]:<10} -> {decide(*pk)}")

# --- Follow-up: Swap Rules 2 and 3, Broken Rule Set Audit & TLS/WAF Analysis ---
print("\n--- Follow-up: Swapping Rules 2 and 3 (Shadowing Bug) ---")
RULES[1], RULES[2] = RULES[2], RULES[1]
for pk in packets:
    print(f"{pk[0]:<5} {str(pk[1]):<5} from {pk[2]:<10} -> {decide(*pk)}")
print("  Effect: ('deny', 'tcp', 22, None) now shadows ('allow', 'tcp', 22, '10.1.'), blocking admin SSH from 10.1.4.20!")

print("\n--- Audit of the Web Server's Original Rule Set ---")
print("  1 allow tcp any -> 443 | 2 allow tcp any -> 22 | 3 deny tcp any -> 22 | 4 allow tcp 10.1.0.0/16 -> 22")
print("  - Shadowed rules : Rules 3 and 4 can NEVER take effect because Rule 2 permits ALL TCP port 22.")
print("  - Security hole  : SSH (port 22) is exposed to the entire public Internet!")
print("  - Corrected order: Move Rule 4 (allow 10.1.0.0/16 -> 22) ABOVE Rule 3 (deny any -> 22) and delete Rule 2.")
print("  - Firewall types : Stateless inspects per-packet 5-tuple; Stateful tracks connection state/return traffic;")
print("                     Application Proxy terminates L7 (HTTP/DNS) to inspect payloads.")

print("\n--- A4.1 TLS/SSL on Cafe Wi-Fi ---")
print("  - Certificate proves server domain ownership/public key via trusted CA; Handshake agrees cipher suite & symmetric session keys.")
print("  - Attacker sees: Client/Server IPs, port 443, TLS SNI hostname, packet sizes/timing; CANNOT see URL paths, cookies, passwords, or HTML.")

print("\n--- Alternative Concept Analysis: Cloud WAF ---")
print("  - Stops L7 attacks packet filter misses: (1) SQL Injection / XSS payloads; (2) HTTP credential stuffing / L7 floods.")
print("  - Extra delay: ~5-25 ms TLS termination + inspection hop (offset by edge caching); YES, company needs WAF for public portal.")
