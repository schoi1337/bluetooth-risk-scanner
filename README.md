# Bluetooth Risk Scanner 🛡️🔍

>[!Note]
>This is currently under development

Bluetooth Risk Scanner is a lightweight tool designed to scan nearby Bluetooth devices and identify potential privacy and security risks associated with them.

It doesn't just list devices — it checks if they belong to vendors known for privacy issues, previous data breaches, or are associated with recent Bluetooth vulnerabilities (CVEs).

## 🚀 Features
- Scan nearby Bluetooth (BLE) devices
- Detect vendors with known privacy concerns
- Highlight devices linked to past security incidents
- Cross-reference devices against recent Bluetooth CVEs
- Display results in terminal and save as JSON
- Generate results as a visual HTML report

### 📊 Comparison with Other Tools

| Tool | Main Features | Bluetooth Risk Scanner |
|:---|:---|:---|
| **Btlejuice** | BLE Man-in-the-Middle attack framework | Focuses on **risk detection**, not active attacks. |
| **BLE Scanner App** | iOS/Android BLE device discovery | Focuses on **security/privacy risk analysis**, not just listing devices. |
| **gatttool (deprecated)** | CLI tool for basic BLE scanning | Offers **risk evaluation, CVE matching, and reporting** on top of scanning. |
| **Nmap Bluetooth Scripts** | Limited Bluetooth scanning scripts | Specializes in **BLE-centric risk analysis and CVE tracking**. |
| **Armis** | Enterprise IoT and BLE device risk management | Provides a **lightweight, free BLE risk detection tool** instead of expensive enterprise SaaS solutions. |
| **Asimily** | BLE/IoT risk detection for healthcare and industrial environments |  **Focuses specifically on BLE device privacy and vulnerabilities**, and does not target general security of IoT environments. |
| **Ordr** | IoT and medical device visibility and risk management |  **Specializes in targeted BLE device risk scanning**, not for full asset management |
| **Nozomi Networks** | Industrial control system (ICS) cybersecurity | **Analyze BLE risks in real-world physical spaces**, does not focus on industrial networks. |
| **Forescout** | Device detection and risk management across networks and IoT | Provide a **simple, deployable BLE risk analysis tool**, not designed for large enterprise network environments. |

## 🎯 Bluetooth Risk Scanner is designed for:

- **Security Researchers**  
  Quickly identify BLE device vulnerabilities and privacy risks during security assessments.
- **Penetration Testers**  
  Add BLE risk detection to physical and wireless security engagements.
- **Red Team Operators**  
  Map nearby BLE device exposures without intrusive scans.
- **IoT/OT Security Analysts**  
  Assess the risk posture of Bluetooth-enabled assets.
- **Privacy Advocates**  
  Detect and highlight BLE devices from vendors known for privacy issues.
- **Cybersecurity Students and Enthusiasts**  
  Learn BLE device security analysis with an easy-to-use open-source tool.

## 🛠️ Installation
```bash
git clone https://github.com/schoi1337/bluetooth-risk-scanner.git
cd bluetooth-risk-scanner
pip install -r requirements.txt
```
> Note: This tool requires a Bluetooth adapter and Python 3.8+.

## 📋 Usage
```bash
python main.py
```

The results will be displayed in the terminal and saved to `output/scan_results.json`.

## 📈 Generating a Scan Report (HTML)

After scanning, you can generate a visual HTML report:

```bash
python generate_report.py
```

The report will be saved as `output/report.html`. Open it in your browser to view the results.

## 🧠 How it Works
- Performs a Bluetooth Low Energy (BLE) scan.
- Checks device names against internal risk databases. (`/data`)
- Optionally, matches devices against known Bluetooth CVEs.

## 🗺️ Roadmap
- [ ] Improve MAC address to vendor matching accuracy (expand OUI database)
- [ ] Integrate CVE database lookup (NVD API integration)
- [ ] Add more privacy risk indicators based on BLE advertisement data
- [ ] Introduce scoring weight configuration for flexible risk assessment
- [ ] Optimize BLE device scanning performance
- [ ] Implement HTML report generation alongside JSON output
- [ ] Add CLI options for advanced scanning parameters (e.g., custom timeout, filter)
- [ ] Prepare full documentation with examples and API references

## 🤝 Contributing
Contributions are welcome!
Feel free to fork the repository, open an issue, or submit a pull request.

## 📄 License
This project is licensed under the MIT License.
