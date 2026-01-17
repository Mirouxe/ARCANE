#!/bin/bash
# Mode : Génération Simple Générique
# Génération pour une seule offre d'emploi (profil générique)

echo "============================================================"
echo "  🌍 MODE : GÉNÉRATION SIMPLE - PROFIL GÉNÉRIQUE"
echo "============================================================"
echo ""

# Répertoires
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
CORE_DIR="$ROOT_DIR/core"

# Si une URL est fournie en argument, l'utiliser directement
if [ $# -gt 0 ]; then
    URL="$1"
else
    # Sinon, mode interactif
    echo "📝 Veuillez fournir l'URL de l'annonce d'emploi"
    echo ""
    echo "Exemples d'URLs valides:"
    echo "  • https://www.linkedin.com/jobs/view/1234567890"
    echo "  • https://www.welcometothejungle.com/fr/companies/..."
    echo "  • https://entreprise.com/carriere/poste"
    echo ""
    read -p "🔗 URL de l'annonce : " URL
    
    # Vérifier que l'URL n'est pas vide
    if [ -z "$URL" ]; then
        echo ""
        echo "❌ Erreur: URL vide"
        exit 1
    fi
fi

echo ""
echo "🔗 URL sélectionnée: $URL"
echo ""

# Copier le config local et les infos dans le root
cp "$SCRIPT_DIR/config.py" "$CORE_DIR/config.py"
cp "$SCRIPT_DIR/infos_statique.txt" "$ROOT_DIR/infos_statique.txt"

# Activer l'environnement virtuel
source "$ROOT_DIR/venv/bin/activate"

# Lancer la génération
cd "$ROOT_DIR"
python3 "$CORE_DIR/generateur_cv_lettre.py" "$URL"

echo ""
echo "✅ Génération terminée ! Les fichiers sont dans le dossier 'candidatures/'"
