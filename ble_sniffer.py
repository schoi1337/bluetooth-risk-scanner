# ble_sniffer.py
# This script scans for nearby BLE devices and analyzes their risk using vendor information, RSSI, and CVE data.

import asyncio
from bleak import BleakScanner
from vendor_lookup import lookup_vendor_from_mac
from risk_analyzer import analyze_device_risk

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

if __name__ == "__main__":
    scanned = asyncio.run(scan_devices(timeout=15, min_rssi=-80))
    for dev in scanned:
        print(dev)
