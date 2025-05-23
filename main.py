import argparse
import asyncio
from ble_sniffer import scan_ble_devices
from score_calculator import score_devices
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

# Run scan only
if args.scan:
    asyncio.run(scan_ble_devices(timeout=args.timeout, min_rssi=args.min_rssi))

# Run scoring only
if args.score:
    score_devices()

# Run report generation only
if args.report:
    generate_html_report()

# Run full pipeline
if args.all:
    asyncio.run(scan_ble_devices(timeout=args.timeout, min_rssi=args.min_rssi))
    score_devices()
    generate_html_report()
