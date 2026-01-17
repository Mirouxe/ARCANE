#!/bin/bash
# Mode : Recherche Complète Spécifique
# Recherche d'offres d'emploi avec critères avancés (profil spécifique)

echo "============================================================"
echo "  ⭐ MODE : RECHERCHE COMPLÈTE - PROFIL SPÉCIFIQUE"
echo "============================================================"
echo ""

# Répertoires
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
CORE_DIR="$ROOT_DIR/core"

# Copier le config local dans le core pour cette exécution
cp "$SCRIPT_DIR/config.py" "$CORE_DIR/config.py"
cp "$SCRIPT_DIR/infos_statique.txt" "$ROOT_DIR/infos_statique.txt"

# Activer l'environnement virtuel
source "$ROOT_DIR/venv/bin/activate"

# Mode interactif complet
echo "🔍 CONFIGURATION DE LA RECHERCHE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 1. Poste recherché
read -p "🎯 Poste recherché (ex: Data Scientist, Ingénieur IA) : " POSTE
if [ -z "$POSTE" ]; then
    echo "❌ Erreur: Le poste est requis"
    exit 1
fi
echo ""

# 2. Localisation
read -p "📍 Localisation (ex: Paris, France, Remote) [défaut: France] : " LOCALISATION
LOCALISATION=${LOCALISATION:-France}
echo ""

# 3. Séniorité
echo "💼 Niveau de séniorité :"
echo "  1) Junior / Débutant"
echo "  2) Confirmé / Intermédiaire"
echo "  3) Senior / Expert"
echo "  4) Lead / Manager"
echo "  5) Tous niveaux (recommandé)"
echo ""
read -p "Votre choix (1-5) [défaut: 5] : " SENIORITE_NUM
SENIORITE_NUM=${SENIORITE_NUM:-5}
echo ""

# 4. Domaines d'expertise
echo "🔬 Domaines d'expertise (optionnel)"
echo "   Séparez les domaines par des virgules"
echo "   Ex: Machine Learning,Deep Learning,NLP"
echo ""
read -p "Domaines : " DOMAINES
echo ""

# 5. Type d'entreprise
echo "🏢 Type d'entreprise :"
echo "  1) Startup"
echo "  2) PME / ETI"
echo "  3) Grande entreprise / CAC40"
echo "  4) Tous types (recommandé)"
echo ""
read -p "Votre choix (1-4) [défaut: 4] : " TYPE_NUM
TYPE_NUM=${TYPE_NUM:-4}
echo ""

# 6. Nombre de postes
read -p "📊 Nombre de postes par plateforme [défaut: 10] : " NB_JOBS
NB_JOBS=${NB_JOBS:-10}
echo ""

# 7. Playwright pour WTTJ
echo "🚀 Activer Playwright pour Welcome To The Jungle ?"
echo "   (Permet de scraper plus d'offres, mais plus lent)"
echo ""
read -p "Activer ? (oui/non) [défaut: non] : " USE_PLAYWRIGHT_INPUT
if [ "$USE_PLAYWRIGHT_INPUT" = "oui" ] || [ "$USE_PLAYWRIGHT_INPUT" = "o" ] || [ "$USE_PLAYWRIGHT_INPUT" = "yes" ] || [ "$USE_PLAYWRIGHT_INPUT" = "y" ]; then
    USE_PLAYWRIGHT="oui"
else
    USE_PLAYWRIGHT="non"
fi
echo ""

# 8. Mode de sélection
echo "🎯 Mode de sélection des offres :"
echo "  1) Interactif (sélection manuelle après recherche)"
echo "  2) Automatique - Top 5 (5 meilleures offres)"
echo "  3) Automatique - Toutes les offres"
echo "  4) Automatique - Liste personnalisée (ex: 1,3,5,7)"
echo ""
read -p "Votre choix (1-4) [défaut: 1] : " SELECTION_MODE
SELECTION_MODE=${SELECTION_MODE:-1}

case "$SELECTION_MODE" in
    1)
        AUTO_SELECTION="interactif"
        ;;
    2)
        AUTO_SELECTION="top5"
        ;;
    3)
        AUTO_SELECTION="all"
        ;;
    4)
        echo ""
        read -p "📝 Liste des numéros (ex: 1,3,5) : " AUTO_SELECTION
        ;;
    *)
        AUTO_SELECTION="interactif"
        ;;
esac

# Afficher le récapitulatif
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 RÉCAPITULATIF DE LA RECHERCHE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🎯 Poste: $POSTE"
echo "  📍 Localisation: $LOCALISATION"
echo "  💼 Séniorité: Niveau $SENIORITE_NUM"
[ -n "$DOMAINES" ] && echo "  🔬 Domaines: $DOMAINES"
echo "  🏢 Type entreprise: Option $TYPE_NUM"
echo "  📊 Nombre: $NB_JOBS postes par plateforme"
echo "  🚀 Playwright: $USE_PLAYWRIGHT"
echo "  🎯 Sélection: $AUTO_SELECTION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
read -p "▶️  Lancer la recherche ? (oui/non) : " CONFIRM

if [ "$CONFIRM" != "oui" ] && [ "$CONFIRM" != "o" ] && [ "$CONFIRM" != "yes" ] && [ "$CONFIRM" != "y" ]; then
    echo ""
    echo "❌ Annulé"
    exit 0
fi

# Lancer la recherche
echo ""
echo "🔍 Lancement de la recherche..."
echo ""
cd "$ROOT_DIR"

if [ "$AUTO_SELECTION" = "interactif" ]; then
    # Mode interactif - fournir les paramètres initiaux, puis laisser stdin ouvert pour la sélection
    (printf "%s\n%s\n%s\n%s\n%s\n%s\n%s\n" "$POSTE" "$LOCALISATION" "$SENIORITE_NUM" "$DOMAINES" "$TYPE_NUM" "$NB_JOBS" "$USE_PLAYWRIGHT"; cat) | python3 "$CORE_DIR/recherche_postes.py"
else
    # Mode automatique
    echo "$POSTE
$LOCALISATION
$SENIORITE_NUM
$DOMAINES
$TYPE_NUM
$NB_JOBS
$USE_PLAYWRIGHT
$AUTO_SELECTION
oui" | python3 "$CORE_DIR/recherche_postes.py"
fi
