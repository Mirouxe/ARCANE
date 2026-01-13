# 🏗️ Architecture ARCANE

## 📁 Structure du Projet

```
ARCANE/
├── core/                              # 🎯 CŒUR DU SYSTÈME (scripts Python)
│   ├── generateur_cv_lettre.py       # Générateur principal
│   ├── recherche_postes.py            # Recherche multi-plateformes
│   ├── batch_depuis_urls.py           # Génération batch
│   ├── wttj_playwright_scraper.py     # Scraper WTTJ
│   └── config.py                      # Config active (copié depuis modes/)
│
├── templates/                         # 📄 TEMPLATES LATEX
│   ├── cv_template.tex                # CV classique 1 colonne
│   ├── cv_template_2col.tex           # CV moderne 2 colonnes
│   └── lettre_motivation_template.tex # Lettre de motivation
│
├── modes/                             # 🎭 MODES D'UTILISATION
│   │
│   ├── recherche_complete_generique/  # 🌍 Recherche + Génération (profil générique)
│   │   ├── lancer.sh                  # Script de lancement
│   │   ├── config.py                  # Configuration (MODE_PROFIL = "generique")
│   │   ├── infos_statique.txt         # Informations du profil (exemple)
│   │   └── README.md                  # Documentation du mode
│   │
│   ├── recherche_complete_specifique/ # ⭐ Recherche + Génération (votre profil)
│   │   ├── lancer.sh
│   │   ├── config.py                  # Configuration (MODE_PROFIL = "specifique")
│   │   ├── infos_statique.txt         # VOS informations personnelles
│   │   └── README.md
│   │
│   ├── generation_urls_generique/     # 🌍 Batch depuis liste URLs (générique)
│   │   ├── lancer.sh
│   │   ├── config.py
│   │   ├── infos_statique.txt
│   │   ├── urls.txt                   # Liste des URLs à traiter
│   │   └── README.md
│   │
│   ├── generation_urls_specifique/    # ⭐ Batch depuis liste URLs (spécifique)
│   │   ├── lancer.sh
│   │   ├── config.py
│   │   ├── infos_statique.txt
│   │   ├── urls.txt
│   │   └── README.md
│   │
│   ├── generation_simple_generique/   # 🌍 Génération unique (générique)
│   │   ├── lancer.sh
│   │   ├── config.py
│   │   ├── infos_statique.txt
│   │   └── README.md
│   │
│   └── generation_simple_specifique/  # ⭐ Génération unique (spécifique)
│       ├── lancer.sh
│       ├── config.py
│       ├── infos_statique.txt
│       └── README.md
│
├── candidatures/                      # 📦 CANDIDATURES GÉNÉRÉES
│   └── [dossiers par candidature]
│
├── venv/                              # 🐍 Environnement virtuel Python
├── .env                               # 🔑 Clé API (ignoré par git)
├── .gitignore                         # 🚫 Fichiers ignorés
├── requirements.txt                   # 📋 Dépendances Python
├── README.md                          # 📖 Documentation principale
└── ARCHITECTURE.md                    # 🏗️ Ce fichier
```

---

## 🎯 Principe de Fonctionnement

### Cœur Unique (`core/`)

Tous les scripts Python sont centralisés dans `core/`. **C'est le seul endroit où vous modifiez le code.**

**Avantages :**
- ✅ Un seul point de maintenance
- ✅ Mise à jour simultanée de tous les modes
- ✅ Code unifié et testé

### Modes d'Utilisation (`modes/`)

Chaque mode est un **dossier avec sa propre configuration** :

| Fichier | Description |
|---------|-------------|
| `lancer.sh` | Script shell qui appelle le cœur avec la bonne config |
| `config.py` | Configuration spécifique (MODE_PROFIL, CV_TEMPLATE, etc.) |
| `infos_statique.txt` | Informations du profil utilisé |
| `urls.txt` | *(modes batch)* Liste des URLs à traiter |
| `README.md` | Documentation du mode |

**Fonctionnement :**
1. Vous allez dans un dossier mode : `cd modes/generation_simple_specifique/`
2. Vous lancez : `./lancer.sh https://job-url`
3. Le script copie `config.py` et `infos_statique.txt` dans le cœur
4. Le script appelle le Python du cœur : `python3 ../../core/generateur_cv_lettre.py`
5. La génération se fait avec la config du mode choisi

---

## 🎭 Les 6 Modes Disponibles

