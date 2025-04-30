import psycopg2
import argparse
from datetime import date

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def insert_to_db(py_base, py_test, cpp_test, cpp_code, label):
    # Connexion à la base Render
    conn = psycopg2.connect(
        host="dpg-cvvpseidbo4c738e0n2g-a.frankfurt-postgres.render.com",
        port=5432,
        dbname="bdd_traduction",
        user="bdd_traduction_user",
        password="o8cTDicIL6LVUUt17qDMVilWvuubtIeD"
    )

    cur = conn.cursor()

    # Insertion des données
    cur.execute("""
        INSERT INTO bdd_traduction (date, test_unitaire_python, test_unitaire_cpp, label, code_cpp, code_python)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        date.today(),
        read_file(py_test),
        read_file(cpp_test),
        label,
        read_file(cpp_code),
        read_file(py_base)
    ))

    conn.commit()
    cur.close()
    conn.close()

    print("✅ Insertion avec code Python réussie.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Insérer des fichiers dans la base PostgreSQL Render.")
    parser.add_argument("--py-base", required=True, help="Fichier contenant le code Python de base")
    parser.add_argument("--py-test", required=True, help="Fichier de test unitaire Python")
    parser.add_argument("--cpp-test", required=True, help="Fichier de test unitaire C++")
    parser.add_argument("--cpp-code", required=True, help="Fichier de code C++")
    parser.add_argument("--label", required=True, help="Label à insérer dans la base")

    args = parser.parse_args()

    insert_to_db(args.py_base, args.py_test, args.cpp_test, args.cpp_code, args.label)
