#!/bin/bash
# Script pour rechercher des postes et générer les candidatures en batch

echo "============================================================"
echo "  RECHERCHE ET GÉNÉRATION AUTOMATIQUE"
echo "============================================================"
echo ""

# Activer l'environnement virtuel
source venv/bin/activate

# Lancer le script de recherche
if [ -z "$1" ]; then
    # Mode interactif
    python3 recherche_postes.py
else
    # Mode avec mots-clés en argument
    python3 recherche_postes.py "$1"
fi
