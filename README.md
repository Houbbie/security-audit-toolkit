Markdown

# 🛡️ Security Audit & PoC Toolkit

**Geautomatiseerde detectie, validatie en forensische analyse van secrets in broncode.**

Deze repository bevat een verzameling Python-scripts ontworpen om de output van security scanners (zoals **Gitleaks** en **TruffleHog**) te verwerken. Het gaat verder dan simpele detectie: deze toolkit biedt "Proof of Concept" (PoC) scripts om de impact van gevonden lekken technisch te valideren en "verwijderde" secrets in de Git-historie op te sporen.

---

## ⚠️ Disclaimer

**Alleen voor educatief en ethisch gebruik.**

Gebruik deze tools nooit op repositories waarvan u niet de eigenaar bent of waarvoor u geen expliciete schriftelijke toestemming heeft voor een security audit. De validatie-scripts voeren lokale cryptografische checks uit en maken standaard geen verbinding met externe netwerken.

---

## 🚀 Features

Deze toolkit pakt de grootste uitdagingen in Secret Management aan:

* **📊 Analyse & Prioritering (`analyze_secrets.py`)**
    * Combineert JSON-output van Gitleaks en TruffleHog.
    * Berekent **Shannon Entropie** om onderscheid te maken tussen echte cryptografische sleutels (hoog risico) en false positives (lage entropie).
    * Genereert een schone rapportage-tabel.

* **🔑 Cryptografische Validatie (`validate_keys.py`)**
    * Probeert gevonden private keys (PEM/RSA) daadwerkelijk te parsen met de `cryptography` library.
    * Checkt of sleutels beveiligd zijn met een wachtwoord.
    * Detecteert zwakke encryptie (bijv. 512-bit RSA).

* **📝 Contextuele Analyse (`reveal_passwords.py`)**
    * Inspecteert de broncode rondom gevonden wachtwoorden.
    * Bepaalt of een wachtwoord gekoppeld is aan actieve resources (zoals een Database of VM in Terraform code).

* **👻 Forensisch Onderzoek (`git_history_revealer.py`)**
    * Zoekt naar "Ghost Secrets": wachtwoorden die uit de bestanden zijn verwijderd, maar nog steeds bestaan in de `.git` geschiedenis.
    * Demonstreert waarom `git rm` onvoldoende is voor het verwijderen van gevoelige data.

---

## 📦 Installatie

1.  **Clone deze repository:**
    ```bash
    git clone [https://github.com/JOUW_GEBRUIKERSNAAM/security-audit-toolkit.git](https://github.com/JOUW_GEBRUIKERSNAAM/security-audit-toolkit.git)
    cd security-audit-toolkit
    ```

2.  **Installeer dependencies:**
    De scripts maken gebruik van de standaard Python libraries, plus `cryptography` voor validatie.
    ```bash
    pip install -r requirements.txt
    ```

---

## 🛠️ Gebruikshandleiding

### Stap 1: Voorbereiding (Scannen)
Zorg dat u `gitleaks` of `trufflehog` lokaal heeft geïnstalleerd en draai een scan op uw **doel-repository**. Sla de output op in de root van deze toolkit.

```bash
# Voorbeeld Gitleaks scan
gitleaks detect --source="/pad/naar/doel-repo" --report-path="gitleaks.json" --report-format="json"
Stap 2: Analyse
Verwerk de ruwe data tot een leesbaar overzicht.

Bash

python analyze_secrets.py
Stap 3: Validatie (PoC)
Open validate_keys.py of reveal_passwords.py in een teksteditor. Pas de variabele REPO_ROOT in het script aan zodat deze verwijst naar de map van de gescande repository:

Python

# Voorbeeld in validate_keys.py
REPO_ROOT = "/Users/gebruiker/pad/naar/gescande_repo"
Voer vervolgens het script uit:

Bash

python validate_keys.py
Stap 4: Historisch Onderzoek
Om te bewijzen dat verwijderde wachtwoorden nog terug te halen zijn ("Time Machine" hack):

Open git_history_revealer.py.

Zet REPO_ROOT naar de juiste map.

Zet SEARCH_TERM naar een fragment van het wachtwoord dat u zoekt.

Draai het script:

Bash

python git_history_revealer.py
📂 Bestandsstructuur
Plaintext

/security-audit-toolkit
├── analyze_secrets.py       # Aggregator & Entropy calculator
├── validate_keys.py         # Private Key validator
├── reveal_passwords.py      # Code context extractor
├── git_history_revealer.py  # Git log forensics tool
├── requirements.txt         # Python dependencies
├── .gitignore               # Voorkomt uploaden van scan-resultaten
└── README.md                # Deze documentatie
🛡️ Remediatie Advies
Indien deze tools kwetsbaarheden vinden, worden de volgende stappen aangeraden:

Revoke: Trek de gevonden sleutels/certificaten onmiddellijk in.

Rotate: Genereer nieuwe credentials.

Rewrite History: Gebruik tools zoals git-filter-repo of BFG Repo-Cleaner om de data permanent uit de .git database te wissen.

Pre-Commit Hooks: Implementeer automatische scanning in de CI/CD pipeline om herhaling te voorkomen.

Licentie: MIT