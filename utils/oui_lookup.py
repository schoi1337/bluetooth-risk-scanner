# utils/oui_lookup.py

import csv
import os

OUI_CSV_PATH = "data/oui.csv"  # Make sure this file is downloaded manually

def load_oui_database():
    oui_map = {}
    if not os.path.exists(OUI_CSV_PATH):
        print(f"[!] OUI database not found at {OUI_CSV_PATH}")
        return oui_map

    with open(OUI_CSV_PATH, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            assignment = row["Assignment"].replace("-", ":").upper()
            org_name = row["Organization Name"].strip()
            oui_map[assignment] = org_name
    return oui_map

def lookup_vendor(mac: str, oui_map: dict) -> str:
    mac_prefix = mac.upper()[:8]
    return oui_map.get(mac_prefix, "Unknown Vendor")
