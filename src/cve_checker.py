# src/cve_checker.py
# Matches device names or vendor names to known CVEs using keyword mapping.

import csv
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data"

def load_cve_data():
    cve_map = {}
    with open(DATA_PATH / 'bluetooth_cve_list.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            keyword = row['keyword'].lower()
            cve_id = row['cve_id']
            description = row['description']
            cvss_score = row.get('cvss', 0)
            cve_map[keyword] = (cve_id, cvss_score)
    return cve_map

cve_data = load_cve_data()

def check_device_cve(device_name):
    name_lower = device_name.lower()
    found = []
    for keyword, (cve_id, score) in cve_data.items():
        if keyword in name_lower:
            found.append((cve_id, score))
    return found

def fetch_cves(vendor_name):
    return check_device_cve(vendor_name)
