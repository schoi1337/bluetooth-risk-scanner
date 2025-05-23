# ble_sniffer.py

import asyncio
import json
from bleak import BleakScanner

RESULTS_FILE = "results.json"

# Optional: vendor lookup stub
OUI_VENDOR_MAP = {
    "D8:58:D7": "WELOCK",
    "A0:91:BC": "Xiaomi",
    "00:11:22": "Fitbit"
}

def get_vendor(mac):
    prefix = mac.upper()[:8]
    return OUI_VENDOR_MAP.get(prefix, "Unknown")

async def scan_ble_devices(timeout=10):
    print(f"[*] Scanning for {timeout} seconds...")
    devices = await BleakScanner.discover(timeout=timeout)
    
    results = []
    for d in devices:
        mac = d.address
        vendor = get_vendor(mac)
        rssi = d.rssi
        results.append({
            "mac": mac,
            "vendor": vendor,
            "rssi": rssi,
            "cve_list": []  # 아직 CVE 연동 안 했으므로 빈 리스트
        })

    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=2)
    print(f"[✓] Found {len(results)} devices. Results saved to {RESULTS_FILE}")

if __name__ == "__main__":
    asyncio.run(scan_ble_devices())
