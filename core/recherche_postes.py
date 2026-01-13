#!/usr/bin/env python3
"""
Script de recherche automatique de postes et génération en batch
"""

import os
import sys
import re
import json
import time
import subprocess
from datetime import datetime
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from anthropic import Anthropic

# Charger les variables d'environnement
load_dotenv()

# Importer la configuration
from config import *

# User Agent pour les requêtes
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


class RechercheurPostes:
    """Recherche des postes sur différentes plateformes"""
    
    def __init__(self, profil_infos: dict, use_playwright: bool = False):
        self.profil = profil_infos
        self.api_key = os.environ.get('ANTHROPIC_API_KEY')
        if self.api_key:
            self.client = Anthropic(api_key=self.api_key)
        
        # Vérifier si Playwright est disponible
        self.playwright_available = False
        self.use_playwright = use_playwright
        
        if use_playwright:
            try:
                from playwright.sync_api import sync_playwright
                self.playwright_available = True
                print("✅ Playwright activé pour WTTJ")
            except ImportError:
                print("⚠️  Playwright non installé. Lancez: ./installer_playwright.sh")
                self.playwright_available = False
    
    def _rechercher_wttj_playwright(self, keywords: str, nb_results: int = 10) -> list:
        """Recherche WTTJ avec Playwright (exécute le JavaScript)"""
        print(f"   🚀 Utilisation de Playwright...")
        
        try:
            from wttj_playwright_scraper import WTTJPlaywrightScraper
            scraper = WTTJPlaywrightScraper(headless=True)
            jobs = scraper.rechercher(keywords, nb_results)
            print(f"   ✓ Playwright: {len(jobs)} offres trouvées")
            return jobs
        except Exception as e:
            print(f"   ⚠️  Erreur Playwright: {e}")
            return []
    
    def rechercher_linkedin(self, keywords: str, location: str = "France", nb_results: int = 10) -> list:
        """Recherche sur LinkedIn (scraping basique)"""
        print(f"🔍 Recherche LinkedIn: {keywords}")
        
        # Construction de l'URL de recherche LinkedIn
        keywords_encoded = keywords.replace(" ", "%20")
        location_encoded = location.replace(" ", "%20")
        url = f"https://www.linkedin.com/jobs/search?keywords={keywords_encoded}&location={location_encoded}&f_TPR=r604800&position=1&pageNum=0"
        
        headers = {'User-Agent': USER_AGENT}
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            job_cards = soup.find_all('div', class_='base-card', limit=nb_results)
            jobs = []
            
            for card in job_cards:
                try:
                    # Extraire le lien
                    link_elem = card.find('a', class_='base-card__full-link')
                    if not link_elem:
                        continue
                    
                    job_url = link_elem.get('href', '').split('?')[0]
                    
                    # Extraire le titre
                    title_elem = card.find('h3', class_='base-search-card__title')
                    title = title_elem.text.strip() if title_elem else "N/A"
                    
                    # Extraire l'entreprise
                    company_elem = card.find('h4', class_='base-search-card__subtitle')
                    company = company_elem.text.strip() if company_elem else "N/A"
                    
                    # Extraire la localisation
                    location_elem = card.find('span', class_='job-search-card__location')
                    loc = location_elem.text.strip() if location_elem else "N/A"
                    
                    if job_url.startswith('http'):
                        jobs.append({
                            'url': job_url,
                            'titre': title,
                            'entreprise': company,
                            'localisation': loc,
                            'plateforme': 'LinkedIn'
                        })
                except Exception as e:
                    continue
            
            return jobs
        
        except Exception as e:
            print(f"   ⚠️  Erreur lors de la recherche LinkedIn: {e}")
            return []
    
    def rechercher_indeed(self, keywords: str, location: str = "France", nb_results: int = 10) -> list:
        """Recherche sur Indeed (avec headers anti-détection améliorés)"""
        print(f"🔍 Recherche Indeed: {keywords}")
        
        keywords_encoded = keywords.replace(" ", "+")
        location_encoded = location.replace(" ", "+")
        url = f"https://fr.indeed.com/jobs?q={keywords_encoded}&l={location_encoded}"
        
        # Headers plus complets pour éviter la détection
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
        }
        
        try:
            # Ajouter un délai pour simuler un comportement humain
            time.sleep(1)
            
            response = requests.get(url, headers=headers, timeout=30, allow_redirects=True)
            
            # Indeed peut bloquer avec 403, on continue sans erreur
            if response.status_code == 403:
                print(f"   ⚠️  Indeed bloque le scraping (403) - Protection anti-bot active")
                print(f"   💡 Conseil: Utilisez l'URL directe d'une offre Indeed avec lancer_generateur.sh")
                return []
            
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Indeed utilise différentes structures selon la page
            job_cards = soup.find_all('div', class_='job_seen_beacon')[:nb_results]
            
            # Si pas de résultats avec cette classe, essayer d'autres
            if not job_cards:
                job_cards = soup.find_all('div', class_='jobsearch-SerpJobCard')[:nb_results]
            
            if not job_cards:
                job_cards = soup.find_all('td', class_='resultContent')[:nb_results]
            
            jobs = []
            
            for card in job_cards:
                try:
                    # Extraire le lien
                    link_elem = card.find('a', class_='jcs-JobTitle')
                    if not link_elem:
                        link_elem = card.find('h2', class_='jobTitle')
                        if link_elem:
                            link_elem = link_elem.find('a')
                    if not link_elem:
                        link_elem = card.find('a', {'data-jk': True})
                    
                    if not link_elem:
                        continue
                    
                    job_id = link_elem.get('data-jk', '')
                    if job_id:
                        job_url = f"https://fr.indeed.com/viewjob?jk={job_id}"
                    else:
                        href = link_elem.get('href', '')
                        if href.startswith('http'):
                            job_url = href
                        else:
                            job_url = "https://fr.indeed.com" + href
                    
                    # Extraire le titre
                    title = link_elem.get('title', '') or link_elem.get('aria-label', '') or link_elem.text.strip()
                    
                    # Extraire l'entreprise
                    company_elem = card.find('span', {'data-testid': 'company-name'})
                    if not company_elem:
                        company_elem = card.find('span', class_='companyName')
                    company = company_elem.text.strip() if company_elem else "N/A"
                    
                    # Extraire la localisation
                    location_elem = card.find('div', {'data-testid': 'text-location'})
                    if not location_elem:
                        location_elem = card.find('div', class_='companyLocation')
                    loc = location_elem.text.strip() if location_elem else location
                    
                    if job_url and 'indeed.com' in job_url:
                        jobs.append({
                            'url': job_url,
                            'titre': title,
                            'entreprise': company,
                            'localisation': loc,
                            'plateforme': 'Indeed'
                        })
                except Exception as e:
                    continue
            
            return jobs
        
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                print(f"   ⚠️  Indeed bloque le scraping (protection anti-bot)")
            else:
                print(f"   ⚠️  Erreur HTTP {e.response.status_code}: {e}")
            return []
        except Exception as e:
            print(f"   ⚠️  Erreur lors de la recherche Indeed: {e}")
            return []
    
    def rechercher_welcome_to_the_jungle(self, keywords: str, nb_results: int = 10) -> list:
        """Recherche sur Welcome to the Jungle"""
        print(f"🔍 Recherche Welcome to the Jungle: {keywords}")
        
        # Si Playwright est activé et disponible, l'utiliser
        if self.use_playwright and self.playwright_available:
            return self._rechercher_wttj_playwright(keywords, nb_results)
        
        # WTTJ utilise une API GraphQL publique
        api_url = "https://www.welcometothejungle.com/api/graphql"
        
        # Query GraphQL pour rechercher des jobs
        query = """
        query JobSearch($query: String!, $page: Int, $limit: Int) {
          jobs(query: $query, page: $page, limit: $limit) {
            edges {
              node {
                id
                name
                slug
                office {
                  name
                }
                company {
                  name
                  slug
                }
              }
            }
          }
        }
        """
        
        headers = {
            'User-Agent': USER_AGENT,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        
        payload = {
            'query': query,
            'variables': {
                'query': keywords,
                'page': 1,
                'limit': nb_results
            }
        }
        
        try:
            response = requests.post(api_url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                jobs = []
                
                edges = data.get('data', {}).get('jobs', {}).get('edges', [])
                
                for edge in edges[:nb_results]:
                    node = edge.get('node', {})
                    company = node.get('company', {})
                    office = node.get('office', {})
                    
                    job_slug = node.get('slug', '')
                    company_slug = company.get('slug', '')
                    
                    if job_slug and company_slug:
                        job_url = f"https://www.welcometothejungle.com/fr/companies/{company_slug}/jobs/{job_slug}"
                        
                        jobs.append({
                            'url': job_url,
                            'titre': node.get('name', 'N/A'),
                            'entreprise': company.get('name', 'N/A'),
                            'localisation': office.get('name', 'France'),
                            'plateforme': 'Welcome to the Jungle'
                        })
                
                return jobs
            else:
                # Fallback: scraping classique si l'API ne fonctionne pas
                return self._rechercher_wttj_fallback(keywords, nb_results)
        
        except Exception as e:
            print(f"   ⚠️  API WTTJ inaccessible, tentative de scraping basique...")
            return self._rechercher_wttj_fallback(keywords, nb_results)
    
    def _rechercher_wttj_fallback(self, keywords: str, nb_results: int) -> list:
        """Fallback: scraping basique de WTTJ"""
        try:
            keywords_encoded = keywords.replace(" ", "%20")
            url = f"https://www.welcometothejungle.com/fr/jobs?query={keywords_encoded}"
            
            headers = {
                'User-Agent': USER_AGENT,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'fr-FR,fr;q=0.9',
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            jobs = []
            
            # Chercher tous les liens vers des jobs
            job_links = soup.find_all('a', href=True)
            
            for link in job_links:
                href = link.get('href', '')
                # Format WTTJ: /fr/companies/{company}/jobs/{job_id}
                if '/companies/' in href and '/jobs/' in href and href not in [j['url'] for j in jobs]:
                    full_url = href if href.startswith('http') else f"https://www.welcometothejungle.com{href}"
                    
                    # Essayer d'extraire le titre
                    title = link.get('aria-label', '') or link.text.strip()
                    if not title or len(title) > 150:
                        title = "Voir l'offre sur WTTJ"
                    
                    jobs.append({
                        'url': full_url,
                        'titre': title,
                        'entreprise': "Voir sur WTTJ",
                        'localisation': "France",
                        'plateforme': 'Welcome to the Jungle'
                    })
                    
                    if len(jobs) >= nb_results:
                        break
            
            if not jobs:
                print(f"   💡 WTTJ: Aucun résultat par scraping (site JavaScript)")
                print(f"   💡 Conseil: Recherchez manuellement sur welcometothejungle.com")
            
            return jobs
        
        except Exception as e:
            print(f"   ⚠️  Erreur scraping WTTJ: {e}")
            return []
    
    def rechercher_apec(self, keywords: str, nb_results: int = 10) -> list:
        """Recherche sur l'Apec (site pour cadres)"""
        print(f"🔍 Recherche Apec: {keywords}")
        
        keywords_encoded = keywords.replace(" ", "+")
        url = f"https://www.apec.fr/candidat/recherche-emploi.html/emploi?motsCles={keywords_encoded}"
        
        headers = {
            'User-Agent': USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9',
        }
        
        try:
            time.sleep(1)
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            jobs = []
            
            # L'Apec utilise des cartes d'offres
            job_cards = soup.find_all('article', class_='box-offer')[:nb_results]
            
            if not job_cards:
                job_cards = soup.find_all('div', {'data-test': 'offer-card'})[:nb_results]
            
            for card in job_cards:
                try:
                    # Extraire le lien
                    link_elem = card.find('a', href=True)
                    if not link_elem:
                        continue
                    
                    href = link_elem.get('href', '')
                    if href.startswith('http'):
                        job_url = href
                    else:
                        job_url = f"https://www.apec.fr{href}"
                    
                    # Extraire le titre
                    title_elem = card.find('h2') or card.find('h3') or link_elem
                    title = title_elem.text.strip() if title_elem else "Voir l'offre"
                    
                    # Extraire l'entreprise
                    company_elem = card.find('span', class_='company')
                    if not company_elem:
                        company_elem = card.find('div', class_='company-name')
                    company = company_elem.text.strip() if company_elem else "N/A"
                    
                    # Extraire la localisation
                    location_elem = card.find('span', class_='location')
                    if not location_elem:
                        location_elem = card.find('div', class_='location')
                    loc = location_elem.text.strip() if location_elem else "France"
                    
                    jobs.append({
                        'url': job_url,
                        'titre': title,
                        'entreprise': company,
                        'localisation': loc,
                        'plateforme': 'Apec'
                    })
                    
                except Exception as e:
                    continue
            
            if not jobs:
                print(f"   💡 Apec: Pas de résultats (site peut nécessiter une connexion)")
            
            return jobs
        
        except Exception as e:
            print(f"   ⚠️  Erreur lors de la recherche Apec: {e}")
            return []
    
    def analyser_pertinence_ia(self, jobs: list) -> list:
        """Utilise l'IA pour scorer la pertinence de chaque poste"""
        if not self.api_key or not jobs:
            return jobs
        
        print(f"\n🤖 Analyse de la pertinence avec Claude ({CLAUDE_MODEL})...")
        
        # Préparer le profil candidat
        profil_resume = f"""
Profil: {self.profil.get('profil', '')}
Compétences Scientific AI: {self.profil.get('competences_scientific_ai', '')}
Compétences Simulation: {self.profil.get('competences_simulation', '')}
Compétences Generative AI: {self.profil.get('competences_generative_ai', '')}
Compétences Informatique: {self.profil.get('competences_informatique', '')}
"""
        
        # Créer un résumé des jobs
        jobs_summary = "\n\n".join([
            f"JOB {i+1}:\nTitre: {job['titre']}\nEntreprise: {job['entreprise']}\nLocalisation: {job['localisation']}"
            for i, job in enumerate(jobs)
        ])
        
        prompt = f"""Analyse ces {len(jobs)} offres d'emploi et score leur pertinence pour ce candidat.

PROFIL CANDIDAT:
{profil_resume}

OFFRES:
{jobs_summary}

Pour chaque offre, donne un score de pertinence de 0 à 10 et une courte justification (1 ligne).

Réponds au format JSON:
{{
  "evaluations": [
    {{"job_id": 1, "score": 8, "justification": "..."}},
    ...
  ]
}}
"""
        
        try:
            response = self.client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=1500,
                temperature=0.3,
                system="Tu es un expert en matching de profils et d'offres d'emploi. Réponds uniquement en JSON.",
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = response.content[0].text
            
            # Parser le JSON
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0].strip()
            
            result = json.loads(response_text)
            evaluations = result.get('evaluations', [])
            
            # Ajouter les scores aux jobs
            for i, job in enumerate(jobs):
                eval_data = next((e for e in evaluations if e['job_id'] == i+1), None)
                if eval_data:
                    job['score_ia'] = eval_data['score']
                    job['justification_ia'] = eval_data['justification']
                else:
                    job['score_ia'] = 5
                    job['justification_ia'] = "Non évalué"
            
            # Trier par score décroissant
            jobs.sort(key=lambda x: x.get('score_ia', 0), reverse=True)
            
            print(f"   ✓ {len(jobs)} offres analysées et triées par pertinence")
            
        except Exception as e:
            print(f"   ⚠️  Impossible d'analyser avec l'IA: {e}")
            # Ajouter un score par défaut
            for job in jobs:
                job['score_ia'] = 5
                job['justification_ia'] = "Non évalué"
        
        return jobs


def charger_profil():
    """Charge le profil depuis infos_statique.txt"""
    with open('infos_statique.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extraction basique
    profil = {}
    
    # Extraire le profil par défaut
    match = re.search(r'profil_defaut:\s*\|\n((?:  .+\n?)+)', content)
    if match:
        profil['profil'] = ' '.join(line.strip() for line in match.group(1).strip().split('\n'))
    
    # Extraire les compétences
    for key in ['competences_scientific_ai', 'competences_simulation', 'competences_generative_ai', 'competences_informatique']:
        match = re.search(f'{key}:\\s*\\|\\n((?:  .+\\n?)+)', content)
        if match:
            profil[key] = ' '.join(line.strip() for line in match.group(1).strip().split('\n'))
    
    return profil


def afficher_jobs(jobs: list):
    """Affiche les jobs avec leur score"""
    print("\n" + "=" * 80)
    print("  OFFRES TROUVÉES")
    print("=" * 80 + "\n")
    
    for i, job in enumerate(jobs, 1):
        score = job.get('score_ia', 'N/A')
        score_display = f"⭐ {score}/10" if isinstance(score, (int, float)) else "N/A"
        
        print(f"[{i}] {score_display} - {job['titre']}")
        print(f"    🏢 {job['entreprise']}")
        print(f"    📍 {job['localisation']}")
        print(f"    🌐 {job['plateforme']}")
        if 'justification_ia' in job and job['justification_ia'] != "Non évalué":
            print(f"    💡 {job['justification_ia']}")
        print(f"    🔗 {job['url']}")
        print()


def selection_interactive(jobs: list) -> list:
    """Permet de sélectionner les jobs à traiter"""
    print("\n" + "=" * 80)
    print("  SÉLECTION DES OFFRES À TRAITER")
    print("=" * 80)
    print("\nEntrez les numéros des offres qui vous intéressent")
    print("(séparés par des espaces, ex: 1 3 5 7)")
    print("Ou tapez 'all' pour toutes les sélectionner")
    print("Ou tapez 'top5' pour les 5 meilleures")
    print()
    
    choix = input("Votre sélection: ").strip().lower()
    
    if choix == 'all':
        return jobs
    elif choix == 'top5':
        return jobs[:5]
    else:
        try:
            indices = [int(x) for x in choix.split()]
            jobs_selectionnes = [jobs[i-1] for i in indices if 1 <= i <= len(jobs)]
            return jobs_selectionnes
        except:
            print("❌ Sélection invalide")
            return []


def generer_batch(jobs: list):
    """Génère les CV/LM pour tous les jobs sélectionnés"""
    print("\n" + "=" * 80)
    print(f"  GÉNÉRATION EN BATCH - {len(jobs)} offres")
    print("=" * 80 + "\n")
    
    resultats = []
    
    for i, job in enumerate(jobs, 1):
        print(f"\n{'='*80}")
        print(f"📄 [{i}/{len(jobs)}] Traitement: {job['titre']}")
        print(f"🏢 {job['entreprise']}")
        print(f"{'='*80}\n")
        
        try:
            # Lancer le générateur
            cmd = ['python3', 'generateur_cv_lettre.py', job['url']]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Génération réussie pour: {job['titre']}")
                resultats.append({'job': job, 'success': True})
            else:
                print(f"❌ Erreur lors de la génération pour: {job['titre']}")
                print(f"   {result.stderr[:200]}")
                resultats.append({'job': job, 'success': False})
            
            # Pause entre chaque génération pour éviter de surcharger l'API
            if i < len(jobs):
                time.sleep(2)
        
        except Exception as e:
            print(f"❌ Exception: {e}")
            resultats.append({'job': job, 'success': False})
    
    # Résumé
    print("\n" + "=" * 80)
    print("  RÉSUMÉ DE LA GÉNÉRATION EN BATCH")
    print("=" * 80 + "\n")
    
    succes = sum(1 for r in resultats if r['success'])
    echecs = len(resultats) - succes
    
    print(f"✅ Réussies: {succes}/{len(resultats)}")
    print(f"❌ Échouées: {echecs}/{len(resultats)}")
    
    if echecs > 0:
        print("\nOffres échouées:")
        for r in resultats:
            if not r['success']:
                print(f"  - {r['job']['titre']} ({r['job']['entreprise']})")


def main():
    print("=" * 80)
    print("  RECHERCHE AUTOMATIQUE DE POSTES")
    print("=" * 80)
    print()
    
    # 1. Charger le profil
    print("📥 Chargement du profil...")
    profil = charger_profil()
    print("   ✓ Profil chargé")
    
    # 2. Demander les critères de recherche
    print("\n📝 Critères de recherche:")
    
    # Mots-clés principaux
    if len(sys.argv) > 1:
        keywords = sys.argv[1]
    else:
        keywords = input("Poste recherché (ex: 'Data Scientist', 'Ingénieur IA'): ").strip()
    
    if not keywords:
        print("❌ Poste requis")
        sys.exit(1)
    
    # Localisation
    location = input("Localisation (défaut: France, ex: Paris, Lyon, Remote): ").strip() or "France"
    
    # Niveau de séniorité
    print("\n💼 Niveau de séniorité:")
    print("   1. Junior / Débutant")
    print("   2. Confirmé / Intermédiaire")
    print("   3. Senior / Expert")
    print("   4. Lead / Manager")
    print("   5. Tous niveaux (défaut)")
    seniorite_choice = input("Choix (1-5, défaut: 5): ").strip()
    
    seniorite_map = {
        '1': 'junior débutant',
        '2': 'confirmé intermédiaire',
        '3': 'senior expert',
        '4': 'lead manager',
        '5': ''
    }
    seniorite = seniorite_map.get(seniorite_choice, '')
    
    # Domaines
    print("\n🎯 Domaines d'expertise (séparés par des virgules):")
    print("   Exemples: IA, Machine Learning, Deep Learning, NLP, Computer Vision")
    domaines = input("Domaines (laisser vide si non applicable): ").strip()
    
    # Type d'entreprise
    print("\n🏢 Type d'entreprise:")
    print("   1. Startup")
    print("   2. PME / ETI")
    print("   3. Grande entreprise / CAC40")
    print("   4. Tous types (défaut)")
    type_entreprise_choice = input("Choix (1-4, défaut: 4): ").strip()
    
    type_entreprise_map = {
        '1': 'startup',
        '2': 'PME ETI',
        '3': 'grande entreprise CAC40',
        '4': ''
    }
    type_entreprise = type_entreprise_map.get(type_entreprise_choice, '')
    
    # Nombre de résultats
    nb_jobs_str = input("\nNombre d'offres à récupérer par plateforme (défaut: 10): ").strip()
    nb_jobs = int(nb_jobs_str) if nb_jobs_str.isdigit() else 10
    
    # Demander si on veut utiliser Playwright pour WTTJ
    use_playwright = False
    playwright_choice = input("Utiliser Playwright pour WTTJ? (oui/non, défaut: non): ").strip().lower()
    if playwright_choice in ['oui', 'o', 'yes', 'y']:
        use_playwright = True
    
    # 2b. Construire la requête de recherche optimisée
    query_parts = [keywords]
    
    if seniorite:
        query_parts.append(seniorite)
    
    if domaines:
        # Nettoyer et ajouter les domaines
        domaines_list = [d.strip() for d in domaines.split(',') if d.strip()]
        if domaines_list:
            query_parts.extend(domaines_list[:3])  # Limiter à 3 pour ne pas surcharger
    
    if type_entreprise:
        query_parts.append(type_entreprise)
    
    # Construire la requête finale
    search_query = ' '.join(query_parts)
    
    # 3. Afficher les critères de recherche
    print(f"\n{'='*80}")
    print("CRITÈRES DE RECHERCHE")
    print(f"{'='*80}")
    print(f"🎯 Poste: {keywords}")
    print(f"📍 Localisation: {location}")
    if seniorite:
        print(f"💼 Séniorité: {seniorite}")
    if domaines:
        print(f"🔬 Domaines: {domaines}")
    if type_entreprise:
        print(f"🏢 Type entreprise: {type_entreprise}")
    print(f"🔍 Requête complète: '{search_query}'")
    if use_playwright:
        print("🚀 Mode Playwright: Activé pour WTTJ")
    print(f"{'='*80}\n")
    
    # 4. Rechercher sur les plateformes
    rechercheur = RechercheurPostes(profil, use_playwright=use_playwright)
    tous_jobs = []
    
    # LinkedIn
    jobs_linkedin = rechercheur.rechercher_linkedin(search_query, location, nb_jobs)
    print(f"   ✓ LinkedIn: {len(jobs_linkedin)} offres trouvées")
    tous_jobs.extend(jobs_linkedin)
    
    time.sleep(2)  # Pause entre plateformes
    
    # Indeed
    jobs_indeed = rechercheur.rechercher_indeed(search_query, location, nb_jobs)
    print(f"   ✓ Indeed: {len(jobs_indeed)} offres trouvées")
    tous_jobs.extend(jobs_indeed)
    
    time.sleep(2)
    
    # Welcome to the Jungle
    jobs_wttj = rechercheur.rechercher_welcome_to_the_jungle(search_query, nb_jobs)
    print(f"   ✓ Welcome to the Jungle: {len(jobs_wttj)} offres trouvées")
    tous_jobs.extend(jobs_wttj)
    
    time.sleep(2)
    
    # Apec (pour les postes cadres)
    jobs_apec = rechercheur.rechercher_apec(search_query, nb_jobs)
    print(f"   ✓ Apec: {len(jobs_apec)} offres trouvées")
    tous_jobs.extend(jobs_apec)
    
    # 4b. Ajouter les critères comme métadonnées
    for job in tous_jobs:
        job['criteres_recherche'] = {
            'poste': keywords,
            'localisation': location,
            'seniorite': seniorite,
            'domaines': domaines,
            'type_entreprise': type_entreprise
        }
    
    if not tous_jobs:
        print("\n❌ Aucune offre trouvée")
        sys.exit(1)
    
    print(f"\n📊 Total: {len(tous_jobs)} offres trouvées")
    
    # 4. Analyser la pertinence avec l'IA
    tous_jobs = rechercheur.analyser_pertinence_ia(tous_jobs)
    
    # 5. Sauvegarder les résultats
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    results_file = f"recherche_postes_{timestamp}.json"
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(tous_jobs, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Résultats sauvegardés dans: {results_file}")
    
    # 6. Afficher les jobs
    afficher_jobs(tous_jobs)
    
    # 7. Sélection interactive
    jobs_selectionnes = selection_interactive(tous_jobs)
    
    if not jobs_selectionnes:
        print("\n❌ Aucune offre sélectionnée")
        sys.exit(0)
    
    print(f"\n✅ {len(jobs_selectionnes)} offre(s) sélectionnée(s)")
    
    # 8. Confirmation
    print("\n⚠️  La génération en batch va:")
    print(f"   - Traiter {len(jobs_selectionnes)} offres")
    print(f"   - Appeler l'API Claude {len(jobs_selectionnes) * 4} fois")
    print(f"   - Prendre environ {len(jobs_selectionnes) * 2} minutes")
    print()
    
    confirmation = input("Confirmer la génération en batch? (oui/non): ").strip().lower()
    
    if confirmation not in ['oui', 'o', 'yes', 'y']:
        print("\n❌ Génération annulée")
        sys.exit(0)
    
    # 9. Générer en batch
    generer_batch(jobs_selectionnes)
    
    print("\n✅ Processus terminé!")
    print(f"📂 Tous les dossiers de candidature sont dans: ./candidatures/")


if __name__ == "__main__":
    main()
