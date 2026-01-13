# 🌍 Mode : Recherche Complète - Profil Générique

## 📝 Description

Ce mode permet de **rechercher des offres d'emploi** sur plusieurs plateformes (LinkedIn, Indeed, WTTJ) et de **générer automatiquement** les candidatures pour les offres sélectionnées.

**Type de profil :** Générique (adapté à tout métier : développeur, designer, manager, etc.)

---

## 🚀 Utilisation

```bash
./lancer.sh --poste "TITRE_POSTE" --localisation "VILLE" [OPTIONS]
```

### Exemples

```bash
# Recherche simple
./lancer.sh --poste "Développeur Full-Stack" --localisation "Paris" --auto top5

# Recherche avec critères avancés
./lancer.sh \
  --poste "Data Scientist" \
  --localisation "Lyon" \
  --seniorite "senior" \
  --domaines "Machine Learning,IA,Python" \
  --type "startup" \
  --nombre 15 \
  --auto top5

# Avec Playwright pour WTTJ
./lancer.sh --poste "Ingénieur DevOps" --localisation "Remote" --playwright --auto all
```

---

## ⚙️ Options

| Option | Description | Valeurs possibles |
|--------|-------------|-------------------|
| `--poste, -p` | Poste recherché **(REQUIS)** | Texte libre |
| `--localisation, -l` | Localisation | Ville ou "France" (défaut) |
| `--seniorite, -s` | Niveau de séniorité | `junior`, `confirmé`, `senior`, `lead` |
| `--domaines, -d` | Domaines (séparés par virgules) | Ex: "React,Node.js,Docker" |
| `--type, -t` | Type d'entreprise | `startup`, `PME`, `grande-entreprise` |
| `--nombre, -n` | Nombre d'offres par plateforme | Défaut: 10 |
| `--playwright` | Activer Playwright pour WTTJ | Flag (pas de valeur) |
| `--auto, -a` | Sélection automatique | `top5`, `all`, ou indices `1,3,5` |

---

## 📂 Fichiers de Configuration

### `config.py`
Configuration du mode (modèle IA, template CV, styles, etc.)

**Paramètres clés :**
- `MODE_PROFIL = "generique"` - Mode de traitement des compétences
- `CLAUDE_MODEL = "claude-sonnet-4-5-20250929"` - Modèle IA utilisé
- `CV_TEMPLATE = "2colonnes"` - Template du CV
- `CV_FORMAT = "1page"` - Format du CV

### `infos_statique.txt`
Informations personnelles du candidat (format générique avec `[[competence]]`)

**À personnaliser :** Remplacez l'exemple par les vraies informations du candidat.

---

## 📊 Workflow

1. **Recherche** : Le script recherche des offres sur LinkedIn, Indeed, WTTJ
2. **Scoring IA** : Claude analyse chaque offre et attribue un score de pertinence /10
3. **Sélection** : Selon `--auto`, le script sélectionne les offres (top5, all, ou indices spécifiques)
4. **Génération** : Pour chaque offre sélectionnée :
   - CV adapté (PDF)
   - Lettre de motivation (PDF)
   - Topo de préparation d'entretien
   - 10 questions techniques avec réponses
   - 5 questions de personnalité avec réponses
5. **Résultat** : Dossiers créés dans `candidatures/`

---

## 💡 Cas d'Usage

### Aider un ami développeur
```bash
# 1. Modifier infos_statique.txt avec ses infos
nano infos_statique.txt

# 2. Lancer la recherche
./lancer.sh --poste "Développeur React" --localisation "Paris" --auto top5
```

### Recherche pour un designer
```bash
# 1. Créer un infos_statique.txt avec catégories design
# [[competence]]
# categorie: Design UI/UX
# contenu: Figma, Adobe XD, Sketch
# ...

# 2. Lancer
./lancer.sh --poste "UI/UX Designer" --localisation "Lyon" --auto top5
```

---

## 🔧 Personnalisation

### Modifier le template CV
Éditez `config.py` :
```python
CV_TEMPLATE = "classique"  # Au lieu de "2colonnes"
```

### Changer le modèle IA (plus économique)
Éditez `config.py` :
```python
CLAUDE_MODEL = "claude-3-haiku-20240307"  # Plus rapide et moins cher
```

### Ajuster le format CV
Éditez `config.py` :
```python
CV_FORMAT = "2pages"  # Pour un CV détaillé
```

---

## ⚠️ Important

- ✅ Mode **générique** : utilise des catégories de compétences dynamiques
- ✅ Adapté à **tout type de profil**
- ✅ Nécessite `infos_statique.txt` au **format générique** avec `[[competence]]`

---

## 📚 Ressources

- [ARCHITECTURE.md](../../ARCHITECTURE.md) - Architecture complète du système
- [README.md](../../README.md) - Documentation principale
- [config.py](config.py) - Configuration de ce mode
- [infos_statique.txt](infos_statique.txt) - Informations du profil
