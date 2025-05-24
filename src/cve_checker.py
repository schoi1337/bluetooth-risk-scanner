# src/cve_checker.py
# Queries NVD for CVEs based on vendor keyword

import requests
import time

NVD_BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
DEFAULT_WAIT = 1  # seconds (rate limiting)

def fetch_cves(vendor_name):
    """
    Query NVD for CVEs related to the given vendor name.
    Returns a list of tuples: (CVE ID, CVSS Score)
    """
    try:
        params = {
            "keywordSearch": vendor_name,
            "resultsPerPage": 5,
            "sortBy": "published"
        }
        response = requests.get(NVD_BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        results = []
        for item in data.get("vulnerabilities", []):
            cve_id = item["cve"]["id"]
            metrics = item["cve"].get("metrics", {})
            cvss = "N/A"

            if "cvssMetricV31" in metrics:
                cvss = metrics["cvssMetricV31"][0]["cvssData"]["baseScore"]
            elif "cvssMetricV30" in metrics:
                cvss = metrics["cvssMetricV30"][0]["cvssData"]["baseScore"]
            elif "cvssMetricV2" in metrics:
                cvss = metrics["cvssMetricV2"][0]["cvssData"]["baseScore"]

            results.append((cve_id, cvss))

        time.sleep(DEFAULT_WAIT)
        return results

    except Exception as e:
        print(f"[!] CVE fetch error for '{vendor_name}': {e}")
        return []
