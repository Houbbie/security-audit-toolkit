# security-audit-toolkit
# 🛡️ Security Audit & PoC Toolkit

**Automated Secret Detection, Validation, and Forensic Analysis tools.**

This repository contains a collection of Python scripts designed to automate the post-processing of security scans (Gitleaks/TruffleHog). It goes beyond detection by providing Proof of Concept (PoC) tools to validate the impact of found secrets.

## 🚀 Features

* **`analyze_secrets.py`**: Aggregates JSON output from Gitleaks and TruffleHog. Calculates **Shannon Entropy** to distinguish between false positives and high-risk keys.
* **`validate_keys.py`**: Cryptographically validates found PEM/RSA files. Checks for key size (e.g., weak 512-bit keys) and password protection.
* **`reveal_passwords.py`**: Extracts context around hardcoded secrets in source files to determine if they are tied to active resources.
* **`git_history_revealer.py`**: A forensic tool that hunts through `git log` to find secrets that were "deleted" but remain in the version history (Ghost Secrets).

## 📦 Installation

1.  Clone this repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## 🛠️ Usage

### 1. Analysis
Place your `gitleaks.json` in the root and run:
```bash
python analyze_secrets.py
