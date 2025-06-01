# Bluetooth Risk Scanner 🔍

Bluetooth Risk Scanner passively detects nearby BLE (Bluetooth Low Energy) devices and evaluates them for privacy and security risks — including silent trackers like AirTags, vulnerable wearables, and devices with exposed GATT services.

Unlike simple scanners, this tool classifies threats based on proximity, vendor reputation, advertising behavior, and CVE history.

## 🚀 Features

- Passive BLE scanning using [`bleak`](https://github.com/hbldh/bleak) (Windows/Linux/macOS)
- Device data: Name, RSSI, UUIDs, Manufacturer ID, MAC (when available)
- Vendor/OUI detection for manufacturer reputation and CVE mapping
- Risk scoring model:
  - Proximity-based scoring (RSSI)
  - Static/rotating MAC analysis
  - Manufacturer-based tracker detection (Apple, Tile, Samsung, etc.)
  - BLE GATT service fingerprinting
  - Behavioral anomaly detection (MAC/name switching)
- CVE lookups (offline DB, auto-mapped by vendor/product)
- YAML-based scoring weights for custom risk models
- HTML/JSON reports with color-coded severity, explanations, and recommendations
- CLI: batch scan, scheduling (cron), offline analysis of stored scan logs
- Modern CLI (color, ASCII art, status icons) via [Rich](https://github.com/Textualize/rich)

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

# Quick start
python cli.py --scan

# Custom scan: 15s timeout, ignore weak signals
python cli.py --scan --timeout 20 --min-rssi -80 --output-dir results/

#Batch/Scheduled Scanning (Linux/macOS cron example)
# Run every day at 3am, save with timestamp
0 3 * * * cd /path/to/bluetooth-risk-scanner && .venv/bin/python cli.py --scan --output-dir /path/to/reports/$(date +\%F
```

### 🔣 CLI Options
- `--timeout`: Scanning timeout in seconds (default: 10)
- `--min-rssi`: Minimum RSSI threshold to filter out weak signals (default: -100)
- `--output-dir <folder>`: Save reports to this directory

📊 Reporting & Output
- **HTML Report**: Color-coded severity (Low/Medium/High/Critical), sortable/filterable, device fingerprint summary, recommendations, explanations per finding.
- **JSON Report**: Structured data for automation or further offline analysis.
- **Sample Output**: See [Sample HTML Report](docs/sample_report.html), [See Sample JSON report](docs/sample_report.json).

Reports are saved to:
- `output/scan_report.json`
- `output/scan_report.html` 

### 📸 Sample Output

![Sample HTML Report](doc/report.png)


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
