# cli.py

import click
from scanner.ble_scanner import run_active_scan
from scanner.ble_sniffer import run_ubertooth_scan
from report.report_generator import generate_report
import json

@click.command()
@click.option("--method", type=click.Choice(["hci", "ubertooth"]), default="hci", help="Scan method to use")
@click.option("--duration", default=30, help="Scan duration in seconds")
def main(method, duration):
    if method == "hci":
        print("[*] Running HCI (BLE dongle) active scan...")
        devices = run_active_scan(duration)
    else:
        print("[*] Running Ubertooth passive scan...")
        devices = run_ubertooth_scan(duration)

    with open("scan_results.json", "w") as f:
        json.dump(devices, f, indent=2)

    print(f"[✓] {len(devices)} devices saved to scan_results.json")
    generate_report("scan_results.json")

if __name__ == "__main__":
    main()
