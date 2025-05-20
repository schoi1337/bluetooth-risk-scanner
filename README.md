# Bluetooth Risk Scanner (Ubertooth Edition)

> Passive BLE risk assessment using [Ubertooth One](https://greatscottgadgets.com/ubertooth/)

This branch enables **passive BLE scanning without a Bluetooth dongle**, using Ubertooth and real-time packet parsing. It builds on the main `bluetooth-risk-scanner` project but replaces active scanning with advertisement packet sniffing.

## 🔍 Key Features

- Real-time BLE advertisement sniffing via `ubertooth-btle -n`
- Risk evaluation based on:
  - MAC vendor prefix
  - Local name keyword matching
- IEEE OUI-based MAC → Vendor mapping
- Auto-generated HTML risk report with color-coded severity

## 📦 Requirements

- **Hardware:** Ubertooth One  
- **Dependencies:**

```bash
  sudo apt install libbtbb-dev
  brew install ubertooth      # (macOS)
```

Python packages:

```bash
pip install -r requirements.txt
```

## 📁 Example Output

| MAC                 | Name         | Vendor         | RSSI | Risk    |
| ------------------- | ------------ | -------------- | ---- | ------- |
| 22:33:44:55:66:77   | LockPad 3000 | Xiaomi Inc.    | -45  | 🔴 High |
| AA\:BB\:CC:11:22:33 | ToySensor    | Unknown Vendor | -78  | 🟢 Low  |

## 📂 Project Structure

```bash
scanner/
├── ble_sniffer.py        # Ubertooth-based passive scan
utils/
├── risk_database.py      # Keyword & MAC risk logic
├── oui_lookup.py         # OUI DB loading + lookup
report/
├── report_generator.py   # HTML report builder
data/
└── oui.csv               # IEEE OUI vendor database
```

## 🧪 Test Mode (Optional)

Use a saved Ubertooth log and simulate parsing without hardware.

## 🧠 Credits
- Built on top of [Great Scott Gadgets Ubertooth](https://github.com/greatscottgadgets/ubertooth)
- IEEE OUI DB via https://standards-oui.ieee.org/oui/

## 📌 Branch Purpose

This branch is experimental and designed for environments without a BLE dongle.
It demonstrates how passive BLE analysis can be used for risk-aware reconnaissance using commodity hardware.