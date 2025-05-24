import argparse
import asyncio
from src.ble_sniffer import scan_ble_devices
from src.risk_analyzer import enrich_devices_with_score
from src.report_generator import save_html_report, save_json_report

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout", type=int, default=10, help="BLE scan timeout in seconds")
    parser.add_argument("--min-rssi", type=int, default=-100, help="Minimum RSSI to filter weak signals")
    args = parser.parse_args()

    print(f"\n🔍 [*] Scanning for BLE devices (timeout={args.timeout}s, min_rssi={args.min_rssi})...\n")

    devices = await scan_ble_devices(args.timeout, args.min_rssi)
    count = len(devices)

    if count == 0:
        print("⚠️  No BLE devices found. Try again or reduce min_rssi threshold.\n")
    else:
        print(f"📡 Found {count} BLE device(s).\n")

    enriched_devices = enrich_devices_with_score(devices)

    save_json_report(enriched_devices, "output/scan_report.json")
    save_html_report(enriched_devices, "output/scan_report.html")

if __name__ == "__main__":
    asyncio.run(main())
