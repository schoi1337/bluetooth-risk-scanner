# src/ble_scanner.py
# Performs BLE scanning and returns nearby device information.

from bleak import BleakScanner
from src.vendor_lookup import lookup_vendor_from_mac
from src.risk_analyzer import analyze_device_risk

async def scan_devices(timeout=10, min_rssi=-100):
    """
    Scan nearby BLE devices using bleak and analyze their risk.
    Returns a list of analyzed device dictionaries.
    """
    print(f"[*] Scanning for {timeout} seconds (min RSSI: {min_rssi})...")
    devices = await BleakScanner.discover(timeout=timeout)

    results = []
    for d in devices:
        if d.rssi < min_rssi:
            continue  # Skip weak signals

        device_info = {
            "address": d.address,
            "name": d.name or "Unknown",
            "rssi": d.rssi,
            "vendor": lookup_vendor_from_mac(d.address)
        }

        analyzed = analyze_device_risk(device_info)
        results.append(analyzed)

    return results
