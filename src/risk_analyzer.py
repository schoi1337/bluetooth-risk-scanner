# src/risk_analyzer.py
# Calculates risk score for a given BLE device based on RSSI and CVE information.

from src.cve_checker import fetch_cves

def analyze_device_risk(device):
    """
    Analyze a BLE device and calculate its risk score based on:
    - RSSI signal strength
    - Known CVEs for the vendor
    """
    vendor = device.get("vendor", "Unknown")
    cve_list = fetch_cves(vendor) if vendor != "Unknown" else []
    cve_score = 0.0

    if cve_list:
        avg_cvss = sum([float(cve[1]) for cve in cve_list if isinstance(cve[1], (int, float, str)) and str(cve[1]).replace('.', '', 1).isdigit()]) / len(cve_list)
        cve_score = round(avg_cvss, 2)

    base_score = 5 if device.get("rssi", -100) > -60 else 2
    total_risk_score = base_score + cve_score

    device["cve_summary"] = [{"id": c[0], "cvss": c[1]} for c in cve_list]
    device["cve_score"] = cve_score
    device["risk_score"] = round(total_risk_score, 2)

    return device
