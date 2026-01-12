#!/bin/bash
# Script de recherche avancée avec arguments en ligne de commande
# Usage: ./recherche_avancee.sh --poste "Data Scientist" --localisation "Paris" --seniorite "senior" --domaines "ML,IA" --type "startup"

echo "============================================================"
echo "  RECHERCHE AVANCÉE DE POSTES"
echo "============================================================"
echo ""

# Activer l'environnement virtuel
source venv/bin/activate

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
            echo "Usage: ./recherche_avancee.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --poste, -p           Poste recherché (REQUIS)"
            echo "  --localisation, -l    Localisation (défaut: France)"
            echo "  --seniorite, -s       Niveau: junior|confirmé|senior|lead"
            echo "  --domaines, -d        Domaines séparés par virgule: ML,IA,NLP"
            echo "  --type, -t            Type: startup|PME|grande-entreprise"
            echo "  --nombre, -n          Nombre d'offres par plateforme (défaut: 10)"
            echo "  --playwright          Activer Playwright pour WTTJ"
            echo "  --auto, -a            Sélection auto: top5|all|1,2,3 (défaut: interactif)"
            echo "  --help, -h            Afficher cette aide"
            echo ""
            echo "Exemples:"
            echo "  ./recherche_avancee.sh --poste 'Data Scientist' --localisation 'Paris'"
            echo "  ./recherche_avancee.sh -p 'Ingénieur IA' -s senior -d 'ML,Deep Learning' -t startup"
            echo "  ./recherche_avancee.sh -p 'ML Engineer' -l Remote --playwright"
            echo "  ./recherche_avancee.sh -p 'Data Scientist' -l Paris --auto top5  # Auto: top 5"
            echo "  ./recherche_avancee.sh -p 'Data Scientist' -l Paris --auto '1,3,5'  # Auto: offres 1,3,5"
            echo ""
            exit 0
            ;;
        *)
            echo "Option inconnue: $1"
            echo "Utilisez --help pour voir les options disponibles"
            exit 1
            ;;
    esac
done

# Vérifier que le poste est fourni
if [ -z "$POSTE" ]; then
    echo "❌ Erreur: Le poste est requis"
    echo ""
    echo "Usage: ./recherche_avancee.sh --poste 'Data Scientist' [OPTIONS]"
    echo "Utilisez --help pour plus d'informations"
    exit 1
fi

# Mapper les valeurs pour le script Python
SENIORITE_NUM=""
case "$SENIORITE" in
    junior|débutant)
        SENIORITE_NUM="1"
        ;;
    confirmé|intermédiaire|confirmed)
        SENIORITE_NUM="2"
        ;;
    senior|expert)
        SENIORITE_NUM="3"
        ;;
    lead|manager)
        SENIORITE_NUM="4"
        ;;
    *)
        SENIORITE_NUM="5"
        ;;
esac

TYPE_NUM=""
case "$TYPE_ENTREPRISE" in
    startup)
        TYPE_NUM="1"
        ;;
    pme|PME|ETI)
        TYPE_NUM="2"
        ;;
    grande-entreprise|grande|CAC40)
        TYPE_NUM="3"
        ;;
    *)
        TYPE_NUM="4"
        ;;
esac

# Afficher les critères
echo "Critères de recherche:"
echo "  🎯 Poste: $POSTE"
echo "  📍 Localisation: $LOCALISATION"
[ -n "$SENIORITE" ] && echo "  💼 Séniorité: $SENIORITE"
[ -n "$DOMAINES" ] && echo "  🔬 Domaines: $DOMAINES"
[ -n "$TYPE_ENTREPRISE" ] && echo "  🏢 Type: $TYPE_ENTREPRISE"
echo "  📊 Nombre: $NB_JOBS par plateforme"
[ "$USE_PLAYWRIGHT" = "oui" ] && echo "  🚀 Playwright: Activé"
[ "$AUTO_SELECTION" != "non" ] && echo "  🤖 Auto-sélection: $AUTO_SELECTION"
echo ""

# Lancer la recherche
if [ "$AUTO_SELECTION" != "non" ]; then
    # Mode automatique - toutes les réponses sont pré-remplies
    echo "$POSTE
$LOCALISATION
$SENIORITE_NUM
$DOMAINES
$TYPE_NUM
$NB_JOBS
$USE_PLAYWRIGHT
$AUTO_SELECTION
oui" | python3 recherche_postes.py
else
    # Mode semi-automatique - recommandation d'utiliser --auto
    echo ""
    echo "⚠️  MODE INTERACTIF NON SUPPORTÉ PAR CE SCRIPT"
    echo ""
    echo "Pour une sélection interactive, veuillez utiliser:"
    echo "  ./rechercher_et_generer.sh"
    echo ""
    echo "OU utilisez l'option --auto pour automatiser:"
    echo "  $0 --poste '$POSTE' --localisation '$LOCALISATION' --auto top5"
    echo "  $0 --poste '$POSTE' --localisation '$LOCALISATION' --auto all"
    echo "  $0 --poste '$POSTE' --localisation '$LOCALISATION' --auto '1,3,5'"
    echo ""
    echo "Voulez-vous continuer avec --auto top5 par défaut? (oui/non)"
    read -r CONTINUE
    
    if [ "$CONTINUE" = "oui" ] || [ "$CONTINUE" = "o" ] || [ "$CONTINUE" = "yes" ] || [ "$CONTINUE" = "y" ]; then
        echo ""
        echo "✓ Continuation avec --auto top5"
        echo ""
        AUTO_SELECTION="top5"
        echo "$POSTE
$LOCALISATION
$SENIORITE_NUM
$DOMAINES
$TYPE_NUM
$NB_JOBS
$USE_PLAYWRIGHT
$AUTO_SELECTION
oui" | python3 recherche_postes.py
    else
        echo ""
        echo "❌ Annulé. Relancez avec --auto [top5|all|1,2,3]"
        exit 0
    fi
fi
