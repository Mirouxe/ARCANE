#!/bin/bash
# Mode : Génération avec URLs Générique
# Génération batch à partir d'une liste d'URLs (profil générique)

echo "============================================================"
echo "  🌍 MODE : GÉNÉRATION BATCH - PROFIL GÉNÉRIQUE"
echo "============================================================"
echo ""

# Répertoires
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
CORE_DIR="$ROOT_DIR/core"

# Vérifier qu'un fichier URLs existe
if [ ! -f "$SCRIPT_DIR/urls.txt" ]; then
    echo "❌ Erreur: Le fichier urls.txt n'existe pas dans ce répertoire"
    echo ""
    echo "Créez un fichier urls.txt avec une URL par ligne, par exemple:"
    echo "https://example.com/job1"
    echo "https://example.com/job2"
    echo ""
    exit 1
fi

# Compter les URLs
NB_URLS=$(grep -v '^#' "$SCRIPT_DIR/urls.txt" | grep -v '^[[:space:]]*$' | wc -l | tr -d ' ')
echo "📋 $NB_URLS URL(s) trouvée(s) dans urls.txt"
echo ""

# Copier le config local et les infos dans le root
cp "$SCRIPT_DIR/config.py" "$CORE_DIR/config.py"
cp "$SCRIPT_DIR/infos_statique.txt" "$ROOT_DIR/infos_statique.txt"
cp "$SCRIPT_DIR/urls.txt" "$ROOT_DIR/urls_a_traiter.txt"

# Activer l'environnement virtuel
source "$ROOT_DIR/venv/bin/activate"

# Lancer la génération batch
cd "$ROOT_DIR"
python3 "$CORE_DIR/batch_depuis_urls.py" urls_a_traiter.txt

echo ""
echo "✅ Génération terminée ! Les candidatures sont dans le dossier 'candidatures/'"
