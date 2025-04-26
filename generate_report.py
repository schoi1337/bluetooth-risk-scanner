import json
from pathlib import Path

# Paths
DATA_PATH = Path(__file__).parent / "output" / "scan_results.json"
REPORT_PATH = Path(__file__).parent / "output" / "report.html"

def load_scan_results():
    """Load scan results from JSON file."""
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_html_report(devices):
    """Generate HTML content from scan results."""
    html = """
    <html>
    <head>
        <title>Bluetooth Scan Report</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            .risk { color: red; font-weight: bold; }
            .cve { color: darkorange; }
        </style>
    </head>
    <body>
        <h2>Bluetooth Scan Report</h2>
        <table>
            <tr>
                <th>Device Name</th>
                <th>MAC Address</th>
                <th>RSSI</th>
                <th>Risks</th>
                <th>CVEs</th>
            </tr>
    """

    for device in devices:
        risks = ', '.join(device['Risks']) if device['Risks'] else 'None'
        risks_html = f"<span class='risk'>{risks}</span>" if device['Risks'] else risks
        cves = ', '.join([cve['id'] for cve in device['CVEs']]) if device['CVEs'] else 'None'
        cves_html = f"<span class='cve'>{cves}</span>" if device['CVEs'] else cves

        html += f"""
            <tr>
                <td>{device['Name']}</td>
                <td>{device['MAC']}</td>
                <td>{device['RSSI']} dBm</td>
                <td>{risks_html}</td>
                <td>{cves_html}</td>
            </tr>
        """

    html += """
        </table>
    </body>
    </html>
    """
    return html

def save_html_report(html_content):
    """Save HTML report to file."""
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"[+] Report generated: {REPORT_PATH}")

def main():
    devices = load_scan_results()
    html_report = generate_html_report(devices)
    save_html_report(html_report)

if __name__ == "__main__":
    main()
