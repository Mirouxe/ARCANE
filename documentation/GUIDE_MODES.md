# Guide : Modes de Profil (Spécifique vs Générique)

## Vue d'ensemble

Le système **ARCANE** supporte deux modes de fonctionnement pour s'adapter à différents profils :

| Mode | Usage | Description |
|------|-------|-------------|
| **`specifique`** | Usage personnel (votre profil) | Catégories de compétences hardcodées, optimisées pour votre domaine |
| **`generique`** | Multi-utilisateurs | Catégories de compétences dynamiques, adapté à tout profil |

---

## 🎯 Mode "specifique" (Par défaut)

### Quand l'utiliser ?
✅ Pour votre usage personnel  
✅ Quand vous avez des catégories de compétences spécifiques (ex: Scientific AI, Simulation, etc.)  
✅ Pour un profil technique spécialisé  

### Configuration

**Dans `config.py` :**
```python
MODE_PROFIL = "specifique"
```

**Dans `infos_statique.txt` :**
```txt
# COMPÉTENCES
competences_scientific_ai: |
  Physics-Informed Neural Networks (DeepXDE), Deep Learning (TensorFlow, PyTorch)

competences_simulation: |
  CFD (STAR CCM+), Éléments Finis (SAMCEF NASTRAN)

competences_generative_ai: |
  LLM locaux (Mistral), RAG, Systèmes Multi-Agents

competences_informatique: |
  Python, MATLAB, Docker, Kubernetes
```

### Avantages
- ✅ Catégories optimisées pour votre domaine
- ✅ Templates LaTeX pré-configurés
- ✅ Sections de compétences bien structurées

---

## 🌍 Mode "generique" (Multi-profils)

### Quand l'utiliser ?
✅ Pour générer des CV pour différentes personnes  
✅ Pour des profils variés (développeur, designer, manager, etc.)  
✅ Pour partager le système avec d'autres utilisateurs  

### Configuration

**Dans `config.py` :**
```python
MODE_PROFIL = "generique"
```

**Dans `infos_statique.txt` :**
```txt
# COMPÉTENCES (Format générique)
[[competence]]
categorie: Front-End
contenu: React, Vue.js, TypeScript, HTML5, CSS3

[[competence]]
categorie: Back-End
contenu: Node.js, Express, Python Django, REST API

[[competence]]
categorie: Base de données
contenu: PostgreSQL, MongoDB, Redis

[[competence]]
categorie: Cloud & DevOps
contenu: AWS, Docker, Kubernetes, CI/CD
```

### Exemple complet
Voir le fichier `infos_statique_exemple_generique.txt` pour un exemple de profil développeur full-stack.

### Avantages
- ✅ Totalement flexible : n'importe quelle catégorie
- ✅ Adapté à tous les métiers
- ✅ Facile à partager avec d'autres personnes

---

## 📋 Comparaison des formats

### Mode Spécifique
```txt
# COMPÉTENCES
competences_scientific_ai: |
  Physics-Informed Neural Networks, DeepXDE

competences_simulation: |
  CFD, Éléments Finis
```

### Mode Générique
```txt
# COMPÉTENCES
[[competence]]
categorie: Machine Learning
contenu: TensorFlow, PyTorch, Scikit-learn

[[competence]]
categorie: Développement
contenu: Python, JavaScript, Docker
```

---

## 🔄 Basculer entre les modes

### Étape 1 : Modifier `config.py`
```python
# Pour mode spécifique (votre profil)
MODE_PROFIL = "specifique"

# OU pour mode générique (tout profil)
MODE_PROFIL = "generique"
```

### Étape 2 : Adapter `infos_statique.txt`

**Si vous passez en mode générique :**
1. Supprimez les lignes `competences_*` (ancien format)
2. Ajoutez des blocs `[[competence]]` (nouveau format)
3. Référez-vous à `infos_statique_exemple_generique.txt`

**Si vous revenez en mode spécifique :**
1. Supprimez les blocs `[[competence]]`
2. Restaurez les lignes `competences_*`
3. Référez-vous à votre `infos_statique.txt` original

### Étape 3 : Tester
```bash
./lancer_generateur.sh https://example.com/job-posting
```

---

## 🎨 Personnalisation avancée

### Ajouter des catégories personnalisées (mode générique)

Vous pouvez créer autant de catégories que nécessaire :

```txt
[[competence]]
categorie: Langages de programmation
contenu: Python, Java, C++, JavaScript

[[competence]]
categorie: Frameworks Web
contenu: React, Angular, Vue.js, Django

[[competence]]
categorie: Design
contenu: Figma, Adobe XD, Sketch, Photoshop

[[competence]]
categorie: Gestion de projet
contenu: Agile, Scrum, Jira, Confluence

[[competence]]
categorie: Soft Skills
contenu: Leadership, Communication, Mentorat
```

### Modifier les templates LaTeX (avancé)

Les templates supportent automatiquement les deux modes :

- **`cv_template.tex`** : CV classique 1 colonne
- **`cv_template_2col.tex`** : CV 2 colonnes

Le placeholder `{COMPETENCES_SECTION}` est automatiquement rempli selon le mode :
- Mode **spécifique** : Vide (les placeholders individuels sont utilisés)
- Mode **générique** : Contient toutes les catégories générées dynamiquement

---

## ❓ FAQ

### Q: Puis-je mélanger les deux modes ?
**R:** Non, vous devez choisir un seul mode. Cependant, en mode générique, vous pouvez recréer vos catégories spécifiques.

### Q: Quel mode est recommandé ?
**R:** 
- **Pour vous** : `specifique` (optimisé et pré-configuré)
- **Pour partager** : `generique` (flexible et universel)

### Q: Le mode affecte-t-il l'IA ?
**R:** Oui, les prompts IA s'adaptent automatiquement au mode choisi pour mieux contextualiser les compétences.

### Q: Dois-je modifier les templates LaTeX ?
**R:** Non, les templates sont déjà compatibles avec les deux modes.

---

## 🚀 Exemples d'usage

### Scénario 1 : Vous utilisez le système pour vous
```python
# config.py
MODE_PROFIL = "specifique"
```
→ Utilisez votre `infos_statique.txt` actuel avec les catégories Scientific AI, Simulation, etc.

### Scénario 2 : Vous aidez un ami développeur
```python
# config.py
MODE_PROFIL = "generique"
```
→ Créez un nouveau fichier (ex: `infos_statique_ami.txt`) avec des catégories Front-End, Back-End, etc.
→ Lancez : `./lancer_generateur.sh https://job-url`

### Scénario 3 : Vous proposez le système à un designer
```python
# config.py
MODE_PROFIL = "generique"
```
→ Créez `infos_statique_designer.txt` avec des catégories : Design UI/UX, Outils, Prototypage, etc.

---

## 📚 Ressources

- **Exemple mode spécifique** : `infos_statique.txt` (votre profil actuel)
- **Exemple mode générique** : `infos_statique_exemple_generique.txt`
- **Configuration** : `config.py`
- **Support** : README.md

---

**Note :** Le mode générique a été conçu pour rendre ARCANE utilisable par n'importe qui, tout en préservant l'optimisation du mode spécifique pour votre usage personnel.
