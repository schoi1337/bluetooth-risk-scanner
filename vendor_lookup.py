# vendor_lookup.py

# Load vendor prefix mappings from Wireshark manuf file
MANUF_FILE = "data/manuf"

vendor_db = {}

# Parse manuf file into vendor_db
with open(MANUF_FILE, "r") as f:
    for line in f:
        if line.startswith("#") or line.strip() == "":
            continue
        parts = line.split()
        if len(parts) >= 2:
            prefix = parts[0].upper().replace(":", "").replace("-", "")
            vendor_name = parts[1]
            vendor_db[prefix] = vendor_name


def get_vendor(mac: str, name: str = "") -> str:
    """
    Attempt to determine the vendor of a BLE device.
    Priority:
    1. BLE name pattern matching (if present)
    2. MAC prefix via manuf lookup
    """
    # 1. First try name-based inference
    if name:
        lname = name.lower()
        if "samsung" in lname:
            return "Samsung"
        elif "mi band" in lname or "xiaomi" in lname:
            return "Xiaomi"
        elif "fitbit" in lname:
            return "Fitbit"
        elif "welock" in lname or "lock" in lname:
            return "WELOCK"
        elif "tile" in lname:
            return "Tile"
        elif "galaxy tag" in lname or ("tag" in lname and "samsung" in lname):
            return "Samsung"

    # 2. Fallback to MAC prefix lookup
    mac = mac.upper().replace(":", "").replace("-", "")
    prefix = mac[:6]
    return vendor_db.get(prefix, "Unknown")
