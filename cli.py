# cli.py

import argparse
import asyncio

from scanner import scan_and_analyze
from reporter import generate_report

def main():
    parser = argparse.ArgumentParser(description="Bluetooth Risk Scanner CLI")
    parser.add_argument("--scan", action="store_true", help="Scan BLE devices and analyze risks.")
    parser.add_argument("--report", action="store_true", help="Generate JSON and HTML reports.")

    args = parser.parse_args()

    if args.scan:
        asyncio.run(scan_and_analyze())

    if args.report:
        generate_report()

if __name__ == "__main__":
    main()
