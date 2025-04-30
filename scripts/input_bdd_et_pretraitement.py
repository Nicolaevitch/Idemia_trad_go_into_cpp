import sys
import re
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf, current_timestamp, lit
from pyspark.sql.types import StringType
import psycopg2

# 🔥 Démarrer une session Spark
spark = SparkSession.builder \
    .appName("PreprocessAndStore") \
    .config("spark.jars.packages", "org.postgresql:postgresql:42.2.27") \
    .getOrCreate()

# ✅ Connexion PostgreSQL (configuration)
db_config = {
    "dbname": "bdd_traduction",
    "user": "postgres",
    "password": "Virafifille",
    "host": "localhost",
    "port": "5432"
}

# 🔹 Vérifier que les arguments sont corrects
if len(sys.argv) < 4 or len(sys.argv) > 5:
    print("❌ Usage : python preprocess_and_store.py <fichier_cpp> <fichier_test_python> <label> [fichier_test_cpp]")
    sys.exit(1)

file_cpp = sys.argv[1]  # Code C++ traduit
file_test_python = sys.argv[2]  # Test unitaire Python
label = sys.argv[3]  # Label associé
file_test_cpp = sys.argv[4] if len(sys.argv) == 5 else None  # Test unitaire C++ optionnel

# 🔹 Fonction pour lire un fichier
def read_code_from_file(file_path):
    """Lit un fichier contenant du code et retourne son contenu."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du fichier : {e}")
        sys.exit(1)

# 🔹 Supprimer les commentaires du code C++
def clean_cpp_code(code):
    """Supprime les commentaires simples // et multi-lignes /* */ du code C++."""
    code = re.sub(r"//.*", "", code)  # Supprime les commentaires simples
    code = re.sub(r"/\*.*?\*/", "", code, flags=re.DOTALL)  # Supprime les commentaires multi-lignes
    return code.strip()

# 🔥 Définition d'une UDF Spark pour nettoyer le code
clean_cpp_udf = udf(clean_cpp_code, StringType())

# 📌 Lire les fichiers fournis
code_cpp = read_code_from_file(file_cpp)
test_python = read_code_from_file(file_test_python)
test_cpp = read_code_from_file(file_test_cpp) if file_test_cpp else ""

# 🛠 Vérification avant insertion dans PySpark
print("✅ Données envoyées à PySpark :", (code_cpp, test_python, test_cpp, label))

# 📊 Créer un DataFrame Spark avec les données
data = [(code_cpp, test_python, test_cpp, label)]
df = spark.createDataFrame(data, ["code_cpp", "test_unitaire_python", "test_unitaire_cpp", "label"])

# 🛠 Appliquer le nettoyage au code C++
df_cleaned = df.withColumn("code_cpp", clean_cpp_udf(col("code_cpp"))) \
               .withColumn("date", current_timestamp()) \
               .withColumn("test_unitaire_cpp", col("test_unitaire_cpp")) \
               .fillna({"test_unitaire_cpp": ""}) \
               .select(col("date"), col("code_cpp"), col("test_unitaire_python"), col("test_unitaire_cpp"), col("label"))

# 🔹 Vérifier le DataFrame nettoyé
df_cleaned.show(truncate=False)

# ✅ Création de la table PostgreSQL si elle n'existe pas
def create_table():
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bdd_traduction (
            id SERIAL PRIMARY KEY,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            code_cpp TEXT NOT NULL,
            test_unitaire_python TEXT NOT NULL,
            test_unitaire_cpp TEXT DEFAULT NULL,
            label TEXT NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

create_table()

# 📌 Enregistrement des données dans PostgreSQL
df_cleaned.write \
    .format("jdbc") \
    .option("url", f"jdbc:postgresql://{db_config['host']}:{db_config['port']}/{db_config['dbname']}") \
    .option("dbtable", "bdd_traduction") \
    .option("user", db_config["user"]) \
    .option("password", db_config["password"]) \
    .option("driver", "org.postgresql.Driver") \
    .mode("append") \
    .save()

print(f"✅ Données enregistrées avec succès dans PostgreSQL ! 🚀")

# 🛑 Arrêter Spark
spark.stop()
