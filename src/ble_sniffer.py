import asyncio
from bleak import BleakScanner

async def scan_ble_devices(timeout=10, min_rssi=-100):
    print(f"[*] Scanning for BLE devices (timeout={timeout}s, min_rssi={min_rssi})...")
    devices = []

    # Callback function to process each detected BLE device
    def detection_callback(device, advertisement_data):
        if advertisement_data.rssi < min_rssi:
            return
        devices.append({
            "name": device.name or "Unknown",
            "mac_address": device.address,
            "rssi": advertisement_data.rssi,
            "vendor": "Unknown"  # Placeholder; will be enriched later
        })

    # Register the detection callback and start scanning
    scanner = BleakScanner(detection_callback=detection_callback)
    await scanner.start()
    await asyncio.sleep(timeout)
    await scanner.stop()

    return devices

# For direct testing of this module
if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout", type=int, default=10, help="Scanning timeout in seconds")
    parser.add_argument("--min-rssi", type=int, default=-100, help="Minimum RSSI threshold")
    args = parser.parse_args()

    results = asyncio.run(scan_ble_devices(args.timeout, args.min_rssi))
    print(json.dumps(results, indent=2))
