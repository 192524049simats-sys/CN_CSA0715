"""Execute all CO5 tasks (TaskA1-A5, TaskB1-B4), capture logs, and generate dark-mode screenshots."""
import os
import subprocess
import sys

TOOLS_DIR = r"C:\Users\19252\.gemini\antigravity\scratch\tools"
sys.path.insert(0, TOOLS_DIR)
from render_screenshot import render_terminal_png

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SS_DIR = os.path.join(BASE_DIR, "output_ss")

TASKS = [
    ("TaskA1", "taska1_delay_bdp.py"),
    ("TaskA2", "taska2_app_protocols.py"),
    ("TaskA3", "taska3_p2p_voip.py"),
    ("TaskA4", "taska4_firewall_tls.py"),
    ("TaskA5", "taska5_dos_protection.py"),
    ("TaskB1", "taskb1_real_network.py"),
    ("TaskB2", "taskb2_varying_sim.py"),
    ("TaskB3", "taskb3_stress_attack.py"),
    ("TaskB4", "taskb4_final_decision.py"),
]


def main():
    os.makedirs(SS_DIR, exist_ok=True)
    py = sys.executable
    for folder, script in TASKS:
        task_dir = os.path.join(BASE_DIR, folder)
        script_path = os.path.join(task_dir, script)
        res = subprocess.run([py, script_path], capture_output=True, text=True, timeout=90)
        if res.returncode != 0:
            raise RuntimeError(f"{folder}/{script} failed:\n{res.stderr}")
        prompt = f"PS C:\\CN_CSA0715\\ASSSIGNMENT CO5\\{folder}> python {script}\n"
        full_log = prompt + res.stdout
        log_path = os.path.join(task_dir, f"experiment_{folder.lower()}.log")
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(full_log)
        png_path = os.path.join(SS_DIR, f"{folder.lower()}_output.png")
        render_terminal_png(
            f"CSA0715 CO5 | {folder} — {script}",
            full_log,
            png_path,
        )
        print(f"[PASS] {folder}: log + screenshot written")


if __name__ == "__main__":
    main()
