import os

# --- CONFIGURATIE ---
# PAS DIT AAN: Het volledige pad naar de map die je gescand hebt
REPO_ROOT = "/Users/edwinhouben/Development/security_poc/target_repo_dev/"

# De locaties uit je eerdere scan (Gitleaks output)
TARGETS = [
    {"file": "modules/_10_ssl_copy_files/main.tf", "line": 17},
    {"file": "modules/_10_ssl_copy_files/main.tf", "line": 3}
]

def print_context(file_path, target_line, context_lines=3):
    full_path = os.path.join(REPO_ROOT, file_path)
    print(f"\n[*] Inspecteren van: {file_path}")
    
    if not os.path.exists(full_path):
        print(f"    [-] Bestand niet gevonden: {full_path}")
        return

    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Line numbers in editors are 1-based, Python lists are 0-based
        idx = target_line - 1
        
        start = max(0, idx - context_lines)
        end = min(len(lines), idx + context_lines + 1)
        
        print(f"    --- CONTEXT START (Regel {start+1} tot {end}) ---")
        for i in range(start, end):
            prefix = ">>" if i == idx else "  "
            # Strip newline voor nette output
            clean_line = lines[i].rstrip()
            print(f"    {i+1:4d} | {prefix} {clean_line}")
        print(f"    --- CONTEXT END ---")
        
        # Eenvoudige heuristiek voor analyse
        target_content = lines[idx].lower()
        if "resource" in lines[max(0, idx-1)].lower() or "module" in lines[max(0, idx-1)].lower():
             print("\n    [!] ANALYSE: Wachtwoord lijkt direct gekoppeld aan een Resource/Module definitie.")
        if "variable" in lines[max(0, idx-1)].lower():
             print("\n    [!] ANALYSE: Wachtwoord staat als 'default' value in een variabele. Dit is een anti-pattern.")

    except Exception as e:
        print(f"    [-] Fout bij lezen: {e}")

if __name__ == "__main__":
    print("=== PROOF OF CONCEPT: HARDCODED PASSWORD CONTEXT ===")
    
    if "NAAM_VAN_JE_REPO_HIER" in REPO_ROOT:
         print("!!! LET OP: Pas REPO_ROOT aan in het script !!!")
    else:
        for t in TARGETS:
            print_context(t["file"], t["line"])