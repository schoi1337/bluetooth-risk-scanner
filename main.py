# main.py

import json
import os
from src.cve_checker import load_ble_cve_db, find_cves_for_device
from src.report_generator import save_html_report, save_json_report
from src.vendor_lookup import lookup_vendor_name
from bleak import BleakScanner

async def scan_ble_devices(timeout=10):
    """
    Scan for BLE devices using bleak and return a list of device info dicts.
    """
    found = await BleakScanner.discover(timeout=timeout)
    devices = []
    for d in found:
        vendor = lookup_vendor_name(d.address) if hasattr(d, "address") else "Unknown"
        devices.append({
            "name": d.name or "Unknown",
            "mac": d.address,
            "vendor_name": vendor,
            "risk_level": "Unknown",
            "score": 0,
            "recommendation": "TBD",
            "risk_reasons": [],
            "uuids": [],
            "anomaly": "None"
        })
    return devices

async def run_scan(timeout=10, json_only=False, html_only=False, offline=None):
    """
    Perform a BLE scan (or analyze offline JSON), match CVEs, and generate reports.
    """
    # Step 1: Load from offline file or scan
    if offline:
        if not os.path.exists(offline):
            print(f"[ERROR] Offline file '{offline}' not found.")
            return []
        with open(offline, "r", encoding="utf-8") as f:
            devices = json.load(f)
    else:
        devices = await scan_ble_devices(timeout=timeout)

    # Step 2: Load BLE CVE DB (all years)
    cve_db = []
    for year in [2020, 2021, 2022, 2023]:  # Add years as available
        cve_db += load_ble_cve_db(year)

    # Step 3: CVE auto-mapping for each device
    for dev in devices:
        vendor = dev.get("vendor_name")
        product = dev.get("name")
        dev["cve_summary"] = find_cves_for_device(vendor, product, cve_db)

    # Step 4: Save reports as requested
    if not html_only:
        save_json_report(devices, output_path="output/report.json")
    if not json_only:
        save_html_report(devices, output_path="output/report.html")

    return devices

# For manual testing (non-CLI)
if __name__ == "__main__":
    import asyncio
    asyncio.run(run_scan())
