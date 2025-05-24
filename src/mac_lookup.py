# src/mac_lookup.py
# Minimal MAC prefix to vendor mapping (sample only)

OUI_VENDOR_MAP = {
    "D4:12:34": "Samsung Electronics",
    "E0:11:22": "Apple, Inc.",
    "00:1A:7D": "Intel Corporation",
    "40:4E:36": "Google, Inc.",
    # ... 추가 가능
}

def lookup_vendor(mac_address):
    prefix = mac_address.upper()[0:8]
    return OUI_VENDOR_MAP.get(prefix, "Unknown")
