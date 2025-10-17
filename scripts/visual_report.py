# scripts/visual_report.py (fixed for newer Trivy JSON)

import json
import os
from datetime import datetime
import matplotlib.pyplot as plt

SCAN_RESULTS_DIR = "scan_results"
REPORTS_DIR = "reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

# Find latest scan JSON
scan_files = sorted([f for f in os.listdir(SCAN_RESULTS_DIR) if f.endswith(".json")])
if not scan_files:
    print("[!] No scan JSON files found.")
    exit(1)

latest_scan_file = os.path.join(SCAN_RESULTS_DIR, scan_files[-1])
print(f"[+] Using latest scan file: {latest_scan_file}")

# Load scan data
with open(latest_scan_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Trivy v0.67+ format uses "Results" key
results = data.get("Results", []) if isinstance(data, dict) else data

# Summarize vulnerabilities
severity_count = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
for result in results:
    vulns = result.get("Vulnerabilities") or []
    for vuln in vulns:
        sev = vuln.get("Severity")
        if sev in severity_count:
            severity_count[sev] += 1

print("\n--- Vulnerability Summary ---")
for sev, count in severity_count.items():
    print(f"{sev}: {count}")
print("-----------------------------\n")

# Pie chart
plt.figure(figsize=(6, 6))
plt.pie(severity_count.values(), labels=severity_count.keys(), autopct='%1.1f%%', startangle=140)
plt.title("Vulnerability Severity Distribution")
chart_file = os.path.join(REPORTS_DIR, "vuln_chart.png")
plt.savefig(chart_file)
plt.close()
print(f"[+] Chart saved to: {chart_file}")

# HTML report
html_file = os.path.join(REPORTS_DIR, f"DockaScanX_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")
html_content = f"""
<html>
<head><title>DockaScanX Vulnerability Report</title></head>
<body>
    <h1>DockaScanX Vulnerability Report</h1>
    <h2>Scan File: {latest_scan_file}</h2>
    <h2>Summary</h2>
    <ul>
        <li>CRITICAL: {severity_count['CRITICAL']}</li>
        <li>HIGH: {severity_count['HIGH']}</li>
        <li>MEDIUM: {severity_count['MEDIUM']}</li>
        <li>LOW: {severity_count['LOW']}</li>
    </ul>
    <h2>Severity Distribution</h2>
    <img src="{os.path.basename(chart_file)}" alt="Vulnerability Chart">
</body>
</html>
"""

with open(html_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"[+] HTML report generated: {html_file}")
print("[+] Open this HTML file in your browser to view the report.")
