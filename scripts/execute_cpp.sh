#!/bin/bash

# Vérifier si un argument est fourni
if [ $# -ne 1 ]; then
    echo "Usage: $0 <fichier_cpp>"
    exit 1
fi

CPP_FILE="$1"
EXE_FILE="${CPP_FILE%.cpp}"  # Nom du fichier exécutable sans extension .cpp
LOG_DIR="log_traduction"
mkdir -p "$LOG_DIR"  # Crée le dossier s'il n'existe pas

# Déterminer le prochain numéro de log
LOG_FILE="$LOG_DIR/log1.txt"
i=1
while [ -f "$LOG_FILE" ]; do
    i=$((i + 1))
    LOG_FILE="$LOG_DIR/log${i}.txt"
done

# Compilation
echo "⏳ Compilation de $CPP_FILE..."
g++ -o "$EXE_FILE" "$CPP_FILE" 2> "$LOG_FILE"
if [ $? -ne 0 ]; then
    echo "❌ Erreur de compilation. Voir $LOG_FILE"
    exit 1
fi

# Exécution et capture des logs
echo "🚀 Exécution de $EXE_FILE..."
./"$EXE_FILE" > "$LOG_FILE" 2>&1

echo "✅ Exécution terminée. Logs disponibles dans $LOG_FILE"
