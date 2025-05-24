# Bluetooth Risk Scanner 🔍

Bluetooth Risk Scanner passively detects nearby BLE (Bluetooth Low Energy) devices and evaluates them for privacy and security risks — including silent trackers like AirTags, vulnerable wearables, and devices with exposed GATT services.

Unlike simple scanners, this tool classifies threats based on proximity, vendor reputation, advertising behavior, and CVE history.

## 🚀 Features

- Passive BLE scan using `bleak`
- Detect name, RSSI, MAC (when available), manufacturer ID, service UUIDs
- Vendor detection using IEEE OUI (`manuf`-like logic)
- Privacy risk scoring:
  - Static MAC behavior
  - Proximity tracking (RSSI-based)
  - Manufacturer-based passive tracker detection (e.g. Apple AirTag)
  - GATT service analysis (e.g. heart rate, user data)
- HTML + JSON reports with color-coded risk indicators
- Ubertooth branch available for sniffer-mode scanning

## 🎛️ Risk Model

The following factors contribute to a device's total `risk_score`:

| Category         | Indicators Detected                                         | Score |
|------------------|-------------------------------------------------------------|-------|
| **Proximity**     | RSSI > -65 → Very Close                                     | +2    |
| **Identity Leakage** | Name is visible / MAC reveals vendor                      | +1–2  |
| **MAC Behavior**   | Static/random MAC address patterns                         | +2    |
| **Passive Tracker** | Apple (AirTag), Tile, Samsung SmartTag via Manufacturer ID | +2    |
| **BLE Services**    | Sensitive UUIDs like Heart Rate, User Data                | +3    |


## 📋 Usage

```bash
git clone https://github.com/schoi1337/bluetooth-risk-scanner.git
cd bluetooth-risk-scanner

# Activate virtualenv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the scanner (default: 10s scan, no RSSI filter)
python main.py

# Custom scan: 15s timeout, ignore weak signals
python main.py --timeout 15 --min-rssi -85
```

Reports are saved to:
- `output/scan_report.json`
- `output/scan_report.html` 

### 📸 Sample Output

![Sample HTML Report](screenshots/Report.png)


## 🧪 Platform Notes

| OS        | BLE MAC Available? | Notes                                                  |
|-----------|---------------------|---------------------------------------------------------|
| Linux     | ✅ Yes              | Full support via BlueZ (recommended)                   |
| Windows   | ✅ Yes              | Most BLE dongles supported                             |
| macOS     | ❌ No               | CoreBluetooth hides MACs → UUIDs only (limited vendor detection) |

## 🛰️ Ubertooth Branch

Use Ubertooth to sniff BLE advertisements without needing an HCI-compatible dongle:

📦 [`feature/ubertooth-support`](https://github.com/schoi1337/bluetooth-risk-scanner/tree/feature/ubertooth-support)

## 🤝 Contributing

PRs welcome. Submit bugs, ideas, or integrations via issues.

## 📄 License

This project is licensed under the MIT License.
