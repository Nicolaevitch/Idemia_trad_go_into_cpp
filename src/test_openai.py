import openai
from src.config import OPENAI_API_KEY  # Assure-toi que ce chemin est correct !

# Vérifier que la clé API est bien définie
if not OPENAI_API_KEY:
    raise ValueError("⚠️ ERREUR : La clé API OpenAI n'est pas définie dans l'environnement.")

# Créer un client OpenAI
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Envoyer une requête de test
chat_completion = client.chat.completions.create(
    messages=[{"role": "user", "content": "Dis-moi une blague sur les programmeurs"}],
    model="gpt-4o",
)

# Afficher la réponse générée
print("🤖 Réponse d'OpenAI :", chat_completion.choices[0].message.content)
