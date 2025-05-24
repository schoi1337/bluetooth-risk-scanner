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
    Save the scan results as a simple HTML report with improved styling and UX note.
    """
    html = [
        "<html><head><title>Bluetooth Risk Report</title>",
        "<style>",
        "body { font-family: Arial, sans-serif; margin: 40px; }",
        "h1 { color: #2C3E50; }",
        "p.note { background-color: #f9f9f9; padding: 10px; border-left: 4px solid #3498db; }",
        "table { border-collapse: collapse; width: 100%; margin-top: 20px; }",
        "th, td { border: 1px solid #ccc; padding: 10px; text-align: left; }",
        "th { background-color: #f2f2f2; }",
        "tr:nth-child(even) { background-color: #fafafa; }",
        "</style>",
        "</head><body>",
        f"<h1>Bluetooth Risk Report</h1>",
        f"<p class='note'><strong>Note:</strong> If a device's name or vendor shows as <code>Unknown</code>, it's likely because the device is not in discovery mode and isn't broadcasting identifying information. Try initiating pairing to see more detailed info in future scans.</p>",
        f"<p><em>Scan timestamp:</em> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>",
        "<table>",
        "<tr><th>MAC Address</th><th>Name</th><th>Vendor</th><th>RSSI</th><th>CVE Score</th><th>Risk Score</th><th>Details</th></tr>"
    ]

    for dev in devices:
        html.append(
            f"<tr>"
            f"<td>{dev.get('mac_address', 'N/A')}</td>"
            f"<td>{dev.get('name', 'N/A')}</td>"
            f"<td>{dev.get('vendor', 'N/A')}</td>"
            f"<td>{dev.get('rssi', 'N/A')}</td>"
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
