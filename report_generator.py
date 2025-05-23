# report_generator.py

import json
from datetime import datetime
import webbrowser
import os

def generate_html_report(input_file="results.json", output_file="report.html", auto_open=True):
    with open(input_file, "r") as f:
        results = json.load(f)

    def score_to_color(score):
        if score >= 8.0:
            return "#ff4d4d"  # High - Red
        elif score >= 5.0:
            return "#ffa64d"  # Medium - Orange
        else:
            return "#90ee90"  # Low - Green

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Bluetooth Risk Scanner Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <h2>Bluetooth Risk Scanner Report</h2>
    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <table>
        <tr>
            <th>MAC</th>
            <th>Vendor</th>
            <th>RSSI</th>
            <th>Risk Score</th>
            <th>CVEs</th>
        </tr>"""

    for device in results:
        color = score_to_color(device.get("risk_score", 0))
        html += f"""
        <tr style="background-color: {color};">
            <td>{device.get("mac", "")}</td>
            <td>{device.get("vendor", "")}</td>
            <td>{device.get("rssi", "")}</td>
            <td>{device.get("risk_score", "N/A")}</td>
            <td>{", ".join(device.get("cve_list", []))}</td>
        </tr>"""

    html += """
    </table>
</body>
</html>"""

    with open(output_file, "w") as f:
        f.write(html)

    if auto_open:
        webbrowser.open(f"file://{os.path.abspath(output_file)}")

# Example run
if __name__ == "__main__":
    generate_html_report()
