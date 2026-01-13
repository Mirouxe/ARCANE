#!/usr/bin/env python3
"""
Configuration centralisée du générateur CV/Lettre
Modifiez ce fichier pour personnaliser le comportement du système
"""

# ==================== MODE DE PROFIL ====================
# Mode de traitement des compétences et du profil
# "specifique" : Utilise les catégories hardcodées spécifiques à votre profil
#                (Scientific AI, Simulation, Generative AI, Informatique)
#                ⭐ RECOMMANDÉ pour votre usage personnel
# "generique"  : Parse les compétences de manière dynamique depuis infos_statique.txt
#                Permet d'utiliser le système pour n'importe quel profil
MODE_PROFIL = "generique"


# ==================== MODÈLE IA ====================
# Modèle Claude (Anthropic) à utiliser pour la génération
# Options disponibles (du plus avancé au plus économique) :
#   - "claude-sonnet-4-5-20250929" : Claude Sonnet 4.5 - Le plus récent et performant ($$$$) ⭐ RECOMMANDÉ
#   - "claude-3-opus-20240229"   : Le plus puissant de la génération 3 ($$$$)
#   - "claude-3-5-sonnet-20241022" : Excellent rapport qualité/prix/vitesse ($$$)
#   - "claude-3-sonnet-20240229"   : Bon équilibre performance/coût ($$)
#   - "claude-3-haiku-20240307"  : Le plus rapide et économique ($)
CLAUDE_MODEL = "claude-sonnet-4-5-20250929"


# ==================== PARAMÈTRES DE GÉNÉRATION ====================

# Température : contrôle la créativité (0.0 = déterministe, 1.0 = créatif)
# Recommandé : 0.7 pour un bon équilibre entre cohérence et créativité
TEMPERATURE = 0.7

# Tokens maximum pour chaque type de génération
MAX_TOKENS_ANALYSE = 1024      # Analyse de l'annonce
MAX_TOKENS_PROFIL = 800        # Génération du profil adapté (augmenté pour plus de qualité)
MAX_TOKENS_LETTRE = 1500       # Génération de la lettre de motivation


# ==================== PROMPTS SYSTÈME ====================

# Prompt système pour l'analyse d'annonce
SYSTEM_PROMPT_ANALYSE = """Tu es un expert en analyse d'offres d'emploi. 
Réponds uniquement en JSON valide."""

# Prompt système pour l'analyse d'entreprise (candidature spontanée)
SYSTEM_PROMPT_ANALYSE_ENTREPRISE = """Tu es un expert en analyse d'entreprises et de marchés. 
Tu analyses les sites web d'entreprises pour identifier leurs activités, valeurs, besoins et culture.
Réponds uniquement en JSON valide."""

# Prompt système pour la génération de profil
SYSTEM_PROMPT_PROFIL = """Tu es un expert en rédaction de CV professionnel avec 15 ans d'expérience. 
Tu rédiges des profils percutants qui captent l'attention des recruteurs en 6 secondes.
Tu adaptes les profils pour qu'ils correspondent parfaitement aux postes visés tout en restant authentique.
Tu utilises un style direct, impactant et professionnel. Tu es précis et factuel.
Tu ne répètes jamais le titre du poste déjà présent dans le CV."""

# Prompt système pour la lettre de motivation
SYSTEM_PROMPT_LETTRE = """Tu es un expert en rédaction de lettres de motivation professionnelles. 
Réponds uniquement en JSON valide.
Tu crées des lettres engageantes, concrètes, factuelles et personnalisées.
Tu n'inventes pas de compétences ou d'expériences."""


# ==================== TEMPLATES DE PROMPTS ====================

# Template pour l'analyse d'annonce
PROMPT_TEMPLATE_ANALYSE = """Analyse cette annonce de poste et extrait les informations suivantes au format JSON:
- poste: titre du poste
- entreprise: nom de l'entreprise
- competences_cles: liste des compétences clés demandées (max 5)
- mots_cles: mots-clés importants pour le poste
- mission_principale: résumé de la mission en une phrase

Annonce:
{annonce_text}

Réponds uniquement avec un objet JSON valide."""

