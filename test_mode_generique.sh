#!/bin/bash
# Test du mode génération simple générique

echo "🧪 TEST MODE GÉNÉRATION SIMPLE GÉNÉRIQUE"
echo "==========================================="
echo ""

# URL de test (peut être remplacée)
TEST_URL="https://www.welcometothejungle.com/fr/companies/chilowe/jobs/community-manager-specialiste-reseaux-sociaux_paris"

echo "🔗 URL de test: $TEST_URL"
echo ""
echo "📂 Copie du profil Armelle dans le mode..."

# S'assurer que le mode a les bons fichiers
cd modes/generation_simple_generique/

if [ ! -f "infos_statique.txt" ]; then
    echo "❌ Erreur: infos_statique.txt manquant"
    exit 1
fi

if [ ! -f "config.py" ]; then
    echo "❌ Erreur: config.py manquant"
    exit 1
fi

echo "✓ Fichiers de configuration présents"
echo ""
echo "🚀 Lancement de la génération..."
echo ""

# Lancer avec l'URL de test
./lancer.sh "$TEST_URL"

EXIT_CODE=$?

echo ""
echo "==========================================="
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ TEST RÉUSSI !"
    echo ""
    echo "📁 Vérifiez le dossier candidatures/ pour voir les résultats"
else
    echo "❌ TEST ÉCHOUÉ (code: $EXIT_CODE)"
fi
echo "==========================================="

exit $EXIT_CODE
