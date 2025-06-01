import argparse
import asyncio
from src.ble_sniffer import scan_ble_devices
from src.risk_analyzer import load_risk_weights, analyze_device_risk, analyze_privacy_risks
from src.report_generator import save_html_report, save_json_report

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout", type=int, default=10, help="BLE scan timeout in seconds")
    parser.add_argument("--min-rssi", type=int, default=-100, help="Minimum RSSI to filter weak signals")
    args = parser.parse_args()

    print(f"\n🔍 Scanning for BLE devices (timeout={args.timeout}s, min_rssi={args.min_rssi})...\n")

    devices = await scan_ble_devices(args.timeout, args.min_rssi)
    count = len(devices)

    if count == 0:
        print("⚠️  No BLE devices found. Try again or reduce min_rssi threshold.\n")
        return

    print(f"📡 Found {count} BLE device(s).\n")

    # Load risk scoring weights
    weights = load_risk_weights()

    # Enrich each device with risk score, reason, and privacy risks
    for dev in devices:
        score, reasons = analyze_device_risk(dev, weights)
        dev["risk_score"] = score
        dev["risk_reason"] = ", ".join(reasons)
        dev["privacy_risks"] = analyze_privacy_risks(dev)

    # Save reports
    save_json_report(devices, "output/scan_report.json")
    save_html_report(devices, "output/scan_report.html")

if __name__ == "__main__":
    asyncio.run(main())
