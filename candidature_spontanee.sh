#!/bin/bash
# Script pour générer une candidature spontanée
# Usage: ./candidature_spontanee.sh <URL_SITE_ENTREPRISE> [POSTE_VISE]

echo "============================================================"
echo "  CANDIDATURE SPONTANÉE"
echo "============================================================"
echo ""

# Vérifier qu'une URL est fournie
if [ -z "$1" ]; then
    echo "❌ Erreur: URL du site web de l'entreprise requise"
    echo ""
    echo "Usage: ./candidature_spontanee.sh <URL_SITE_ENTREPRISE> [POSTE_VISE]"
    echo ""
    echo "Exemples:"
    echo "  ./candidature_spontanee.sh https://www.entreprise.com"
    echo "  ./candidature_spontanee.sh https://www.entreprise.com 'Data Scientist'"
    exit 1
fi

URL_SITE="$1"
POSTE_VISE="${2:-Ingénieur IA}"  # Valeur par défaut si non fourni

echo "🚀 Génération d'une candidature spontanée..."
echo "   Site web: $URL_SITE"
echo "   Poste visé: $POSTE_VISE"
echo ""

# Activer l'environnement virtuel
source venv/bin/activate

# Lancer le générateur en mode spontané
python3 generateur_cv_lettre.py --spontanee "$URL_SITE" "$POSTE_VISE"
