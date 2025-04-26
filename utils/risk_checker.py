import csv
from pathlib import Path

# Path to the data directory
DATA_PATH = Path(__file__).parent.parent / "data"

def load_vendor_list(filename):
    """Load a list of vendors from a CSV file."""
    vendors = set()
    with open(DATA_PATH / filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            vendors.add(row[0].lower())
    return vendors

# Load privacy risk and incident vendor lists
privacy_risk_vendors = load_vendor_list('privacy_risk_vendors.csv')
incident_vendors = load_vendor_list('incident_vendors.csv')

def check_vendor_risk(device_name):
    """Check if a device is associated with privacy concerns or past
