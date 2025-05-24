import argparse
import asyncio
import json
from ble_sniffer import scan_ble_devices
from scoring import enrich_devices_with_score
from report_generator import generate_html_report

# Define CLI arguments
parser = argparse.ArgumentParser(description="Bluetooth Risk Scanner CLI")

parser.add_argument('--scan', action='store_true', help='Scan BLE devices and save results')
parser.add_argument('--score', action='store_true', help='Score scanned devices based on risk')
parser.add_argument('--report', action='store_true', help='Generate an HTML risk report')
parser.add_argument('--all', action='store_true', help='Run full scan → score → report pipeline')

# BLE scanning options
parser.add_argument('--timeout', type=int, default=10, help='BLE scan duration in seconds (default: 10)')
parser.add_argument('--min-rssi', type=int, default=-100, help='Minimum RSSI threshold for device inclusion (default: -100)')

args = parser.parse_args()

# Run BLE scan
if args.scan:
    asyncio.run(scan_ble_devices(timeout=args.timeout, min_rssi=args.min_rssi))

# Run risk scoring
if args.score:
    try:
        with open("results.json", "r") as f:
            devices = json.load(f)
    except FileNotFoundError:
        print("[!] results.json not found. Please run --scan first.")
        exit(1)

    enriched = enrich_devices_with_score(devices)
    with open("results.json", "w") as f:
        json.dump(enriched, f, indent=2)

    print("[✓] Risk scoring complete. Results saved to results.json")

# Run report generation
if args.report:
    generate_html_report()

# Run full pipeline
if args.all:
    asyncio.run(scan_ble_devices(timeout=args.timeout, min_rssi=args.min_rssi))

    try:
        with open("results.json", "r") as f:
            devices = json.load(f)
    except FileNotFoundError:
        print("[!] results.json not found after scan.")
        exit(1)

    enriched = enrich_devices_with_score(devices)
    with open("results.json", "w") as f:
        json.dump(enriched, f, indent=2)

    print("[✓] Risk scoring complete. Results saved to results.json")

    generate_html_report()
