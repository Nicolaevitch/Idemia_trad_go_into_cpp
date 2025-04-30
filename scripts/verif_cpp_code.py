import openai
import os
import subprocess
import sys
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("\u274c ERREUR : La clé API OPENAI_API_KEY n'est pas définie.")
    sys.exit(1)

def get_next_log_filename():
    """Trouve le prochain fichier de log disponible dans log_traduction/"""
    log_dir = "log_traduction"
    if not os.path.exists(log_dir):
        print(f"\u274c Le dossier {log_dir} n'existe pas.")
        sys.exit(1)
    
    i = 1
    log_file = os.path.join(log_dir, f"log{i}.txt")
    while os.path.exists(log_file):
        i += 1
        log_file = os.path.join(log_dir, f"log{i}.txt")
    return log_file

def compile_and_run(cpp_file):
    exe_file = cpp_file.replace(".cpp", "")
    log_file = get_next_log_filename()
    
    # Compilation
    compile_cmd = ["g++", "-o", exe_file, cpp_file]
    compile_result = subprocess.run(compile_cmd, capture_output=True, text=True)
    
    with open(log_file, "w") as log:
        if compile_result.returncode != 0:
            log.write("Compilation Error:\n")
            log.write(compile_result.stderr)
            return False, log_file  # Compilation échouée

        # Exécution
        run_result = subprocess.run([f"./{exe_file}"], stdout=log, stderr=log, text=True)
    
    return run_result.returncode == 0, log_file  # Succès si returncode == 0

def ask_openai_for_fix(cpp_file, log_file):
    with open(log_file, "r") as log:
        error_content = log.read()
    with open(cpp_file, "r") as src:
        cpp_code = src.read()
    
    prompt = f"Voici un fichier source C++ qui ne compile/exécute pas correctement.\n\nCode actuel :\n{cpp_code}\n\nLogs d'erreur :\n{error_content}\n\nCorrige le code en expliquant les modifications."
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Vous êtes un assistant expert en C++."},
            {"role": "user", "content": prompt},
        ]
    )
    
    fix_suggestion = response["choices"][0]["message"]["content"]
    return fix_suggestion

def write_fixed_code(cpp_file, fixed_code):
    with open(cpp_file, "w") as f:
        f.write(fixed_code)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 verif_cpp_code.py <fichier_cpp>")
        sys.exit(1)
    
    cpp_file = sys.argv[1]
    
    if not os.path.exists(cpp_file):
        print(f"\u274c Le fichier C++ spécifié ({cpp_file}) n'existe pas.")
        sys.exit(1)
    
    while True:
        success, log_file = compile_and_run(cpp_file)
        if success:
            print("✅ Le programme s'est exécuté avec succès !")
            break
        
        print(f"❌ Erreur détectée, voir {log_file}. Demande de correction à OpenAI...")
        fix = ask_openai_for_fix(cpp_file, log_file)
        
        print("💡 Nouvelle version générée, remplacement du fichier...")
        write_fixed_code(cpp_file, fix)
        print("🔄 Recompilation et test de la nouvelle version...")

if __name__ == "__main__":
    main()
