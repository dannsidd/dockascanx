import json
import os
from datetime import datetime
from pathlib import Path

def summarize_vulns(data):
    summaries = []
    if isinstance(data, dict):
        results = data.get("Results", [])
    elif isinstance(data, list):
        results = data
    else:
        return summaries

    for result in results:
        vulns = result.get("Vulnerabilities", [])
        if not vulns:
            continue

        for vuln in vulns:
            summaries.append({
                "CVE": vuln.get("VulnerabilityID", "N/A"),
                "Package": vuln.get("PkgName", "N/A"),
                "Installed": vuln.get("InstalledVersion", "N/A"),
                "Fixed": vuln.get("FixedVersion", "N/A"),
                "Severity": vuln.get("Severity", "UNKNOWN"),
                "Title": vuln.get("Title", "No description provided."),
                "URL": vuln.get("PrimaryURL", ""),
            })
    return summaries


def ai_fix_recommendation(vuln):
    """Simple AI-style logic for remediation."""
    fixed = vuln.get("Fixed")
    severity = vuln.get("Severity", "UNKNOWN").upper()
    pkg = vuln.get("Package")

    if not fixed or fixed.lower() in ["none", "null", "n/a"]:
        return f"⚠️ No fixed version yet. Monitor {pkg} for security updates."
    else:
        if severity in ["CRITICAL", "HIGH"]:
            return f"🩹 Upgrade {pkg} to {fixed} immediately."
        elif severity == "MEDIUM":
            return f"🔧 Consider updating {pkg} to {fixed} soon."
        else:
            return f"ℹ️ Optional update to {fixed} for best security hygiene."


def generate_html_report(vulns, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>DockaScanX AI Remediation Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; background: #0d1117; color: #e6edf3; }}
            h1 {{ color: #00ffb3; text-align: center; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ border: 1px solid #444; padding: 8px; text-align: left; }}
            th {{ background-color: #161b22; color: #00ffb3; }}
            tr:nth-child(even) {{ background-color: #161b22; }}
            tr:hover {{ background-color: #21262d; }}
        </style>
    </head>
    <body>
        <h1>🚀 DockaScanX AI Remediation Report</h1>
        <p>Generated on: {now}</p>
        <table>
            <tr>
                <th>CVE</th>
                <th>Package</th>
                <th>Installed</th>
                <th>Fixed Version</th>
                <th>Severity</th>
                <th>AI Suggestion</th>
            </tr>
    """

    for v in vulns:
        suggestion = ai_fix_recommendation(v)
        html += f"""
        <tr>
            <td><a href="{v.get("URL")}" target="_blank" style="color:#58a6ff;">{v.get("CVE")}</a></td>
            <td>{v.get("Package")}</td>
            <td>{v.get("Installed")}</td>
            <td>{v.get("Fixed") or "N/A"}</td>
            <td>{v.get("Severity")}</td>
            <td>{suggestion}</td>
        </tr>
        """

    html += """
        </table>
    </body>
    </html>
    """

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n✅ AI Remediation Report saved to: {output_path}")
    print("📂 Opening in browser...")
    os.startfile(output_path)


def main():
    file_path = input("Enter Trivy JSON file path: ").strip()
    if not os.path.exists(file_path):
        print("❌ File not found.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    vulns = summarize_vulns(data)
    if not vulns:
        print("✅ No vulnerabilities found.")
        return

    output_path = f"reports/ai_remediation_report.html"
    generate_html_report(vulns, output_path)


if __name__ == "__main__":
    main()
