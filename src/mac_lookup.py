# src/mac_lookup.py
# MAC OUI → Vendor name static mapping (BLE device focused)

OUI_VENDOR_MAP = {
    # Samsung
    "D0:27:88": "Samsung Electronics",
    "DC:A6:32": "Samsung Electronics",
    "84:C9:B2": "Samsung Electronics",

    # Apple
    "E0:11:22": "Apple Inc.",
    "F4:5C:89": "Apple Inc.",
    "A4:5E:60": "Apple Inc.",
    "3C:15:C2": "Apple Inc.",

    # Xiaomi
    "F8:04:2E": "Xiaomi Inc.",
    "FC:64:BA": "Xiaomi Inc.",
    "A4:77:33": "Xiaomi Inc.",

    # Huawei
    "C0:98:E5": "Huawei Technologies",
    "60:45:BD": "Huawei Technologies",

    # Fitbit
    "C8:FF:28": "Fitbit Inc.",
    "B0:B4:48": "Fitbit Inc.",

    # Realme / Oppo / OnePlus
    "74:30:E6": "Realme",
    "D0:76:E7": "OnePlus",
    "E4:A4:71": "Oppo",

    # Google Nest / Pixel
    "40:4E:36": "Google Inc.",
    "8C:85:90": "Google Inc.",

    # Sony
    "AC:23:3F": "Sony Corporation",
    "FC:58:FA": "Sony Corporation",

    # ESP32 (IoT)
    "A4:C1:38": "Espressif Inc.",
    "24:6F:28": "Espressif Inc.",

    # Raspberry Pi
    "B8:27:EB": "Raspberry Pi Foundation",
    "DC:A6:32": "Raspberry Pi Foundation",

    # JBL / Harman
    "00:02:5B": "Harman International (JBL)",
    "30:21:1B": "Harman International (JBL)",

    # Bose
    "38:18:4C": "Bose Corporation",
    "F4:8C:50": "Bose Corporation"
}

def lookup_vendor(mac_address):
    """Return vendor name for given MAC address prefix (first 3 bytes)."""
    prefix = mac_address.upper()[0:8]
    return OUI_VENDOR_MAP.get(prefix, "Unknown")
