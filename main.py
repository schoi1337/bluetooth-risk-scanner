# main.py

import argparse
import json
import os
from scoring import enrich_devices_with_score
from report_generator import generate_html_report

RESULTS_FILE = "results.json"

def load_devices():
    if not os.path.exists(RESULTS_FILE):
        print(f"[!] {RESULTS_FILE} not found.")
        return []
    with open(RESULTS_FILE, "r") as f:
        return json.load(f)

def save_devices(devices):
    with open(RESULTS_FILE, "w") as f:
        json.dump(devices, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description="Bluetooth Risk Scanner CLI")
    parser.add_argument("--scan", action="store_true", help="Run BLE scan and save results")
    parser.add_argument("--score", action="store_true", help="Calculate and update risk scores")
    parser.add_argument("--report", action="store_true", help="Generate HTML report")
    parser.add_argument("--all", action="store_true", help="Run full pipeline")

    args = parser.parse_args()

    if args.scan:
        print("[*] BLE scan not implemented. Load existing results.json instead.")
        # TODO: Replace this with real scan logic
        return

    if args.score or args.all:
        devices = load_devices()
        if not devices:
            return
        print("[*] Calculating risk scores...")
        devices = enrich_devices_with_score(devices)
        save_devices(devices)
        print("[✓] Scores updated.")

    if args.report or args.all:
        print("[*] Generating HTML report...")
        generate_html_report()
        print("[✓] Report generated: report.html")

if __name__ == "__main__":
    main()
