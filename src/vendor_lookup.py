# vendor_lookup.py
# This module loads a local OUI manufacturer database (manuf file)
# and provides MAC address to vendor name lookup functionality.

from pathlib import Path

# Global dictionary to store MAC prefix to vendor mappings
mac_prefix_to_vendor = {}

def load_oui_database(manuf_file="manuf"):
    """
    Load MAC address prefix to vendor mappings from a manuf file.
    Ignores lines starting with # and handles UTF-8 decoding errors.
    """
    manuf_path = Path(manuf_file)
    if not manuf_path.exists():
        print(f"[!] OUI database file '{manuf_file}' not found.")
        return

    with manuf_path.open(encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(None, 2)
            if len(parts) >= 2:
                prefix = parts[0].upper()
                vendor = parts[1]
                mac_prefix_to_vendor[prefix] = vendor

def lookup_vendor_from_mac(mac_address):
    """
    Lookup the vendor name for a given MAC address using the loaded OUI database.
    Returns 'Unknown' if not found.
    """
    if not mac_prefix_to_vendor:
        load_oui_database()

    prefix = ":".join(mac_address.upper().split(":")[0:3])
    return mac_prefix_to_vendor.get(prefix, "Unknown")
