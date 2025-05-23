# vendor_lookup.py

import os
import re

MANUF_FILE = os.path.join("data", "manuf")

def load_oui_map():
    oui_map = {}
    with open(MANUF_FILE, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # Wireshark's manuf: tab-separated (but may have spaces)
            parts = re.split(r'\s{2,}|\t+', line)
            if len(parts) < 2:
                continue
            raw_prefix = parts[0].split("/")[0]
            mac_prefix = raw_prefix.replace(":", "").replace("-", "").upper()[:6]
            vendor = parts[1]
            oui_map[mac_prefix] = vendor
    return oui_map

OUI_MAP = load_oui_map()

def get_vendor(mac):
    prefix = mac.replace(":", "").upper()[:6]
    return OUI_MAP.get(prefix, "Unknown")
