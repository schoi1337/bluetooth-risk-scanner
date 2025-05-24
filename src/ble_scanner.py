# src/ble_scanner.py
# Performs BLE scanning using bleak.discover() and returns nearby device information.
# Intended for Ubertooth-compatible environments (limited advertisement data).

from bleak import BleakScanner
from src.vendor_lookup import lookup_vendor_from_mac
from src.risk_analyzer import analyze_device_risk

async def scan_devices(timeout=10, min_rssi=-100):
    """
    Scan nearby BLE devices using bleak.discover() and analyze their risk.
    Returns a list of analyzed device dictionaries.
    """
    devices = await BleakScanner.discover(timeout=timeout)

    results = []
    for d in devices:
        if d.rssi < min_rssi:
            continue  # Skip weak signals

        device_info = {
            "address": d.address,
            "name": d.name or "Unknown",
            "rssi": d.rssi,
            "vendor": lookup_vendor_from_mac(d.address),
            "uuids": [],  # Not available from discover()
            "manufacturer": "Unknown"  # Placeholder for compatibility
        }

        analyzed = analyze_device_risk(device_info)
        results.append(analyzed)

    return results
