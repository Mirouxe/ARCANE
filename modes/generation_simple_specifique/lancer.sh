#!/bin/bash
# Mode : Génération Simple Spécifique
# Génération pour une seule offre d'emploi (profil spécifique)

echo "============================================================"
echo "  ⭐ MODE : GÉNÉRATION SIMPLE - PROFIL SPÉCIFIQUE"
echo "============================================================"
echo ""

# Répertoires
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
CORE_DIR="$ROOT_DIR/core"

# Vérifier qu'une URL est fournie
if [ $# -eq 0 ]; then
    echo "❌ Erreur: Veuillez fournir l'URL de l'annonce"
    echo ""
    echo "Usage: ./lancer.sh <URL_ANNONCE>"
    echo ""
    echo "Exemple:"
    echo "  ./lancer.sh https://www.linkedin.com/jobs/view/1234567890"
    echo ""
    exit 1
fi

URL="$1"
echo "🔗 URL: $URL"
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
