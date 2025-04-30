📌 Enchaînement des commandes à exécuter

Traduction via des tests unitaires
1. Lancer le script de génération des tests :
python3 scripts/Generate_test_unitaire.py input_code/gestion_bancaire.py
2. Vérifier que __init__.py existe dans input_code/ et préciser le chemin dans le code généré :
from input_code.gestion_bancaire import BankAccount


3. Lancer le script de test en précisant PYTHONPATH :
PYTHONPATH=input_code python3 -m unittest -v test_unitaire/test_gestion_bancaire.py

4. Lancer le script de construction du script C++ en prenant comme argument les test python générés :
python3 scripts/Translate_test_into_C++_code.py test_unitaire/test_gestion_bancaire.py

5. Rendre le script généré (reconstructed_code) executable avec python :
g++ -std=c++11 -o bank_account output_code/reconstructed_code.cpp

6. Tester le C++ :
./bank_account

7. Enregistrer le code C++ et les tests dans postgreSQL 

python3 scripts/input_bdd_et_pretraitement.py <fichier_cpp> <fichier_test_python> <label> [fichier_test_cpp]

7. bis base de données Render (en ligne) : 
Integration de données dans la table, script insert_into_render_db: 

python insert_into_render_db.py \
  --py-base chemin/vers/code_python.py \
  --py-test chemin/vers/test_python.py \
  --cpp-test chemin/vers/test_cpp.cpp \
  --cpp-code chemin/vers/code_cpp.cpp \
  --label "Nom_du_label"



(local) Utilisation de la base postgreSQL : 

1. Se connecter à PostgreSQL (via TCP/IP)
psql -U <utilisateur> -h localhost -p 5432
Exemple :
psql -U postgres -h localhost -p 5432
2. Lister toutes les bases de données
\l
3. Se connecter à une base de données
\c nom_de_la_base
Exemple :
\c bdd_traduction
4. Lister toutes les tables dans la base courante
\dt
5. Afficher les données d'une table
SELECT * FROM nom_de_la_table LIMIT 10;
Exemple :
SELECT * FROM bdd_traduction LIMIT 10;

Chargement dans le modèle fine-tuné : 

1. Exporter la base SQL en fichier JSONL

python3 scripts/Export_bdd_into_finetuning_format.py
2. Import dans le modèle OpenAI (il faut rentrer la clé dans le terminal avant : export OPENAI_API_KEY="sk-..) 

openai files create -f export_finetune_gpt.jsonl -p fine-tune

3. Entrainer le modèle en utilisant l’id du fichier importé 
python3 scripts/Entrainement_modele.py file-AP4iVWgaBkeVxQLobuZgv9

4. Voir le modele : 
https://platform.openai.com/finetune/ftjob-QqjTqEcZD4RtXjHOgbQDaJcO




Traduction du code Python en C++ via API de LLM 
1. Exécuter le script de traduction :
python3 scripts/translate_code.py input_code/gestion_bancaire.py > output_code/<nom_script>.cpp
2. Vérifier le fichier généré :
Ouvrir output_code/<nom_script>.cpp et s'assurer que la traduction est correcte.

3️⃣ Compilation et exécution du fichier C++
1. Compiler et exécuter automatiquement avec un script Bash : 
 ./scripts/execute_cpp.sh output_code/script_C++.cpp

4️⃣ (Optionnel) Vérification et correction automatique du code C++
1. Exécuter le script de vérification automatique : 
 python3 scripts/verif_cpp_code.py output_code/script_C++.cpp

5️⃣ Exécution manuelle du programme C++
1. Compiler le fichier C++ :
g++ -std=c++17 output_code/strict_traduit_gestion_bancaire.cpp -o output_code/executable
3. Exécuter le programme compilé :
./output_code/executable

📊 Consommation API OpenAI
Consulter la consommation API OpenAI

📂 Structure du projet
Programme TEST UNITAIRE/
│── input_code/               # Contient les fichiers Python à traduire
│   ├── gestion_bancaire.py   # Exemple de script Python
│── output_code/              # Contient les fichiers C++ traduits
│   ├── strict_traduit_script_C++.cpp  # Fichier généré en C++
│── log_traduction/           # Dossier contenant les logs d'exécution
│── scripts/                  # Dossier contenant les scripts principaux
│   ├── translate_code.py     # Traduction Python → C++
│   ├── verif_cpp_code.py     # Vérification et correction du C++
│   ├── Generate_test_unitaire.py
│   ├── Translate_test_into_C++_code
│── .env                      # Fichier contenant la clé API 
OpenAI
│── test_unitaire/
│   ├── test_gestion_bancaire
│── README.md                 # Documentation du projet

🚀


