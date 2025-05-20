# utils/risk_database.py

# Risk levels based on known MAC address vendor prefixes
MAC_VENDOR_RISK = {
    "22:33:44": "Medium",  # Example: Smart lock vendor with past vulnerabilities
    "AA:BB:CC": "High",    # Example: Vendor known for data privacy issues
}

# Risk levels based on device name keywords
NAME_KEYWORDS_RISK = {
    "lock": "High",
    "watch": "Medium",
    "toy": "Low",
}

def evaluate_risk(local_name: str, mac: str) -> str:
    """
    Evaluate the risk level of a BLE device based on its local name and MAC address.

    Args:
        local_name (str): The advertised local name of the device.
        mac (str): The MAC address of the device.

    Returns:
        str: Risk level ("High", "Medium", or "Low")
    """
    local_name = local_name.lower()
    mac_prefix = mac.upper()[:8]  # Get the first 3 bytes of the MAC (OUI)

    # 1. Check MAC vendor prefix
    if mac_prefix in MAC_VENDOR_RISK:
        return MAC_VENDOR_RISK[mac_prefix]

    # 2. Check name keyword matches
    for keyword, risk in NAME_KEYWORDS_RISK.items():
        if keyword in local_name:
            return risk

    # 3. Default to Low risk
    return "Low"
