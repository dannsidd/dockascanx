import os
import json
import subprocess
from datetime import datetime
import matplotlib.pyplot as plt

def run_trivy_scan(image_name):
    """Run Trivy scan on a Docker image and save JSON report"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"scan_results/scan_{image_name}_{timestamp}.json"

    print(f"[+] Scanning image: {image_name}")
    cmd = ["trivy", "image", "--quiet", "--format", "json", "-o", output_file, image_name]

    try:
        subprocess.run(cmd, check=True)
        print(f"[+] Scan completed. Report saved to: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"[!] Scan failed: {e}")
        return None

    return output_file

def summarize_scan(json_path):
    """Summarize vulnerability counts by severity"""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    severity_count = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
    results = data.get("Results", [])
    for result in results:
        vulnerabilities = result.get("Vulnerabilities") or []
        for vuln in vulnerabilities:
            sev = vuln.get("Severity")
            if sev in severity_count:
                severity_count[sev] += 1

    return severity_count

def compare_scans(count_before, count_after):
    """Print a comparison table between two scans"""
    print("\n--- Vulnerability Comparison ---")
    print(f"{'Severity':<10}{'Before':>8}{'After':>8}{'Delta':>8}")
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        before = count_before.get(sev, 0)
        after = count_after.get(sev, 0)
        delta = before - after
        print(f"{sev:<10}{before:>8}{after:>8}{delta:>8}")
    print("-------------------------------\n")

def plot_comparison(count_before, count_after):
    """Generate a bar chart comparing before/after counts"""
    severities = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
    before = [count_before.get(s, 0) for s in severities]
    after = [count_after.get(s, 0) for s in severities]

    x = range(len(severities))
    width = 0.35

    plt.figure(figsize=(8,5))
    plt.bar(x, before, width, label='Before', color='red')
    plt.bar([i + width for i in x], after, width, label='After', color='green')
    plt.xticks([i + width/2 for i in x], severities)
    plt.ylabel("Number of Vulnerabilities")
    plt.title("Vulnerabilities Before and After Fix")
    plt.legend()
    plt.tight_layout()
    chart_file = f"scan_results/vuln_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(chart_file)
    plt.show()
    print(f"[+] Chart saved to {chart_file}")

if __name__ == "__main__":
    os.makedirs("scan_results", exist_ok=True)

    # Step 1: Scan original vulnerable image
    vuln_image = input("Enter vulnerable image name (e.g., vuln-image): ")
    json_vuln = run_trivy_scan(vuln_image)
    if json_vuln is None:
        print("[!] Vulnerable image scan failed. Exiting.")
        exit(1)
    count_vuln = summarize_scan(json_vuln)

    # Step 2: Scan fixed image
    fixed_image = input("Enter fixed image name (e.g., vuln-image-fixed): ")
    json_fixed = run_trivy_scan(fixed_image)
    if json_fixed is None:
        print("[!] Fixed image scan failed. Exiting.")
        exit(1)
    count_fixed = summarize_scan(json_fixed)

    # Step 3: Compare and print table
    compare_scans(count_vuln, count_fixed)

    # Step 4: Generate visual chart
    plot_comparison(count_vuln, count_fixed)
