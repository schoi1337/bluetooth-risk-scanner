# generate_sample_report.py

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from report_generator import save_html_report

# Sample anonymized BLE scan results
devices = [
    {
        "name": "Fitness Band",
        "mac": "AA:BB:CC:DD:EE:01",
        "vendor": "GenericVendor",
        "rssi": -60,
        "risk_score": 45,
        "risk_level": "Medium",
        "recommendation": "Review BLE visibility settings",
        "risk_reason": "Static MAC and moderate signal strength",
        "uuids": ["0000180d-0000-1000-8000-00805f9b34fb"]
    },
    {
        "name": "Smart Lock",
        "mac": "AA:BB:CC:DD:EE:02",
        "vendor": "SmartHomeCo",
        "rssi": -40,
        "risk_score": 88,
        "risk_level": "High",
        "recommendation": "Disable BLE if not actively used",
        "risk_reason": "Static MAC + advertising identifiable info",
        "uuids": ["00001810-0000-1000-8000-00805f9b34fb"]
    }
]

save_html_report(devices, output_path="docs/sample_report.html")
