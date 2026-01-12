# 🔍 Exemples de Recherche Avancée

## ✅ **Système de Recherche Installé avec Succès !**

Vous disposez maintenant d'un système complet de recherche de postes avec :
- ✅ **Critères avancés** : Séniorité, domaines, type d'entreprise
- ✅ **LinkedIn fonctionnel** (source principale fiable)
- ✅ **Playwright pour WTTJ** (optionnel, requiert installation)
- ✅ **Génération en batch** automatique

---

## 📋 **Méthodes de Recherche Disponibles**

### **1. Mode Interactif (Recommandé pour débuter)**
```bash
./rechercher_et_generer.sh
```
Le script vous posera des questions étape par étape.

### **2. Mode Ligne de Commande (Rapide)**
```bash
./recherche_avancee.sh --poste "Data Scientist" --localisation "Paris"
```

### **3. Mode Batch depuis URLs (Le plus fiable)**
```bash
# 1. Créez urls_a_traiter.txt avec vos URLs
# 2. Lancez :
./batch_urls.sh
```

---

## 🎯 **Exemples Concrets**

### **Exemple 1: Recherche Simple**
```bash
./recherche_avancee.sh \
  --poste "Data Scientist" \
  --localisation "Paris"
```

### **Exemple 2: Recherche avec Séniorité**
```bash
./recherche_avancee.sh \
  --poste "Machine Learning Engineer" \
  --localisation "Remote" \
  --seniorite "senior"
```

### **Exemple 3: Recherche avec Domaines**
```bash
./recherche_avancee.sh \
  --poste "Ingénieur IA" \
  --localisation "Lyon" \
  --domaines "NLP,Computer Vision"
```

### **Exemple 4: Recherche Startup**
```bash
./recherche_avancee.sh \
  --poste "Data Scientist" \
  --localisation "Paris" \
  --type "startup" \
  --seniorite "confirmé"
```

### **Exemple 5: Recherche avec Playwright (WTTJ)**
```bash
./recherche_avancee.sh \
  --poste "ML Engineer" \
  --localisation "France" \
  --playwright
```

### **Exemple 6: Recherche Complète**
```bash
./recherche_avancee.sh \
  --poste "Lead Data Scientist" \
  --localisation "Paris" \
  --seniorite "lead" \
  --domaines "Deep Learning,MLOps" \
  --type "grande-entreprise" \
  --nombre 5 \
  --playwright
```

---

## 💡 **Conseils d'Utilisation**

### **Pour de Meilleurs Résultats**

1. **Commencez simple** : Testez d'abord avec juste le poste
   ```bash
   ./recherche_avancee.sh -p "Data Scientist"
   ```

2. **Ajoutez progressivement** des critères si trop de résultats
   ```bash
   ./recherche_avancee.sh -p "Data Scientist" -l "Paris" -s "senior"
   ```

3. **Ne surchargez pas** : Trop de critères = aucun résultat
   - ❌ Mauvais : `--poste "X" --seniorite "Y" --domaines "A,B,C" --type "Z"`
   - ✅ Bon : `--poste "X" --localisation "Paris" --seniorite "senior"`

4. **Utilisez Playwright pour WTTJ** si vous voulez vraiment ces offres
   ```bash
   ./recherche_avancee.sh -p "Data Scientist" --playwright
   ```

---

## 🚀 **Workflow Recommandé**

### **Stratégie Efficace en 3 Étapes**

#### **Étape 1: Recherche Large (LinkedIn)**
```bash
# Recherche simple pour obtenir ~30 offres
./recherche_avancee.sh --poste "Data Scientist" --localisation "Paris" --nombre 10
```

#### **Étape 2: Sélection Interactive**
Le script affiche les offres triées par pertinence IA (score /10).
Sélectionnez celles qui vous intéressent :
- Tapez `1 3 5` pour les offres 1, 3 et 5
- Tapez `top5` pour les 5 meilleures
- Tapez `all` pour tout traiter

#### **Étape 3: Génération Automatique**
Le script génère automatiquement pour chaque offre sélectionnée :
- ✅ CV personnalisé
- ✅ Lettre de motivation
- ✅ Topo de préparation d'entretien
- ✅ 10 questions techniques avec réponses
- ✅ 5 questions de personnalité (méthode STAR)

---

## 📊 **Comparaison des Sources**

