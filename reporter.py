# reporter.py

import json
import os

RESULTS_DIR = "results"
INPUT_FILE = "scan_results.json"
OUTPUT_JSON = "report.json"
OUTPUT_HTML = "report.html"

def load_scan_results():
    """Load scanned device analysis results."""
    input_path = os.path.join(RESULTS_DIR, INPUT_FILE)
    with open(input_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json_report(results):
    """Save a full JSON report."""
    output_path = os.path.join(RESULTS_DIR, OUTPUT_JSON)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

def save_html_report(results):
    """Save a simple human-readable HTML report."""
    output_path = os.path.join(RESULTS_DIR, OUTPUT_HTML)

    html_content = "<html><head><title>BLE Risk Report</title></head><body>"
    html_content += "<h1>Bluetooth Risk Scanner Report</h1>"

    for device in results:
        html_content += f"<h2>{device['name']} ({device['address']})</h2><ul>"
        html_content += f"<li>Vendor: {device['vendor']}</li>"
        html_content += f"<li>Risk Level: {device['risk_level']}</li>"
        html_content += f"<li>Risk Score: {device['risk_score']}</li>"
        if device.get("cve_hits"):
            html_content += f"<li>CVE Hits: {device['cve_hits']}</li>"
        html_content += "</ul>"

    html_content += "</body></html>"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

def generate_report():
    """Generate JSON and HTML reports from scan results."""
    results = load_scan_results()
    save_json_report(results)
    save_html_report(results)
    print(f"[*] Reports generated: {OUTPUT_JSON}, {OUTPUT_HTML}")

if __name__ == "__main__":
    generate_report()
