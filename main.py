import argparse
import asyncio
import json
from src.ble_sniffer import scan_ble_devices
from scoring import enrich_devices_with_score
from src.report_generator import generate_html_report

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout", type=int, default=10, help="BLE scan timeout in seconds")
    parser.add_argument("--min-rssi", type=int, default=-100, help="Minimum RSSI to filter weak signals")
    args = parser.parse_args()

    # Scan BLE devices
    devices = await scan_ble_devices(args.timeout, args.min_rssi)

    # Enrich with risk score
    enriched_devices = enrich_devices_with_score(devices)

    # Save reports
    with open("results/scan_report.json", "w") as f:
        json.dump(enriched_devices, f, indent=2)
    generate_html_report(enriched_devices, "results/scan_report.html")

    print("[✓] JSON and HTML reports saved to results/")

if __name__ == "__main__":
    asyncio.run(main())
