#!/usr/bin/env python3
import openai
import os
import sys
import importlib.util
from dotenv import load_dotenv

class UnitTestGenerator:
    """Classe pour générer des tests unitaires en utilisant OpenAI."""

    def __init__(self, api_key: str):
        """Initialise le générateur de tests avec la clé API OpenAI."""
        if not api_key:
            print("ERREUR : La clé API OPENAI_API_KEY n'est pas définie.")
            sys.exit(1)
        self.client = openai.OpenAI(api_key=api_key)

    def load_module(self, module_name: str, module_path: str):
        """Charge dynamiquement un module Python depuis un fichier."""
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module
    
    def generate_unittest(self, python_file: str):
        """Génère un fichier de test unitaire pour un script Python donné."""
        if not os.path.exists(python_file):
            print(f"ERREUR : Le fichier {python_file} n'existe pas.")
            sys.exit(1)

        with open(python_file, 'r') as file:
            python_code = file.read()

        module_name = os.path.splitext(os.path.basename(python_file))[0]

        messages = [
            {"role": "system", "content": "Tu es un assistant expert en tests unitaires. Analyse le code et traduit le en C++."},
            {"role": "user", "content": f"Voici un script de test unitaire python nommé {module_name}. Analyse-le et traduit le en C++, avec des cas de test bien réfléchis et pertinents. Voici le code du fichier :\n\n{python_code}"}
        ]

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.2,
            max_tokens=1000
        )

        test_code = response.choices[0].message.content.strip()

        test_dir = "test_unitaire"
        os.makedirs(test_dir, exist_ok=True)

        test_filename = os.path.join(test_dir, f"test_cpp_{module_name}.cpp")

        with open(test_filename, "w") as test_file:
            test_file.write(test_code)

        print(f"Tests unitaires générés et enregistrés dans : {test_filename}")


if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if len(sys.argv) != 2:
        print("Usage : python scripts/generate_unittest.py <fichier_python>")
        sys.exit(1)

    unittest_generator = UnitTestGenerator(api_key)
    unittest_generator.generate_unittest(sys.argv[1])
