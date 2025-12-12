import json
import math
import os
from dataclasses import dataclass
from typing import List, Dict, Optional

# --- CONFIGURATIE ---
GITLEAKS_FILE = 'gitleaks_results.json'
TRUFFLEHOG_FILE = 'trufflehog_results.json'

@dataclass
class Finding:
    tool: str
    rule_id: str
    file_path: str
    line_number: int
    secret: str
    entropy: float

class SecurityAnalyzer:
    def __init__(self):
        self.findings: List[Finding] = []

    def calculate_shannon_entropy(self, data: str) -> float:
        """
        Berekent de Shannon-entropie van een string.
        Hoge entropie (> 3.5 - 4.0) duidt vaak op willekeurig gegenereerde secrets.
        """
        if not data:
            return 0
        entropy = 0
        for x in range(256):
            p_x = float(data.count(chr(x))) / len(data)
            if p_x > 0:
                entropy += - p_x * math.log(p_x, 2)
        return entropy

    def load_gitleaks(self, filepath: str):
        print(f"[*] Bezig met laden van Gitleaks: {filepath}...")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Gitleaks output is typically a list of dicts
            for item in data:
                secret = item.get('Secret', '')
                self.findings.append(Finding(
                    tool="Gitleaks",
                    rule_id=item.get('RuleID', 'Unknown'),
                    file_path=item.get('File', 'Unknown'),
                    line_number=item.get('StartLine', 0),
                    secret=secret,
                    entropy=self.calculate_shannon_entropy(secret)
                ))
        except FileNotFoundError:
            print(f"[-] Bestand niet gevonden: {filepath}")
        except json.JSONDecodeError:
            print(f"[-] Fout bij parsen JSON: {filepath}")

    def load_trufflehog(self, filepath: str):
        print(f"[*] Bezig met laden van TruffleHog: {filepath}...")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                # Trufflehog filesystem scan output is vaak line-delimited JSON (JSONL)
                # Soms ook een JSON list, afhankelijk van versie/flags. We proberen beide.
                content = f.read()
                
            try:
                # Probeer als normale JSON list
                data = json.loads(content)
                if isinstance(data, dict): data = [data] # Single object case
            except json.JSONDecodeError:
                # Probeer als JSONL (Line delimited)
                data = []
                for line in content.splitlines():
                    if line.strip():
                        data.append(json.loads(line))

            for item in data:
                # Trufflehog v3 structuur extractie
                detector = item.get('DetectorName', 'Unknown')
                source_meta = item.get('SourceMetadata', {})
                data_obj = source_meta.get('Data', {})
                filesystem = data_obj.get('Filesystem', {})
                
                file_path = filesystem.get('file', 'Unknown')
                line_num = filesystem.get('line', 0)
                
                # Secret extractie (soms in Raw, soms elders)
                secret = item.get('Raw', '')
                if not secret and 'RawV2' in item:
                    secret = item['RawV2']

                self.findings.append(Finding(
                    tool="TruffleHog",
                    rule_id=detector,
                    file_path=file_path,
                    line_number=line_num,
                    secret=secret,
                    entropy=self.calculate_shannon_entropy(secret)
                ))

        except FileNotFoundError:
            print(f"[-] Bestand niet gevonden: {filepath}")
        except Exception as e:
            print(f"[-] Algemene fout bij Trufflehog parsing: {e}")

    def generate_report(self):
        print("\n" + "="*80)
        print(f"{'TOOL':<12} | {'TYPE/RULE':<20} | {'ENTROPY':<8} | {'FILE LOCATION'}")
        print("-" * 80)
        
        # Sorteer op entropie (hoogste risico bovenaan)
        sorted_findings = sorted(self.findings, key=lambda x: x.entropy, reverse=True)
        
        for f in sorted_findings:
            # We maskeren de secret voor display, maar tonen wel de locatie
            print(f"{f.tool:<12} | {f.rule_id[:20]:<20} | {f.entropy:.2f}     | {f.file_path}:{f.line_number}")
        
        print("="*80)
        print(f"Totaal aantal potentiële secrets gevonden: {len(self.findings)}")
        
        # Optioneel: Dump details voor PoC vervolgstappen
        # Hier printen we de raw findings in een compact formaat dat de AI makkelijk kan lezen
        print("\n--- RAW DATA FOR AI ANALYSIS (COPY BELOW) ---")
        export_data = [
            {
                "tool": f.tool,
                "rule": f.rule_id,
                "entropy": round(f.entropy, 2),
                "secret_snippet": f.secret[:10] + "..." if len(f.secret) > 10 else f.secret,
                # In een echte omgeving stuur je NOOIT de volledige secret naar een AI. 
                # Voor deze PoC/Demo, als je wilt dat ik de secret valideer, moet ik hem wel 'zien' of 'kennen'.
                # Ik print hier de snippet.
                "location": f"{f.file_path}:{f.line_number}"
            }
            for f in sorted_findings
        ]
        print(json.dumps(export_data, indent=2))
        print("--- END RAW DATA ---")

if __name__ == "__main__":
    analyzer = SecurityAnalyzer()
    
    # Controleer of bestanden bestaan
    if os.path.exists(GITLEAKS_FILE):
        analyzer.load_gitleaks(GITLEAKS_FILE)
    
    if os.path.exists(TRUFFLEHOG_FILE):
        analyzer.load_trufflehog(TRUFFLEHOG_FILE)
        
    if not analyzer.findings:
        print("Geen findings gevonden of bestanden ontbreken.")
        print(f"Zorg dat '{GITLEAKS_FILE}' en/of '{TRUFFLEHOG_FILE}' in deze map staan.")
    else:
        analyzer.generate_report()