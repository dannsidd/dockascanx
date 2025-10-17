import json
import matplotlib.pyplot as plt
from datetime import datetime

def summarize_scan(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    severity_count = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for result in data:
        for vuln in result.get("Vulnerabilities", []) or []:
            sev = vuln.get("Severity")
            if sev in severity_count:
                severity_count[sev] += 1

    return severity_count

# Input files
vuln_scan = input("Path to vulnerable image JSON scan: ")
fixed_scan = input("Path to fixed image JSON scan: ")

vuln_counts = summarize_scan(vuln_scan)
fixed_counts = summarize_scan(fixed_scan)

# Plotting
labels = list(vuln_counts.keys())
vuln_values = list(vuln_counts.values())
fixed_values = list(fixed_counts.values())

x = range(len(labels))
plt.bar(x, vuln_values, width=0.4, label='Vulnerable Image', align='center')
plt.bar(x, fixed_values, width=0.4, label='Fixed Image', align='edge')
plt.xticks(x, labels)
plt.ylabel("Number of Vulnerabilities")
plt.title("Vulnerability Comparison")
plt.legend()
plt.tight_layout()

# Save chart
chart_file = f"scan_results/vuln_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
plt.savefig(chart_file)
print(f"[+] Vulnerability comparison chart saved at {chart_file}")
plt.show()
