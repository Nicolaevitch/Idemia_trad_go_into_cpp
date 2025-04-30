import sys
import os
from dotenv import load_dotenv
import openai

class FineTuneLauncher:
    """Lance un fine-tuning avec les fichiers fournis."""

    def __init__(self, api_key: str = None):
        load_dotenv()
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            print("❌ ERREUR : Clé API non trouvée. Ajoute-la dans .env ou passe-la en argument.")
            sys.exit(1)

        self.client = openai.OpenAI(api_key=self.api_key)

    def launch(self, training_file_id: str, model: str = "gpt-3.5-turbo"):
        """Lance un job de fine-tuning."""
        try:
            response = self.client.fine_tuning.jobs.create(
                training_file=training_file_id,
                model=model
            )
            print("✅ Fine-tuning lancé avec succès !")
            print(f"📦 Job ID     : {response.id}")
            print(f"🔗 Dashboard : https://platform.openai.com/finetune/{response.id}")
        except Exception as e:
            print(f"❌ Erreur lors du lancement : {e}")

# 🚀 Point d'entrée
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage : python scripts/launch_fine_tune.py <TRAINING_FILE_ID> [<API_KEY_OPTIONNEL>]")
        sys.exit(1)

    file_id = sys.argv[1]
    api_key = sys.argv[2] if len(sys.argv) == 3 else None

    launcher = FineTuneLauncher(api_key)
    launcher.launch(file_id)
