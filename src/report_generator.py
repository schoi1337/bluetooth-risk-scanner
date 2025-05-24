# src/report_generator.py
# Generates HTML and JSON reports from analyzed BLE scan results.

import json
from datetime import datetime
from pathlib import Path

def save_json_report(devices, output_path="output/report.json"):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(devices, f, indent=2)
    print(f"[+] JSON report saved to {output_path.resolve()}")

def save_html_report(devices, output_path="output/report.html"):
    html = [
        "<html><head><title>BLE Risk Report</title></head><body>",
        f"<h1>Bluetooth Risk Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</h1>",
        "<table border='1' cellpadding='6' cellspacing='0'>",
        "<tr><th>Address</th><th>Name</th><th>Vendor</th><th>RSSI</th><th>CVE Score</th><th>Risk Score</th><th>CVE Summary</th></tr>"
    ]

    for dev in devices:
        cves = dev.get("cve_summary", [])
        cve_display = "<ul>" + "".join([f"<li>{cve['id']} (CVSS: {cve['cvss']})</li>" for cve in cves]) + "</ul>" if cves else "None"
        html.append(
            f"<tr>"
            f"<td>{dev.get('address')}</td>"
            f"<td>{dev.get('name')}</td>"
            f"<td>{dev.get('vendor')}</td>"
            f"<td>{dev.get('rssi')}</td>"
            f"<td>{dev.get('cve_score', 0)}</td>"
            f"<td>{dev.get('risk_score', 0)}</td>"
            f"<td>{cve_display}</td>"
            f"</tr>"
        )

    html.append("</table></body></html>")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        f.write("\n".join(html))
    print(f"[+] HTML report saved to {output_path.resolve()}")
