import json
import os
from glob import glob

def get_latest_trivy_json(scan_folder="scan_results"):
    """Return the path to the latest Trivy JSON scan file"""
    json_files = glob(os.path.join(scan_folder, "*.json"))
    if not json_files:
        print(f"[!] No JSON files found in {scan_folder}")
        return None
    # Sort by modified time, descending
    latest_file = max(json_files, key=os.path.getmtime)
    return latest_file

def generate_fixed_dockerfile(trivy_json_path):
    """Generate an auto-fixed Dockerfile from Trivy JSON report without hard version pins."""
    with open(trivy_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Collect all package names that appear as vulnerable
    vulnerable_packages = set()
    for result in data:
        if isinstance(result, dict):
            for vuln in result.get("Vulnerabilities", []) or []:
                pkg_name = vuln.get("PkgName")
                if pkg_name:
                    vulnerable_packages.add(pkg_name)
        else:
            # Skip if result is a string or unexpected type
            continue

    # Default base image
    dockerfile_lines = [
        "FROM python:3.8-slim",
        "",
        "# Install latest patched versions of vulnerable packages",
    ]

    if vulnerable_packages:
        # Convert set to sorted list
        pkg_list = " \\\n    ".join(sorted(vulnerable_packages))
        dockerfile_lines.append(
            f"RUN apt-get update && apt-get install -y --no-install-recommends \\\n    {pkg_list} \\\n && apt-get clean && rm -rf /var/lib/apt/lists/*"
        )
    else:
        dockerfile_lines.append("# No vulnerable packages detected, no fixes required")

    dockerfile_lines.append("")
    dockerfile_lines.append("# Copy application files")
    dockerfile_lines.append("COPY app /app")
    dockerfile_lines.append("WORKDIR /app")
    dockerfile_lines.append("")
    dockerfile_lines.append("# Default command")
    dockerfile_lines.append('CMD ["python3"]')

    # Write Dockerfile
    output_path = "Dockerfile.auto-fixed"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(dockerfile_lines))

    print(f"[+] Auto-fixed Dockerfile generated at: {output_path}")


# --- Main ---
if __name__ == "__main__":
    os.makedirs("scan_results", exist_ok=True)
    latest_json = get_latest_trivy_json()
    if latest_json:
        print(f"[+] Using latest Trivy scan file: {latest_json}")
        generate_fixed_dockerfile(latest_json)
    else:
        print("[!] No Trivy scan file found. Please run the scanner first.")
