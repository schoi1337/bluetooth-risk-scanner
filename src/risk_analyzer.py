# src/risk_analyzer.py

import yaml
from pathlib import Path

def load_risk_weights(filepath="data/risk_weights.yaml"):
    """Load risk weights from a YAML config file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def analyze_device_risk(device, risk_weights):
    """Calculate risk score and reasons based on YAML-defined risk weights."""
    score = 0
    reasons = []

    # Static MAC
    if device.get("mac_randomized") is False:
        score += risk_weights.get("static_mac", 0)
        reasons.append("Device uses static MAC address.")

    # Public name
    if device.get("name") and device["name"] not in ["Unknown", ""]:
        score += risk_weights.get("public_name", 0)
        reasons.append("Device broadcasts public name.")

    # Known tracking vendor
    if device.get("vendor_risk") == "tracking":
        score += risk_weights.get("known_tracking_vendor", 0)
        reasons.append("Vendor is associated with BLE tracking.")

    # BLE advertising enabled
    if device.get("advertising_enabled") is True:
        score += risk_weights.get("ble_advertising_enabled", 0)
        reasons.append("BLE advertising is enabled.")

    # Manufacturer-specific data
    if device.get("manufacturer_data"):
        score += risk_weights.get("exposes_manufacturer_data", 0)
        reasons.append("Device exposes manufacturer-specific data.")

    # Strong signal = close proximity
    if device.get("rssi") and device["rssi"] > -50:
        score += risk_weights.get("weak_signal_proximity", 0)
        reasons.append("Device is in close proximity (strong RSSI).")

    return score, reasons

def analyze_privacy_risks(device):
    """
    Analyze BLE advertisement fields to detect privacy risks.
    Returns a list of human-readable risk indicators.
    """

    risks = []

    # Manufacturer-specific data reveals vendor identity
    if device.get("manufacturer_data"):
        risks.append("Exposes manufacturer-specific BLE data")

    # Service data may contain UUIDs that reveal functionality
    if device.get("service_data"):
        risks.append("Exposes service-specific data in advertisements")

    # BLE flags indicate discoverability and connectability
    if device.get("flags") in [0x02, 0x04, 0x06]:
        risks.append("BLE is discoverable and connectable")

    return risks
