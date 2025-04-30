#!/usr/bin/env python3
import openai
import os
import sys
from dotenv import load_dotenv

class CppCodeGenerator:
    """Classe pour générer du code C++ à partir de fichiers de test Python."""

    def __init__(self, api_key: str):
        """Initialise le générateur avec la clé API OpenAI."""
        if not api_key:
            print("ERREUR : La clé API OPENAI_API_KEY n'est pas définie.")
            sys.exit(1)
        self.client = openai.OpenAI(api_key=api_key)

    def read_test_file(self, test_file: str) -> str:
        """Lit le fichier de test et retourne son contenu."""
        if not os.path.exists(test_file):
            print(f"ERREUR : Le fichier {test_file} n'existe pas.")
            sys.exit(1)
        
        with open(test_file, "r", encoding="utf-8") as file:
            return file.read()

    def generate_cpp_from_tests(self, test_file: str) -> str:
        """Analyse un fichier de test Python et génère le code C++ correspondant."""
        test_code = self.read_test_file(test_file)

        messages = [
            {"role": "system", "content": "Tu es un assistant expert en programmation. Analyse un fichier de test écrit en Python (unittest) et recrée en C++ les classes et fonctions qui étaient testées, en respectant la logique et les validations du test."},
            {"role": "user", "content": f"Voici un fichier de test écrit en Python. Analyse-le et recrée en C++ les fonctionnalités testées.\n\n{test_code}"}
        ]

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.2,
                max_tokens=2000
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"ERREUR : Impossible de générer le code C++ ({e})")
            sys.exit(1)

    def save_cpp_file(self, cpp_code: str, output_file: str = "output_code/reconstructed_code.cpp"):
        """Enregistre le code C++ généré dans un fichier."""
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(cpp_code)
        print(f"✅ Fichier C++ généré avec succès : {output_file}")


if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if len(sys.argv) != 2:
        print("Usage : python scripts/Translate_test_into_C++_code.py <fichier_test_python>")
        sys.exit(1)

    test_file = sys.argv[1]
    generator = CppCodeGenerator(api_key)
    cpp_code = generator.generate_cpp_from_tests(test_file)
    generator.save_cpp_file(cpp_code)
