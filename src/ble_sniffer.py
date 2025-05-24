# src/ble_sniffer.py
# Scans BLE devices (or loads test data) and generates risk reports.

import argparse
import asyncio
import json
from pathlib import Path

from src.risk_analyzer import analyze_device_risk
from src.vendor_lookup import lookup_vendor_from_mac
from src.report_generator import save_json_report, save_html_report
from src.ble_scanner import scan_devices
from src.cve_checker import fetch_cves  # Used indirectly via analyzer


def load_test_devices():
    """Load predefined test-mode devices for offline testing."""
    test_data_path = Path("example_reports/sample_devices.json")
    if test_data_path.exists():
        with test_data_path.open() as f:
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


def main():
    """Main entry point for BLE scanning and report generation."""
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
