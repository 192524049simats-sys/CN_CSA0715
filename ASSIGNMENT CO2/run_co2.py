"""Execute all CO2 tasks (Q1-Q7), capture logs, and generate dark-mode terminal screenshots."""
import os
import subprocess
import sys

TOOLS_DIR = r"C:\Users\19252\.gemini\antigravity\scratch\tools"
sys.path.insert(0, TOOLS_DIR)
from render_screenshot import render_terminal_png

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SS_DIR = os.path.join(BASE_DIR, "output_ss")

TASKS = [
    ("Q1", "q1_address_audit.py"),
    ("Q2", "q2_vlsm_campus.py"),
    ("Q3", "q3_longest_prefix_static.py"),
    ("Q4", "q4_bellman_ford.py"),
    ("Q5", "q5_ospf_dijkstra.py"),
    ("Q6", "q6_ipv6_sdn.py"),
    ("Q7", "q7_redesign_challenge.py"),
]


def main():
    os.makedirs(SS_DIR, exist_ok=True)
    py = sys.executable
    for folder, script in TASKS:
        task_dir = os.path.join(BASE_DIR, folder)
        script_path = os.path.join(task_dir, script)
        res = subprocess.run([py, script_path], capture_output=True, text=True, timeout=60)
        if res.returncode != 0:
            raise RuntimeError(f"{folder}/{script} failed:\n{res.stderr}")
        prompt = f"PS C:\\CN_CSA0715\\ASSIGNMENT CO2\\{folder}> python {script}\n"
        full_log = prompt + res.stdout
        log_path = os.path.join(task_dir, f"experiment_{folder.lower()}.log")
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(full_log)
        png_path = os.path.join(SS_DIR, f"{folder.lower()}_output.png")
        render_terminal_png(
            f"CSA0715 CO2 | {folder} — {script}",
            full_log,
            png_path,
        )
        print(f"[PASS] {folder}: log + screenshot written")


if __name__ == "__main__":
    main()
