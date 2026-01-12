#!/bin/bash
# Script pour générer en batch depuis un fichier d'URLs

echo "============================================================"
echo "  GÉNÉRATION EN BATCH DEPUIS FICHIER D'URLs"
echo "============================================================"
echo ""

# Vérifier si le fichier existe
if [ ! -f "urls_a_traiter.txt" ]; then
    echo "❌ Fichier urls_a_traiter.txt non trouvé"
    echo ""
    echo "💡 Créez-le à partir de l'exemple:"
    echo "   cp urls_a_traiter_exemple.txt urls_a_traiter.txt"
    echo "   # Puis éditez urls_a_traiter.txt avec vos URLs"
    echo ""
    exit 1
fi

# Activer l'environnement virtuel
source venv/bin/activate

# Lancer le générateur en batch
python3 batch_depuis_urls.py urls_a_traiter.txt
