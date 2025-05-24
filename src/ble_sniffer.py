import asyncio
from bleak import BleakScanner
from src.mac_lookup import lookup_vendor

async def scan_ble_devices(timeout=10, min_rssi=-100):
    print(f"[*] Scanning for BLE devices (timeout={timeout}s, min_rssi={min_rssi})...")
    seen_macs = set()
    devices = []

    def detection_callback(device, advertisement_data):
        if advertisement_data.rssi < min_rssi:
            return
        if device.address in seen_macs:
            return  # Skip duplicate devices
        seen_macs.add(device.address)

        name = advertisement_data.local_name or device.name or "Unknown"
        vendor = lookup_vendor(device.address)

        devices.append({
            "name": name,
            "mac_address": device.address,
            "rssi": advertisement_data.rssi,
            "vendor": vendor,
            "uuids": advertisement_data.service_uuids or []
        })


    scanner = BleakScanner(detection_callback=detection_callback)
    await scanner.start()
    await asyncio.sleep(timeout)
    await scanner.stop()

    return devices
