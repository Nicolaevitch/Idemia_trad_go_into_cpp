from pyspark.sql import SparkSession
import psycopg2

# 🔥 Vérification de Spark
def check_spark():
    try:
        spark = SparkSession.builder.appName("SparkCheck").getOrCreate()
        print("✅ Spark est bien installé et fonctionne !")
        spark.stop()
    except Exception as e:
        print(f"❌ Erreur : Impossible de démarrer Spark ({e})")

# 🔥 Vérification de PostgreSQL
def check_postgresql(db_config):
    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        cur.execute("SELECT version();")
        db_version = cur.fetchone()
        print(f"✅ Connexion PostgreSQL réussie : {db_version[0]}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Erreur : Impossible de se connecter à PostgreSQL ({e})")

# Configuration PostgreSQL
db_config = {
    "dbname": "code_translations",
    "user": "postgres",
    "password": "your_password",
    "host": "localhost",
    "port": "5432"
}

# Exécuter les vérifications
check_spark()
check_postgresql(db_config)
