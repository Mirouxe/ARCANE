# 📖 Guide d'utilisation Interactive

Tous les modes d'ARCANE sont maintenant **100% interactifs** ! Plus besoin de mémoriser les arguments en ligne de commande, le système vous guide étape par étape.

---

## 🎯 Vue d'ensemble des 6 modes

### Mode 1 & 2 : Génération Simple
**Un seul poste, génération rapide**

- 🌟 **Mode Spécifique** : `modes/generation_simple_specifique/`
- 🌍 **Mode Générique** : `modes/generation_simple_generique/`

**Ce qui vous sera demandé :**
- URL de l'annonce d'emploi

**Exemple d'utilisation :**
```bash
cd modes/generation_simple_specifique/
./lancer.sh
# Le script vous demandera : URL de l'annonce
```

---

### Mode 3 & 4 : Génération par Batch d'URLs
**Plusieurs postes, génération groupée**

- 🌟 **Mode Spécifique** : `modes/generation_urls_specifique/`
- 🌍 **Mode Générique** : `modes/generation_urls_generique/`

**Ce qui vous sera demandé :**
1. Comment fournir les URLs ?
   - Utiliser `urls.txt` (si existant)
   - Entrer manuellement les URLs
   - Utiliser un fichier personnalisé
2. Confirmation des URLs à traiter

**Exemple d'utilisation :**
```bash
cd modes/generation_urls_specifique/
./lancer.sh
# Le script vous guide pour la saisie des URLs
```

---

### Mode 5 & 6 : Recherche Complète
**Recherche automatique + génération batch**

- 🌟 **Mode Spécifique** : `modes/recherche_complete_specifique/`
- 🌍 **Mode Générique** : `modes/recherche_complete_generique/`

**Ce qui vous sera demandé :**

1. **🎯 Poste recherché**
   - Exemple : "Data Scientist", "Community Manager", "Ingénieur IA"

2. **📍 Localisation**
   - Exemple : "Paris", "Remote", "France"
   - Défaut : France

3. **💼 Niveau de séniorité**
   - Options : Junior / Confirmé / Senior / Lead / Tous niveaux
   - Défaut : Tous niveaux

4. **🔬 Domaines d'expertise** (optionnel)
   - Exemple : "Machine Learning,Deep Learning,NLP"
   - Séparés par des virgules

5. **🏢 Type d'entreprise**
   - Options : Startup / PME-ETI / Grande entreprise / Tous types
   - Défaut : Tous types

6. **📊 Nombre de postes par plateforme**
   - Exemple : 10, 20, 50
   - Défaut : 10

7. **🚀 Activer Playwright pour WTTJ ?**
   - Plus d'offres mais plus lent
   - Défaut : non

8. **🎯 Mode de sélection**
   - Interactif : vous sélectionnez après la recherche
   - Top 5 : génère automatiquement les 5 meilleurs postes
   - Toutes : génère pour toutes les offres trouvées
   - Liste personnalisée : ex. 1,3,5,7

**Exemple d'utilisation :**
```bash
cd modes/recherche_complete_specifique/
./lancer.sh
# Le script vous pose 8 questions, puis lance automatiquement
```

---

## 🔄 Workflow Typique

### Scénario 1 : Je postule à un poste que j'ai trouvé
```bash
cd modes/generation_simple_specifique/
./lancer.sh
# Entrer l'URL → Génération automatique
```

### Scénario 2 : J'ai une liste de 5 postes intéressants
```bash
cd modes/generation_urls_specifique/
./lancer.sh
# Choisir "Entrer manuellement"
# Coller les 5 URLs
# Confirmer → Génération batch
```

### Scénario 3 : Je cherche un nouveau job
```bash
cd modes/recherche_complete_specifique/
./lancer.sh
# Répondre aux 8 questions
# Le système trouve et génère automatiquement
```

### Scénario 4 : J'aide un ami (profil générique)
```bash
cd modes/generation_simple_generique/
# Modifier infos_statique.txt avec ses informations
./lancer.sh
# Entrer l'URL → Génération pour lui
```

---

## 🎨 Avantages du Mode Interactif

### ✅ Facile à utiliser
- Pas besoin de mémoriser les options
- Guidage étape par étape
- Valeurs par défaut intelligentes

### ✅ Sûr et contrôlé
- Récapitulatif avant lancement
- Confirmation pour les actions importantes
- Affichage clair des paramètres

### ✅ Flexible
- Accepte toujours les arguments en ligne de commande (modes 1-2)
- Mode interactif si aucun argument fourni
- Compatible avec l'automatisation

---

## 💡 Astuces Pro

### Astuce 1 : Utiliser les valeurs par défaut
Si une valeur par défaut vous convient, appuyez simplement sur `Entrée` :
```
📍 Localisation [défaut: France] : [Entrée]
→ Utilisera "France"
```

### Astuce 2 : Recherche large puis affinage
Pour découvrir le marché :
- Séniorité : **Tous niveaux**
- Type entreprise : **Tous types**
- Nombre : **20 ou 50**
- Sélection : **Interactif** (pour trier après)

### Astuce 3 : Recherche ciblée
Pour candidater rapidement :
- Critères précis (séniorité, domaines, type)
- Nombre : **10**
- Sélection : **Top 5** (génération auto des meilleurs)

### Astuce 4 : Batch depuis recherche
Après une recherche :
- Le système sauvegarde `recherche_postes_YYYYMMDD_HHMM.json`
- Vous pouvez relancer plus tard avec les URLs sauvegardées

---

## 🆘 Aide & Support

### Q : Je me suis trompé dans un paramètre
**R :** Pas de récapitulatif de confirmation ? Annulez avec `Ctrl+C` et relancez.

### Q : Le script se bloque
**R :** Vérifiez que vous avez bien activé l'environnement virtuel :
```bash
source ../../venv/bin/activate
```

### Q : Je veux automatiser quand même
**R :** Les modes de recherche acceptent toujours `<<EOF` avec des valeurs prédéfinies, voir les scripts pour exemples.

### Q : Erreur "fichier non trouvé"
**R :** Assurez-vous d'être dans le bon répertoire :
```bash
pwd  # Doit afficher : .../myCV/modes/[mode_name]/
```

---

## 📚 Ressources

- **README principal** : `../../README.md`
- **Guide des modes** : `GUIDE_MODES.md`
- **Architecture** : `../../ARCHITECTURE.md`
- **Démarrage rapide** : `../../DEMARRAGE_RAPIDE.md`

---

**🎯 Prêt à commencer ? Choisissez un mode et lancez `./lancer.sh` !**
