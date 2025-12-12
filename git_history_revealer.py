import subprocess
import json
import os
import shutil

# --- Configuratie ---
REPO_URL = "https://github.com/Houbbie/dev"
REPO_DIR = "target_repo_dev"
GITLEAKS_OUTPUT_FILE = "gitleaks_results.json"
TRUFFLEHOG_OUTPUT_FILE = "trufflehog_results.json"

def clone_repo(url, target_dir):
    """Kloont de repository."""
    print(f"🚀 Kloon de repository {url} naar {target_dir}...")
    if os.path.exists(target_dir):
        # Veilig verwijderen van bestaande directory
        # We negeren errors hier om permissie-issues op Windows/Linux te omzeilen in de demo
        shutil.rmtree(target_dir, ignore_errors=True)
        
    try:
        subprocess.run(["git", "clone", url, target_dir], check=True, capture_output=True, text=True)
        print("✅ Repository succesvol gekloond.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Fout bij het klonen: {e.stderr}")
        raise

def run_gitleaks(repo_dir, output_file):
    """Voert Gitleaks uit op de gekloonde repository."""
    print(f"\n🔬 Voer Gitleaks uit in {repo_dir}...")
    try:
        command = [
            "gitleaks", "detect",
            f"--source={repo_dir}",
            f"--report-format=json",
            f"--report-path={output_file}",
            "--verbose"
        ]
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"✅ Gitleaks scan voltooid (Geen bevindingen of exit code 0).")
        return 0
    except FileNotFoundError:
        print("❌ Fout: Gitleaks is niet gevonden. Zorg dat het in je PATH staat.")
        return 1
    except subprocess.CalledProcessError as e:
        # Gitleaks exit code 1 betekent dat er leaks gevonden zijn (dit is goed voor ons)
        if e.returncode == 1:
             print(f"✅ Gitleaks scan voltooid. LEAKS GEVONDEN! Opgeslagen in {output_file}")
             return 0
        else:
             print(f"❌ Fout bij Gitleaks-scan (Return Code {e.returncode}): {e.stderr}")
             return e.returncode

def run_trufflehog(repo_url, output_file):
    """
    Voert TruffleHog uit.
    FIX: Gebruikt 'git' subcommand in plaats van 'github' voor directe URL scans.
    """
    print(f"\n🔬 Voer TruffleHog uit op {repo_url}...")
    try:
        # CORRECTIE: De moderne syntax is 'trufflehog git <url> --json'
        command = [
            "trufflehog", "git",
            repo_url,
            "--json"
        ]
        
        # TruffleHog print JSON naar stdout, dus we vangen het af
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        
        # We schrijven de stdout (die de JSON bevat) naar een bestand
        with open(output_file, 'w') as f:
            f.write(result.stdout)
            
        print(f"✅ TruffleHog scan voltooid. Resultaten opgeslagen in {output_file}")
        return result.returncode

    except FileNotFoundError:
        print("❌ Fout: TruffleHog is niet gevonden. Zorg dat het in je PATH staat.")
        return 1
    except subprocess.CalledProcessError as e:
        # TruffleHog geeft ook een non-zero exit code als er secrets gevonden zijn
        # We moeten de output alsnog opslaan als die bestaat
        if e.stdout:
            with open(output_file, 'w') as f:
                f.write(e.stdout)
            print(f"✅ TruffleHog scan voltooid met bevindingen. Opgeslagen in {output_file}")
            return 0
        else:
            print(f"❌ Fout bij TruffleHog-scan (Return Code {e.returncode}): {e.stderr}")
            return e.returncode

def main():
    try:
        # Stap 1: Kloon de repository
        clone_repo(REPO_URL, REPO_DIR)
        
        # Stap 2: Voer Gitleaks uit
        run_gitleaks(REPO_DIR, GITLEAKS_OUTPUT_FILE)
        
        # Stap 3: Voer TruffleHog uit (Gecorrigeerde functie)
        run_trufflehog(REPO_URL, TRUFFLEHOG_OUTPUT_FILE)

        print("\n--- Scans voltooid ---")
        print("Plak de inhoud van de volgende bestanden hieronder voor analyse:")
        print(f"1. {GITLEAKS_OUTPUT_FILE}")
        print(f"2. {TRUFFLEHOG_OUTPUT_FILE}")
        
    except Exception as e:
        print(f"\n🛑 Kritieke fout in het hoofdscript: {e}")

if __name__ == "__main__":
    main()
    
# In een geautomatiseerde pipeline zou je hier command-line argumenten parsen
    # validate_aws_credentials(FOUND_ACCESS_KEY, FOUND_SECRET_KEY)