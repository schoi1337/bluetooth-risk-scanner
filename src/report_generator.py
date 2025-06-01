import json
from datetime import datetime
from pathlib import Path

def save_json_report(devices, output_path="output/report.json"):
    """Save the scan results as a JSON file."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(devices, f, indent=2)
    print(f"[+] JSON report saved to {output_path.resolve()}")


def save_html_report(devices, output_path="output/report.html"):
    """Save the scan results as an HTML report with risk explanation and recommendation."""
    risk_levels = {"Low": "#e8f5e9", "Medium": "#fff3e0", "High": "#ffebee", "Critical": "#ffcdd2"}
    risk_count = {"Low": 0, "Medium": 0, "High": 0, "Critical": 0}

    for dev in devices:
        level = dev.get("risk_level", "Low")
        if level in risk_count:
            risk_count[level] += 1

    html = [
        "<html><head><title>Bluetooth Risk Report</title>",
        "<style>",
        "body { font-family: Arial, sans-serif; margin: 30px; }",
        "table { width: 100%; border-collapse: collapse; margin-top: 20px; }",
        "th, td { padding: 10px; border: 1px solid #ccc; text-align: left; vertical-align: top; }",
        "th { background-color: #f2f2f2; }",
        ".summary { background-color: #e3f2fd; padding: 15px; border: 1px solid #90caf9; margin-bottom: 20px; }",
    ]

    for level, color in risk_levels.items():
        html.append(f".risk-{level.lower()} {{ background-color: {color}; }}")

    html += [
        "</style></head><body>",
        "<h1>Bluetooth Device Risk Assessment</h1>",
        "<div class='summary'>",
        f"<p><strong>Total Devices Scanned:</strong> {len(devices)}</p>",
        "<p><strong>Risk Level Breakdown:</strong></p>",
        "<ul>",
        f"<li>Low: {risk_count['Low']}</li>",
        f"<li>Medium: {risk_count['Medium']}</li>",
        f"<li>High: {risk_count['High']}</li>",
        f"<li>Critical: {risk_count['Critical']}</li>",
        "</ul>",
        "</div>",
        "<table>",
        "<thead><tr><th>Device Name</th><th>MAC Address</th><th>Vendor</th><th>RSSI</th><th>Risk Score</th><th>Risk Level</th><th>Recommendation</th><th>Risk Explanation</th></tr></thead>",
        "<tbody>"
    ]

    for dev in devices:
        name = dev.get("name", "Unknown")
        mac = dev.get("mac", "Unknown")
        vendor = dev.get("vendor", "Unknown")
        rssi = dev.get("rssi", "N/A")
        score = dev.get("risk_score", "N/A")
        level = dev.get("risk_level", "Low")
        rec = dev.get("recommendation", "N/A")
        reason = dev.get("risk_reason", "N/A")
        row_class = f"risk-{level.lower()}"

        html.append(f"<tr class='{row_class}'>")
        html.append(f"<td>{name}</td><td>{mac}</td><td>{vendor}</td><td>{rssi}</td><td>{score}</td><td>{level}</td><td>{rec}</td><td>{reason}</td>")
        html.append("</tr>")

    html += ["</tbody></table></body></html>"]

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        f.write("\\n".join(html))

    print(f"[+] HTML report saved to {output_path.resolve()}")