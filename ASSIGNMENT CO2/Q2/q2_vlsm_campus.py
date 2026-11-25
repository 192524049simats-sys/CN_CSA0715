"""Variable-length subnetting (VLSM) of 192.168.10.0/24 for a college campus."""
import ipaddress
import math


def to_int(ip):
    a, b, c, d = map(int, ip.split("."))
    return (a << 24) | (b << 16) | (c << 8) | d


def to_ip(n):
    return ".".join(str((n >> s) & 255) for s in (24, 16, 8, 0))


def vlsm(base, needs):
    addr = to_int(base)
    for name, hosts in sorted(needs, key=lambda x: -x[1]):
        # TODO 1: Find the smallest block that holds hosts + 2 addresses (a power of
        # two), its prefix length 32 - log2(block), and print the network, prefix,
        # first and last usable host and broadcast address. Then move addr to the next
        # block
        bits = math.ceil(math.log2(hosts + 2))
        block = 1 << bits
        prefix = 32 - bits
        net = to_ip(addr)
        first = to_ip(addr + 1)
        last = to_ip(addr + block - 2)
        bcast = to_ip(addr + block - 1)
        print(f"{name:<10} {net}/{prefix}  hosts {first} - {last}  bcast {bcast}")
        addr += block
    return to_ip(addr)


needs = [("Labs", 100), ("Staff", 50), ("Library", 25), ("WAN link", 2)]
print("next free address:", vlsm("192.168.10.0", needs))

# --- Follow-up: ipaddress Verification, Equal-Size vs VLSM, Hostel Trap & Route Summarisation ---
print("\n--- Verification with Python ipaddress module ---")
parent = ipaddress.IPv4Network("192.168.10.0/24")
vlsm_nets = [
    ("Labs", ipaddress.IPv4Network("192.168.10.0/25")),
    ("Staff", ipaddress.IPv4Network("192.168.10.128/26")),
    ("Library", ipaddress.IPv4Network("192.168.10.192/27")),
    ("WAN link", ipaddress.IPv4Network("192.168.10.224/30")),
]
used = 0
for label, net in vlsm_nets:
    hosts_list = list(net.hosts())
    print(f"  {label:<10} {str(net):<18} mask={net.netmask} first={hosts_list[0]} last={hosts_list[-1]} bcast={net.broadcast_address} usable={len(hosts_list)}")
    used += net.num_addresses

print(f"\nEqual-size (FLSM) Comparison on 192.168.10.0/24:")
print("  - 4 equal /26 subnets give only 62 usable hosts each -> FAILS Labs (100 hosts)!")
print("  - /25 gives 126 usable hosts, but only 2 subnets exist in /24 -> FAILS 4-subnet requirement!")

print(f"\nHostel Trap (60 hosts added 6 months later):")
print(f"  - Remaining space in 192.168.10.0/24: 192.168.10.228 - 192.168.10.255 ({256 - used} addresses).")
print("  - 60 hosts needs /26 (64 addresses). Cannot fit without renumbering!")
print("  - Smallest change: Expand college block to 192.168.10.0/23 (adds 192.168.11.0/24) and assign 192.168.11.0/26 to Hostel (zero renumbering).")

print("\nRoute Summarisation:")
city_nets = [ipaddress.IPv4Network(f"172.16.{x}.0/24") for x in (8, 9, 10, 11)]
summary = list(ipaddress.collapse_addresses(city_nets))
print(f"  - Summary of 172.16.8.0/24 .. 172.16.11.0/24 : {summary[0]}")
bad_sum = ipaddress.IPv4Network("172.16.8.0/21")
leaked = [str(n) for n in bad_sum.subnets(new_prefix=24) if n not in city_nets and str(n) != "172.16.12.0/24"]
print(f"  - Erroneous 172.16.8.0/21 after adding .12.0/24 also advertises non-owned blocks: {leaked}")

print("\n--- Alternative Concept Analysis: Smallest-First VLSM Allocation ---")
cur = to_int("192.168.10.0")
for name, hosts in sorted(needs, key=lambda x: x[1]):
    bits = math.ceil(math.log2(hosts + 2))
    block = 1 << bits
    aligned = (cur % block == 0)
    print(f"  {name:<10} (needs {block:3d} IPs, /{32-bits}) at {to_ip(cur)} -> aligned={aligned}")
    cur += block
print("  Result: Smallest-first leaves Library/Staff/Labs misaligned (e.g. /25 cannot start at .100!), causing overlaps or wasted gaps.")
