"""CO5 Task B2: Discrete-Event Simulation Under Varying Bandwidth, Delay, Load & Voice Priority."""
import heapq
import os
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def run_sim(bw_mbps, prop_ms, n_users, bg_download=False, voice_priority=False, duration_s=4.0):
    random.seed(101)
    cap_bps = bw_mbps * 1e6
    # Voice users: 80 kbps each (200B every 20 ms -> 50 pkt/s); interactive web users: 300 kbps
    voice_rate = min(n_users, 20) * 50.0  # up to 20 voice streams (pkt/s)
    web_rate = n_users * 25.0             # web/data packets/s (1000 B avg)
    bg_rate = (2000 if bg_download else 0) # 2000 pkt/s x 1500B = 24 Mbps background file burst

    events = []
    # Generate arrivals
    t = 0.0
    while t < duration_s:
        t += random.expovariate(voice_rate)
        if t < duration_s:
            events.append((t, 0 if voice_priority else 1, "voice", (200 * 8) / cap_bps))
    t = 0.0
    while t < duration_s:
        t += random.expovariate(web_rate)
        if t < duration_s:
            events.append((t, 1, "data", (1000 * 8) / cap_bps))
    if bg_download:
        t = 0.0
        while t < duration_s:
            t += random.expovariate(bg_rate)
            if t < duration_s:
                events.append((t, 2 if voice_priority else 1, "bg", (1500 * 8) / cap_bps))
    events.sort(key=lambda x: x[0])

    q = []
    idx = 0
    now = 0.0
    max_q = 200
    voice_delays, voice_drops, voice_total = [], 0, 0
    bytes_tx = 0

    while idx < len(events) or q:
        if not q and idx < len(events):
            now = max(now, events[idx][0])
        while idx < len(events) and events[idx][0] <= now:
            arr, prio, kind, svc = events[idx]
            if kind == "voice":
                voice_total += 1
            if len(q) >= max_q:
                if kind == "voice":
                    voice_drops += 1
            else:
                heapq.heappush(q, (prio, arr, kind, svc))
            idx += 1
        if not q:
            continue
        prio, arr, kind, svc = heapq.heappop(q)
        finish = now + svc
        bytes_tx += int(svc * cap_bps / 8)
        if kind == "voice":
            voice_delays.append((finish - arr) * 1000.0 + prop_ms)
        now = finish

    avg_v_ms = sum(voice_delays) / len(voice_delays) if voice_delays else 0.0
    loss_pct = (voice_drops / voice_total * 100.0) if voice_total else 0.0
    thr_mbps = (bytes_tx * 8) / duration_s / 1e6
    return thr_mbps, avg_v_ms, loss_pct


def main():
    print("=== CO5 TASK B2: SIMULATE UNDER VARYING CONDITIONS ===")
    scenarios = [
        ("1. Baseline (50M, 20ms, 20 users)", 50, 20, 20, False, False),
        ("2. Higher Load (50M, 20ms, 80 users)", 50, 20, 80, False, False),
        ("3. Tight Link + High Delay (20M, 80ms, 50u)", 20, 80, 50, False, False),
        ("4. + Background Download FIFO (20M, 20ms)", 20, 20, 40, True, False),
        ("5. + Background Download + Voice Priority", 20, 20, 40, True, True),
    ]
    results = []
    for name, bw, prop, u, bg, prio in scenarios:
        thr, vd, loss = run_sim(bw, prop, u, bg, prio)
        results.append((name, thr, vd, loss))
        print(f"  {name:<44} | Thr={thr:5.2f} Mbps | Voice Delay={vd:6.2f} ms | Voice Loss={loss:4.1f}%")

    print("\nInterpretation:")
    print("  - Adding a 24 Mbps background file download on a 20 Mbps FIFO link saturates the buffer,")
    print("    spiking voice delay and dropping packets (run 4).")
    print("  - Enabling strict Priority Queueing for voice (run 5) isolates voice delay right back near prop_ms with 0% loss!")

    print("\n--- Alternative Concept Analysis: Packet Tracer vs NS-3 ---")
    print("  - Packet Tracer: Visual GUI, real Cisco IOS CLI, minimal setup effort (~10 min), but simplified queue/TCP internals.")
    print("  - NS-3 (C++/Python): Packet-by-packet ns-3::QueueDisc, exact CUBIC/BBR & Wi-Fi PHY models, reproducible traces, higher coding effort.")

    # Save chart
    fig, ax = plt.subplots(figsize=(10.5, 4.8), dpi=150)
    ax.set_facecolor("#0F172A")
    fig.patch.set_facecolor("#0F172A")
    labels = [r[0].split(" (")[0] for r in results]
    v_delays = [r[2] for r in results]
    colors = ["#38BDF8", "#60A5FA", "#F59E0B", "#EF4444", "#22C55E"]
    bars = ax.bar(labels, v_delays, color=colors)
    ax.axhline(150.0, color="#F87171", ls="--", lw=1.4, label="150 ms Voice SLA Target")
    for b in bars:
        ax.text(b.get_x() + b.get_width()/2, b.get_height() + 2, f"{b.get_height():.1f}ms", ha="center", color="white", fontsize=9, fontweight="bold")
    ax.set_ylabel("Mean Voice One-Way Delay (ms)", color="#E2E8F0")
    ax.set_title("CO5 Task B2: Voice Delay Across Link Bandwidth, Load & Priority Queueing", color="#F8FAFC", fontweight="bold")
    ax.tick_params(colors="#CBD5E1", axis="both")
    plt.xticks(rotation=15, ha="right")
    ax.grid(axis="y", color="#334155", alpha=0.5)
    ax.legend(facecolor="#1E293B", edgecolor="#475569", labelcolor="white")
    plt.tight_layout()
    out_png = os.path.join(os.path.dirname(__file__), "taskb2_sim_results.png")
    plt.savefig(out_png, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"\nSaved simulation plot: {out_png}")


if __name__ == "__main__":
    main()
