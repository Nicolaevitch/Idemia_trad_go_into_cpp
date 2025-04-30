#!/usr/bin/env python3
import openai
import os
import sys
from dotenv import load_dotenv

# Charger `.env`
load_dotenv()

# Vérifier que la clé API est bien définie
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ ERREUR : La clé API OPENAI_API_KEY n'est pas définie.")
    sys.exit(1)

# Utiliser la clé API
client = openai.OpenAI(api_key=api_key)

# Vérifier les arguments
if len(sys.argv) < 2:
    print("❌ Usage : python3 translate_code.py <code_python.txt>")
    sys.exit(1)

# Lire le fichier à traduire
input_file = sys.argv[1]
try:
    with open(input_file, "r") as f:
        code_to_translate = f.read()
except FileNotFoundError:
    print("❌ Fichier introuvable.")
    sys.exit(1)

# Appel à l'API OpenAI
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "Tu es un assistant qui traduit du code Python en C++."},
        {"role": "user", "content": f"Traduis ce code Python en C++ :\n\n{code_to_translate}"}
    ]
)

# Afficher la traduction
translated_code = response.choices[0].message.content
print("\n🎯 **Code C++ traduit :**\n")
print(translated_code)
