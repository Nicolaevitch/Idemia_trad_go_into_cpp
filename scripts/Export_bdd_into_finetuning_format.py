import psycopg2
import pandas as pd
import json

# Connexion à PostgreSQL
conn = psycopg2.connect(
    dbname="bdd_traduction",
    user="postgres",           # modifie si besoin
    password="Virafifille",    # ton mot de passe
    host="localhost",
    port="5432"
)

# Lire la table
df = pd.read_sql_query("SELECT * FROM bdd_traduction", conn)
conn.close()

# Nettoyage
df = df.dropna(subset=["test_unitaire_python", "code_cpp"])
df["test_unitaire_python"] = df["test_unitaire_python"].apply(lambda x: x.strip())
df["code_cpp"] = df["code_cpp"].apply(lambda x: " " + x.strip())  # important pour le token de départ

# Export JSONL pour GPT-3.5-turbo fine-tuning
with open("export_finetune_gpt.jsonl", "w", encoding="utf-8") as f:
    for _, row in df.iterrows():
        entry = {
            "messages": [
                {"role": "system", "content": "Tu es un traducteur Python vers C++"},
                {"role": "user", "content": row["test_unitaire_python"]},
                {"role": "assistant", "content": row["code_cpp"]}
            ]
        }
        json.dump(entry, f, ensure_ascii=False)
        f.write("\n")

print("✅ Export terminé : fichier export_finetune_gpt.jsonl (format GPT-3.5 turbo)")
