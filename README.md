---

# 🚀 DockaScanX – AI-Enhanced Container Vulnerability Scanner

**DockaScanX** is an advanced **AI-integrated DevSecOps toolkit** that automates **Docker image vulnerability scanning**, provides **intelligent fix suggestions**, and generates **interactive HTML remediation reports** — empowering teams to **secure containerized applications effortlessly**.

---

## 🧠 Overview

DockaScanX integrates traditional vulnerability scanning tools like **Trivy** with an **AI-driven fix recommendation system**. It not only detects security issues in Docker images but also provides **automated remediation guidance**, **before/after comparisons**, and **ready-to-deploy fixes**.

---

## ✨ Features

### 🔍 Vulnerability Scanning

* Scans Docker images using **Trivy** to detect OS and package vulnerabilities.
* Supports multiple output formats (JSON, HTML).

### 🤖 AI-Enhanced Fix Suggestions

* Analyzes each CVE with context-aware AI remediation.
* Suggests **Dockerfile updates**, **package patches**, and **secure base images**.
* Supports **HTML-based visualization** for easy review.

### 🧩 Auto Dockerfile Fixes

* Automatically updates vulnerable base images or packages.
* Creates **new fixed image** tagged with `-fixed` suffix.

### 📊 Reporting

* Generates detailed **AI Remediation Reports** (`ai_remediation_report.html`).
* Includes vulnerability severity, fix description, and references.

### 🔗 DevSecOps Integration

* Easily integrates into CI/CD pipelines (Jenkins, GitHub Actions, GitLab CI).
* Lightweight CLI execution for automation.

---

## ⚙️ Installation

```bash
git clone https://github.com/<your-org>/dockascanx.git
cd dockascanx
pip install -r requirements.txt
```

Ensure **Trivy** is installed:

```bash
sudo apt install trivy
```

---

## 🧪 Usage Workflow

### 1️⃣ Run a Vulnerability Scan

```bash
python scripts/scan_image.py
```

You’ll be prompted to enter your Docker image name.
Results are saved in `/scan_results/`.

---

### 2️⃣ Apply AI-Enhanced Fix Suggestions

```bash
python scripts/ai_fix_suggestions.py
```

Enter the path to your Trivy JSON result.
An AI-generated remediation report is created under `/reports/ai_remediation_report.html`.

---

### 3️⃣ (Optional) Auto-Fix the Docker Image

```bash
python scripts/fix_vulnerable_image.py
```

DockaScanX automatically:

* Pulls the vulnerable image
* Updates the Dockerfile with secure components
* Builds and tags the **new fixed image**

---

## 📁 Project Structure

```
dockascanx/
│
├── scripts/
│   ├── scan_image.py              # Runs Trivy scans
│   ├── ai_fix_suggestions.py      # AI remediation integration
│   ├── fix_vulnerable_image.py    # Automated Dockerfile fixing
│
├── reports/                       # Generated AI remediation reports
├── scan_results/                  # Raw Trivy scan outputs
├── Dockerfile                     # Sample vulnerable image
├── requirements.txt
└── README.md
```

---

## 📈 Example Output

### ✅ Vulnerability Detected

```
CVE-2022-0563 – util-linux 2.38.1-5+deb12u1
Severity: LOW
Description: Partial disclosure of arbitrary files in chfn and chsh
```

### 💡 AI Fix Suggestion

```
Suggested Action:
Upgrade util-linux to version ≥ 2.37.4
or switch base image to debian:bookworm-20241010
```

### 📄 Generated Report

`reports/ai_remediation_report.html`
Includes severity charts, CVE summaries, and recommended fixes.

---

## 🧩 Capabilities & Limitations

| ✅ What It Can Do               | 🚫 What It Cannot Do               |
| -------------------------------- | ---------------------------------- |
| Automated vulnerability scanning | Fix **all** CVEs automatically     |
| AI-enhanced remediation          | Fix app-level (custom code) issues |
| Auto Dockerfile patching         | Guarantee 100% security            |
| Before/After image comparison    | Run on all OSes (limited support)  |
| Generate visual reports          | Work without Trivy dependency      |

---

## 🛡️ License

**MIT License**
Developed under open-source standards for community use.

---

## 👥 Contributors

* **Dan [@dannsidd]** – Developer & Maintainer

---

## 🌐 Project Links

* 📦 [GitHub Repository](https://github.com/dannsidd/dockascanx)
* 🧰 [Trivy Documentation](https://aquasecurity.github.io/trivy/)
* ⚙️ [Ready Tensor Page (if applicable)](https://readytensor.ai/)

---


