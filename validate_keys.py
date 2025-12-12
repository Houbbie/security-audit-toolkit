import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# --- CONFIGURATIE ---
# PAS DIT AAN: Het volledige pad naar de map die je gescand hebt
REPO_ROOT = "/Users/edwinhouben/Development/security_poc/target_repo_dev/"
# De relatieve paden gevonden door Gitleaks/Trufflehog
TARGET_FILES = [
    "modules/_10_ssl_copy_files/test",
    "ota/certs/test.local.com-root.key",
    "ota/certs/test.local.com.key",
    # We voegen de terraform state toe om het bestaan te verifieren
    "ota/gw-vs-1-tier2/terraform.tfstate" 
]

def analyze_path(relative_path):
    # Bouw het volledige pad
    full_path = os.path.join(REPO_ROOT, relative_path)
    print(f"\n[*] Analyseren van: {full_path}")
    
    if not os.path.exists(full_path):
        print(f"    [-] Bestand NIET gevonden. Controleer of '{REPO_ROOT}' klopt.")
        return

    # Check 1: Is het een Terraform State file?
    if full_path.endswith(".tfstate") or full_path.endswith(".tfstate.backup"):
        print(f"    [!] KRITIEK: Terraform State file gevonden.")
        print(f"    [!] RISICO: State files bevatten ALTIJD secrets in plain-text.")
        print(f"    [i] Advies: Migreer naar Remote State (S3 + DynamoDB) met encryptie.")
        return

    # Check 2: Is het een Private Key?
    try:
        with open(full_path, "rb") as key_file:
            private_key_data = key_file.read()

        try:
            private_key = serialization.load_pem_private_key(
                private_key_data,
                password=None,
                backend=default_backend()
            )
            key_size = private_key.key_size
            print(f"    [!] CRITICAL: Geldige Private Key gevonden!")
            print(f"    [!] Status: ONBEVEILIGD (Geen wachtwoord)")
            print(f"    [+] Key Size: {key_size} bits (RSA)")
                 
        except TypeError:
            print("    [?] Key is versleuteld met een wachtwoord (Beter, maar hoort niet in repo).")
        except ValueError:
             print("    [-] Inhoud is geen geldige PEM key (mogelijk corrupt of ander formaat).")

    except Exception as e:
        print(f"    [-] Error tijdens lezen: {e}")

if __name__ == "__main__":
    print("=== PROOF OF CONCEPT: SECRET VALIDATION V2 ===")
    if "NAAM_VAN_JE_REPO_HIER" in REPO_ROOT:
        print("!!! LET OP: Je moet de variabele REPO_ROOT in het script nog aanpassen !!!")
    else:
        for target in TARGET_FILES:
            analyze_path(target)