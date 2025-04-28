import asyncio
import json
from utils.ble_scanner import scan_bluetooth_devices
from utils.risk_analyzer import check_vendor_risk
from utils.cve_checker import check_device_cve
from pathlib import Path

# Output directory for saving scan results
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

async def main():
    # Perform Bluetooth scan
    devices = await scan_bluetooth_devices()
    results = []

    # Analyze each scanned device
    for device in devices:
        risks = check_vendor_risk(device['name'])
        cves = check_device_cve(device['name'])
        device_info = {
            'Name': device['name'],
            'MAC': device['address'],
            'RSSI': device['rssi'],
            'Risks': risks,
            'CVEs': [{'id': cve[0], 'description': cve[1]} for cve in cves]
        }
        results.append(device_info)

    # Display results in the terminal
    print("\nScan Results:\n")
    for d in results:
        print(f"- {d['Name']} ({d['MAC']}) RSSI: {d['RSSI']} dBm")
        if d['Risks']:
            print(f"  ⚠️ Risks: {', '.join(d['Risks'])}")
        if d['CVEs']:
            print(f"  🛡️ CVEs: {', '.join([c['id'] for c in d['CVEs']])}")

    # Save results to a JSON file
    with open(OUTPUT_DIR / "scan_results.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4)

if __name__ == "__main__":
    asyncio.run(main())
