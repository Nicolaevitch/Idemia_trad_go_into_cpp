import openai
from src.config import OPENAI_API_KEY

# Création d'un client OpenAI (nouvelle API)
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def extraire_resume(texte):
    """
    Envoie un texte à l'API OpenAI pour générer un résumé (nouvelle API OpenAI >=1.0.0).
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un assistant qui résume des textes."},
                {"role": "user", "content": f"Résumé ce texte : {texte}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"⚠️ Erreur lors de l'appel à OpenAI : {e}")
        return None
