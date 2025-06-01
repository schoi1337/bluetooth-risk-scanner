# src/behavior_tracker.py

import os
import json
from pathlib import Path

FINGERPRINTS_DIR = Path("fingerprints")
MAC_LOG_PATH = FINGERPRINTS_DIR / "mac_rotation_log.json"
NAME_LOG_PATH = FINGERPRINTS_DIR / "name_change_log.json"

def ensure_dir_exists(path: Path):
    """Ensure that the specified directory exists."""
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)

def load_json(path: Path):
    """Load JSON data from a file or return empty dict if file doesn't exist."""
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path: Path, data):
    """Save data as JSON to a file."""
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def convert_bytes_to_hex(obj):
    """
    Recursively convert any bytes objects to hex strings to make JSON serializable.
    """
    if isinstance(obj, dict):
        return {k: convert_bytes_to_hex(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_bytes_to_hex(i) for i in obj]
    elif isinstance(obj, bytes):
        return obj.hex()
    else:
        return obj

def save_device_profile(device: dict):
    """
    Save device fingerprint/profile as a JSON file with bytes converted to hex strings.
    """
    ensure_dir_exists(FINGERPRINTS_DIR)
    mac = device.get("mac", device.get("address", "unknown")).replace(":", "_").lower()
    filepath = FINGERPRINTS_DIR / f"{mac}.json"

    cleaned_device = convert_bytes_to_hex(device)

    with filepath.open("w", encoding="utf-8") as f:
        json.dump(cleaned_device, f, indent=2)

def check_mac_rotation(device: dict) -> bool:
    """
    Detect if a device name is associated with multiple MAC addresses,
    indicating possible MAC address rotation.
    """
    ensure_dir_exists(FINGERPRINTS_DIR)
    name = device.get("name", "")
    mac = device.get("mac", "").upper()
    if not name or not mac:
        return False

    data = load_json(MAC_LOG_PATH)
    macs = set(data.get(name, []))
    macs.add(mac)
    data[name] = list(macs)
    save_json(MAC_LOG_PATH, data)

    # If more than 2 unique MACs for the same name, flag as rotating MAC
    return len(macs) > 2

def check_name_switching(device: dict) -> bool:
    """
    Detect if a MAC address is associated with multiple device names,
    indicating possible name spoofing or switching.
    """
    ensure_dir_exists(FINGERPRINTS_DIR)
    name = device.get("name", "")
    mac = device.get("mac", "").upper()
    if not name or not mac:
        return False

    data = load_json(NAME_LOG_PATH)
    names = set(data.get(mac, []))
    names.add(name)
    data[mac] = list(names)
    save_json(NAME_LOG_PATH, data)

    # If more than 2 unique names for the same MAC, flag as name switching
    return len(names) > 2
