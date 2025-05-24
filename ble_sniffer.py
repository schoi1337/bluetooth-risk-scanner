# ble_sniffer.py
# This script scans for nearby BLE devices or uses test mode data,
# and analyzes their risk using vendor information, RSSI, and CVE data.

import asyncio
import argparse
import json
from pathlib import Path
from bleak import BleakScanner
from vendor_lookup import lookup_vendor_from_mac
from risk_analyzer import analyze_device_risk
from report_generator import save_json_report, save_html_report

async def scan_devices(timeout=10, min_rssi=-100):
    """
    Scan nearby BLE devices for a specified timeout and filter by RSSI.
    """
    print(f"[*] Scanning for {timeout} seconds (min RSSI: {min_rssi})...")
    devices = await BleakScanner.discover(timeout=timeout)

    results = []
    for d in devices:
        if d.rssi < min_rssi:
            continue  # Ignore weak signal devices

        address = d.address
        name = d.name or "Unknown"
        rssi = d.rssi
        vendor = lookup_vendor_from_mac(address)

        device_info = {
            "address": address,
            "name": name,
            "rssi": rssi,
            "vendor": vendor
        }

        # Analyze risk using RSSI and CVE info
        analyzed = analyze_device_risk(device_info)
        results.append(analyzed)

    return results

def load_test_devices():
    """
    Load test devices from predefined JSON or use inline sample data.
    """
    test_data_path = Path("test/sample_devices.json")
    if test_data_path.exists():
        with open(test_data_path) as f:
            return json.load(f)
    else:
        print("[!] sample_devices.json not found, using inline dummy data")
        return [
            {
                "address": "D7:58:AA:11:22:33",
                "name": "SmartLock",
                "rssi": -55,
                "vendor": "Samsung"
            },
            {
                "address": "00:11:22:33:44:55",
                "name": "UnknownDevice",
                "rssi": -85,
                "vendor": "Unknown"
            }
        ]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bluetooth Risk Scanner")
    parser.add_argument("--timeout", type=int, default=15, help="Scan timeout in seconds")
    parser.add_argument("--min-rssi", type=int, default=-100, help="Minimum RSSI threshold")
    parser.add_argument("--test-mode", action="store_true", help="Run in test mode without BLE scan")
    args = parser.parse_args()

    if args.test_mode:
        print("[*] Running in TEST MODE")
        raw_devices = load_test_devices()
        analyzed_devices = [analyze_device_risk(dev) for dev in raw_devices]
    else:
        raw_devices = asyncio.run(scan_devices(args.timeout, args.min_rssi))
        analyzed_devices = raw_devices

    save_json_report(analyzed_devices)
    save_html_report(analyzed_devices)
