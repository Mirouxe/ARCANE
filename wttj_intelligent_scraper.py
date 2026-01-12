#!/usr/bin/env python3
"""
Scraper intelligent pour Welcome to the Jungle
Stratégies détournées pour obtenir les offres WTTJ
"""

import requests
import json
import time
from bs4 import BeautifulSoup
from urllib.parse import quote, urljoin


class WTTJIntelligentScraper:
    """Scraper avec stratégies détournées pour WTTJ"""
    
    def __init__(self):
        self.base_url = "https://www.welcometothejungle.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9',
        })
    
    def strategie_1_google_jobs(self, keywords: str, nb_results: int = 10) -> list:
        """
        STRATÉGIE 1: Google Jobs Search
        Google indexe les offres WTTJ et les rend accessibles via recherche
        """
        print(f"🔍 Stratégie 1: Google Jobs Search...")
        
        try:
            # Google Search avec filtre "site:welcometothejungle.com"
            google_query = f"site:welcometothejungle.com/fr/companies jobs {keywords}"
            google_url = f"https://www.google.com/search?q={quote(google_query)}&num={nb_results}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Accept': 'text/html',
                'Accept-Language': 'fr-FR,fr;q=0.9',
            }
            
            response = requests.get(google_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                jobs = []
                
                # Extraire les résultats de recherche Google
                search_results = soup.find_all('div', class_='g')
                
                for result in search_results[:nb_results]:
                    link_elem = result.find('a', href=True)
                    if link_elem:
                        url = link_elem.get('href', '')
                        
                        # Vérifier que c'est bien un lien WTTJ jobs
                        if '/companies/' in url and '/jobs/' in url:
                            title_elem = result.find('h3')
                            title = title_elem.text if title_elem else "Voir l'offre"
                            
                            jobs.append({
                                'url': url,
                                'titre': title,
                                'entreprise': self._extract_company_from_url(url),
                                'localisation': 'France',
                                'plateforme': 'WTTJ (via Google)',
                                'source': 'Google Jobs'
                            })
                
                if jobs:
                    print(f"   ✓ Trouvé {len(jobs)} offres via Google")
                    return jobs
            
        except Exception as e:
            print(f"   ⚠️  Erreur Google Jobs: {e}")
        
        return self.strategie_2_json_ld(keywords, nb_results)
    
    def strategie_2_json_ld(self, keywords: str, nb_results: int = 10) -> list:
        """
        STRATÉGIE 2: JSON-LD structuré
        Les sites modernes incluent des données structurées pour le SEO
        """
        print(f"🔍 Stratégie 2: Données structurées JSON-LD...")
        
        try:
            keywords_encoded = quote(keywords)
            url = f"{self.base_url}/fr/jobs?query={keywords_encoded}"
            
            response = self.session.get(url, timeout=30)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                jobs = []
                
                # Chercher les scripts JSON-LD (Schema.org)
                json_ld_scripts = soup.find_all('script', type='application/ld+json')
                
                for script in json_ld_scripts:
                    try:
                        data = json.loads(script.string)
                        
                        # Chercher les JobPosting
                        self._extract_job_postings(data, jobs, nb_results)
                        
                        if len(jobs) >= nb_results:
                            break
                    except:
                        continue
                
                if jobs:
                    print(f"   ✓ Trouvé {len(jobs)} offres via JSON-LD")
                    return jobs
        
        except Exception as e:
            print(f"   ⚠️  Erreur JSON-LD: {e}")
        
        return self.strategie_3_api_interne(keywords, nb_results)
    
    def strategie_3_api_interne(self, keywords: str, nb_results: int = 10) -> list:
        """
        STRATÉGIE 3: Appel direct à l'API interne
        Trouver les endpoints API utilisés par le frontend
        """
        print(f"🔍 Stratégie 3: API interne WTTJ...")
        
        # Liste d'endpoints API potentiels à tester
        api_endpoints = [
            f"/api/v1/jobs?query={quote(keywords)}&page=1&per_page={nb_results}",
            f"/fr/api/jobs?query={quote(keywords)}",
            f"/api/search/jobs?q={quote(keywords)}&limit={nb_results}",
            f"/graphql",  # Pour GraphQL
        ]
        
        for endpoint in api_endpoints:
            try:
                url = urljoin(self.base_url, endpoint)
                
                # Headers pour API
                api_headers = {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                }
                
                if endpoint == "/graphql":
                    # Requête GraphQL
                    payload = {
                        'query': '''
                        query SearchJobs($query: String!, $limit: Int!) {
                          jobs(query: $query, limit: $limit) {
                            edges {
                              node {
                                id
                                name
                                slug
                                office { name }
                                company { name slug }
                              }
                            }
                          }
                        }
                        ''',
                        'variables': {
                            'query': keywords,
                            'limit': nb_results
                        }
                    }
                    response = self.session.post(url, json=payload, headers=api_headers, timeout=30)
                else:
                    response = self.session.get(url, headers=api_headers, timeout=30)
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        jobs = self._parse_api_response(data, nb_results)
                        
                        if jobs:
                            print(f"   ✓ Trouvé {len(jobs)} offres via API {endpoint}")
                            return jobs
                    except:
                        continue
            
            except Exception as e:
                continue
        
        return self.strategie_4_rss_feed(keywords, nb_results)
    
    def strategie_4_rss_feed(self, keywords: str, nb_results: int = 10) -> list:
        """
        STRATÉGIE 4: Flux RSS si disponible
        """
        print(f"🔍 Stratégie 4: Flux RSS...")
        
        rss_urls = [
            f"{self.base_url}/fr/jobs.rss?query={quote(keywords)}",
            f"{self.base_url}/rss/jobs?query={quote(keywords)}",
            f"{self.base_url}/feed/jobs?search={quote(keywords)}",
        ]
        
        for rss_url in rss_urls:
            try:
                response = self.session.get(rss_url, timeout=30)
                
                if response.status_code == 200 and ('xml' in response.headers.get('content-type', '').lower() 
                                                     or '<?xml' in response.text[:100]):
                    soup = BeautifulSoup(response.content, 'xml')
                    items = soup.find_all('item')[:nb_results]
                    
                    if items:
                        jobs = []
                        for item in items:
                            title = item.find('title')
                            link = item.find('link')
                            description = item.find('description')
                            
                            if title and link:
                                jobs.append({
                                    'url': link.text.strip(),
                                    'titre': title.text.strip(),
                                    'entreprise': self._extract_company_from_description(
                                        description.text if description else ''
                                    ),
                                    'localisation': 'France',
                                    'plateforme': 'WTTJ (via RSS)',
                                    'source': 'RSS Feed'
                                })
                        
                        if jobs:
                            print(f"   ✓ Trouvé {len(jobs)} offres via RSS")
                            return jobs
            
            except Exception as e:
                continue
        
        return self.strategie_5_sitemap(keywords, nb_results)
    
    def strategie_5_sitemap(self, keywords: str, nb_results: int = 10) -> list:
        """
        STRATÉGIE 5: Sitemap XML
        Parser le sitemap pour trouver les URLs de jobs
        """
        print(f"🔍 Stratégie 5: Sitemap XML...")
        
        sitemap_urls = [
            f"{self.base_url}/sitemap.xml",
            f"{self.base_url}/sitemap_jobs.xml",
            f"{self.base_url}/fr/sitemap.xml",
        ]
        
        for sitemap_url in sitemap_urls:
            try:
                response = self.session.get(sitemap_url, timeout=30)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'xml')
                    
                    # Trouver toutes les URLs
                    urls = soup.find_all('loc')
                    
                    jobs = []
                    keywords_lower = keywords.lower().split()
                    
                    for url_elem in urls:
                        url = url_elem.text.strip()
                        
                        # Filtrer les URLs de jobs
                        if '/companies/' in url and '/jobs/' in url:
                            # Filtrer par mots-clés dans l'URL
                            url_lower = url.lower()
                            if any(kw in url_lower for kw in keywords_lower):
                                jobs.append({
                                    'url': url,
                                    'titre': self._extract_title_from_url(url),
                                    'entreprise': self._extract_company_from_url(url),
                                    'localisation': 'France',
                                    'plateforme': 'WTTJ (via Sitemap)',
                                    'source': 'Sitemap'
                                })
                                
                                if len(jobs) >= nb_results:
                                    break
                    
                    if jobs:
                        print(f"   ✓ Trouvé {len(jobs)} offres via Sitemap")
                        return jobs
            
            except Exception as e:
                continue
        
        return self.strategie_6_alternatives_aggregators(keywords, nb_results)
    
    def strategie_6_alternatives_aggregators(self, keywords: str, nb_results: int = 10) -> list:
        """
        STRATÉGIE 6: Agrégateurs alternatifs
        Utiliser des agrégateurs qui indexent WTTJ
        """
        print(f"🔍 Stratégie 6: Agrégateurs alternatifs...")
        
        jobs = []
        
        # Jooble agrège plusieurs sites dont WTTJ
        try:
            jooble_url = f"https://fr.jooble.org/SearchResult?ukw={quote(keywords)}"
            response = self.session.get(jooble_url, timeout=30)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                job_cards = soup.find_all('article', class_='job-item')
                
                for card in job_cards[:nb_results]:
                    link = card.find('a', class_='job-item-title')
                    if link:
                        onclick = link.get('onclick', '')
                        if 'welcometothejungle.com' in onclick or 'welcometothejungle.com' in link.get('href', ''):
                            jobs.append({
                                'url': link.get('href', ''),
                                'titre': link.text.strip(),
                                'entreprise': 'Voir sur WTTJ',
                                'localisation': 'France',
                                'plateforme': 'WTTJ (via Jooble)',
                                'source': 'Jooble'
                            })
        except:
            pass
        
        if jobs:
            print(f"   ✓ Trouvé {len(jobs)} offres via agrégateurs")
            return jobs
        
        print(f"   ⚠️  Aucune stratégie n'a réussi à récupérer des offres WTTJ")
        return []
    
    # Méthodes utilitaires
    
    def _extract_job_postings(self, data, jobs: list, limit: int):
        """Extrait les JobPosting du JSON-LD"""
        if isinstance(data, dict):
            if data.get('@type') == 'JobPosting':
                jobs.append({
                    'url': data.get('url', ''),
                    'titre': data.get('title', 'N/A'),
                    'entreprise': data.get('hiringOrganization', {}).get('name', 'N/A'),
                    'localisation': data.get('jobLocation', {}).get('address', {}).get('addressLocality', 'France'),
                    'plateforme': 'WTTJ (JSON-LD)',
                    'source': 'Structured Data'
                })
            
            for value in data.values():
                if len(jobs) >= limit:
                    return
                self._extract_job_postings(value, jobs, limit)
        
        elif isinstance(data, list):
            for item in data:
                if len(jobs) >= limit:
                    return
                self._extract_job_postings(item, jobs, limit)
    
    def _parse_api_response(self, data: dict, limit: int) -> list:
        """Parse la réponse API"""
        jobs = []
        
        # Patterns communs dans les APIs
        if 'jobs' in data:
            items = data['jobs']
        elif 'data' in data and 'jobs' in data['data']:
            items = data['data']['jobs'].get('edges', [])
        elif 'results' in data:
            items = data['results']
        else:
            return []
        
        for item in items[:limit]:
            if isinstance(item, dict):
                # GraphQL format
                if 'node' in item:
                    node = item['node']
                    company_slug = node.get('company', {}).get('slug', '')
                    job_slug = node.get('slug', '')
                    
                    if company_slug and job_slug:
                        jobs.append({
                            'url': f"{self.base_url}/fr/companies/{company_slug}/jobs/{job_slug}",
                            'titre': node.get('name', 'N/A'),
                            'entreprise': node.get('company', {}).get('name', 'N/A'),
                            'localisation': node.get('office', {}).get('name', 'France'),
                            'plateforme': 'WTTJ (API)',
                            'source': 'API'
                        })
                # REST format
                else:
                    jobs.append({
                        'url': item.get('url', ''),
                        'titre': item.get('name') or item.get('title', 'N/A'),
                        'entreprise': item.get('company', {}).get('name', 'N/A'),
                        'localisation': item.get('location', 'France'),
                        'plateforme': 'WTTJ (API)',
                        'source': 'API'
                    })
        
        return jobs
    
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
    
    def _extract_company_from_description(self, description: str) -> str:
        """Extrait l'entreprise de la description"""
        if 'chez' in description.lower():
            parts = description.lower().split('chez')
            if len(parts) > 1:
                return parts[1].split('-')[0].split('.')[0].strip().title()
        return "Voir sur WTTJ"
    
    def rechercher(self, keywords: str, nb_results: int = 10) -> list:
        """Lance toutes les stratégies en cascade"""
        print(f"\n{'='*80}")
        print(f"RECHERCHE INTELLIGENTE WTTJ: {keywords}")
        print(f"{'='*80}\n")
        
        # Essayer toutes les stratégies dans l'ordre
        jobs = self.strategie_1_google_jobs(keywords, nb_results)
        
        return jobs


def tester():
    """Test du scraper"""
    scraper = WTTJIntelligentScraper()
    jobs = scraper.rechercher("data scientist", 5)
    
    print(f"\n{'='*80}")
    print(f"RÉSULTATS")
    print(f"{'='*80}\n")
    
    if jobs:
        print(f"✅ {len(jobs)} offres trouvées\n")
        for i, job in enumerate(jobs, 1):
            print(f"{i}. {job['titre']}")
            print(f"   🏢 {job['entreprise']}")
            print(f"   📍 {job['localisation']}")
            print(f"   🔗 {job['url']}")
            print(f"   📊 Source: {job.get('source', 'N/A')}")
            print()
    else:
        print("❌ Aucune offre trouvée")


if __name__ == "__main__":
    tester()