# Template pour l'analyse d'entreprise (candidature spontanée)
PROMPT_TEMPLATE_ANALYSE_ENTREPRISE = """Analyse ce site web d'entreprise et extrait les informations suivantes au format JSON:
- entreprise: nom de l'entreprise
- secteur: secteur d'activité principal
- activites_principales: liste des activités principales (max 5)
- valeurs: valeurs et culture d'entreprise identifiées
- technologies: technologies et outils utilisés/mentionnés (si applicable)
- besoins_potentiels: besoins potentiels en recrutement que tu peux déduire (basé sur croissance, projets, etc.)
- mots_cles: mots-clés stratégiques de l'entreprise

Contenu du site:
{site_text}

Poste cible du candidat: {poste_cible}

Réponds uniquement avec un objet JSON valide."""

# Template pour la génération de profil adapté
PROMPT_TEMPLATE_PROFIL = """Rédige un profil professionnel percutant pour un CV ciblant le poste ci-dessous.

CONTEXTE DU CANDIDAT:
Profil actuel: {profil_base}

Expériences clés:
{experiences_resume}

Compétences techniques:
{competences_techniques}

POSTE VISÉ:
- Titre: {poste}
- Entreprise: {entreprise}
- Compétences recherchées: {competences}
- Mission principale: {mission}

CONSIGNES DE RÉDACTION:
1. Rédige un profil de 3-4 phrases (80-100 mots maximum)
2. Commence par une phrase d'accroche forte qui positionne le candidat
3. Intègre naturellement les compétences clés recherchées dans le poste
4. Utilise les termes techniques exacts de l'annonce quand pertinent
5. Mets en valeur les réalisations concrètes et l'impact du candidat
6. Style: direct, factuel, impactant, sans fioriture
7. NE répète PAS le titre exact du poste (déjà affiché en en-tête)
8. Privilégie les verbes d'action et les résultats quantifiables

IMPORTANT: 
- Ne jamais inventer de compétences ou expériences
- Reste authentique au profil du candidat
- Adapte l'angle mais garde les faits réels

Réponds UNIQUEMENT avec le profil rédigé, sans titre, sans introduction, sans commentaire."""

# Template pour la génération de profil adapté (candidature spontanée)
PROMPT_TEMPLATE_PROFIL_SPONTANEE = """Rédige un profil professionnel percutant pour un CV de candidature spontanée.

CONTEXTE DU CANDIDAT:
Profil actuel: {profil_base}

Expériences clés:
{experiences_resume}

Compétences techniques:
{competences_techniques}

ENTREPRISE VISÉE:
- Nom: {entreprise}
- Secteur: {secteur}
- Activités: {activites}
- Valeurs: {valeurs}
- Technologies: {technologies}
- Poste cible: {poste_cible}

CONSIGNES DE RÉDACTION:
1. Rédige un profil de 3-4 phrases (80-100 mots maximum)
2. Positionne le candidat pour le poste cible dans le contexte de l'entreprise
3. Intègre naturellement les technologies et compétences pertinentes pour l'entreprise
4. Mets en avant l'alignement avec les valeurs et activités de l'entreprise
5. Style: direct, factuel, impactant, sans fioriture
6. Privilégie les verbes d'action et les résultats quantifiables

IMPORTANT: 
- Ne jamais inventer de compétences ou expériences
- Reste authentique au profil du candidat
- Montre la valeur ajoutée pour l'entreprise

Réponds UNIQUEMENT avec le profil rédigé, sans titre, sans introduction, sans commentaire."""

# Template pour la lettre de motivation
PROMPT_TEMPLATE_LETTRE = """Tu es un expert en rédaction de lettres de motivation.

Candidat:
- Nom: {nom}
- Profil: {profil}
- Expérience principale: {experience}

Poste visé:
- Poste: {poste}
- Entreprise: {entreprise}
- Compétences clés: {competences}
- Mission: {mission}

Génère une lettre de motivation structurée en 3 paragraphes + conclusion:

PARAGRAPHE_1 (Accroche): Pourquoi ce poste m'intéresse, et pourquoi je suis le bon candidat
PARAGRAPHE_2 (Expérience): Mes expériences pertinentes et compétences techniques qui matchent
PARAGRAPHE_3 (Valeur ajoutée): Ce que je peux apporter à l'entreprise
CONCLUSION: Phrase de conclusion et disponibilité pour un entretien

Réponds au format JSON avec les clés: paragraphe_1, paragraphe_2, paragraphe_3, conclusion
Style: professionnel, engagé, concret."""

