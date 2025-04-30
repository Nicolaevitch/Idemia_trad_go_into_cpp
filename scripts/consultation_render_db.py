import psycopg2

conn = psycopg2.connect(
    host="dpg-cvvpseidbo4c738e0n2g-a.frankfurt-postgres.render.com",
    port=5432,
    dbname="bdd_traduction",
    user="bdd_traduction_user",
    password="o8cTDicIL6LVUUt17qDMVilWvuubtIeD"
)

cur = conn.cursor()

print("🟢 Connecté à la base. Tapez une requête SQL (ou 'exit' pour quitter).\n")

while True:
    query = input("SQL > ").strip()
    if query.lower() in ("exit", "quit"):
        break
    try:
        cur.execute(query)
        if cur.description:
            rows = cur.fetchall()
            for row in rows:
                print(row)
        else:
            conn.commit()
            print("✅ Requête exécutée.")
    except Exception as e:
        print(f"❌ Erreur : {e}")

cur.close()
conn.close()
print("🔴 Déconnexion.")
