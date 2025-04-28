# utils/ble_scanner.py

from bleak import BleakScanner

async def scan_ble_devices(timeout=10):
    """
    Scan for nearby BLE devices.

    Args:
        timeout (int): Scanning duration in seconds.

    Returns:
        list: List of dictionaries containing device information.
    """
    devices = await BleakScanner.discover(timeout=timeout)
    device_list = []

    for d in devices:
        device_info = {
            "address": d.address,
            "name": d.name or "Unknown",
            "rssi": d.rssi,
            "uuids": d.metadata.get("uuids", [])
        }
        device_list.append(device_info)

    return device_list
