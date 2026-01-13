#!/bin/bash
# Mode : Recherche Complète Générique
# Recherche d'offres d'emploi avec critères avancés (profil générique)

echo "============================================================"
echo "  🌍 MODE : RECHERCHE COMPLÈTE - PROFIL SPÉCIFIQUE"
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

# Parser les arguments
POSTE=""
LOCALISATION="France"
SENIORITE=""
DOMAINES=""
TYPE_ENTREPRISE=""
NB_JOBS="10"
USE_PLAYWRIGHT="non"
AUTO_SELECTION="non"

while [[ $# -gt 0 ]]; do
    case $1 in
        --poste|-p)
            POSTE="$2"
            shift 2
            ;;
        --localisation|-l|--location)
            LOCALISATION="$2"
            shift 2
            ;;
        --seniorite|-s|--seniority)
            SENIORITE="$2"
            shift 2
            ;;
        --domaines|-d|--domains)
            DOMAINES="$2"
            shift 2
            ;;
        --type|-t|--type-entreprise)
            TYPE_ENTREPRISE="$2"
            shift 2
            ;;
        --nombre|-n|--nb)
            NB_JOBS="$2"
            shift 2
            ;;
        --playwright)
            USE_PLAYWRIGHT="oui"
            shift
            ;;
        --auto|-a)
            AUTO_SELECTION="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: ./lancer.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --poste, -p           Poste recherché (REQUIS)"
            echo "  --localisation, -l    Localisation (défaut: France)"
            echo "  --seniorite, -s       Niveau: junior|confirmé|senior|lead"
            echo "  --domaines, -d        Domaines séparés par virgule"
            echo "  --type, -t            Type: startup|PME|grande-entreprise"
            echo "  --nombre, -n          Nombre d'offres (défaut: 10)"
            echo "  --playwright          Activer Playwright pour WTTJ"
            echo "  --auto, -a            Sélection auto: top5|all|1,2,3"
            echo ""
            exit 0
            ;;
        *)
            echo "Option inconnue: $1"
            exit 1
            ;;
    esac
done

# Vérifier que le poste est fourni
if [ -z "$POSTE" ]; then
    echo "❌ Erreur: Le poste est requis"
    echo "Usage: ./lancer.sh --poste 'Développeur Full-Stack' [OPTIONS]"
    exit 1
fi

# Mapper les valeurs pour le script Python
SENIORITE_NUM=""
case "$SENIORITE" in
    junior|débutant) SENIORITE_NUM="1" ;;
    confirmé|intermédiaire) SENIORITE_NUM="2" ;;
    senior|expert) SENIORITE_NUM="3" ;;
    lead|manager) SENIORITE_NUM="4" ;;
    *) SENIORITE_NUM="5" ;;
esac

TYPE_NUM=""
case "$TYPE_ENTREPRISE" in
    startup) TYPE_NUM="1" ;;
    pme|PME|ETI) TYPE_NUM="2" ;;
    grande-entreprise|grande) TYPE_NUM="3" ;;
    *) TYPE_NUM="4" ;;
esac

# Afficher les critères
echo "Critères de recherche:"
echo "  🎯 Poste: $POSTE"
echo "  📍 Localisation: $LOCALISATION"
[ -n "$SENIORITE" ] && echo "  💼 Séniorité: $SENIORITE"
[ -n "$DOMAINES" ] && echo "  🔬 Domaines: $DOMAINES"
[ -n "$TYPE_ENTREPRISE" ] && echo "  🏢 Type: $TYPE_ENTREPRISE"
echo "  📊 Nombre: $NB_JOBS par plateforme"
echo ""

# Lancer la recherche
cd "$ROOT_DIR"
if [ "$AUTO_SELECTION" != "non" ]; then
    echo "$POSTE
$LOCALISATION
$SENIORITE_NUM
$DOMAINES
$TYPE_NUM
$NB_JOBS
$USE_PLAYWRIGHT
$AUTO_SELECTION
oui" | python3 "$CORE_DIR/recherche_postes.py"
else
    echo "⚠️  Pour mode automatique, utilisez --auto top5|all|1,2,3"
    exit 1
fi