| Source | Fiabilité | Vitesse | Offres Tech | Installation |
|--------|-----------|---------|-------------|--------------|
| **LinkedIn** | ⭐⭐⭐⭐⭐ | ⚡⚡⚡ | Excellent | Aucune |
| **Indeed** | ⭐⭐ | ⚡⚡⚡ | Moyen | Aucune |
| **WTTJ (Playwright)** | ⭐⭐⭐⭐ | ⚡ | Excellent | Playwright requis |
| **Apec** | ⭐⭐ | ⚡⚡⚡ | Bon (cadres) | Aucune |
| **Batch URLs** | ⭐⭐⭐⭐⭐ | ⚡ | Parfait | Aucune |

---

## 🎓 **Cas d'Usage Avancés**

### **1. Recherche Multi-Localisations**
```bash
# Paris
./recherche_avancee.sh -p "Data Scientist" -l "Paris" -n 5

# Lyon
./recherche_avancee.sh -p "Data Scientist" -l "Lyon" -n 5

# Remote
./recherche_avancee.sh -p "Data Scientist" -l "Remote" -n 5
```

### **2. Recherche par Niveau de Carrière**
```bash
# Junior
./recherche_avancee.sh -p "Data Scientist" -s "junior" -n 10

# Senior
./recherche_avancee.sh -p "Data Scientist" -s "senior" -n 10

# Lead
./recherche_avancee.sh -p "Data Scientist" -s "lead" -n 10
```

### **3. Recherche par Type d'Entreprise**
```bash
# Startups
./recherche_avancee.sh -p "ML Engineer" -t "startup" -l "Paris" -n 10

# Grandes entreprises
./recherche_avancee.sh -p "ML Engineer" -t "grande-entreprise" -l "Paris" -n 10
```

### **4. Recherche Hybride (Manuelle + Auto)**
```bash
# 1. Recherchez manuellement sur LinkedIn, WTTJ, etc.
# 2. Copiez les URLs dans urls_a_traiter.txt
# 3. Lancez la génération batch
./batch_urls.sh
```

---

## ⚙️ **Installation Playwright (Optionnel)**

Si vous voulez scraper WTTJ automatiquement :

```bash
# Installation (une seule fois)
./installer_playwright.sh

# Ensuite utilisez --playwright dans vos recherches
./recherche_avancee.sh -p "Data Scientist" --playwright
```

**Note** : Playwright prend ~15-20 secondes par recherche WTTJ (vs 2s pour LinkedIn)

---

## 🐛 **Dépannage**

### **Problème : Aucune offre trouvée**
**Solutions** :
1. Simplifiez la requête (moins de critères)
2. Essayez une localisation plus large ("France" au lieu de ville spécifique)
3. Utilisez le mode batch avec URLs directes

### **Problème : Indeed bloqué (403)**
**Solution** : C'est normal, Indeed bloque le scraping. Utilisez LinkedIn ou batch URLs.

### **Problème : WTTJ ne trouve rien**
**Solutions** :
1. Installez Playwright : `./installer_playwright.sh`
2. Utilisez `--playwright` dans votre commande
3. Ou recherchez manuellement et utilisez batch URLs

### **Problème : Trop de résultats non pertinents**
**Solution** : Ajoutez plus de critères spécifiques

---

## 📈 **Statistiques Typiques**

### **Recherche "Data Scientist" à Paris (10 offres par plateforme)**
- LinkedIn : ~8-10 offres ✅
- Indeed : 0-3 offres (souvent bloqué) ⚠️
- WTTJ sans Playwright : 0 offres ⚠️
- WTTJ avec Playwright : ~5-10 offres ✅
- **Total : 8-23 offres selon configuration**

### **Temps d'Exécution**
- Recherche seule : ~10-15 secondes
- Recherche + Analyse IA : ~20-30 secondes
- Génération batch (5 offres) : ~10-15 minutes

### **Coûts API Claude**
- Analyse de 30 offres : ~0.05€
- Génération complète (1 offre) : ~0.20€
- Batch 5 offres : ~1.00€

---

## 🎯 **Recommandation Finale**

**Pour un usage quotidien optimal** :

1. **Recherche rapide** : LinkedIn uniquement
   ```bash
   ./recherche_avancee.sh -p "Data Scientist" -l "Paris"
   ```

2. **Recherche complète** : LinkedIn + WTTJ (Playwright)
   ```bash
   ./recherche_avancee.sh -p "Data Scientist" -l "Paris" --playwright
   ```

3. **Recherche ciblée** : Batch URLs (le plus fiable)
   ```bash
   # Recherchez manuellement, copiez les URLs, puis :
   ./batch_urls.sh
   ```

**Choisissez selon vos besoins !** 🚀
