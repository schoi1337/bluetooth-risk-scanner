# src/cve_checker.py

import json
import os

def load_ble_cve_db(*years):
    """
    Load BLE CVE database JSON files for the specified years.
    Returns a single list of all CVE entries.
    """
    db = []
    for y in years:
        fname = os.path.join("data", f"ble_cve_db_{y}.json")
        if os.path.exists(fname):
            with open(fname, "r", encoding="utf-8") as f:
                db.extend(json.load(f))
    return db

def find_cves_for_device(vendor, product, cve_db):
    """
    Search the CVE DB for entries matching the device's vendor or product name.
    Returns a list of dicts with id, cvss, description, and URL.
    """
    v = (vendor or "").lower()
    p = (product or "").lower()
    result = []
    for c in cve_db:
        desc = c.get("description", "").lower()
        if (v and v in desc) or (p and p in desc):
            result.append({
                "id": c["cve"],
                "cvss": c.get("severity", "N/A"),
                "desc": c.get("description", ""),
                "url": c.get("url", "")
            })
    return result
