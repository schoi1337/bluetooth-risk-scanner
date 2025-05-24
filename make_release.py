# make_release.py
# This script creates a ZIP archive containing the Bluetooth Risk Scanner for release or portfolio sharing.

import zipfile
from pathlib import Path

def make_release_zip():
    # Define files and folders to include
    files_to_include = [
        "ble_sniffer.py",
        "cve_lookup.py",
        "risk_analyzer.py",
        "report_generator.py",
        "requirements.txt",
        "README.md"
    ]

    folders_to_include = ["example_reports"]

    output_dir = Path("dist")
    output_zip = output_dir / "bluetooth-risk-scanner.zip"

    output_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in files_to_include:
            path = Path(file)
            if path.exists():
                zipf.write(path, arcname=path.name)

        for folder in folders_to_include:
            folder_path = Path(folder)
            if folder_path.exists() and folder_path.is_dir():
                for file_path in folder_path.rglob("*"):
                    if file_path.is_file():
                        zipf.write(file_path, arcname=file_path.relative_to(Path(".")))

    print(f"[+] Release zip created: {output_zip.resolve()}")

if __name__ == "__main__":
    make_release_zip()
