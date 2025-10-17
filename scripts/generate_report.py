import json
from jinja2 import Template
from weasyprint import HTML

# Load scan JSON
vuln_scan = "scan_results/scan_vuln-image_20251015_203344.json"
fixed_scan = "scan_results/scan_vuln-image-fixed_20251015_221720.json"

with open(vuln_scan, "r") as f:
    vuln_data = json.load(f)

with open(fixed_scan, "r") as f:
    fixed_data = json.load(f)

# Count vulnerabilities
def count_severity(data):
    counts = {"CRITICAL":0,"HIGH":0,"MEDIUM":0,"LOW":0}
    for result in data:
        for vuln in result.get("Vulnerabilities", []) or []:
            sev = vuln.get("Severity")
            if sev in counts:
                counts[sev] += 1
    return counts

vuln_counts = count_severity(vuln_data)
fixed_counts = count_severity(fixed_data)

# HTML template
html_template = """
<h1>DockaScanX Vulnerability Report</h1>
<h2>Summary</h2>
<table border="1" cellpadding="5">
<tr><th>Severity</th><th>Vulnerable Image</th><th>Fixed Image</th></tr>
{% for sev in counts.keys() %}
<tr>
<td>{{ sev }}</td>
<td>{{ counts[sev] }}</td>
<td>{{ fixed_counts[sev] }}</td>
</tr>
{% endfor %}
</table>
<img src="vuln_comparison.png" alt="Comparison Chart">
"""

template = Template(html_template)
html_content = template.render(counts=vuln_counts, fixed_counts=fixed_counts)

# Save PDF
report_file = "scan_results/DockaScanX_Report.pdf"
HTML(string=html_content).write_pdf(report_file)
print(f"[+] PDF report generated at {report_file}")
