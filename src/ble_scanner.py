import asyncio
from bleak import BleakScanner

# Async BLE scan function that returns both BLEDevice and AdvertisementData
async def scan_devices(timeout=10, min_rssi=-100, return_advertisement=False):
    found = []

    # Callback to process BLE advertisements
    def detection_callback(device, advertisement_data):
        # Skip weak signals
        if advertisement_data.rssi < min_rssi:
            return

        found.append((device, advertisement_data))

    scanner = BleakScanner(detection_callback=detection_callback)
    await scanner.start()
    await asyncio.sleep(timeout)
    await scanner.stop()

    return found if return_advertisement else [d[0] for d in found]
