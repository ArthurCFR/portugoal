#!/bin/bash

echo "🏠 Lancement de TaskGame - Colocation"
echo "======================================"

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé"
    exit 1
fi

# Vérifier si pip est installé
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 n'est pas installé"
    exit 1
fi

echo "📦 Installation des dépendances..."
pip3 install -r requirements.txt

echo "🚀 Lancement de l'application..."
echo "L'application sera accessible sur: http://localhost:8501"
echo "Appuyez sur Ctrl+C pour arrêter l'application"
echo "======================================"

streamlit run app.py