"""Execute all CO4 tasks (Task01-Task06), capture logs, and generate dark-mode terminal screenshots."""
import os
import subprocess
import sys

TOOLS_DIR = r"C:\Users\19252\.gemini\antigravity\scratch\tools"
sys.path.insert(0, TOOLS_DIR)
from render_screenshot import render_terminal_png

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SS_DIR = os.path.join(BASE_DIR, "output_ss")

TASKS = [
    ("Task01", "task01_office_redesign.py"),
    ("Task02", "task02_hospital_topologies.py"),
    ("Task03", "task03_cabling_bom.py"),
    ("Task04", "task04_aloha_wlan_wan.py"),
    ("Task05", "task05_vlans_acl.py"),
    ("Task06", "task06_university_campus.py"),
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
        prompt = f"PS C:\\CN_CSA0715\\ASSIGNMENT CO4\\{folder}> python {script}\n"
        full_log = prompt + res.stdout
        log_path = os.path.join(task_dir, f"experiment_{folder.lower()}.log")
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(full_log)
        png_path = os.path.join(SS_DIR, f"{folder.lower()}_output.png")
        render_terminal_png(
            f"CSA0715 CO4 | {folder} — {script}",
            full_log,
            png_path,
        )
        print(f"[PASS] {folder}: log + screenshot written")


if __name__ == "__main__":
    main()
