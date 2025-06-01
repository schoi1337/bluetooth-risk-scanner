import sys
import os
import asyncio
from pathlib import Path

# Add src folder to Python module search path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from ble_scanner import scan_devices
from risk_analyzer import load_risk_weights, analyze_device_risk, analyze_privacy_risks
from vendor_lookup import lookup_vendor_from_mac as get_vendor_name
from behavior_tracker import check_mac_rotation, check_name_switching, save_device_profile
from report_generator import save_html_report, save_json_report


def convert_bytes_to_hex(obj):
    """
    Recursively convert bytes objects to hex strings for JSON serialization.
    """
    if isinstance(obj, dict):
        return {k: convert_bytes_to_hex(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_bytes_to_hex(i) for i in obj]
    elif isinstance(obj, bytes):
        return obj.hex()
    else:
        return obj


async def run_scan(timeout=10, json_only=False, html_only=False, offline=None):
    """
    Core scan and analysis function.
    If offline is set, analyze the given JSON file instead of scanning.
    """
    weights = load_risk_weights()
    enriched_devices = []

    if offline:
        import json
        with open(offline, "r", encoding="utf-8") as f:
            devices_raw = json.load(f)
        # Assume devices_raw is already enriched JSON data
        enriched_devices = devices_raw
    else:
        devices_raw = await scan_devices(return_advertisement=True, timeout=timeout)

        # Remove duplicates by MAC address
        unique_devices = {}
        for device_info, advertisement_data in devices_raw:
            mac = device_info.address
            if mac not in unique_devices:
                unique_devices[mac] = (device_info, advertisement_data)

        for device_info, advertisement_data in unique_devices.values():
            mac = device_info.address
            name = device_info.name or "Unknown"
            rssi = advertisement_data.rssi
            manufacturer_data = advertisement_data.manufacturer_data

            vendor_name = get_vendor_name(mac)

            dev = {
                "mac": mac,
                "name": name,
                "rssi": rssi,
                "vendor_name": vendor_name,
                "mac_randomized": False,
                "manufacturer_data": manufacturer_data
            }

            score, reasons = analyze_device_risk(dev, weights)
            dev["score"] = score
            dev["risk_reasons"] = reasons
            dev["privacy_risks"] = analyze_privacy_risks(dev)

            rotating_mac = check_mac_rotation(dev)
            name_switch = check_name_switching(dev)

            anomalies = []
            if rotating_mac:
                anomalies.append("Rotating MAC detected")
            if name_switch:
                anomalies.append("Name switching detected")

            dev["anomaly"] = ", ".join(anomalies) if anomalies else "Normal"

            save_device_profile(dev)
            enriched_devices.append(dev)

    # Clean bytes for serialization
    cleaned_devices = convert_bytes_to_hex(enriched_devices)

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    if not json_only:
        save_html_report(cleaned_devices, output_path=output_dir / "report.html")
        print(f"[INFO] HTML report saved to {output_dir / 'report.html'}")

    if not html_only:
        save_json_report(cleaned_devices, output_path=output_dir / "scan_report.json")
        print(f"[INFO] JSON report saved to {output_dir / 'scan_report.json'}")
