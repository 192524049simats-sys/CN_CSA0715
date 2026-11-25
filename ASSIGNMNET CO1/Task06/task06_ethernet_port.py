"""CO1 Task 6: Ethernet Port Report Diagnosis, MAC Addressing, Jumbo Frames & Live NIC Check."""
import subprocess


def main():
    print("=== CO1 TASK 6: ETHERNET PORT REPORT DIAGNOSIS ===")
    report = {
        "Speed": "100Mb/s",
        "Duplex": "Half",
        "Auto-negotiation": "off",
        "Link detected": "yes",
        "rx_errors": 2381,
        "late_collisions": 412,
        "crc_errors": 1907,
    }
    for k, v in report.items():
        print(f"  {k:<18}: {v}")

    print("\n1. Root Cause Diagnosis (Duplex Mismatch):")
    print("  - late_collisions (412) : Collision detected AFTER transmitting 512 bits (64B slot time);")
    print("    signature symptom of Half-Duplex PC receiving simultaneous frames from a Full-Duplex switch.")
    print("  - crc_errors (1907)     : Corrupted frames arriving mid-transmission or damaged by EMI.")
    print("  - Switch side           : Gigabit switch port set to Auto-negotiation defaults to Half-Duplex when")
    print("    parallel-detecting a forced 100M/Half PC, OR switch was forced Full-Duplex while PC is Half.")

    print("\n2. Corrective Configuration Commands:")
    print("  Linux   : sudo ethtool -s eth0 speed 1000 duplex full autoneg on")
    print("            (verify with: ethtool eth0 && ethtool -S eth0)")
    print("  Windows : Set-NetAdapterAdvancedProperty -Name 'Ethernet' -DisplayName 'Speed & Duplex' -DisplayValue 'Auto Negotiation'")

    print("\n3. MAC Address Analysis:")
    print("  - 01:00:5e:0a:01:02 -> GROUP (IPv4 Multicast) MAC: LSB of first byte (0x01) is 1,")
    print("    and 01:00:5e prefix maps IPv4 multicast (e.g. 224.10.1.2 / 234.10.1.2).")
    print("  - 3c:52:82:4e:11:07 -> First 3 bytes (3c:52:82) are the OUI identifying the NIC vendor (HP Inc.).")

    print("\n4. Jumbo Frames (9,000 bytes) for CCTV Storage Server:")
    print("  - Benefit: Cuts framing/interrupt overhead (6x fewer headers/IRQs for large sequential video writes).")
    print("  - Requirement: End-to-end MTU=9000 must be configured on server NIC, ALL switches in path, and storage NAS;")
    print("    otherwise frames are dropped or fragmented.")

    print("\n5. Alternative Concept Analysis: Industrial Switch Ring (MRP/RSTP) vs Star:")
    print("  - Ring (IEC 62439-2 MRP / Rapid Ring): Single cable cut recovers in <10-50 ms; ZERO devices lose connection.")
    print("  - Star of switches: Cut on uplink disconnects entire downstream switch (~1-30 s only if redundant STP link exists).")

    print("\n6. Live Host NIC Status Check (PowerShell Get-NetAdapter):")
    try:
        out = subprocess.check_output(
            ["powershell", "-NoProfile", "-Command",
             "Get-NetAdapter | Select-Object Name, Status, LinkSpeed, FullDuplex, MacAddress | Format-Table -AutoSize"],
            text=True, timeout=10
        )
        print(out.strip())
    except Exception as exc:
        print(f"  [Info] Live adapter check skipped: {exc}")


if __name__ == "__main__":
    main()
