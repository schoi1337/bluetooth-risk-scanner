# src/report_generator.py

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
    """Save the scan results as an HTML report with risk severity visualization and filter buttons."""
    risk_levels = {"Low": "#9e9e9e", "Medium": "#ff9800", "High": "#f44336", "Critical": "#b71c1c"}
    risk_count = {level: 0 for level in risk_levels}

    for dev in devices:
        level = dev.get("risk_level", "Low")
        if level in risk_count:
            risk_count[level] += 1

    html = [
        "<html><head><title>Bluetooth Risk Report</title>",
        "<style>",
        "body { font-family: Arial, sans-serif; margin: 30px; background-color: #ffffff; color: #333; }",
        "table { width: 100%; border-collapse: collapse; margin-top: 20px; }",
        "th, td { padding: 10px; border: 1px solid #ccc; text-align: left; vertical-align: top; }",
        "th { background-color: #f2f2f2; }",
        ".summary { background-color: #e3f2fd; padding: 15px; border: 1px solid #90caf9; margin-bottom: 20px; }",
        ".badge { padding: 4px 10px; border-radius: 8px; color: white; font-weight: bold; }",
        ".filter-btn { margin-right: 8px; padding: 6px 12px; font-size: 14px; cursor: pointer; }",
    ]

    # Add dynamic badge color classes
    for level, color in risk_levels.items():
        html.append(f".badge-{level.lower()} {{ background-color: {color}; }}")

    html += [
        "</style>",
        "<script>",
        "function filterRisk(level) {",
        "  var rows = document.querySelectorAll('tbody tr');",
        "  rows.forEach(row => {",
        "    if (level === 'All') { row.style.display = ''; return; }",
        "    row.style.display = row.classList.contains('risk-' + level.toLowerCase()) ? '' : 'none';",
        "  });",
        "}",
        "</script>",
        "</head><body>",
        "<h1>Bluetooth Device Risk Assessment</h1>",
        "<div class='summary'>",
        f"<p><strong>Total Devices Scanned:</strong> {len(devices)}</p>",
        "<p><strong>Risk Level Breakdown:</strong></p>",
        "<ul>",
    ]

    for level in risk_levels:
        html.append(f"<li>{level}: {risk_count[level]}</li>")
    html += ["</ul></div>"]

    # Add filter buttons
    html += [
        "<div>",
        "<button class='filter-btn' onclick=\"filterRisk('All')\">Show All</button>",
        "<button class='filter-btn' onclick=\"filterRisk('Low')\">Low</button>",
        "<button class='filter-btn' onclick=\"filterRisk('Medium')\">Medium</button>",
        "<button class='filter-btn' onclick=\"filterRisk('High')\">High</button>",
        "<button class='filter-btn' onclick=\"filterRisk('Critical')\">Critical</button>",
        "</div>"
    ]

    html += [
        "<table>",
        "<thead><tr>",
        "<th>Risk Score</th><th>Risk Level</th><th>Recommendation</th><th>Risk Explanation</th><th>Fingerprint Summary</th>",
        "</tr></thead><tbody>"
    ]

    for dev in devices:
        score = dev.get("risk_score", "N/A")
        level = dev.get("risk_level", "Low")
        rec = dev.get("recommendation", "N/A")
        reason = dev.get("risk_reason", "N/A")
        uuids = dev.get("uuids", [])
        name = dev.get("name", "Unknown")
        mac = dev.get("mac", "Unknown")
        vendor = dev.get("vendor", "Unknown")

        # Fingerprint summary section
        fp_lines = [
            f"<strong>Name:</strong> {name}",
            f"<strong>MAC:</strong> {mac}",
            f"<strong>Vendor:</strong> {vendor}",
        ]
        if uuids:
            fp_lines.append("<strong>UUIDs:</strong><ul>")
            for u in uuids:
                fp_lines.append(f"<li>{u}</li>")
            fp_lines.append("</ul>")
        else:
            fp_lines.append("<strong>UUIDs:</strong> None")

        fingerprint_html = "<br>".join(fp_lines)
        row_class = f"risk-{level.lower()}"

        html.append(f"<tr class='{row_class}'>")
        html.append(f"<td>{score}</td>")
        html.append(f"<td><span class='badge badge-{level.lower()}'>{level}</span></td>")
        html.append(f"<td>{rec}</td><td>{reason}</td><td>{fingerprint_html}</td>")
        html.append("</tr>")

    html += ["</tbody></table></body></html>"]

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        f.write("\n".join(html))

    print(f"[+] HTML report saved to {output_path.resolve()}")
