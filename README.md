# **🛡️ Apex Hunter: Security Audit Engine**

**Apex Hunter** is een gecontaineriseerde security engine ontworpen om "geheimen" (secrets) op te sporen in de volledige historie van een GitHub repository. Het vindt API-sleutels, wachtwoorden en certificaten die per ongeluk zijn gecommit, zelfs als ze inmiddels uit de huidige code zijn verwijderd.

---

## **📖 Inhoudsopgave**

1. [Hoe het werkt](https://www.google.com/search?q=%23-hoe-het-werkt&authuser=1)
2. [Systeemvereisten](https://www.google.com/search?q=%23-systeemvereisten&authuser=1)
3. [Installatie & Setup](https://www.google.com/search?q=%23-installatie--setup&authuser=1)
4. [Gebruik](https://www.google.com/search?q=%23-gebruik&authuser=1)
5. [Het Rapport Begrijpen](https://www.google.com/search?q=%23-het-rapport-begrijpen&authuser=1)
6. [Incident Response Playbook](https://www.google.com/search?q=%23-incident-response-playbook&authuser=1)
7. [Probleemoplossing](https://www.google.com/search?q=%23-probleemoplossing&authuser=1)

---

## **🧐 Hoe het werkt**

In de moderne softwareontwikkeling is een "delete" in je code niet genoeg. Git onthoudt alles. Apex Hunter gebruikt een **Multi-stage Docker Build** om de krachtige TruffleHog v3 engine te combineren met een op maat gemaakte Python wrapper.

1. **De Engine:** Scant elke commit, branch en tag in de opgegeven GitHub URL.
2. **De Analyse:** Filtert ruwe data en bepaalt de ernst (Critical, High, Medium).
3. **De Rapportage:** Genereert een Markdown-bestand dat direct bruikbaar is voor security-audits.

---

## **💻 Systeemvereisten**

* **Docker Desktop:** Geïnstalleerd en actief.
* **Git:** Voor het beheren van je broncode.
* **GitHub Account:** Met een repository om te scannen.

---

## **🛠️ Installatie & Setup**

### **1. Bestanden voorbereiden**

Zorg dat de volgende twee bestanden in je projectmap staan:

* **hunter.py**: De logica van de audit.
* **Dockerfile**: De instructies voor de Docker-container.

### **2. De Engine Bouwen**

Open je terminal en voer het volgende commando uit om de Docker-image te maken:

| Bashdocker build -t apex-hunter-engine . |
| :---- |

---

## **🚀 Gebruik**

Om een scan uit te voeren op je repository, gebruik je het onderstaande commando. De -v vlag zorgt ervoor dat het rapport direct op je lokale machine (je MacBook) wordt opgeslagen.

| Bashdocker run -it -v "$(pwd):/app" apex-hunter-engine |
| :---- |

### **Wat gebeurt er tijdens de run?**

* De container start op en zoekt naar de geconfigureerde GitHub URL.
* TruffleHog analyseert de gehele Git-historie.
* Het script hunter.py vangt de resultaten op en schrijft deze naar SECURITY\_AUDIT\_REPORT.md.

---

## **📊 Het Rapport Begrijpen**

Na de scan vind je een bestand genaamd SECURITY\_AUDIT\_REPORT.md.

* **🔴 KRITIEK:** Er zijn actieve keys gevonden (bijv. AWS, Azure, Private Keys).
* **🟠 HOOG:** Er zijn API-sleutels gevonden (bijv. Stripe, Slack, Twilio).
* **🟢 VEILIG:** Er zijn geen lekken gevonden in de historie.

---

## **🚨 Incident Response Playbook**

Wat moet je doen als Apex Hunter een lek vindt?

1. **Revoke:** Deactiveer de sleutel onmiddellijk in het dashboard van de provider (bijv. AWS Console).
2. **Rotate:** Genereer een nieuwe sleutel.
3. **Remediate:** Gebruik tools zoals BfG Repo-Cleaner of git-filter-repo om de historie van je GitHub repo te wissen. *Alleen de code aanpassen is niet voldoende!*

---

## **❓ Probleemoplossing**

| Probleem                 | Oplossing                                                                                                                          |
| :----------------------- | :--------------------------------------------------------------------------------------------------------------------------------- |
| Repository not found     | Controleer of de URL in hunter.py correct is en of de repo publiek is (of gebruik een token).                                      |
| Docker permission denied | Zorg dat Docker Desktop actief is en je de juiste rechten hebt op de map.                                                          |
| 0 Findings               | Gefeliciteerd\\! Of je hebt de "Push Protection" van GitHub nog aanstaan waardoor je test-keys nooit op de server zijn aangekomen. |

---

## **🤖 CI/CD Integratie (GitHub Actions)**

Het handmatig draaien van een scan is goed, maar automatische controle bij elke "push" is beter. Hiermee voorkom je dat een lek ooit de productie-omgeving bereikt.

### **Automatische Security Scan instellen**

1. Maak in je project de mappenstructuur aan: `.github/workflows/`
2. Maak hierin een bestand genaamd `security-scan.yml`.
3. Plak de volgende configuratie in dat bestand:

| YAMLname: Apex Hunter Security Auditon:  push:    branches: [ main ]  pull\_request:    branches: [ main ]jobs:  audit:    runs-on: ubuntu-latest    steps:      - name: Checkout code        uses: actions/checkout@v3        with:          fetch-depth: 0 \\# Nodig om de volledige historie te scannen      - name: Build Apex Hunter Engine        run: docker build -t apex-hunter-engine .      - name: Run Security Audit        run: docker run apex-hunter-engine      - name: Upload Audit Rapport        uses: actions/upload-artifact@v3        if: always() \\# Upload het rapport ook als er lekken zijn gevonden        with:          name: security-audit-report          path: SECURITY\_AUDIT\_REPORT.md |
| :---- |

### **Wat gebeurt er nu?**

* **Shift Left Security:** Elke keer dat jij of een teamgenoot code pusht naar GitHub, start de Apex Hunter Engine automatisch.
* **Failsafe:** Als er een geheim wordt gevonden, kun je de "build" laten falen, zodat de onveilige code nooit live gaat.
* **Artifacts:** Het gegenereerde `SECURITY_AUDIT_REPORT.md` wordt opgeslagen bij de GitHub Action-run, zodat je het altijd kunt teruglezen.

**📄 Licentie & Auteur**

Ontwikkeld door **Edwin Houben**.

*Disclaimer: Deze tool is uitsluitend bedoeld voor educatieve doeleinden en geautoriseerde security-audits.*