# Template pour la lettre de motivation (candidature spontanée)
PROMPT_TEMPLATE_LETTRE_SPONTANEE = """Tu es un expert en rédaction de lettres de motivation pour candidatures spontanées.

Candidat:
- Nom: {nom}
- Profil: {profil}
- Expérience principale: {experience}

Entreprise visée:
- Entreprise: {entreprise}
- Secteur: {secteur}
- Activités principales: {activites}
- Valeurs: {valeurs}
- Technologies: {technologies}
- Poste cible: {poste_cible}
- Besoins potentiels identifiés: {besoins}

Génère une lettre de motivation de candidature spontanée structurée en 3 paragraphes + conclusion:

PARAGRAPHE_1 (Motivation & Alignement): Pourquoi cette entreprise m'intéresse spécifiquement, et comment mes valeurs s'alignent avec les leurs
PARAGRAPHE_2 (Expertise & Valeur ajoutée): Mes compétences clés et comment elles répondent aux besoins potentiels de l'entreprise pour le poste visé
PARAGRAPHE_3 (Contribution concrète): Ce que je peux apporter immédiatement et à moyen terme à l'entreprise
CONCLUSION: Proposition de rencontre et ouverture au dialogue

Réponds au format JSON avec les clés: paragraphe_1, paragraphe_2, paragraphe_3, conclusion
Style: proactif, enthousiaste mais professionnel, démontrant une vraie connaissance de l'entreprise."""


# ==================== PARAMÈTRES LATEX ====================

# -------------------- TEMPLATE CV --------------------
# Choix du template de CV
# "classique" : CV classique 1 colonne (professionnel, standard)
# "2colonnes" : CV 2 colonnes style journal scientifique (moderne, compact)
CV_TEMPLATE = "2colonnes"  # Options : "classique" ou "2colonnes"

# Format du CV : "1page" ou "2pages"
# "1page" : CV compact sur une seule page (marges réduites, espacement compact)
# "2pages" : CV détaillé sur deux pages (plus d'espace, plus lisible)
CV_FORMAT = "1page"  # Options : "1page" ou "2pages"

# -------------------- TAILLES DE POLICE --------------------
# Taille de police de base du document (en pt)
# Recommandé : 10pt (compact), 11pt (standard), 12pt (lisible)
FONT_SIZE_BASE = "10pt"

# Taille du nom dans l'en-tête (commande LaTeX)
# Options : \Huge, \LARGE, \Large, \large, \normalsize
FONT_SIZE_NAME = r"\LARGE"

# Taille du titre/métier dans l'en-tête
# Options : \Large, \large, \normalsize
FONT_SIZE_TITLE = r"\normalsize"

# Taille des titres de sections
# Options : \large, \Large, \normalsize
FONT_SIZE_SECTION = r"\large"

# -------------------- COULEURS --------------------
# Colorer les titres des missions (texte avant ':') en bleu
# True = Les titres comme "Formation & Transfert de compétences :" seront en bleu et gras
# False = Tout le texte reste noir
COLORIZE_MISSION_TITLES = True

# -------------------- STYLE DES BULLETS (PUCES) --------------------
# Symbole utilisé pour les listes dans le CV
# Options disponibles :
#   "blacksquare"     : ■ Carré plein noir (moderne)
#   "bullet"          : • Point rond classique (standard)
#   "diamond"         : ◆ Losange plein (élégant)
#   "triangleright"   : ▶ Triangle pointant à droite (dynamique)
#   "circ"            : ○ Cercle vide (minimaliste)
#   "star"            : ★ Étoile pleine (créatif)
#   "checkmark"       : ✓ Coche (validation)
#   "rightarrow"      : → Flèche droite (progression)
#   "dash"            : — Tiret long (classique)
BULLET_STYLE = "bullet"

# Indentation des paragraphes (0pt = pas d'alinéa)
LATEX_PARINDENT = "0pt"

# Espacement entre paragraphes (selon format)
LATEX_PARSKIP_1PAGE = "0.1em"    # Compact pour 1 page
LATEX_PARSKIP_2PAGES = "0.3em"   # Standard pour 2 pages

# Marges du CV (selon format)
CV_MARGINS_1PAGE = "1.2cm"       # Marges réduites pour 1 page
CV_MARGINS_2PAGES = "1.6cm"      # Marges standard pour 2 pages

# Marges de la lettre
LETTRE_MARGINS = "2.5cm"

# Couleur principale (format RGB)
COLOR_DARKBLUE = "RGB}{20,40,90"

# Couleur secondaire
COLOR_GRAYTEXT = "RGB}{80,80,80"

# Espacements verticaux (selon format)
VSPACE_BETWEEN_EXPERIENCES_1PAGE = "0.1cm"
VSPACE_BETWEEN_EXPERIENCES_2PAGES = "0.15cm"