### 1️⃣ **Recherche Complète Générique** 🌍
- **Dossier :** `modes/recherche_complete_generique/`
- **Usage :** Recherche d'offres + génération automatique (profil générique)
- **Commande :** `./lancer.sh --poste "Développeur" --localisation "Paris" --auto top5`
- **Profil :** Générique (n'importe quel métier)

### 2️⃣ **Recherche Complète Spécifique** ⭐
- **Dossier :** `modes/recherche_complete_specifique/`
- **Usage :** Recherche d'offres + génération automatique (votre profil)
- **Commande :** `./lancer.sh --poste "Ingénieur IA" --localisation "Paris" --auto top5`
- **Profil :** Spécifique (vos catégories hardcodées)

### 3️⃣ **Génération URLs Générique** 🌍
- **Dossier :** `modes/generation_urls_generique/`
- **Usage :** Génération batch depuis liste d'URLs (profil générique)
- **Commande :** `./lancer.sh` (lit `urls.txt`)
- **Profil :** Générique

### 4️⃣ **Génération URLs Spécifique** ⭐
- **Dossier :** `modes/generation_urls_specifique/`
- **Usage :** Génération batch depuis liste d'URLs (votre profil)
- **Commande :** `./lancer.sh` (lit `urls.txt`)
- **Profil :** Spécifique

### 5️⃣ **Génération Simple Générique** 🌍
- **Dossier :** `modes/generation_simple_generique/`
- **Usage :** Génération pour une seule offre (profil générique)
- **Commande :** `./lancer.sh https://job-url`
- **Profil :** Générique

### 6️⃣ **Génération Simple Spécifique** ⭐
- **Dossier :** `modes/generation_simple_specifique/`
- **Usage :** Génération pour une seule offre (votre profil)
- **Commande :** `./lancer.sh https://job-url`
- **Profil :** Spécifique

---

## 🔧 Modifier le Système

### ✏️ Modifier le code (logique métier)

**Emplacement :** `core/`

**Fichiers à modifier :**
- `generateur_cv_lettre.py` - Logique de génération
- `recherche_postes.py` - Logique de recherche
- `batch_depuis_urls.py` - Traitement batch
- `wttj_playwright_scraper.py` - Scraping WTTJ

**Impact :** Tous les modes sont mis à jour automatiquement ✅

### ⚙️ Modifier la configuration d'un mode

**Emplacement :** `modes/<nom_du_mode>/config.py`

**Exemples de modifications :**
```python
# Changer le modèle IA
CLAUDE_MODEL = "claude-3-haiku-20240307"  # Plus économique

# Changer le template CV
CV_TEMPLATE = "classique"  # Au lieu de "2colonnes"

# Changer le format CV
CV_FORMAT = "2pages"  # Au lieu de "1page"

# Changer les bullets
BULLET_STYLE = "blacksquare"  # Au lieu de "bullet"
```

**Impact :** Seulement ce mode est affecté ✅

### 👤 Modifier les informations personnelles d'un mode

**Emplacement :** `modes/<nom_du_mode>/infos_statique.txt`

**Impact :** Seulement ce mode est affecté ✅

---

## 🚀 Workflow Recommandé

### Pour votre usage personnel (Profil Spécifique) ⭐

1. **Génération unique :**
   ```bash
   cd modes/generation_simple_specifique/
   ./lancer.sh https://job-url
   ```

2. **Génération batch :**
   ```bash
   cd modes/generation_urls_specifique/
   # Éditez urls.txt avec vos URLs
   ./lancer.sh
   ```

3. **Recherche complète :**
   ```bash
   cd modes/recherche_complete_specifique/
   ./lancer.sh --poste "Ingénieur IA" --localisation "Paris" --auto top5
   ```

### Pour aider quelqu'un (Profil Générique) 🌍

1. **Modifiez `infos_statique.txt` dans le mode générique**
   ```bash
   cd modes/generation_simple_generique/
   nano infos_statique.txt  # Ajustez les infos
   ```

2. **Lancez la génération**
   ```bash
   ./lancer.sh https://job-url
   ```

---

## 📝 Ajouter un Nouveau Mode

Si vous voulez créer un mode personnalisé :

```bash
# 1. Créer le dossier
mkdir modes/mon_mode_perso/

# 2. Copier depuis un mode existant
cp modes/generation_simple_generique/* modes/mon_mode_perso/

# 3. Personnaliser
cd modes/mon_mode_perso/
# Éditez config.py, infos_statique.txt, lancer.sh
# Ajustez le script lancer.sh si besoin

# 4. Tester
./lancer.sh <arguments>
```

---

## 🎨 Avantages de cette Architecture

| Avantage | Description |
|----------|-------------|
| **🔧 Maintenance facile** | Un seul endroit pour le code (`core/`) |
| **🎭 Flexibilité** | Plusieurs configurations possibles |
| **👥 Multi-utilisateurs** | Profils génériques pour aider d'autres personnes |
| **📦 Isolation** | Chaque mode est indépendant |
| **🚀 Évolutivité** | Facile d'ajouter de nouveaux modes |
| **⚡ Performance** | Pas de duplication de code |

---

## ❓ FAQ

### Q: Dois-je modifier les scripts dans `core/` ?
**R:** Seulement si vous voulez changer la logique du système. Sinon, modifiez seulement les `config.py` dans les modes.

### Q: Puis-je supprimer un mode ?
**R:** Oui, supprimez simplement le dossier dans `modes/`. Cela n'affecte pas les autres modes.

### Q: Comment partager un mode avec quelqu'un ?
**R:** Compressez le dossier du mode + le dossier `core/` + `templates/` + `.env.exemple` + `requirements.txt`.

### Q: Quelle est la différence entre générique et spécifique ?
**R:** 
- **Spécifique** : Catégories de compétences hardcodées (Scientific AI, Simulation, etc.)
- **Générique** : Catégories dynamiques (adapté à tout métier)

Voir [GUIDE_MODES.md](GUIDE_MODES.md) pour plus de détails.

---

**🎯 L'architecture ARCANE : Un cœur, plusieurs visages !**
