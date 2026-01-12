#!/usr/bin/env python3
"""
Scrapers avancés pour Welcome to the Jungle et Apec
Utilise différentes stratégies pour contourner les limitations JavaScript
"""

import requests
import json
import time
from bs4 import BeautifulSoup


class WTTJScraper:
    """Scraper avancé pour Welcome to the Jungle"""
    
    def __init__(self):
        self.base_url = "https://www.welcometothejungle.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'fr-FR,fr;q=0.9',
            'Origin': 'https://www.welcometothejungle.com',
            'Referer': 'https://www.welcometothejungle.com/fr/jobs',
        })
    
    def rechercher_via_api(self, keywords: str, nb_results: int = 10) -> list:
        """
        Stratégie 1: Utiliser l'API interne de WTTJ
        En inspectant le réseau, on voit que WTTJ fait des requêtes à une API REST
        """
        print(f"🔍 WTTJ - Stratégie API REST...")
        
        try:
            # L'URL de l'API interne (trouvée via inspection réseau)
            api_url = f"{self.base_url}/api/v1/jobs"
            
            params = {
                'query': keywords,
                'page': 1,
                'per_page': nb_results,
                'refinement_list[offices.country_code][]': 'FR',
            }
            
            response = self.session.get(api_url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                jobs = []
                
                for job_data in data.get('jobs', [])[:nb_results]:
                    company_slug = job_data.get('company', {}).get('slug', '')
                    job_slug = job_data.get('slug', '')
                    
                    if company_slug and job_slug:
                        jobs.append({
                            'url': f"{self.base_url}/fr/companies/{company_slug}/jobs/{job_slug}",
                            'titre': job_data.get('name', 'N/A'),
                            'entreprise': job_data.get('company', {}).get('name', 'N/A'),
                            'localisation': job_data.get('office', {}).get('name', 'France'),
                            'plateforme': 'Welcome to the Jungle'
                        })
                
                return jobs
            
        except Exception as e:
            print(f"   ⚠️  Stratégie API REST échouée: {e}")
        
        return self.rechercher_via_scraping_ameliore(keywords, nb_results)
    
    def rechercher_via_scraping_ameliore(self, keywords: str, nb_results: int = 10) -> list:
        """
        Stratégie 2: Scraping amélioré avec cookies et headers complets
        """
        print(f"🔍 WTTJ - Stratégie scraping amélioré...")
        
        try:
            keywords_encoded = keywords.replace(" ", "%20")
            url = f"{self.base_url}/fr/jobs?query={keywords_encoded}"
            
            # Première requête pour obtenir les cookies
            response = self.session.get(self.base_url, timeout=30)
            time.sleep(1)
            
            # Deuxième requête avec les cookies
            response = self.session.get(url, timeout=30)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                jobs = []
                
                # Chercher les données embarquées dans le HTML (Next.js/React)
                scripts = soup.find_all('script', type='application/json')
                
                for script in scripts:
                    try:
                        data = json.loads(script.string)
                        # Les données peuvent être dans différentes structures
                        self._extract_jobs_from_json(data, jobs, nb_results)
                        
                        if len(jobs) >= nb_results:
                            break
                    except:
                        continue
                
                # Si on a trouvé des jobs dans le JSON embarqué
                if jobs:
                    return jobs[:nb_results]
                
                # Sinon, scraping classique des liens
                return self._scraping_classique(soup, nb_results)
            
        except Exception as e:
            print(f"   ⚠️  Stratégie scraping amélioré échouée: {e}")
        
        return []
    
    def _extract_jobs_from_json(self, data: dict, jobs: list, limit: int):
        """Extrait récursivement les jobs du JSON"""
        if isinstance(data, dict):
            # Chercher les patterns de jobs
            if 'jobs' in data and isinstance(data['jobs'], list):
                for job in data['jobs']:
                    if len(jobs) >= limit:
                        return
                    
                    if isinstance(job, dict):
                        company_slug = job.get('company', {}).get('slug') or job.get('companySlug')
                        job_slug = job.get('slug')
                        
                        if company_slug and job_slug:
                            jobs.append({
                                'url': f"{self.base_url}/fr/companies/{company_slug}/jobs/{job_slug}",
                                'titre': job.get('name', 'N/A'),
                                'entreprise': job.get('company', {}).get('name', 'N/A'),
                                'localisation': job.get('office', {}).get('name', 'France'),
                                'plateforme': 'Welcome to the Jungle'
                            })
            
            # Recherche récursive
            for value in data.values():
                if len(jobs) >= limit:
                    return
                self._extract_jobs_from_json(value, jobs, limit)
        
        elif isinstance(data, list):
            for item in data:
                if len(jobs) >= limit:
                    return
                self._extract_jobs_from_json(item, jobs, limit)
    
    def _scraping_classique(self, soup: BeautifulSoup, nb_results: int) -> list:
        """Fallback: scraping des liens uniquement"""
        jobs = []
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link.get('href', '')
            if '/companies/' in href and '/jobs/' in href:
                if href not in [j['url'] for j in jobs]:
                    full_url = href if href.startswith('http') else f"{self.base_url}{href}"
                    
                    title = link.get('aria-label', '') or link.text.strip()[:100]
                    if not title or title == '':
                        title = "Voir l'offre"
                    
                    jobs.append({
                        'url': full_url,
                        'titre': title,
                        'entreprise': "Voir sur WTTJ",
                        'localisation': "France",
                        'plateforme': 'Welcome to the Jungle'
                    })
                    
                    if len(jobs) >= nb_results:
                        break
        
        return jobs


class ApecScraper:
    """Scraper avancé pour l'Apec"""
    
    def __init__(self):
        self.base_url = "https://www.apec.fr"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/html, */*',
            'Accept-Language': 'fr-FR,fr;q=0.9',
            'Referer': 'https://www.apec.fr/',
        })
    
    def rechercher_via_api(self, keywords: str, nb_results: int = 10) -> list:
        """
        Stratégie 1: API Apec (recherche publique)
        L'Apec expose une API pour les recherches publiques
        """
        print(f"🔍 Apec - Stratégie API...")
        
        try:
            # API endpoint (trouvé via inspection réseau)
            api_url = f"{self.base_url}/candidat/recherche-emploi.html/emploi"
            
            # Première requête pour obtenir les cookies et token
            init_response = self.session.get(self.base_url, timeout=30)
            time.sleep(1)
            
            # Paramètres de recherche
            params = {
                'motsCles': keywords,
                'page': 0,
                'nbResultatsParPage': nb_results,
            }
            
            response = self.session.get(api_url, params=params, timeout=30)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                return self._parse_apec_results(soup, nb_results)
            
        except Exception as e:
            print(f"   ⚠️  Stratégie API Apec échouée: {e}")
        
        return self.rechercher_via_rss(keywords, nb_results)
    
    def rechercher_via_rss(self, keywords: str, nb_results: int = 10) -> list:
        """
        Stratégie 2: Flux RSS de l'Apec
        L'Apec propose des flux RSS pour certaines recherches
        """
        print(f"🔍 Apec - Stratégie RSS...")
        
        try:
            keywords_encoded = keywords.replace(" ", "+")
            rss_url = f"{self.base_url}/candidat/recherche-emploi.html/emploi/rss?motsCles={keywords_encoded}"
            
            response = self.session.get(rss_url, timeout=30)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'xml')
                items = soup.find_all('item')[:nb_results]
                
                jobs = []
                for item in items:
                    title = item.find('title')
                    link = item.find('link')
                    description = item.find('description')
                    
                    if title and link:
                        jobs.append({
                            'url': link.text.strip(),
                            'titre': title.text.strip(),
                            'entreprise': self._extract_company_from_description(description.text if description else ''),
                            'localisation': 'France',
                            'plateforme': 'Apec'
                        })
                
                if jobs:
                    return jobs
            
        except Exception as e:
            print(f"   ⚠️  Stratégie RSS échouée: {e}")
        
        return self.rechercher_alternative(keywords, nb_results)
    
    def rechercher_alternative(self, keywords: str, nb_results: int = 10) -> list:
        """
        Stratégie 3: Scraping direct avec simulation de navigation
        """
        print(f"🔍 Apec - Stratégie scraping direct...")
        
        try:
            keywords_encoded = keywords.replace(" ", "%20")
            search_url = f"{self.base_url}/candidat/recherche-emploi.html/emploi?motsCles={keywords_encoded}"
            
            # Simuler une navigation normale
            self.session.get(self.base_url, timeout=30)
            time.sleep(1)
            
            response = self.session.get(search_url, timeout=30)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Chercher les données JSON embarquées
                scripts = soup.find_all('script', type='application/json')
                
                for script in scripts:
                    try:
                        data = json.loads(script.string)
                        jobs = self._extract_jobs_from_json(data, nb_results)
                        if jobs:
                            return jobs
                    except:
                        continue
                
                # Scraping HTML classique
                return self._parse_apec_results(soup, nb_results)
            
        except Exception as e:
            print(f"   ⚠️  Scraping Apec échoué: {e}")
        
        return []
    
    def _parse_apec_results(self, soup: BeautifulSoup, nb_results: int) -> list:
        """Parse les résultats HTML de l'Apec"""
        jobs = []
        
        # Différentes structures possibles
        selectors = [
            ('article', 'box-offer'),
            ('div', 'offer-card'),
            ('li', 'result-item'),
            ('div', 'OffreCard'),
        ]
        
        for tag, class_name in selectors:
            job_cards = soup.find_all(tag, class_=class_name)
            
            if job_cards:
                for card in job_cards[:nb_results]:
                    try:
                        link = card.find('a', href=True)
                        if not link:
                            continue
                        
                        href = link.get('href', '')
                        job_url = href if href.startswith('http') else f"{self.base_url}{href}"
                        
                        title_elem = card.find('h2') or card.find('h3') or link
                        title = title_elem.text.strip() if title_elem else "Voir l'offre"
                        
                        company_elem = card.find('span', class_='company') or card.find('div', class_='company-name')
                        company = company_elem.text.strip() if company_elem else "N/A"
                        
                        location_elem = card.find('span', class_='location') or card.find('div', class_='location')
                        location = location_elem.text.strip() if location_elem else "France"
                        
                        jobs.append({
                            'url': job_url,
                            'titre': title,
                            'entreprise': company,
                            'localisation': location,
                            'plateforme': 'Apec'
                        })
                    except:
                        continue
                
                if jobs:
                    break
        
        return jobs[:nb_results]
    
    def _extract_jobs_from_json(self, data: dict, limit: int) -> list:
        """Extrait les jobs du JSON embarqué"""
        jobs = []
        
        def search_jobs(obj):
            if isinstance(obj, dict):
                if 'offres' in obj or 'offers' in obj:
                    offers = obj.get('offres') or obj.get('offers', [])
                    for offer in offers[:limit]:
                        if isinstance(offer, dict):
                            jobs.append({
                                'url': offer.get('lienApec') or offer.get('url', ''),
                                'titre': offer.get('intitule') or offer.get('title', 'N/A'),
                                'entreprise': offer.get('nomEntreprise') or offer.get('company', 'N/A'),
                                'localisation': offer.get('lieuTravail') or offer.get('location', 'France'),
                                'plateforme': 'Apec'
                            })
                
                for value in obj.values():
                    if len(jobs) >= limit:
                        return
                    search_jobs(value)
            
            elif isinstance(obj, list):
                for item in obj:
                    if len(jobs) >= limit:
                        return
                    search_jobs(item)
        
        search_jobs(data)
        return jobs
    
    def _extract_company_from_description(self, description: str) -> str:
        """Extrait le nom de l'entreprise de la description"""
        # Pattern basique pour extraire l'entreprise
        if 'chez' in description.lower():
            parts = description.lower().split('chez')
            if len(parts) > 1:
                company = parts[1].split('-')[0].split('.')[0].strip()
                return company.title()
        return "N/A"


# Fonction de test
def tester_scrapers():
    """Teste les différents scrapers"""
    print("="*80)
    print("TEST DES SCRAPERS AVANCÉS")
    print("="*80)
    print()
    
    # Test WTTJ
    print("1. Test Welcome to the Jungle")
    print("-"*80)
    wttj = WTTJScraper()
    jobs_wttj = wttj.rechercher_via_api("data scientist", 5)
    print(f"✓ WTTJ: {len(jobs_wttj)} offres trouvées")
    if jobs_wttj:
        for i, job in enumerate(jobs_wttj[:2], 1):
            print(f"  {i}. {job['titre']} - {job['entreprise']}")
    print()
    
    time.sleep(2)
    
    # Test Apec
    print("2. Test Apec")
    print("-"*80)
    apec = ApecScraper()
    jobs_apec = apec.rechercher_via_api("data scientist", 5)
    print(f"✓ Apec: {len(jobs_apec)} offres trouvées")
    if jobs_apec:
        for i, job in enumerate(jobs_apec[:2], 1):
            print(f"  {i}. {job['titre']} - {job['entreprise']}")
    print()


if __name__ == "__main__":
    tester_scrapers()
