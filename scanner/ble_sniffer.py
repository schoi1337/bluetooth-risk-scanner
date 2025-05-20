# scanner/ble_sniffer.py

import subprocess
import time
import json

from report.report_generator import generate_report
from utils.risk_database import evaluate_risk
from utils.oui_lookup import load_oui_database, lookup_vendor


def run_ubertooth_scan(duration=30):
    print("[*] Starting Ubertooth passive scan...")
    proc = subprocess.Popen(
        ["ubertooth-btle", "-n"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        bufsize=1,
        universal_newlines=True
    )

    discovered_devices = {}
    current_device = {}
    vendor_map = load_oui_database()
    start_time = time.time()

    try:
        for line in proc.stdout:
            line = line.strip()

            if "ADV_IND" in line:
                current_device = {}

            elif "AdvA:" in line:
                mac = line.split("AdvA:")[1].strip()
                current_device["mac"] = mac

            elif "Local Name:" in line:
                name = line.split("Local Name:")[1].strip()
                current_device["name"] = name

            elif "RSSI:" in line:
                rssi = line.split("RSSI:")[1].strip()
                current_device["rssi"] = rssi

                mac = current_device.get("mac", "")
                name = current_device.get("name", "Unknown")
                rssi = current_device.get("rssi", "")

                if mac not in discovered_devices:
                    risk = evaluate_risk(name, mac)
                    vendor = lookup_vendor(mac, vendor_map)
                    discovered_devices[mac] = {
                        "mac": mac,
                        "name": name,
                        "rssi": rssi,
                        "risk": risk,
                        "vendor": vendor,
                    }
                    print(f"[+] Found {mac} ({name}) - RSSI {rssi} → Risk: {risk} | Vendor: {vendor}")

            if time.time() - start_time > duration:
                break

    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user.")

    finally:
        proc.terminate()

    return list(discovered_devices.values())


if __name__ == "__main__":
    devices = run_ubertooth_scan(duration=30)

    with open("scan_results.json", "w") as f:
        json.dump(devices, f, indent=2)

    print(f"\n[*] Scan complete. {len(devices)} devices saved to scan_results.json.")

    generate_report("scan_results.json")
