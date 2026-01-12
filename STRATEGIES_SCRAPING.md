# Stratégies de Scraping pour WTTJ et Apec

## 🎯 Résumé du problème

**Welcome to the Jungle** et **Apec** utilisent :
- ✅ Chargement JavaScript dynamique (React/Next.js)
- ✅ Protections anti-bot sophistiquées
- ✅ APIs privées nécessitant des tokens
- ✅ Détection de comportement automatisé

## 📊 Solutions possibles

### ✅ **Solution 1: Selenium (RECOMMANDÉE)**

**Avantages:**
- Exécute le JavaScript
- Simule un vrai navigateur
- Contourne la plupart des protections

**Installation:**
```bash
pip install selenium webdriver-manager
```

**Code exemple:**
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def rechercher_wttj_selenium(keywords, nb_results=10):
    # Configuration Chrome headless
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    
    try:
        url = f"https://www.welcometothejungle.com/fr/jobs?query={keywords}"
        driver.get(url)
        time.sleep(5)  # Attendre le chargement
        
        jobs = []
        # Extraire les éléments après rendu JavaScript
        job_elements = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/jobs/"]')
        
        for elem in job_elements[:nb_results]:
            jobs.append({
                'url': elem.get_attribute('href'),
                'titre': elem.text
            })
        
        return jobs
    finally:
        driver.quit()
```

**Coût:** Temps d'exécution ~10-20s par recherche (vs 2s avec requests)

---

### ⚡ **Solution 2: Playwright (MODERNE)**

**Avantages:**
- Plus rapide que Selenium
- API moderne
- Multi-navigateurs (Chrome, Firefox, WebKit)

**Installation:**
```bash
pip install playwright
playwright install chromium
```

**Code exemple:**
```python
from playwright.sync_api import sync_playwright

def rechercher_wttj_playwright(keywords, nb_results=10):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        url = f"https://www.welcometothejungle.com/fr/jobs?query={keywords}"
        page.goto(url)
        page.wait_for_selector('a[href*="/jobs/"]', timeout=10000)
        
        jobs = []
        links = page.query_selector_all('a[href*="/jobs/"]')
        
        for link in links[:nb_results]:
            jobs.append({
                'url': link.get_attribute('href'),
                'titre': link.inner_text()
            })
        
        browser.close()
        return jobs
```

---

### 🔌 **Solution 3: Service tiers (API aggregator)**

Utiliser des services qui agrègent plusieurs job boards :

**Options:**
- **Adzuna API** (gratuit jusqu'à 200 req/mois)
- **The Muse API** 
- **GitHub Jobs API** (pour tech)
- **Reed API** (UK mais parfois FR)

**Exemple Adzuna:**
```python
import requests

def rechercher_adzuna(keywords, location="France"):
    app_id = "YOUR_APP_ID"
    app_key = "YOUR_APP_KEY"
    
    url = f"https://api.adzuna.com/v1/api/jobs/fr/search/1"
    params = {
        'app_id': app_id,
        'app_key': app_key,
        'what': keywords,
        'where': location,
        'results_per_page': 10
    }
    
    response = requests.get(url, params=params)
    return response.json()
```

---

### 🎯 **Solution 4: PRAGMATIQUE (Recommandée pour votre cas)**

**Approche hybride:**
1. ✅ **LinkedIn fonctionne** → Utilisez-le comme source principale
2. 🔗 **Collecte manuelle** → Recherchez sur WTTJ/Apec manuellement, copiez les URLs
3. 📝 **Batch processing** → Créez un fichier `urls_a_traiter.txt` avec les URLs

**Créer un script de batch depuis fichier:**

```bash
# urls_a_traiter.txt
https://www.welcometothejungle.com/fr/companies/xxx/jobs/yyy
https://www.apec.fr/candidat/offres-emploi.html?id=zzz
https://fr.linkedin.com/jobs/view/123456
```

```python
# batch_depuis_fichier.py
with open('urls_a_traiter.txt', 'r') as f:
    urls = [line.strip() for line in f if line.strip()]

for url in urls:
    subprocess.run(['python3', 'generateur_cv_lettre.py', url])
```

---

## 💡 Ma recommandation finale

### Pour un usage immédiat (AUJOURD'HUI):
```python
# Dans recherche_postes.py, gardez seulement LinkedIn
# Utilisez la recherche manuelle pour WTTJ/Apec
# Créez un workflow hybride
```

### Pour aller plus loin (PLUS TARD):
```bash
# Installez Playwright (plus simple que Selenium)
pip install playwright
playwright install chromium

# Ajoutez l'option --selenium au script
./rechercher_et_generer.sh "data scientist" --selenium
```

---

## 📈 Comparaison

| Solution | Complexité | Vitesse | Fiabilité | Coût |
|----------|------------|---------|-----------|------|
| **LinkedIn (actuel)** | ⭐ Simple | ⚡⚡⚡ Rapide | ✅ 90% | Gratuit |
| **Selenium** | ⭐⭐⭐ Complexe | ⚡ Lent | ✅✅ 80% | Gratuit |
| **Playwright** | ⭐⭐ Moyen | ⚡⚡ Moyen | ✅✅ 85% | Gratuit |
| **API Adzuna** | ⭐ Simple | ⚡⚡⚡ Rapide | ✅✅✅ 95% | Limité |
| **Manuel + Batch** | ⭐ Simple | ⚡ Lent | ✅✅✅ 100% | Gratuit |

---

## 🚀 Implémentation recommandée

**Phase 1 (Maintenant):** 
Gardez LinkedIn + workflow hybride manuel

**Phase 2 (Optionnel):**
Ajoutez Playwright si vraiment nécessaire

**Code à ajouter:**
```bash
# Dans requirements.txt
playwright==1.49.0

# Nouveau fichier: scraper_selenium.py
# (voir ci-dessus)
```
