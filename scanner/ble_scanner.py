from bleak import BleakScanner

async def scan_bluetooth_devices():
    """Scan nearby Bluetooth devices and return basic info."""
    devices = await BleakScanner.discover()
    results = []
    for d in devices:
        results.append({
            'name': d.name or 'Unknown',
            'address': d.address,
            'rssi': d.rssi
        })
    return results
