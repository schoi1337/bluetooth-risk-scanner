# report/report_generator.py

import json
from datetime import datetime

def generate_report(json_path, output_path="ble_report.html"):
    with open(json_path, "r") as f:
        devices = json.load(f)

    html = """
    <html>
    <head>
        <title>BLE Scan Report</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            h1 { color: #333; }
            table { border-collapse: collapse; width: 100%; margin-top: 20px; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: center; }
            th { background-color: #f2f2f2; position: sticky; top: 0; }
            .risk-High { background-color: #ffcccc; font-weight: bold; }
            .risk-Medium { background-color: #fff0b3; }
            .risk-Low { background-color: #ccffcc; }
        </style>
    </head>
    <body>
    """

    html += f"<h1>BLE Scan Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</h1>"
    html += "<table>"
    html += "<tr><th>MAC</th><th>Name</th><th>Vendor</th><th>RSSI</th><th>Risk</th></tr>"

    for d in devices:
        risk = d.get("risk", "Unknown")
        risk_class = f"risk-{risk}"
        html += (
            f"<tr>"
            f"<td>{d.get('mac', '')}</td>"
            f"<td>{d.get('name', '')}</td>"
            f"<td>{d.get('vendor', 'Unknown')}</td>"
            f"<td>{d.get('rssi', '')}</td>"
            f"<td class='{risk_class}'>{risk}</td>"
            f"</tr>"
        )

    html += "</table></body></html>"

    with open(output_path, "w") as f:
        f.write(html)

    print(f"[+] HTML report saved to {output_path}")
