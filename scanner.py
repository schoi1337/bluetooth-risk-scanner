# scanner.py

import asyncio
import json
import os

from utils.ble_scanner import scan_ble_devices
from utils.risk_analyzer import analyze_device_risk

OUTPUT_DIR = "results"
OUTPUT_FILE = "scan_results.json"

async def scan_and_analyze():
    """Scan BLE devices and analyze their risks."""
    print("[*] Scanning for BLE devices...")
    devices = await scan_ble_devices()

    if not devices:
        print("[!] No BLE devices found.")
        return

    print(f"[*] {len(devices)} devices found. Analyzing risks...")

    analyzed_results = []
    for device in devices:
        risk_info = analyze_device_risk(device)
        analyzed_results.append(risk_info)

    save_results(analyzed_results)
    print(f"[*] Scan and analysis complete. Results saved to {os.path.join(OUTPUT_DIR, OUTPUT_FILE)}")

def save_results(results):
    """Save scan results to a JSON file."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    asyncio.run(scan_and_analyze())
