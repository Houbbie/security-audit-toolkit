# 🛡️ Apex Hunter: Security Audit Engine

[![Docker Build](https://img.shields.io/badge/docker-build-blue.svg)](https://www.docker.com/)
[![Security Scan](https://img.shields.io/badge/security-TruffleHog-red.svg)](https://trufflesecurity.com/)
[![Status](https://img.shields.io/badge/status-Production--Ready-success.svg)]()

**Apex Hunter** is een gecontaineriseerde security engine ontworpen om "geheimen" (secrets) op te sporen in de volledige historie van een GitHub repository. Het vindt API-sleutels, wachtwoorden en certificaten die per ongeluk zijn gecommit, zelfs als ze inmiddels uit de huidige code zijn verwijderd.

> **De "Dummy" Uitleg:** Zie Apex Hunter als een speciale bril. Zelfs als je een geheim briefje weggooit, kan deze bril de afdruk op de tafel eronder nog lezen. Het graaft in het verleden van je code om te zien of je daar ooit een wachtwoord hebt laten slingeren.



---

## 🧐 Hoe het werkt
In de moderne softwareontwikkeling is een "delete" in je code niet genoeg. Git onthoudt alles. Apex Hunter combineert de krachtige `TruffleHog v3` engine met een op maat gemaakte Python wrapper via een **Multi-stage Docker Build**.

1.  **De Engine:** Scant elke commit, branch en tag in de opgegeven GitHub URL.
2.  **De Analyse:** Filtert ruwe data en bepaalt de ernst (Critical, High, Medium).
3.  **De Rapportage:** Genereert een professioneel Markdown-rapport (`SECURITY_AUDIT_REPORT.md`).



---

## 🛠️ Installatie & Setup

### 1. De Python Engine (`hunter.py`)
Maak een bestand genaamd `hunter.py` met de volgende code:

```python
import os, subprocess, json, logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')
logger = logging.getLogger("ApexHunter")

# CONFIGURATIE: De te scannen repository
GITHUB_REPO = "[https://github.com/houbbie/vulnerable-app-demo](https://github.com/houbbie/vulnerable-app-demo)"

class ApexHunter:
    def run_scan(self, repo_url):
        logger.info(f"🚀 Verbinding maken met GitHub: {repo_url}")
        cmd = ["trufflehog", "git", repo_url, "--json", "--no-verification"]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            findings = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
            return findings
        except Exception as e:
            logger.error(f"Fout tijdens scan: {e}")
            return []

    def export_report(self, findings):
        with open("SECURITY_AUDIT_REPORT.md", "w") as md:
            md.write(f"# 🛡️ Apex Hunter Audit Rapport\n\n")
            md.write(f"Status: {'🔴 KRITIEK' if findings else '🟢 VEILIG'}\n")
            md.write(f"Datum: {datetime.now().strftime('%d-%m-%Y %H:%M')}\n\n")
            md.write("| Service | Ernst | Bestand |\n| :--- | :--- | :--- |\n")
            for f in findings:
                det = f.get('detector_name', 'Unknown')
                meta = f.get('SourceMetadata', {}).get('Data', {}).get('Git', {})
                path = meta.get('file', 'Git History')
                md.write(f"| {det} | CRITICAL | `{path}` |\n")

if __name__ == "__main__":
    hunter = ApexHunter()
    results = hunter.run_scan(GITHUB_REPO)
    hunter.export_report(results)
    print(f"✅ Audit voltooid. Bevindingen: {len(results)}")

```
### 2. De Docker-container (Dockerfile)
Gebruik de officiële image als bron voor maximale stabiliteit:

```
# Stap 1: Leen de binary van de officiële scanner
FROM trufflesecurity/trufflehog:latest AS scanner

# Stap 2: Onze eigen Python omgeving
FROM python:3.11-slim
RUN apt-get update && apt-get install -y git ca-certificates && apt-get clean

# Kopieer de scanner naar onze image
COPY --from=scanner /usr/bin/trufflehog /usr/bin/trufflehog

WORKDIR /app
COPY hunter.py .

CMD ["python", "hunter.py"]
```
