import os
import json
import subprocess
from datetime import datetime

def run_trivy_scan(image_name):
    """Run Trivy scan on a Docker image and save JSON report"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"scan_results/scan_{timestamp}.json"
    
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

    # Trivy stores vulnerabilities under data["Results"]
    results = data.get("Results", [])
    for result in results:
        vulnerabilities = result.get("Vulnerabilities") or []
        for vuln in vulnerabilities:
            sev = vuln.get("Severity")
            if sev in severity_count:
                severity_count[sev] += 1

    print("\n--- Vulnerability Summary ---")
    for level, count in severity_count.items():
        print(f"{level}: {count}")
    print("-----------------------------\n")



if __name__ == "__main__":
    os.makedirs("scan_results", exist_ok=True)
    image = input("Enter Docker image name (e.g., vuln-image): ")
    json_path = run_trivy_scan(image)
    if json_path:
        summarize_scan(json_path)
