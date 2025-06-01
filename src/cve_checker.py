# src/cve_checker.py

import requests

def query_nvd(keyword, max_results=5):
    """
    Search NVD for CVEs related to the given keyword (e.g. vendor or product name).
    Returns a list of dicts: [{"id": CVE-ID, "cvss": score}, ...]
    """
    url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    params = {
        "keywordSearch": keyword,
        "resultsPerPage": max_results
    }

    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        results = []
        for item in data.get("vulnerabilities", []):
            cve = item["cve"]
            cve_id = cve["id"]
            cvss = (
                cve.get("metrics", {}).get("cvssMetricV31", [{}])[0]
                .get("cvssData", {}).get("baseScore", 0.0)
            )
            results.append({"id": cve_id, "cvss": cvss})
        return results

    except Exception as e:
        print(f"[!] NVD API error for keyword {keyword}: {e}")
        return []
