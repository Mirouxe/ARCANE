# ⚡ Démarrage Rapide ARCANE

## 🎯 Choisir votre Mode

ARCANE propose **6 modes d'utilisation** selon vos besoins :

```
📂 modes/
├── 🌍 recherche_complete_generique/    # Recherche + Génération (tout profil)
├── ⭐ recherche_complete_specifique/   # Recherche + Génération (votre profil)
├── 🌍 generation_urls_generique/       # Batch URLs (tout profil)
├── ⭐ generation_urls_specifique/      # Batch URLs (votre profil)
├── 🌍 generation_simple_generique/     # Une offre (tout profil)
└── ⭐ generation_simple_specifique/    # Une offre (votre profil)
```

**Légende :**
- 🌍 **Générique** : Adapté à tout métier (développeur, designer, etc.)
- ⭐ **Spécifique** : Optimisé pour votre profil (catégories hardcodées)

---

## 🚀 Usage Personnel (Profil Spécifique) ⭐

### Génération pour une seule offre

```bash
cd modes/generation_simple_specifique/
./lancer.sh https://www.linkedin.com/jobs/view/1234567890
```

### Génération pour plusieurs offres (batch)

```bash
cd modes/generation_urls_specifique/

# Éditez urls.txt et ajoutez vos URLs
nano urls.txt

# Lancez la génération batch
./lancer.sh
```

### Recherche automatique + Génération

```bash
cd modes/recherche_complete_specifique/

./lancer.sh \
  --poste "Ingénieur IA" \
  --localisation "Paris" \
  --auto top5
```

---

## 🌍 Aider Quelqu'un (Profil Générique)

### 1. Préparer le profil

```bash
cd modes/generation_simple_generique/

# Éditez infos_statique.txt avec les infos de la personne
nano infos_statique.txt
```

**Format des compétences (générique) :**
```txt
[[competence]]
categorie: Programmation
contenu: Python, JavaScript, Java

[[competence]]
categorie: Frameworks
contenu: React, Node.js, Django
```

### 2. Générer la candidature

```bash
./lancer.sh https://job-url
```

---

## ⚙️ Personnaliser un Mode

Chaque mode a sa propre configuration dans `config.py` :

```bash
cd modes/generation_simple_specifique/
nano config.py
```

**Exemples de personnalisation :**

```python
# Changer le template CV
CV_TEMPLATE = "classique"  # ou "2colonnes"

# Changer le format
CV_FORMAT = "2pages"  # ou "1page"

# Changer le modèle IA (économiser)
CLAUDE_MODEL = "claude-3-haiku-20240307"

# Changer les bullets
BULLET_STYLE = "blacksquare"  # ou "bullet", "diamond", etc.
```

---

## 📊 Que se passe-t-il ?

### Fichiers Générés

Pour chaque candidature, vous obtenez :

```
candidatures/Poste_Entreprise_Date/
├── cv.pdf                        # CV personnalisé
├── lettre_motivation.pdf         # Lettre de motivation
├── preparation_entretien.txt     # Topo du poste
├── questions_techniques.txt      # 10 questions tech + réponses
└── questions_personnalite.txt    # 5 questions comportementales + réponses
```

### Workflow

1. **Scraping** : Récupération du contenu de l'annonce
2. **Analyse IA** : Claude extrait les compétences clés
3. **Adaptation** : Génération du profil et de la lettre adaptés
4. **LaTeX** : Création des fichiers `.tex`
5. **Compilation** : PDFs automatiques
6. **Préparation** : Questions d'entretien personnalisées

---

## 🔧 Modifier le Cœur du Système

Le code source est dans `core/` :

```bash
cd core/

# Scripts principaux
- generateur_cv_lettre.py       # Logique de génération
- recherche_postes.py            # Recherche multi-plateformes
- batch_depuis_urls.py           # Traitement batch
- wttj_playwright_scraper.py     # Scraping WTTJ
```

**⚠️ Important :** Les modifications dans `core/` affectent **tous les modes** !

---

## 📁 Structure Simplifiée

```
ARCANE/
│
├── core/           # Code Python (à modifier pour changer la logique)
├── templates/      # Templates LaTeX (CV, lettre)
├── modes/          # 6 modes d'utilisation (scripts + configs)
├── candidatures/   # Résultats générés
└── venv/           # Environnement Python
```

---

## 💡 Exemples Courants

### Exemple 1 : Génération rapide pour vous

```bash
cd modes/generation_simple_specifique/
./lancer.sh https://www.linkedin.com/jobs/view/123456
```

### Exemple 2 : Recherche pour un ami développeur

```bash
cd modes/recherche_complete_generique/

# Éditez d'abord infos_statique.txt avec ses infos
nano infos_statique.txt

# Lancez la recherche
./lancer.sh --poste "Développeur React" --localisation "Paris" --auto top5
```

### Exemple 3 : Batch de 10 offres (votre profil)

```bash
cd modes/generation_urls_specifique/

# Ajoutez vos 10 URLs dans urls.txt
nano urls.txt

# Lancez le batch
./lancer.sh
```

---

## ❓ FAQ Rapide

### Q: Quel mode dois-je utiliser ?
**R:** 
- **Pour vous** : Modes **spécifique** ⭐
- **Pour aider quelqu'un** : Modes **générique** 🌍

### Q: Comment changer le template CV ?
**R:** Éditez `config.py` dans le mode choisi → `CV_TEMPLATE = "classique"` ou `"2colonnes"`

### Q: Puis-je utiliser plusieurs modes en même temps ?
**R:** Oui ! Chaque mode est indépendant. Ouvrez plusieurs terminaux.

### Q: Où sont générées les candidatures ?
**R:** Dans le dossier `candidatures/` à la racine du projet.

### Q: Comment économiser les tokens IA ?
**R:** Changez `CLAUDE_MODEL` dans `config.py` → `"claude-3-haiku-20240307"` (plus économique)

---

## 🎓 Aller Plus Loin

- 📖 [README.md](README.md) - Documentation complète
- 🏗️ [ARCHITECTURE.md](ARCHITECTURE.md) - Architecture détaillée
- 🎭 [modes/*/README.md](modes/) - Documentation de chaque mode

---

**🚀 Prêt à générer vos candidatures !**
