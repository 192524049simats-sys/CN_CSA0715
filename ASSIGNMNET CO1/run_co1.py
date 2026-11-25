"""Execute all CO1 tasks (Task01-Task12), capture logs, and generate dark-mode terminal screenshots."""
import os
import subprocess
import sys

TOOLS_DIR = r"C:\Users\19252\.gemini\antigravity\scratch\tools"
sys.path.insert(0, TOOLS_DIR)
from render_screenshot import render_terminal_png

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SS_DIR = os.path.join(BASE_DIR, "output_ss")

TASKS = [
    ("Task01", "task01_traffic_sizing.py"),
    ("Task02", "task02_domains_diagram.py"),
    ("Task03", "task03_encapsulation.py"),
    ("Task04", "task04_nyquist_shannon.py"),
    ("Task05", "task05_agv_handover.py"),
    ("Task06", "task06_ethernet_port.py"),
    ("Task07", "task07_crc_checksum.py"),
    ("Task08", "task08_hamming.py"),
    ("Task09", "task09_sliding_window.py"),
    ("Task10", "task10_delay_measurements.py"),
    ("Task11", "task11_design_defence.py"),
    ("Task12", "task12_design_challenge.py"),
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
        prompt = f"PS C:\\CN_CSA0715\\ASSIGNMNET CO1\\{folder}> python {script}\n"
        full_log = prompt + res.stdout
        log_path = os.path.join(task_dir, f"experiment_{folder.lower()}.log")
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(full_log)
        png_path = os.path.join(SS_DIR, f"{folder.lower()}_output.png")
        render_terminal_png(
            f"CSA0715 CO1 | {folder} — {script}",
            full_log,
            png_path,
        )
        print(f"[PASS] {folder}: log + screenshot written")


if __name__ == "__main__":
    main()
