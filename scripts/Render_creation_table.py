import psycopg2

# Connexion à ta base Render
conn = psycopg2.connect(
    host="dpg-cvvpseidbo4c738e0n2g-a.frankfurt-postgres.render.com",
    port=5432,
    dbname="bdd_traduction",
    user="bdd_traduction_user",
    password="o8cTDicIL6LVUUt17qDMVilWvuubtIeD"
)

cur = conn.cursor()

# Création de la table
cur.execute("""
CREATE TABLE IF NOT EXISTS bdd_traduction (
    id SERIAL PRIMARY KEY,
    date DATE,
    test_unitaire_python TEXT,
    test_unitaire_cpp TEXT,
    label TEXT,
    code_cpp TEXT
)
""")

conn.commit()
cur.close()
conn.close()

print("✅ Table 'bdd_traduction' créée avec succès.")
