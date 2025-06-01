# Bluetooth Risk Scanner 🔍

Bluetooth Risk Scanner passively detects nearby BLE (Bluetooth Low Energy) devices and evaluates them for privacy and security risks — including silent trackers like AirTags, vulnerable wearables, and devices with exposed GATT services.

Unlike simple scanners, this tool classifies threats based on proximity, vendor reputation, advertising behavior, and CVE history.

## 🚀 Features

## 🚀 Features

- Passive BLE scanning using [`bleak`](https://github.com/hbldh/bleak)  
  (Supported on Windows, Linux, and macOS)
- Device information collection: Name, RSSI, UUIDs, Manufacturer ID, MAC address (when available)
- Vendor/OUI detection:  
  Identifies vendor/brand using BLE device MAC (OUI) and manufacturer data, with reputation lookup and CVE mapping
- Flexible risk scoring model:  
  - Proximity-based risk scoring (using RSSI)
  - MAC address analysis (detects static or rotating/random MACs)
  - Known tracker vendor/product detection (Apple, Tile, Samsung, etc. based on OUI and device name patterns)\*
  - GATT service/characteristic collection (collects and matches service and characteristic UUIDs)\*
  - Behavioral anomaly detection (flags MAC or device name switching patterns)\*
- CVE lookups:  
  Automatically maps known vulnerabilities using an offline CVE database matched by vendor/product
- YAML-based risk weights:  
  Supports custom risk scoring weights via a `risk_model.yaml` file (defaults are used if not present)
- HTML/JSON report generation:  
  Generates color-coded reports with severity, explanations, and actionable recommendations
- CLI batch and scheduled scan:  
  Supports batch scanning, cron scheduling, and offline analysis of stored scan logs
- Modern CLI output:  
  Uses the [Rich](https://github.com/Textualize/rich) library for colored output, ASCII art banners, and intuitive status icons

\* **Note:**  
Tracker/vendor detection, GATT fingerprinting, and behavioral anomaly detection are limited to passive analysis based on OUI, device name, and UUID patterns. The tool does not provide device type clustering, advanced behavioral analysis, or real-time tracking capabilities.


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
## 📋 Usage

```bash
# Clone the repository
git clone https://github.com/schoi1337/bluetooth-risk-scanner.git
cd bluetooth-risk-scanner

# (Recommended) Create and activate a Python virtual environment
python -m venv .venv
source .venv/bin/activate    # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Quick start: Run a default scan
python cli.py --scan

# Custom scan: e.g., set a 20s timeout, ignore weak signals, save to a results folder
python cli.py --scan --timeout 20 --min-rssi -80 --output-dir results/

# Batch/Scheduled Scanning (Linux/macOS cron example)
# Run every day at 3am and save results with a date-stamped filename
0 3 * * * cd /path/to/bluetooth-risk-scanner && .venv/bin/python cli.py --scan --output-dir /path/to/reports/$(date +\%F)
```

### 🔣 CLI Options

- `--scan` : Perform a BLE scan (required for scanning).
- `--timeout <seconds>` : Scanning timeout in seconds (default: 10).
- `--min-rssi <dBm>` : Minimum RSSI threshold; filters out devices with weaker signals (default: -100).
- `--output-dir <folder>` : Save scan reports to the specified directory.
- `--json-only` : Output only the JSON report.
- `--html-only` : Output only the HTML report.
- `--offline <jsonfile>` : Analyze a previously saved JSON scan log file (offline analysis mode).
- `--banner` : Display the ASCII art banner and exit.
- `--version` : Print the tool version and exit.

## 📊 Reporting & Output
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
