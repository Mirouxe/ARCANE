#!/bin/bash
# Script de lancement du générateur CV/Lettre

cd "$(dirname "$0")"

echo "============================================================"
echo "  LANCEMENT DU GÉNÉRATEUR CV/LETTRE"
echo "============================================================"
echo ""

# Vérifier que .env existe et n'est pas vide
if [ ! -f .env ]; then
    echo "❌ Fichier .env manquant"
    echo ""
    echo "Créez un fichier .env avec votre clé API OpenAI:"
    echo "  echo 'OPENAI_API_KEY=sk-proj-votre-clé' > .env"
    echo ""
    exit 1
fi

if [ ! -s .env ]; then
    echo "❌ Fichier .env vide"
    echo ""
    echo "Ajoutez votre clé API OpenAI dans le fichier .env:"
    echo "  echo 'OPENAI_API_KEY=sk-proj-votre-clé' > .env"
    echo ""
    echo "Obtenez votre clé sur: https://platform.openai.com/api-keys"
    echo ""
    exit 1
fi

# Vérifier que l'environnement virtuel existe
if [ ! -d "venv" ]; then
    echo "❌ Environnement virtuel manquant"
    echo "   Créez-le avec: python3 -m venv venv"
    echo "   Puis installez les dépendances: venv/bin/pip install -r requirements.txt"
    exit 1
fi

# Vérifier qu'une URL est fournie
if [ -z "$1" ]; then
    echo "❌ URL de l'annonce requise"
    echo ""
    echo "Usage:"
    echo "  ./lancer_generateur.sh \"https://url-de-l-annonce.com\""
    echo ""
    exit 1
fi

echo "🚀 Lancement du générateur..."
echo "   URL: $1"
echo ""

# Lancer le script Python avec l'environnement virtuel
venv/bin/python generateur_cv_lettre.py "$1"

