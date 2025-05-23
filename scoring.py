# scoring.py

def calculate_risk_score(device: dict) -> float:
    """
    Calculate a risk score based on CVEs, RSSI, and vendor reputation.

    Parameters:
    - device (dict): {
        "mac": str,
        "vendor": str,
        "rssi": int,
        "cve_list": list[str]
    }

    Returns:
    - float: Risk score between 0.0 (safe) and 10.0 (critical)
    """
    cve_score = min(len(device.get("cve_list", [])) * 2.0, 6.0)
    rssi_score = 2.0 if device.get("rssi", -100) > -70 else 1.0
    vendor_score = {
        "WELOCK": 2.0,
        "Xiaomi": 1.5,
        "Fitbit": 1.0
    }.get(device.get("vendor", ""), 1.0)

    total_score = round(min(cve_score + rssi_score + vendor_score, 10.0), 1)
    return total_score


def enrich_devices_with_score(devices: list[dict]) -> list[dict]:
    """
    Adds a 'risk_score' field to each device in the list.
    """
    for device in devices:
        device["risk_score"] = calculate_risk_score(device)
    return devices


# 🧪 Example usage
if __name__ == "__main__":
    test_devices = [
        {
            "mac": "D8:58:D7:12:34:56",
            "vendor": "WELOCK",
            "rssi": -67,
            "cve_list": ["CVE-123", "CVE-456"]
        },
        {
            "mac": "00:11:22:33:44:55",
            "vendor": "Fitbit",
            "rssi": -82,
            "cve_list": []
        }
    ]

    enriched = enrich_devices_with_score(test_devices)
    for d in enriched:
        print(f"{d['mac']} → Risk Score: {d['risk_score']}")
