import os
import json
import subprocess
from datetime import datetime

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

if __name__ == "__main__":
    os.makedirs("scan_results", exist_ok=True)

    # Step 1: scan original vulnerable image
    vuln_image = input("Enter vulnerable image name (e.g., vuln-image): ")
    json_vuln = run_trivy_scan(vuln_image)
    count_vuln = summarize_scan(json_vuln)

    # Step 2: scan fixed/upgraded image
    fixed_image = input("Enter fixed image name (e.g., vuln-image-fixed): ")
    json_fixed = run_trivy_scan(fixed_image)
    count_fixed = summarize_scan(json_fixed)

    # Step 3: compare
    compare_scans(count_vuln, count_fixed)
