import os
from dotenv import load_dotenv

# Charger `.env`
load_dotenv()

# Vérifier si la clé API est bien récupérée
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("⚠️ ERREUR : La clé API OpenAI n'a pas été trouvée. Vérifiez votre fichier .env.")

print(f"✅ Clé API chargée dans config.py : {OPENAI_API_KEY[:5]}... (sécurisé)")
