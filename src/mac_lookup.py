# src/mac_lookup.py
# Minimal MAC prefix to vendor name mapping

OUI_VENDOR_MAP = {
    "D4:12:34": "Samsung Electronics",
    "E0:11:22": "Apple, Inc.",
    "00:1A:7D": "Intel Corporation",
    "40:4E:36": "Google, Inc.",
    "F8:04:2E": "Xiaomi Inc.",
    "AC:23:3F": "Sony Corporation",
    "B8:27:EB": "Raspberry Pi Foundation"
    # Add more as needed
}

def lookup_vendor(mac_address):
    """Lookup vendor based on MAC address prefix (first 3 bytes)."""
    prefix = mac_address.upper()[0:8]
    return OUI_VENDOR_MAP.get(prefix, "Unknown")
