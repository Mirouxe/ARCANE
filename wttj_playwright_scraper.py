#!/usr/bin/env python3
"""
Scraper WTTJ avec Playwright - LA solution qui fonctionne
Installation: pip install playwright && playwright install chromium
"""

import sys

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("❌ Playwright n'est pas installé")
    print("\n💡 Installation:")
    print("   pip install playwright")
    print("   playwright install chromium")
    print()
    sys.exit(1)

import time
import json


class WTTJPlaywrightScraper:
    """Scraper WTTJ utilisant Playwright"""
    
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.base_url = "https://www.welcometothejungle.com"
    
    def rechercher(self, keywords: str, nb_results: int = 10) -> list:
        """Recherche des offres WTTJ avec Playwright"""
        print(f"🚀 Lancement de Playwright (headless={self.headless})...")
        
        jobs = []
        
        with sync_playwright() as p:
            # Lancer le navigateur
            browser = p.chromium.launch(headless=self.headless)
            
            try:
                # Créer une page
                page = browser.new_page()
                
                # Aller sur la page de recherche
                search_url = f"{self.base_url}/fr/jobs?query={keywords.replace(' ', '%20')}"
                print(f"🔍 Navigation vers: {search_url}")
                
                page.goto(search_url, wait_until='networkidle', timeout=30000)
                
                # Attendre que les résultats se chargent
                print(f"⏳ Attente du chargement des offres...")
                time.sleep(3)  # Laisser le temps au JavaScript de s'exécuter
                
                # Essayer différents sélecteurs possibles
                selectors_to_try = [
                    'a[href*="/companies/"][href*="/jobs/"]',
                    '[data-testid="job-card"]',
                    'article a[href*="/jobs/"]',
                    'div[class*="job"] a',
                ]
                
                job_elements = []
                for selector in selectors_to_try:
                    try:
                        job_elements = page.query_selector_all(selector)
                        if job_elements:
                            print(f"✓ Trouvé {len(job_elements)} éléments avec sélecteur: {selector}")
                            break
                    except:
                        continue
                
                if not job_elements:
                    print("⚠️  Aucun élément trouvé, tentative d'extraction du HTML complet...")
                    # Fallback: extraire tous les liens
                    job_elements = page.query_selector_all('a')
                
                # Extraire les informations
                seen_urls = set()
                
                for element in job_elements:
                    if len(jobs) >= nb_results:
                        break
                    
                    try:
                        href = element.get_attribute('href')
                        
                        if not href:
                            continue
                        
                        # Filtrer les URLs de jobs
                        if '/companies/' in href and '/jobs/' in href:
                            # Construire l'URL complète
                            if href.startswith('http'):
                                url = href
                            else:
                                url = f"{self.base_url}{href}"
                            
                            # Éviter les doublons
                            if url in seen_urls:
                                continue
                            seen_urls.add(url)
                            
                            # Extraire le titre
                            try:
                                # Essayer de trouver le titre dans le parent
                                parent = element.evaluate('el => el.closest("article") || el.closest("div")')
                                title = element.inner_text().strip()
                                
                                if not title or len(title) > 150:
                                    title = self._extract_title_from_url(url)
                            except:
                                title = self._extract_title_from_url(url)
                            
                            # Extraire l'entreprise
                            company = self._extract_company_from_url(url)
                            
                            jobs.append({
                                'url': url,
                                'titre': title,
                                'entreprise': company,
                                'localisation': 'France',
                                'plateforme': 'WTTJ (Playwright)',
                                'source': 'Browser Automation'
                            })
                    
                    except Exception as e:
                        continue
                
                # Si on n'a toujours rien, essayer d'extraire du JSON dans le HTML
                if not jobs:
                    print("⚠️  Extraction directe échouée, recherche de données JSON...")
                    jobs = self._extract_from_page_json(page, nb_results)
                
            finally:
                browser.close()
        
        return jobs
    
    def _extract_from_page_json(self, page, nb_results: int) -> list:
        """Extrait les jobs des données JSON embarquées dans la page"""
        jobs = []
        
        try:
            # Récupérer tout le HTML
            html_content = page.content()
            
            # Chercher les scripts JSON
            import re
            from bs4 import BeautifulSoup
            
            soup = BeautifulSoup(html_content, 'html.parser')
            scripts = soup.find_all('script', type='application/json')
            
            for script in scripts:
                try:
                    data = json.loads(script.string)
                    self._extract_jobs_recursive(data, jobs, nb_results)
                    
                    if len(jobs) >= nb_results:
                        break
                except:
                    continue
            
        except Exception as e:
            print(f"   ⚠️  Erreur extraction JSON: {e}")
        
        return jobs
    
    def _extract_jobs_recursive(self, data, jobs: list, limit: int):
        """Extraction récursive des jobs du JSON"""
        if len(jobs) >= limit:
            return
        
        if isinstance(data, dict):
            # Patterns de jobs
            if 'slug' in data and 'company' in data and isinstance(data.get('company'), dict):
                company_slug = data['company'].get('slug', '')
                job_slug = data.get('slug', '')
                
                if company_slug and job_slug:
                    url = f"{self.base_url}/fr/companies/{company_slug}/jobs/{job_slug}"
                    
                    jobs.append({
                        'url': url,
                        'titre': data.get('name', 'N/A'),
                        'entreprise': data['company'].get('name', 'N/A'),
                        'localisation': data.get('office', {}).get('name', 'France'),
                        'plateforme': 'WTTJ (JSON)',
                        'source': 'Page Data'
                    })
                    return
            
            # Recherche récursive
            for value in data.values():
                if len(jobs) >= limit:
                    return
                self._extract_jobs_recursive(value, jobs, limit)
        
        elif isinstance(data, list):
            for item in data:
                if len(jobs) >= limit:
                    return
                self._extract_jobs_recursive(item, jobs, limit)
    
    def _extract_company_from_url(self, url: str) -> str:
        """Extrait le nom de l'entreprise de l'URL"""
        if '/companies/' in url:
            parts = url.split('/companies/')
            if len(parts) > 1:
                company_slug = parts[1].split('/')[0]
                return company_slug.replace('-', ' ').title()
        return "Voir sur WTTJ"
    
    def _extract_title_from_url(self, url: str) -> str:
        """Extrait le titre du job de l'URL"""
        if '/jobs/' in url:
            parts = url.split('/jobs/')
            if len(parts) > 1:
                job_slug = parts[1].split('?')[0].rstrip('/')
                return job_slug.replace('-', ' ').title()
        return "Voir l'offre"


def tester():
    """Test du scraper Playwright"""
    print("="*80)
    print("SCRAPER WTTJ AVEC PLAYWRIGHT")
    print("="*80)
    print()
    
    scraper = WTTJPlaywrightScraper(headless=True)
    jobs = scraper.rechercher("data scientist", 5)
    
    print()
    print("="*80)
    print("RÉSULTATS")
    print("="*80)
    print()
    
    if jobs:
        print(f"✅ {len(jobs)} offres trouvées\n")
        for i, job in enumerate(jobs, 1):
            print(f"{i}. {job['titre']}")
            print(f"   🏢 {job['entreprise']}")
            print(f"   📍 {job['localisation']}")
            print(f"   🔗 {job['url'][:80]}...")
            print()
    else:
        print("❌ Aucune offre trouvée")
        print("\n💡 Conseils:")
        print("   - Vérifiez que Playwright est bien installé")
        print("   - Essayez en mode non-headless: WTTJPlaywrightScraper(headless=False)")
        print("   - Vérifiez votre connexion internet")


if __name__ == "__main__":
    tester()