VSPACE_BETWEEN_FORMATIONS_1PAGE = "0.1cm"
VSPACE_BETWEEN_FORMATIONS_2PAGES = "0.15cm"

VSPACE_BETWEEN_PROJETS_1PAGE = "0.15cm"
VSPACE_BETWEEN_PROJETS_2PAGES = "0.3cm"

# Taille de l'en-tête (selon format)
HEADER_SPACING_1PAGE = "0.1cm"   # Espacement réduit
HEADER_SPACING_2PAGES = "0.3cm"  # Espacement standard


# ==================== MODE DE GÉNÉRATION ====================

# Mode de génération : "annonce" ou "spontanee"
# "annonce" : Génération basée sur une annonce de poste spécifique (URL d'annonce requise)
# "spontanee" : Candidature spontanée basée sur le site web de l'entreprise (URL site entreprise)
MODE_GENERATION = "annonce"  # Options : "annonce" ou "spontanee"

# Pour les candidatures spontanées : poste cible à mentionner
# Exemple : "Ingénieur IA", "Data Scientist", "Lead Machine Learning"
POSTE_CIBLE_SPONTANEE = "Ingénieur IA"


# ==================== PRÉPARATION ENTRETIEN ====================

# Nombre de questions techniques à générer
NB_QUESTIONS_TECHNIQUES = 10

# Nombre de questions de personnalité à générer
NB_QUESTIONS_PERSONNALITE = 5

# Tokens maximum pour les générations de préparation d'entretien
MAX_TOKENS_TOPO = 2000           # Topo général sur le poste
MAX_TOKENS_QUESTIONS_TECH = 3000  # Questions techniques avec réponses
MAX_TOKENS_QUESTIONS_PERSO = 2000 # Questions personnalité avec réponses

# Prompt système pour le topo de préparation
SYSTEM_PROMPT_TOPO = """Tu es un expert en préparation d'entretiens d'embauche dans les secteurs de l'ingénierie, 
de la tech et de l'IA. Tu analyses les postes en profondeur pour aider les candidats à se préparer efficacement."""

# Template pour le topo de préparation
PROMPT_TEMPLATE_TOPO = """Crée un topo de préparation d'entretien complet pour ce poste.

POSTE VISÉ:
- Titre: {poste}
- Entreprise: {entreprise}
- Compétences clés: {competences}
- Mission principale: {mission}

ANNONCE COMPLÈTE:
{annonce_text}

PROFIL DU CANDIDAT:
{profil_candidat}

Structure ton topo en 5 sections:

1. CONTEXTE DU POSTE (2-3 paragraphes)
   - Enjeux stratégiques du poste
   - Position dans l'organisation
   - Défis principaux à relever

2. COMPÉTENCES CLÉS À METTRE EN AVANT (liste à puces)
   - Les 5-7 compétences les plus importantes pour le poste
   - Pour chaque compétence, 1 exemple concret du candidat

3. POINTS DE VIGILANCE (liste à puces)
   - Ce que le recruteur va particulièrement scruter
   - Les éventuelles zones de faiblesse à anticiper

4. AXES DE DISCUSSION STRATÉGIQUES (liste numérotée)
   - 5-6 sujets à aborder proactivement en entretien
   - Questions pertinentes à poser au recruteur

5. PRÉPARATION TECHNIQUE
   - Technologies/outils à réviser en priorité
   - Concepts clés à maîtriser

Sois concret, factuel et actionnable. Fournis des insights stratégiques."""

# Prompt système pour les questions techniques
SYSTEM_PROMPT_QUESTIONS_TECH = """Tu es un expert technique en ingénierie, IA et simulation numérique.
Tu prépares des questions d'entretien techniques pertinentes et réalistes."""

# Template pour les questions techniques
PROMPT_TEMPLATE_QUESTIONS_TECH = """Génère {nb_questions} questions techniques d'entretien pour ce poste, avec leurs réponses détaillées.

POSTE VISÉ:
- Titre: {poste}
- Entreprise: {entreprise}
- Compétences clés: {competences}

ANNONCE COMPLÈTE:
{annonce_text}

PROFIL DU CANDIDAT:
Expériences: {experiences_resume}
Compétences: {competences_techniques}

CONSIGNES:
1. Génère exactement {nb_questions} questions progressives (du fondamental à l'avancé)
2. Les questions doivent être réalistes et en lien direct avec l'annonce
3. Couvre différents aspects : théorie, pratique, outils, méthodologie
4. Pour chaque question, fournis une réponse complète et technique (3-5 phrases)
5. Intègre des exemples concrets du profil du candidat quand pertinent

FORMAT DE RÉPONSE:
Pour chaque question, utilise ce format:

**Question X: [Titre de la question]**
[Énoncé détaillé de la question]

**Réponse:**
[Réponse technique complète avec exemples]

**Conseil:** [Un conseil stratégique pour bien répondre]

---"""

