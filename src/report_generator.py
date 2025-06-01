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
    """Save the scan results as a dark-themed HTML report with CVE and fingerprint data."""
    risk_levels = {"Low": "#90caf9", "Medium": "#ffb74d", "High": "#ef5350", "Critical": "#d32f2f"}
    risk_count = {level: 0 for level in risk_levels}

    for dev in devices:
        level = dev.get("risk_level", "Low")
        if level in risk_count:
            risk_count[level] += 1

    html = [
        "<html><head><title>Bluetooth Risk Report</title>",
        "<style>",
        "body { font-family: 'Segoe UI', sans-serif; background-color: #121212; color: #f5f5f5; margin: 30px; }",
        "table { width: 100%; border-collapse: collapse; margin-top: 20px; }",
        "th, td { padding: 12px; border: 1px solid #444; text-align: left; vertical-align: top; }",
        "th { background-color: #1e1e1e; color: #ffffff; }",
        "tr:nth-child(even) { background-color: #1a1a1a; }",
        "tr:hover { background-color: #2a2a2a; }",
        ".summary { background-color: #1e1e1e; padding: 15px; border: 1px solid #333; margin-bottom: 20px; border-radius: 8px; }",
        ".badge { padding: 5px 12px; border-radius: 10px; font-weight: bold; color: #111; display: inline-block; }",
        ".filter-btn { margin-right: 10px; padding: 8px 16px; font-size: 14px; cursor: pointer; border: none; border-radius: 6px; background-color: #333; color: #f5f5f5; transition: 0.2s; }",
        ".filter-btn:hover { background-color: #555; }",
    ]

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
        "<h1>🔒 Bluetooth Device Risk Assessment</h1>",
        "<div class='summary'>",
        f"<p><strong>Total Devices Scanned:</strong> {len(devices)}</p>",
        "<p><strong>Risk Level Breakdown:</strong></p><ul>",
    ]

    for level in risk_levels:
        html.append(f"<li>{level}: {risk_count[level]}</li>")
    html += ["</ul></div>"]

    html += [
        "<div style='margin-bottom: 20px;'>",
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
        "<th>Risk Score</th><th>Risk Level</th><th>Recommendation</th><th>Risk Explanation</th>",
        "<th>CVE Summary</th>",
        "<th>Fingerprint Summary</th>",
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
        row_class = f"risk-{level.lower()}"

        # Fingerprint summary
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

        # CVE summary
        cves = dev.get("cve_summary", [])
        if cves:
            cve_lines = [f"<li>{c['id']} (CVSS: {c['cvss']})</li>" for c in cves]
            cve_html = "<ul>" + "".join(cve_lines) + "</ul>"
        else:
            cve_html = "None"

        html.append(f"<tr class='{row_class}'>")
        html.append(f"<td>{score}</td>")
        html.append(f"<td><span class='badge badge-{level.lower()}'>{level}</span></td>")
        html.append(f"<td>{rec}</td><td>{reason}</td><td>{cve_html}</td><td>{fingerprint_html}</td>")
        html.append("</tr>")

    html += ["</tbody></table></body></html>"]

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        f.write("\n".join(html))

    print(f"[+] HTML report saved to {output_path.resolve()}")
