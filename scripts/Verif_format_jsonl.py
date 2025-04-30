import json
import sys

def validate_jsonl(file_path):
    issues = []
    valid_lines = 0
    total_lines = 0

    with open(file_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            total_lines += 1
            stripped = line.strip()
            if not stripped:
                issues.append((i, "❌ Ligne vide"))
                continue
            try:
                obj = json.loads(stripped)
                if not isinstance(obj, dict):
                    issues.append((i, "❌ Ligne non JSON"))
                elif "prompt" not in obj or "completion" not in obj:
                    issues.append((i, "❌ Clé 'prompt' ou 'completion' manquante"))
                else:
                    valid_lines += 1
            except json.JSONDecodeError as e:
                issues.append((i, f"❌ Erreur JSON: {e}"))

    print(f"\n📊 Résultat de la vérification :")
    print(f"Total lignes lues : {total_lines}")
    print(f"Lignes valides    : {valid_lines}")
    print(f"Lignes avec erreur: {len(issues)}\n")

    if issues:
        print("🧨 Détail des erreurs :")
        for i, msg in issues:
            print(f"Ligne {i}: {msg}")
    else:
        print("✅ Le fichier est conforme au format OpenAI JSONL.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Utilisation : python3 verif_jsonl_openai.py fichier.jsonl")
    else:
        validate_jsonl(sys.argv[1])
