# utils/risk_analyzer.py

import csv
import os

DATA_DIR = "data"

def load_csv_to_dict(filepath):
    """Load a CSV file into a dictionary."""
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        return {rows[0]: rows[1] for rows in reader if rows}

def load_cve_list(filepath):
    """Load a CVE list into a list."""
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

# Load databases
OUI_DB = load_csv_to_dict(os.path.join(DATA_DIR, "oui.csv"))
VENDOR_RISK_DB = load_csv_to_dict(os.path.join(DATA_DIR, "ble_vendors.csv"))
PRIVACY_RISK_VENDORS = set(load_csv_to_dict(os.path.join(DATA_DIR, "privacy_risk_vendors.csv")).keys())
INCIDENT_VENDORS = set(load_csv_to_dict(os.path.join(DATA_DIR, "incident_vendors.csv")).keys())
CVE_LIST = load_cve_list(os.path.join(DATA_DIR, "bluetooth_cve_list.cve"))

def lookup_vendor(mac_address):
    """Lookup vendor based on MAC address prefix."""
    prefix = mac_address.upper().replace(":", "")[0:6]
    return OUI_DB.get(prefix, "Unknown Vendor")

def lookup_vendor_risk(vendor):
    """Lookup risk level based on vendor name."""
    return VENDOR_RISK_DB.get(vendor, "Unknown")

def check_privacy_risk_vendor(vendor):
    """Check if the vendor has known privacy risks."""
    return vendor in PRIVACY_RISK_VENDORS

def check_incident_vendor(vendor):
    """Check if the vendor has known security incidents."""
    return vendor in INCIDENT_VENDORS

def search_cve(device_name, uuids):
    """Search for matching CVEs based on device name or UUIDs."""
    hits = []
    for cve in CVE_LIST:
        if device_name and device_name.lower() in cve.lower():
            hits.append(cve)
        for uuid in uuids:
            if uuid.lower() in cve.lower():
                hits.append(cve)
    return hits

def analyze_device_risk(device_info):
    """Analyze a device's risk based on collected information."""
    vendor = lookup_vendor(device_info["address"])
    risk_level = lookup_vendor_risk(vendor)
    privacy_risk = check_privacy_risk_vendor(vendor)
    incident_risk = check_incident_vendor(vendor)
    cve_hits = search_cve(device_info.get("name"), device_info.get("uuids", []))

    risk_score = 0
    if risk_level == "High":
        risk_score += 30
    elif risk_level == "Medium":
        risk_score += 20
    elif risk_level == "Low":
        risk_score += 10

    if privacy_risk:
        risk_score += 10
    if incident_risk:
        risk_score += 10
    if cve_hits:
        risk_score += 30

    return {
        "address": device_info["address"],
        "name": device_info["name"],
        "vendor": vendor,
        "risk_level": risk_level,
        "privacy_risk_vendor": privacy_risk,
        "incident_vendor": incident_risk,
        "cve_hits": cve_hits,
        "risk_score": risk_score
    }
