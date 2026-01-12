# 🚀 ARCANE - Système Automatique de Génération de CV et Lettres de Motivation

**ARCANE** (Automated Resume and Cover letter ANalysis Engine) est un système intelligent qui automatise la création de CV personnalisés, lettres de motivation et préparation d'entretiens en utilisant l'IA Claude Sonnet 4.5.

[![Python](https://img.shields.io/badge/Python-3.14+-blue.svg)](https://www.python.org/)
[![Claude](https://img.shields.io/badge/Claude-Sonnet%204.5-purple.svg)](https://www.anthropic.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## ✨ Fonctionnalités

### 🎯 **Génération Automatique**
- ✅ **CV personnalisé** (PDF) adapté à chaque offre
- ✅ **Lettre de motivation** (PDF) ciblée
- ✅ **Topo de préparation d'entretien** avec insights stratégiques
- ✅ **10 questions techniques** avec réponses détaillées
- ✅ **5 questions de personnalité** (méthode STAR)

### 🔍 **Recherche Intelligente**
- ✅ **Recherche multi-plateformes** (LinkedIn, Indeed, WTTJ, Apec)
- ✅ **Analyse de pertinence IA** (scoring automatique /10)
- ✅ **Critères avancés** (séniorité, domaines, type d'entreprise)
- ✅ **Scraping WTTJ** avec Playwright (optionnel)

### 📝 **Personnalisation Avancée**
- ✅ **2 templates CV** : Classique 1 colonne ou Moderne 2 colonnes
- ✅ **Styles configurables** : polices, couleurs, puces, marges
- ✅ **Prompts IA personnalisables** pour chaque section
- ✅ **Mode candidature spontanée** (analyse site web entreprise)

---

## 📋 Prérequis

- **Python 3.14+**
- **LaTeX** (MacTeX, MiKTeX ou TeX Live)
- **Clé API Claude** (Anthropic)
- **Playwright** (optionnel, pour scraping WTTJ)

---

## 🚀 Installation

### 1️⃣ **Cloner le Repository**
```bash
git clone https://github.com/Mirouxe/ARCANE.git
cd ARCANE
```

### 2️⃣ **Créer l'Environnement Virtuel**
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# ou
venv\Scripts\activate  # Windows
```

### 3️⃣ **Installer les Dépendances**
```bash
pip install -r requirements.txt
```

### 4️⃣ **Installer LaTeX**

**macOS:**
```bash
brew install --cask mactex
```

**Linux:**
```bash
sudo apt-get install texlive-full
```

**Windows:**  
Téléchargez [MiKTeX](https://miktex.org/)

### 5️⃣ **Configurer l'API Claude**

1. Obtenez votre clé API sur [console.anthropic.com](https://console.anthropic.com/)
2. Copiez le fichier de configuration :
```bash
cp env.exemple .env
```
3. Éditez `.env` et ajoutez votre clé :
```
ANTHROPIC_API_KEY=sk-ant-votre-cle-api-ici
```

### 6️⃣ **Configurer vos Informations**

```bash
cp infos_statique_exemple.txt infos_statique.txt
# Éditez infos_statique.txt avec vos vraies informations
```

### 7️⃣ **[Optionnel] Installer Playwright pour WTTJ**

Si vous voulez scraper Welcome to the Jungle automatiquement :
```bash
./installer_playwright.sh
```

---

## 📖 Utilisation

### 🎯 **Cas d'Usage 1: Répondre à une Annonce**

```bash
./lancer_generateur.sh "https://www.linkedin.com/jobs/view/123456"
```

**Génère automatiquement:**
- CV adapté (PDF + LaTeX)
- Lettre de motivation (PDF + LaTeX)
- Topo de préparation d'entretien
- 10 questions techniques avec réponses
- 5 questions de personnalité avec réponses STAR

---

### 🎯 **Cas d'Usage 2: Candidature Spontanée**

```bash
./candidature_spontanee.sh "https://www.entreprise.com" "Ingénieur IA"
```

Analyse le site web de l'entreprise et génère une candidature adaptée.

---

### 🎯 **Cas d'Usage 3: Recherche Automatique**

**Recherche simple:**
```bash
./recherche_avancee.sh \
  --poste "Data Scientist" \
  --localisation "Paris" \
  --auto top5
```

**Recherche avec critères:**
```bash
./recherche_avancee.sh \
  --poste "ML Engineer" \
  --localisation "Remote" \
  --seniorite "senior" \
  --domaines "Deep Learning,NLP" \
  --type "startup" \
  --auto all
```

**Options disponibles:**
- `--poste, -p` : Poste recherché (REQUIS)
- `--localisation, -l` : Localisation (défaut: France)
- `--seniorite, -s` : junior | confirmé | senior | lead
- `--domaines, -d` : Domaines séparés par virgule (ML,IA,NLP)
- `--type, -t` : startup | PME | grande-entreprise
- `--nombre, -n` : Nombre d'offres par plateforme (défaut: 10)
- `--playwright` : Activer Playwright pour WTTJ
- `--auto, -a` : Sélection automatique (top5 | all | 1,2,3)

---

### 🎯 **Cas d'Usage 4: Génération en Batch**

1. Créez un fichier `urls_a_traiter.txt`:
```
https://www.linkedin.com/jobs/view/123456
https://www.welcometothejungle.com/fr/companies/xxx/jobs/yyy
https://fr.indeed.com/viewjob?jk=abc123
```

2. Lancez la génération batch:
```bash
./batch_urls.sh
```

Génère automatiquement pour toutes les URLs ! 🚀

---

## ⚙️ Configuration

### **Fichier `config.py`**

Tous les paramètres sont centralisés dans `config.py` :

#### **Modèle IA**
```python
CLAUDE_MODEL = "claude-sonnet-4-5-20250929"  # Le plus performant
TEMPERATURE = 0.7  # Créativité (0.0 = déterministe, 1.0 = créatif)
```

#### **Template CV**
```python
CV_TEMPLATE = "2colonnes"  # ou "classique"
CV_FORMAT = "1page"  # ou "2pages"
```

#### **Styles**
```python
FONT_SIZE_BASE = "10pt"  # 10pt, 11pt, 12pt
BULLET_STYLE = "bullet"  # bullet, blacksquare, checkmark, etc.
COLORIZE_MISSION_TITLES = True  # Titres missions en bleu
```

#### **Nombre de Questions**
```python
NB_QUESTIONS_TECHNIQUES = 10
NB_QUESTIONS_PERSONNALITE = 5
```

Consultez `config.py` pour la liste complète des options !

---

## 📂 Structure des Dossiers

```
ARCANE/
├── 📄 Scripts Principaux
│   ├── generateur_cv_lettre.py      # Moteur principal
│   ├── recherche_postes.py          # Recherche multi-plateformes
│   ├── batch_depuis_urls.py         # Génération batch
│   └── wttj_playwright_scraper.py   # Scraper WTTJ
│
├── 🔧 Scripts Shell
│   ├── lancer_generateur.sh         # Générer pour 1 annonce
│   ├── candidature_spontanee.sh     # Candidature spontanée
│   ├── recherche_avancee.sh         # Recherche avec critères
│   ├── rechercher_et_generer.sh     # Mode interactif
│   ├── batch_urls.sh                # Batch depuis fichier
│   └── installer_playwright.sh      # Installer Playwright
│
├── 📝 Templates LaTeX
│   ├── cv_template.tex              # CV 1 colonne
│   ├── cv_template_2col.tex         # CV 2 colonnes
│   └── lettre_motivation_template.tex
│
├── ⚙️ Configuration
│   ├── config.py                    # Configuration centralisée
│   ├── infos_statique.txt           # Vos informations (PRIVÉ)
│   ├── infos_statique_exemple.txt   # Exemple
│   ├── .env                         # Clé API (PRIVÉ)
│   └── env.exemple                  # Exemple
│
├── 📚 Documentation
│   ├── README.md                    # Ce fichier
│   ├── GUIDE_UTILISATION.txt        # Guide détaillé
│   ├── EXEMPLES_RECHERCHE.md        # Exemples de recherche
│   └── STRATEGIES_SCRAPING.md       # Stratégies scraping
│
└── 📁 Générés (ignorés par git)
    └── candidatures/                # Dossiers de candidatures
        └── Poste_Entreprise_Date/
            ├── cv.pdf
            ├── lettre_motivation.pdf
            ├── preparation_entretien.txt
            ├── questions_techniques.txt
            └── questions_personnalite.txt
```

---

## 💰 Coûts API Claude

### **Par Candidature** (~0.20€)
- Analyse annonce: ~0.01€
- Génération profil: ~0.02€
- Génération lettre: ~0.03€
- Topo entretien: ~0.04€
- Questions techniques: ~0.06€
- Questions personnalité: ~0.04€

### **Recherche + Batch**
- Analyse de 30 offres: ~0.05€
- Génération de 5 candidatures: ~1.00€

**Total ~1.05€ pour une session complète** (recherche + 5 candidatures)

---

## 🎨 Exemples de Résultats

### **Templates CV Disponibles**

**1. Classique (1 colonne)**
- Format traditionnel
- Lecture linéaire
- Idéal pour recruteurs conservateurs

**2. Moderne (2 colonnes)**
- Style journal scientifique
- Gain de place
- Aspect visuel moderne

### **Personnalisation**

Changez le style de puces en 1 ligne dans `config.py`:
```python
BULLET_STYLE = "blacksquare"  # ■
BULLET_STYLE = "bullet"       # •
BULLET_STYLE = "checkmark"    # ✓
```

---

## 🔍 Plateformes Supportées

| Plateforme | Status | Vitesse | Qualité Offres |
|------------|--------|---------|----------------|
| **LinkedIn** | ✅ Excellent | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ |
| **Indeed** | ⚠️ Bloqué souvent | ⚡⚡⚡ | ⭐⭐⭐ |
| **WTTJ** (Playwright) | ✅ Excellent | ⚡ | ⭐⭐⭐⭐⭐ |
| **Apec** | ⚠️ Limité | ⚡⚡ | ⭐⭐⭐⭐ |
| **Batch URLs** | ✅ Parfait | ⚡ | ⭐⭐⭐⭐⭐ |

**Recommandation:** LinkedIn + Batch URLs pour meilleure fiabilité

---

## 🛠️ Dépannage

### **Problème: ANTHROPIC_API_KEY non définie**
```bash
# Vérifiez votre fichier .env
cat .env
# Doit contenir: ANTHROPIC_API_KEY=sk-ant-...
```

### **Problème: pdflatex not found**
```bash
# macOS
brew install --cask mactex

# Linux
sudo apt-get install texlive-full
```

### **Problème: Aucune offre trouvée**
- Simplifiez les critères de recherche
- Utilisez --auto top5 pour éviter les blocages
- Ou utilisez le mode batch avec URLs directes

### **Problème: WTTJ ne trouve rien**
```bash
# Installez Playwright
./installer_playwright.sh

# Puis utilisez --playwright
./recherche_avancee.sh -p "Data Scientist" --playwright
```

---

## 📊 Workflow Recommandé

### **Pour une Candidature Rapide** (5 minutes)
```bash
./lancer_generateur.sh "https://linkedin.com/jobs/view/123456"
```

### **Pour une Recherche Approfondie** (30 minutes)
```bash
# 1. Recherche automatique
./recherche_avancee.sh -p "Data Scientist" -l "Paris" --auto top5

# 2. Revue des CVs générés
open candidatures/*/cv.pdf

# 3. Personnalisation si nécessaire
code candidatures/Poste_Entreprise_Date/cv.tex
```

### **Pour Candidatures Multiples** (1 heure)
```bash
# 1. Recherchez manuellement sur LinkedIn, WTTJ
# 2. Copiez les URLs dans urls_a_traiter.txt
# 3. Lancez le batch
./batch_urls.sh
```

---

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- 🐛 Signaler des bugs
- 💡 Proposer des améliorations
- 📝 Améliorer la documentation
- 🔧 Ajouter de nouvelles fonctionnalités

---

## 📄 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

## 🙏 Remerciements

- **Anthropic** pour Claude Sonnet 4.5
- **LaTeX** pour le rendu professionnel des documents
- **Playwright** pour le scraping moderne

---

## 📬 Contact

Pour toute question ou suggestion, ouvrez une **issue** sur GitHub.

---

**⭐ Si ce projet vous est utile, n'hésitez pas à lui donner une étoile !**

---

## 🔐 Sécurité

- ⚠️ Ne commitez **JAMAIS** votre `.env` ou `infos_statique.txt`
- ⚠️ Ajoutez toujours `candidatures/` au `.gitignore`
- ⚠️ Ne partagez jamais votre clé API publiquement

---

Made with ❤️ by [Mirouxe](https://github.com/Mirouxe)
