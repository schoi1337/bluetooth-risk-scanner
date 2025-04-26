import csv
from pathlib import Path

# Path to the data directory
DATA_PATH = Path(__file__).parent.parent / "data"

def load_cve_data():
    """Load Bluetooth-related CVE data from a CSV file."""
    cve_map = {}
    with open(DATA_PATH / 'bluetooth_cve_list.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            keyword = row['keyword'].lower()
            cve_id = row['cve_id']
            description = row['description']
            cve_map[keyword] = (cve_id, description)
    return cve_map

# Load CVE data
cve_data = load_cve_data()

def check_device_cve(device_name):
    """Check if the device name matches any known Bluetooth CVEs."""
    name_lower = device_name.lower()
    found = []
    for keyword, (cve_id, description) in cve_data.items():
        if keyword in name_lower:
            found.append((cve_id, description))
    return found
