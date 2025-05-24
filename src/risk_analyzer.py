# src/risk_analyzer.py

from src.cve_checker import fetch_cves

def assess_privacy_risks(device):
    """Detect potential privacy risks and return list of risks and a score."""
    risks = []
    score = 0

    rssi = device.get("rssi", -100)
    name = device.get("name", "").lower()
    mac = device.get("mac_address", "").upper()

    if name != "unknown":
        risks.append("Device name is visible")
        score += 2

    if device.get("vendor") != "Unknown":
        risks.append("Vendor can be inferred from MAC")
        score += 1

    if mac and len(mac) >= 2 and mac[1] in "26AE":
        risks.append("Possible static random MAC address")
        score += 2

    if any(x in name for x in ["lock", "sensor", "watch", "tag", "cam", "track"]):
        risks.append("Device type is inferable from name")
        score += 1

    if rssi > -65:
        risks.append("Very close proximity detected")
        score += 2
    elif rssi > -75:
        risks.append("Close-range signal detected")
        score += 1
    elif rssi > -85:
        risks.append("Device signal is very strong")
        score += 1

    # Manufacturer ID-based risk
    mfg_id = device.get("manufacturer_id")
    if mfg_id == 76:  # Apple
        risks.append("Apple manufacturer data detected")
        score += 2
    elif mfg_id == 1177:  # Tile
        risks.append("Tile tracking device detected via manufacturer ID")
        score += 2
    elif mfg_id == 533:  # Samsung
        risks.append("Samsung manufacturer ID detected (may indicate SmartTag)")
        score += 2

    services = device.get("uuids", [])
    sensitive_services = {
        "180D": "Heart Rate",
        "180F": "Battery",
        "181A": "Environmental Sensor",
        "181C": "User Data",
        "181E": "Weight Scale",
        "1822": "Pulse Oximeter",
        "1823": "HTTP Proxy"
    }
    for uuid in services:
        short_uuid = uuid[-4:].upper()
        if short_uuid in sensitive_services:
            risks.append(f"Sensitive GATT service exposed: {sensitive_services[short_uuid]}")
            score += 3

    return risks, score


def analyze_device_risk(device):
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
    privacy_risks, privacy_score = assess_privacy_risks(device)
    total_risk_score = base_score + cve_score + privacy_score

    device["cve_summary"] = [{"id": c[0], "cvss": c[1]} for c in cve_list]
    device["cve_score"] = cve_score
    device["privacy_risks"] = privacy_risks
    device["privacy_score"] = privacy_score
    device["risk_score"] = round(total_risk_score, 2)

    return device


def enrich_devices_with_score(devices):
    return [analyze_device_risk(device) for device in devices]
