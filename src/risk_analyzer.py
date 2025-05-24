# src/risk_analyzer.py
# Calculates risk score for a given BLE device based on RSSI, CVE info, and privacy risks.

from src.cve_checker import fetch_cves

def assess_privacy_risks(device):
    """Detect potential privacy risks and return list of risks and a score."""
    risks = []
    score = 0

    if device.get("name") != "Unknown":
        risks.append("Device name is visible")
        score += 2

    if device.get("vendor") != "Unknown":
        risks.append("Vendor can be inferred from MAC")
        score += 1

    mac = device.get("address", "").upper()
    if mac and len(mac) >= 2 and mac[1] in "26AE":
        risks.append("Possible static random MAC address")
        score += 2

    name = device.get("name", "").lower()
    if any(x in name for x in ["lock", "sensor", "watch", "tag"]):
        risks.append("Device type is inferable from name")
        score += 1

    return risks, score


def analyze_device_risk(device):
    """Analyze a BLE device and calculate its risk score based on CVE, RSSI, and privacy risks."""
    vendor = device.get("vendor", "Unknown")
    cve_list = fetch_cves(vendor) if vendor != "Unknown" else []
    cve_score = 0.0

    if cve_list:
        cvss_values = [
            float(cve[1]) for cve in cve_list
            if isinstance(cve[1], (int, float, str)) and str(cve[1]).replace('.', '', 1).isdigit()
        ]
        if cvss_values:
            avg_cvss = sum(cvss_values) / len(cvss_values)
            cve_score = round(avg_cvss, 2)

    base_score = 5 if device.get("rssi", -100) > -60 else 2

    # New: Privacy Risk Scoring
    privacy_risks, privacy_score = assess_privacy_risks(device)

    total_risk_score = base_score + cve_score + privacy_score

    device["cve_summary"] = [{"id": c[0], "cvss": c[1]} for c in cve_list]
    device["cve_score"] = cve_score
    device["privacy_risks"] = privacy_risks
    device["privacy_score"] = privacy_score
    device["risk_score"] = round(total_risk_score, 2)

    return device
