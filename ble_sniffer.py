import asyncio
from bleak import BleakScanner
import json

RESULTS_FILE = "results.json"

# Perform BLE scan with timeout and RSSI filter
async def scan_ble_devices(timeout=10, min_rssi=-100):
    print(f"[i] Scanning for BLE devices (timeout={timeout}s, min_rssi={min_rssi} dBm)...")

    devices = await BleakScanner.discover(timeout=timeout)
    results = []

    for d in devices:
        rssi = d.rssi
        if rssi < min_rssi:
            continue  # Skip weak signal devices

        result = {
            "mac": d.address,
            "name": d.name or "Unknown",
            "rssi": rssi
        }

        # Placeholder: you may add vendor detection here
        from vendor_lookup import get_vendor
        result["vendor"] = get_vendor(d.address)

        results.append(result)

    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=2)

    print(f"[✓] Found {len(results)} device(s). Results saved to {RESULTS_FILE}")
