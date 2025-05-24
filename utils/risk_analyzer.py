# risk_analyzer.py
# This module analyzes the security risk of a BLE device based on vendor, RSSI, and CVE data.

from cve_lookup import fetch_cves

def analyze_device_risk(device):
    """
    Analyze a BLE device and calculate its risk score based on:
    - RSSI signal strength
    - Known CVEs for the vendor
    """
    vendor = device.get("vendor", "Unknown")
    cve_list = []
    cve_score = 0.0

    if vendor != "Unknown":
        cve_list = fetch_cves(vendor)
        if cve_list:
            # Calculate average CVSS score from recent CVEs
            avg_cvss = sum([cve["cvss"] for cve in cve_list]) / len(cve_list)
            cve_score = round(avg_cvss, 2)

    # Base score determined by RSSI signal strength
    base_score = 5 if device.get("rssi", -100) > -60 else 2

    # Final risk score = base score + CVE score
    total_risk_score = base_score + cve_score

    # Add CVE and risk info to the device dictionary
    device["cve_summary"] = cve_list
    device["cve_score"] = cve_score
    device["risk_score"] = round(total_risk_score, 2)

    return device
