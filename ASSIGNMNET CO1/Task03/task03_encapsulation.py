"""How data is wrapped by each layer at the sender and unwrapped at the receiver."""

LAYERS = [("Application", "HTTP"), ("Transport", "TCP"), ("Network", "IP"),
          ("Data link", "ETH")]


def send(message):
    pdu = message
    for layer, tag in LAYERS:
        # TODO 1: Wrap pdu with this layer's header "[tag|" and, for the data link layer
        # only, also a trailer "|FCS]"; for other layers close with "]". Print the
        # layer name and the size of the new PDU
        if tag == "ETH":
            pdu = f"[{tag}|{pdu}|FCS]"
        else:
            pdu = f"[{tag}|{pdu}]"
        print(f"{layer:<12} adds {tag:<4} -> {len(pdu)} bytes")
    return pdu


def receive(frame):
    pdu = frame
    for layer, tag in reversed(LAYERS):
        head = "[" + tag + "|"
        tail = "|FCS]" if tag == "ETH" else "]"
        assert pdu.startswith(head) and pdu.endswith(tail), f"{layer}: bad header"
        pdu = pdu[len(head):-len(tail)]
    return pdu


frame = send("GET /results")
print("on the wire:", frame)
print("delivered  :", receive(frame))
print(f"overhead   : {len(frame) - len('GET /results')} bytes for 12 bytes of data")

# --- Follow-up & Capture Analysis ---
print("\n--- Follow-up: 1,400-byte payload comparison ---")
big_msg = "A" * 1400
big_frame = send(big_msg)
small_ov = (len(frame) - 12) / len(frame) * 100
big_ov = (len(big_frame) - 1400) / len(big_frame) * 100
print(f"12-byte payload   : total {len(frame)} B, overhead 28 B ({small_ov:.2f}%)")
print(f"1400-byte payload : total {len(big_frame)} B, overhead 28 B ({big_ov:.2f}%)")

print("\n--- Captured Modbus Robot Frame Analysis ---")
print("  Line 1 (Ethernet II) -> Layer 2 (Data Link), PDU: Frame, 14B hdr + 4B FCS = 18B")
print("  Line 2 (IPv4)        -> Layer 3 (Network),   PDU: Packet, 20B hdr, TTL 64 -> 61 => 3 routers crossed")
print("  Line 3 (TCP)         -> Layer 4 (Transport), PDU: Segment, 20B hdr (Src 51522 -> Dst 502 Modbus)")
print("  Line 4 (Data)        -> Layer 7 (App),       PDU: Data/Message, 12B payload")
print(f"  Wire size (12B cmd)  : {14+20+20+12+4} bytes | Overhead = 58/70 = {58/70*100:.2f}%")
print(f"  Wire size (1400B cam): {14+20+20+1400+4} bytes | Overhead = 58/1458 = {58/1458*100:.2f}%")
print("  Fault mapping        : (a) Wrong MAC -> L2 Data Link; (b) TTL=0 -> L3 Network; (c) Port closed -> L4 Transport")

# Alternative Concept Analysis: Direct Ethernet (EtherType 0x8892)
print("\n--- Alternative Concept: Raw Ethernet (EtherType 0x8892, no IP/TCP) ---")
# Ethernet min frame on wire is 64B (plus 20B IFG+preamble = 84B), or without padding 30B vs 70B
saved_bytes = 20 + 20  # 20B IPv4 + 20B TCP
# At 100 Mbps, 70B frame (+20B preamble/IFG = 90B = 720 bits) vs min 64B padded (+20B = 84B = 672 bits)
# Pure serialization comparison: 70B (560 bits) vs 30B logical / 64B min Ethernet
fps_with_ip_tcp = 100_000_000 / (70 * 8)
fps_without_ip_tcp_unpadded = 100_000_000 / (30 * 8)
fps_without_ip_tcp_min64 = 100_000_000 / (64 * 8)
print(f"  Header bytes saved per command        : {saved_bytes} bytes (20B IP + 20B TCP)")
print(f"  Logical wire size                     : 70 B -> 30 B (padded to 64 B IEEE 802.3 min frame)")
print(f"  Commands/sec freed (100 Mbps, 70B->64B): {fps_without_ip_tcp_min64 - fps_with_ip_tcp:,.0f} cmd/s (or {fps_without_ip_tcp_unpadded - fps_with_ip_tcp:,.0f} cmd/s unpadded)")
print("  Lost by dropping IP/TCP               : No L3 routing across subnets/plants, no congestion/flow control, no TCP ordering.")
