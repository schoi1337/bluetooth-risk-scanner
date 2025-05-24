import asyncio
import json
from bleak import BleakScanner
from vendor_lookup import get_vendor

RESULTS_FILE = "results.json"

# Scan for BLE devices with timeout and RSSI threshold
async def scan_ble_devices(timeout=10, min_rssi=-100):
    print(f"[i] Scanning for BLE devices (timeout={timeout}s, min_rssi={min_rssi} dBm)...")

    devices = await BleakScanner.discover(timeout=timeout)
    results = []

    for d in devices:
        rssi = d.rssi
        if rssi < min_rssi:
            continue  # Skip weak signal devices

        mac = d.address
        name = d.name or ""

        result = {
            "mac": mac,
            "name": name,
            "rssi": rssi,
            "vendor": get_vendor(mac, name)  # ✅ name-based vendor inference
        }

        results.append(result)

    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=2)

    print(f"[✓] Found {len(results)} device(s). Results saved to {RESULTS_FILE}")
