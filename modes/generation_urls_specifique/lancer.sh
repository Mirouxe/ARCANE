#!/bin/bash
# Mode : Génération avec URLs Spécifique
# Génération batch à partir d'une liste d'URLs (profil spécifique)

echo "============================================================"
echo "  ⭐ MODE : GÉNÉRATION BATCH - PROFIL SPÉCIFIQUE"
echo "============================================================"
echo ""

# Répertoires
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
CORE_DIR="$ROOT_DIR/core"

# Mode interactif pour obtenir les URLs
echo "📝 Comment souhaitez-vous fournir les URLs des offres d'emploi ?"
echo ""
echo "  1) Utiliser le fichier urls.txt (s'il existe)"
echo "  2) Entrer les URLs manuellement"
echo "  3) Utiliser un fichier personnalisé"
echo ""
read -p "Votre choix (1-3) : " CHOIX_URLS

case "$CHOIX_URLS" in
    1)
        # Vérifier qu'un fichier URLs existe
        if [ ! -f "$SCRIPT_DIR/urls.txt" ]; then
            echo ""
            echo "❌ Erreur: Le fichier urls.txt n'existe pas dans ce répertoire"
            echo ""
            echo "Créez un fichier urls.txt avec une URL par ligne, par exemple:"
            echo "https://example.com/job1"
            echo "https://example.com/job2"
            echo ""
            exit 1
        fi
        URL_FILE="$SCRIPT_DIR/urls.txt"
        ;;
    2)
        # Entrer les URLs manuellement
        echo ""
        echo "📝 Entrez les URLs une par ligne (ligne vide pour terminer) :"
        echo ""
        URL_FILE="$SCRIPT_DIR/urls_temp.txt"
        > "$URL_FILE"  # Créer un fichier vide
        
        while true; do
            read -p "URL : " URL_INPUT
            if [ -z "$URL_INPUT" ]; then
                break
            fi
            echo "$URL_INPUT" >> "$URL_FILE"
        done
        
        # Vérifier qu'au moins une URL a été entrée
        if [ ! -s "$URL_FILE" ]; then
            echo ""
            echo "❌ Erreur: Aucune URL fournie"
            rm -f "$URL_FILE"
            exit 1
        fi
        ;;
    3)
        # Utiliser un fichier personnalisé
        echo ""
        read -p "📁 Chemin du fichier contenant les URLs : " CUSTOM_FILE
        
        if [ ! -f "$CUSTOM_FILE" ]; then
            echo ""
            echo "❌ Erreur: Le fichier '$CUSTOM_FILE' n'existe pas"
            exit 1
        fi
        URL_FILE="$CUSTOM_FILE"
        ;;
    *)
        echo ""
        echo "❌ Choix invalide"
        exit 1
        ;;
esac

# Compter les URLs
NB_URLS=$(grep -v '^#' "$URL_FILE" | grep -v '^[[:space:]]*$' | wc -l | tr -d ' ')
echo ""
echo "📋 $NB_URLS URL(s) trouvée(s)"
echo ""

# Afficher les URLs pour confirmation
echo "URLs à traiter :"
grep -v '^#' "$URL_FILE" | grep -v '^[[:space:]]*$' | nl -w2 -s'. '
echo ""
read -p "▶️  Continuer avec ces URLs ? (oui/non) : " CONFIRM

if [ "$CONFIRM" != "oui" ] && [ "$CONFIRM" != "o" ] && [ "$CONFIRM" != "yes" ] && [ "$CONFIRM" != "y" ]; then
    echo ""
    echo "❌ Annulé"
    [ -f "$SCRIPT_DIR/urls_temp.txt" ] && rm -f "$SCRIPT_DIR/urls_temp.txt"
    exit 0
fi

# Copier le config local et les infos dans le root
cp "$SCRIPT_DIR/config.py" "$CORE_DIR/config.py"
cp "$SCRIPT_DIR/infos_statique.txt" "$ROOT_DIR/infos_statique.txt"
cp "$URL_FILE" "$ROOT_DIR/urls_a_traiter.txt"

# Activer l'environnement virtuel
source "$ROOT_DIR/venv/bin/activate"

# Lancer la génération batch
echo ""
cd "$ROOT_DIR"
python3 "$CORE_DIR/batch_depuis_urls.py" urls_a_traiter.txt

# Nettoyer le fichier temporaire
[ -f "$SCRIPT_DIR/urls_temp.txt" ] && rm -f "$SCRIPT_DIR/urls_temp.txt"

echo ""
echo "✅ Génération terminée ! Les candidatures sont dans le dossier 'candidatures/'"