# Prompt système pour les questions de personnalité
SYSTEM_PROMPT_QUESTIONS_PERSO = """Tu es un expert en recrutement et culture d'entreprise.
Tu analyses les valeurs d'entreprise et prépares des questions comportementales pertinentes."""

# Template pour les questions de personnalité
PROMPT_TEMPLATE_QUESTIONS_PERSO = """Génère {nb_questions} questions de personnalité/comportementales pour ce poste, avec des réponses adaptées.

ENTREPRISE: {entreprise}
POSTE: {poste}

ANNONCE COMPLÈTE:
{annonce_text}

PROFIL DU CANDIDAT:
Nom: {nom}
Expériences: {experiences_resume}

CONSIGNES:
1. Génère exactement {nb_questions} questions comportementales/personnalité
2. Base-toi sur les valeurs implicites ou explicites de l'entreprise dans l'annonce
3. Les questions doivent permettre d'évaluer le fit culturel
4. Pour chaque question, fournis une réponse authentique utilisant la méthode STAR (Situation, Tâche, Action, Résultat)
5. Les réponses doivent s'appuyer sur les vraies expériences du candidat

Exemples de thématiques:
- Travail en équipe / Leadership
- Gestion de la complexité / Prise de décision
- Innovation / Initiative
- Adaptation au changement
- Gestion de conflits / Communication

FORMAT DE RÉPONSE:
Pour chaque question, utilise ce format:

**Question X: [Thématique]**
[Énoncé de la question]

**Réponse (méthode STAR):**
- **Situation:** [Contexte]
- **Tâche:** [Défi/objectif]
- **Action:** [Ce que j'ai fait concrètement]
- **Résultat:** [Impact mesurable]

**Message clé:** [L'idée principale à faire passer]

---"""


# ==================== SCRAPING ====================

# Longueur maximale de l'annonce à analyser
MAX_ANNONCE_LENGTH = 5000

# User Agent pour les requêtes HTTP
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Timeout des requêtes HTTP (en secondes)
HTTP_TIMEOUT = 30


# ==================== FICHIERS ET DOSSIERS ====================

# Dossier de stockage des candidatures
CANDIDATURES_DIR = "candidatures"
OUTPUT_FOLDER = "candidatures"

# Noms des fichiers générés
FILENAME_CV = "cv.tex"
FILENAME_LETTRE = "lettre_motivation.tex"
FILENAME_ANNONCE = "annonce_originale.txt"
FILENAME_ANALYSE = "analyse_poste.txt"


# ==================== COMPILATION LATEX ====================

# Compiler automatiquement en PDF
AUTO_COMPILE_PDF = True

# Nombre de passes de compilation LaTeX (2-3 recommandé pour les références)
LATEX_COMPILE_PASSES = 2

# Mode debug (affiche les erreurs de compilation)
DEBUG_MODE = False


# ==================== MESSAGES D'INTERFACE ====================

MSG_HEADER = """
============================================================
  GÉNÉRATEUR AUTOMATIQUE DE CV ET LETTRE DE MOTIVATION
============================================================
"""

MSG_CHARGEMENT_INFOS = "📥 Chargement des informations statiques..."
MSG_SCRAPING = "🔍 Scraping de l'annonce..."
MSG_ANALYSE_IA = "🤖 Analyse de l'annonce avec Claude ({model})..."
MSG_GENERATION_PROFIL = "✍️  Génération du profil adapté..."
MSG_GENERATION_LETTRE = "✍️  Génération de la lettre de motivation..."
MSG_CREATION_DOSSIER = "📁 Création du dossier de candidature..."
MSG_CREATION_LATEX = "📝 Création des fichiers LaTeX..."
MSG_CREATION_FICHIERS = "📝 Création des fichiers LaTeX..."
MSG_COMPILATION = "🔨 Compilation en PDF..."
MSG_SUCCESS = """
============================================================
✅ GÉNÉRATION TERMINÉE AVEC SUCCÈS!
============================================================
"""
MSG_SUCCES = """
============================================================
✅ GÉNÉRATION TERMINÉE AVEC SUCCÈS!
============================================================
"""
