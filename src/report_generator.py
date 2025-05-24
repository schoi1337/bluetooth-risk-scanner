# src/report_generator.py
# Generates HTML and JSON reports from analyzed BLE scan results.

import json
from datetime import datetime
from pathlib import Path

def save_json_report(devices, output_path="output/report.json"):
    """
    Save the scan results as a JSON file.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(devices, f, indent=2)
    print(f"[+] JSON report saved to {output_path.resolve()}")

def format_cve_summary(dev):
    """
    Combine CVE and privacy risks into an HTML block for report display.
    """
    cves = dev.get("cve_summary", [])
    risks = dev.get("privacy_risks", [])
    html = []

    if cves:
        html.append("<strong>CVEs:</strong><ul>")
        for cve in cves:
            html.append(f"<li>{cve['id']} (CVSS: {cve['cvss']})</li>")
        html.append("</ul>")
    else:
        html.append("<strong>CVEs:</strong> None")

    if risks:
        html.append("<br><strong>Privacy Risks:</strong><ul>")
        for r in risks:
            html.append(f"<li>{r}</li>")
        html.append("</ul>")
    else:
        html.append("<br><strong>Privacy Risks:</strong> None")

    return "".join(html)

def save_html_report(devices, output_path="output/report.html"):
    """
    Save the scan results as a simple HTML report.
    """
    html = [
        "<html><head><title>BLE Risk Report</title></head><body>",
        f"<h1>Bluetooth Risk Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</h1>",
        "<table border='1' cellpadding='6' cellspacing='0'>",
        "<tr><th>Address</th><th>Name</th><th>Vendor</th><th>RSSI</th><th>CVE Score</th><th>Risk Score</th><th>Details</th></tr>"
    ]

    for dev in devices:
        html.append(
            f"<tr>"
            f"<td>{dev.get('address')}</td>"
            f"<td>{dev.get('name')}</td>"
            f"<td>{dev.get('vendor')}</td>"
            f"<td>{dev.get('rssi')}</td>"
            f"<td>{dev.get('cve_score', 0)}</td>"
            f"<td>{dev.get('risk_score', 0)}</td>"
            f"<td>{format_cve_summary(dev)}</td>"
            f"</tr>"
        )

    html.append("</table></body></html>")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        f.write("\n".join(html))
    print(f"[+] HTML report saved to {output_path.resolve()}")
