#!/usr/bin/env python3
"""
Générateur automatique de CV et lettre de motivation personnalisés
Auteur: Maxime Miroux
"""

import re
import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import requests
from bs4 import BeautifulSoup
from anthropic import Anthropic
from dotenv import load_dotenv
from dataclasses import dataclass, field

# Déterminer le répertoire racine du projet
SCRIPT_DIR = Path(__file__).parent.absolute()
ROOT_DIR = SCRIPT_DIR.parent
TEMPLATES_DIR = ROOT_DIR / "templates"

# Charger les variables d'environnement depuis .env
load_dotenv(ROOT_DIR / ".env")

# Importer la configuration centralisée
from config import *


@dataclass
class InfosPersonnelles:
    """Structure pour stocker les informations personnelles"""
    nom: str
    titre: str
    localisation: str
    email: str
    linkedin: str
    telephone: str
    profil_defaut: str
    experiences: List[Dict]
    formations: List[Dict]
    certifications: List[Dict]
    projets: List[Dict]
    langues: List[Dict]
    # Compétences - deux modes possibles :
    # Mode specifique : champs individuels (pour compatibilité)
    competences_scientific_ai: str = ""
    competences_simulation: str = ""
    competences_generative_ai: str = ""
    competences_informatique: str = ""
    # Mode generique : liste de dictionnaires {categorie: str, contenu: str}
    competences: List[Dict] = field(default_factory=list)


class ParseurInfosStatiques:
    """Parse le fichier infos_statique.txt"""
    
    @staticmethod
    def parse(filepath: str) -> InfosPersonnelles:
        """Parse le fichier et retourne un objet InfosPersonnelles"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extraction simple des informations
        data = {
            'nom': ParseurInfosStatiques._extract('nom:', content),
            'titre': ParseurInfosStatiques._extract('titre:', content),
            'localisation': ParseurInfosStatiques._extract('localisation:', content),
            'email': ParseurInfosStatiques._extract('email:', content),
            'linkedin': ParseurInfosStatiques._extract('linkedin:', content),
            'telephone': ParseurInfosStatiques._extract('telephone:', content),
            'profil_defaut': ParseurInfosStatiques._extract_multiline('profil_defaut:', content),
        }
        
        # Parser les compétences selon le mode (specifique ou generique)
        if MODE_PROFIL == "specifique":
            # Mode spécifique : catégories hardcodées
            data['competences_scientific_ai'] = ParseurInfosStatiques._extract_multiline('competences_scientific_ai:', content)
            data['competences_simulation'] = ParseurInfosStatiques._extract_multiline('competences_simulation:', content)
            data['competences_generative_ai'] = ParseurInfosStatiques._extract_multiline('competences_generative_ai:', content)
            data['competences_informatique'] = ParseurInfosStatiques._extract_multiline('competences_informatique:', content)
            data['competences'] = []
        else:
            # Mode générique : parse les catégories dynamiquement
            data['competences'] = ParseurInfosStatiques._parse_competences_generique(content)
            data['competences_scientific_ai'] = ""
            data['competences_simulation'] = ""
            data['competences_generative_ai'] = ""
            data['competences_informatique'] = ""
        
        # Pour simplifier, on parse les sections complexes manuellement
        # (Dans une version production, utiliser un vrai parser TOML/YAML)
        data['experiences'] = ParseurInfosStatiques._parse_experiences(content)
        data['formations'] = ParseurInfosStatiques._parse_formations(content)
        data['certifications'] = ParseurInfosStatiques._parse_certifications(content)
        data['projets'] = ParseurInfosStatiques._parse_projets(content)
        data['langues'] = ParseurInfosStatiques._parse_langues(content)
        
        return InfosPersonnelles(**data)
    
    @staticmethod
    def _extract(key: str, content: str) -> str:
        """Extrait une valeur simple"""
        match = re.search(f'{key}\\s*(.*)$', content, re.MULTILINE)
        if match:
            value = match.group(1).strip()
            # Ignorer les lignes qui commencent par # (commentaires markdown)
            if value and not value.startswith('#'):
                return value
        return ""
    
    @staticmethod
    def _extract_multiline(key: str, content: str) -> str:
        """Extrait une valeur multiligne"""
        pattern = f'{key}\\s*\\|\\n((?:  .+\\n?)+)'
        match = re.search(pattern, content)
        if match:
            lines = match.group(1).strip().split('\n')
            return ' '.join(line.strip() for line in lines)
        return ""
    
    @staticmethod
    def _parse_experiences(content: str) -> List[Dict]:
        """Parse les expériences"""
        experiences = []
        sections = re.findall(r'\[\[experience\]\](.+?)(?=\[\[|# FORMATION)', content, re.DOTALL)
        
        for section in sections:
            exp = {
                'poste': ParseurInfosStatiques._extract('poste:', section),
                'entreprise': ParseurInfosStatiques._extract('entreprise:', section),
                'periode': ParseurInfosStatiques._extract('periode:', section),
                'missions': re.findall(r'  - (.+)', section)
            }
            experiences.append(exp)
        
        return experiences
    
    @staticmethod
    def _parse_formations(content: str) -> List[Dict]:
        """Parse les formations"""
        formations = []
        sections = re.findall(r'\[\[formation\]\](.+?)(?=\[\[|# CERTIFICATIONS)', content, re.DOTALL)
        
        for section in sections:
            form = {
                'diplome': ParseurInfosStatiques._extract('diplome:', section),
                'etablissement': ParseurInfosStatiques._extract('etablissement:', section),
                'periode': ParseurInfosStatiques._extract('periode:', section),
                'details': re.findall(r'  - (.+)', section)
            }
            formations.append(form)
        
        return formations
    
    @staticmethod
    def _parse_certifications(content: str) -> List[Dict]:
        """Parse les certifications"""
        certifications = []
        sections = re.findall(r'\[\[certification\]\](.+?)(?=\[\[|# PROJETS)', content, re.DOTALL)
        
        for section in sections:
            cert = {
                'titre': ParseurInfosStatiques._extract('titre:', section),
                'date': ParseurInfosStatiques._extract('date:', section)
            }
            certifications.append(cert)
        
        return certifications
    
    @staticmethod
    def _parse_projets(content: str) -> List[Dict]:
        """Parse les projets"""
        projets = []
        sections = re.findall(r'\[\[projet\]\](.+?)(?=\[\[|# COMPÉTENCES)', content, re.DOTALL)
        
        for section in sections:
            # Extraire titre (avec ou sans espaces autour de :)
            titre_match = re.search(r'titre\s*:\s*(.+?)(?:\n|$)', section)
            titre = titre_match.group(1).strip() if titre_match else ""
            
            # Extraire description multiligne
            desc_match = re.search(r'description\s*:\s*\n(.+?)(?=compétences et outils|$)', section, re.DOTALL)
            description = desc_match.group(1).strip() if desc_match else ""
            
            # Extraire compétences et outils multiligne
            comp_match = re.search(r'compétences et outils\s*:\s*\n(.+?)(?=\n\n|\[\[|$)', section, re.DOTALL)
            competences = comp_match.group(1).strip() if comp_match else ""
            
            proj = {
                'titre': titre,
                'description': description,
                'competences': competences
            }
            projets.append(proj)
        
        return projets
    
    @staticmethod
    def _parse_langues(content: str) -> List[Dict]:
        """Parse les langues"""
        langues = []
        sections = re.findall(r'\[\[langue\]\](.+?)(?=\[\[|$)', content, re.DOTALL)
        
        for section in sections:
            lang = {
                'langue': ParseurInfosStatiques._extract('langue:', section),
                'niveau': ParseurInfosStatiques._extract('niveau:', section)
            }
            langues.append(lang)
        
        return langues
    
    @staticmethod
    def _parse_competences_generique(content: str) -> List[Dict]:
        """Parse les compétences en mode générique (pour tout type de profil)"""
        competences = []
        # Chercher la section COMPÉTENCES
        sections = re.findall(r'\[\[competence\]\](.+?)(?=\[\[|# LANGUES|$)', content, re.DOTALL)
        
        for section in sections:
            categorie = ParseurInfosStatiques._extract('categorie:', section)
            contenu = ParseurInfosStatiques._extract_multiline('contenu:', section)
            # Si contenu n'est pas multiligne, essayer extraction simple
            if not contenu:
                contenu = ParseurInfosStatiques._extract('contenu:', section)
            
            if categorie and contenu:
                comp = {
                    'categorie': categorie,
                    'contenu': contenu
                }
                competences.append(comp)
        
        return competences


class ScraperAnnonce:
    """Scrape une annonce de poste depuis une URL"""
    
    @staticmethod
    def scraper(url: str) -> str:
        """Scrape le contenu d'une annonce"""
        try:
            headers = {
                'User-Agent': USER_AGENT
            }
            response = requests.get(url, headers=headers, timeout=HTTP_TIMEOUT)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Retirer les scripts et styles
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Extraire le texte
            text = soup.get_text()
            
            # Nettoyer
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            return text
            
        except Exception as e:
            print(f"Erreur lors du scraping: {e}")
            return ""


class GenerateurIA:
    """Utilise Claude (Anthropic) pour générer du contenu personnalisé"""
    
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
    
    def analyser_annonce(self, annonce_text: str) -> Dict[str, str]:
        """Analyse l'annonce et extrait les informations clés"""
        
        prompt = PROMPT_TEMPLATE_ANALYSE.format(
            annonce_text=annonce_text[:MAX_ANNONCE_LENGTH]
        )

        response = self.client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=MAX_TOKENS_ANALYSE,
            temperature=TEMPERATURE,
            system=SYSTEM_PROMPT_ANALYSE,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = response.content[0].text
        
        # Parser le JSON
        import json
        try:
            # Extraire le JSON si entouré de ```json
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0].strip()
            return json.loads(response_text)
        except:
            # Si le parsing échoue, retourner des valeurs par défaut
            return {
                'poste': 'Poste non identifié',
                'entreprise': 'Entreprise non identifiée',
                'competences_cles': [],
                'mots_cles': '',
                'mission_principale': ''
            }
    
    def analyser_entreprise(self, site_text: str, poste_cible: str) -> Dict[str, str]:
        """Analyse le site web d'une entreprise pour candidature spontanée"""
        
        prompt = PROMPT_TEMPLATE_ANALYSE_ENTREPRISE.format(
            site_text=site_text[:MAX_ANNONCE_LENGTH],
            poste_cible=poste_cible
        )

        response = self.client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=MAX_TOKENS_ANALYSE,
            temperature=TEMPERATURE,
            system=SYSTEM_PROMPT_ANALYSE_ENTREPRISE,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = response.content[0].text
        
        # Parser le JSON
        import json
        try:
            # Extraire le JSON si entouré de ```json
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0].strip()
            result = json.loads(response_text)
            # Ajouter le poste cible pour compatibilité avec le reste du code
            result['poste'] = poste_cible
            return result
        except:
            # Si le parsing échoue, retourner des valeurs par défaut
            return {
                'poste': poste_cible,
                'entreprise': 'Entreprise non identifiée',
                'secteur': 'Secteur non identifié',
                'activites_principales': [],
                'valeurs': '',
                'technologies': '',
                'besoins_potentiels': '',
                'mots_cles': ''
            }
    
    def generer_profil_adapte(self, profil_base: str, analyse_annonce: Dict, infos: 'InfosPersonnelles' = None) -> str:
        """Génère un profil adapté à l'annonce"""
        
        # Préparer un résumé des expériences
        experiences_resume = ""
        if infos and infos.experiences:
            for i, exp in enumerate(infos.experiences[:2]):  # Prendre les 2 premières expériences
                experiences_resume += f"- {exp['poste']} chez {exp['entreprise']} ({exp['periode']})\n"
                # Ajouter 2-3 missions clés
                for mission in exp['missions'][:3]:
                    experiences_resume += f"  • {mission}\n"
        
        # Préparer un résumé des compétences (selon le mode)
        competences_techniques = ""
        if infos:
            if MODE_PROFIL == "specifique":
                # Mode spécifique : catégories hardcodées
                if infos.competences_scientific_ai:
                    competences_techniques += f"Scientific AI: {infos.competences_scientific_ai.strip()}\n"
                if infos.competences_simulation:
                    competences_techniques += f"Simulation: {infos.competences_simulation.strip()}\n"
                if infos.competences_generative_ai:
                    competences_techniques += f"Generative AI: {infos.competences_generative_ai.strip()}\n"
                if infos.competences_informatique:
                    competences_techniques += f"Informatique: {infos.competences_informatique.strip()}\n"
            else:
                # Mode générique : catégories dynamiques
                for comp in infos.competences:
                    competences_techniques += f"{comp['categorie']}: {comp['contenu']}\n"
        
        prompt = PROMPT_TEMPLATE_PROFIL.format(
            profil_base=profil_base,
            experiences_resume=experiences_resume or "Non disponible",
            competences_techniques=competences_techniques or "Non disponible",
            poste=analyse_annonce['poste'],
            entreprise=analyse_annonce['entreprise'],
            competences=', '.join(analyse_annonce.get('competences_cles', [])),
            mission=analyse_annonce.get('mission_principale', '')
        )

        response = self.client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=MAX_TOKENS_PROFIL,
            temperature=TEMPERATURE,
            system=SYSTEM_PROMPT_PROFIL,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.content[0].text.strip()
    
    def generer_profil_adapte_spontanee(self, profil_base: str, analyse_entreprise: Dict, infos: 'InfosPersonnelles' = None) -> str:
        """Génère un profil adapté pour une candidature spontanée"""
        
        # Préparer un résumé des expériences
        experiences_resume = ""
        if infos and infos.experiences:
            for i, exp in enumerate(infos.experiences[:2]):
                experiences_resume += f"- {exp['poste']} chez {exp['entreprise']} ({exp['periode']})\n"
                for mission in exp['missions'][:3]:
                    experiences_resume += f"  • {mission}\n"
        
        # Préparer un résumé des compétences (selon le mode)
        competences_techniques = ""
        if infos:
            if MODE_PROFIL == "specifique":
                # Mode spécifique : catégories hardcodées
                if infos.competences_scientific_ai:
                    competences_techniques += f"Scientific AI: {infos.competences_scientific_ai.strip()}\n"
                if infos.competences_simulation:
                    competences_techniques += f"Simulation: {infos.competences_simulation.strip()}\n"
                if infos.competences_generative_ai:
                    competences_techniques += f"Generative AI: {infos.competences_generative_ai.strip()}\n"
                if infos.competences_informatique:
                    competences_techniques += f"Informatique: {infos.competences_informatique.strip()}\n"
            else:
                # Mode générique : catégories dynamiques
                for comp in infos.competences:
                    competences_techniques += f"{comp['categorie']}: {comp['contenu']}\n"
        
        prompt = PROMPT_TEMPLATE_PROFIL_SPONTANEE.format(
            profil_base=profil_base,
            experiences_resume=experiences_resume or "Non disponible",
            competences_techniques=competences_techniques or "Non disponible",
            entreprise=analyse_entreprise['entreprise'],
            secteur=analyse_entreprise.get('secteur', ''),
            activites=', '.join(analyse_entreprise.get('activites_principales', [])),
            valeurs=analyse_entreprise.get('valeurs', ''),
            technologies=analyse_entreprise.get('technologies', ''),
            poste_cible=analyse_entreprise['poste']
        )

        response = self.client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=MAX_TOKENS_PROFIL,
            temperature=TEMPERATURE,
            system=SYSTEM_PROMPT_PROFIL,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.content[0].text.strip()
    
    def generer_lettre_motivation(self, infos: InfosPersonnelles, analyse_annonce: Dict) -> Dict[str, str]:
        """Génère les paragraphes de la lettre de motivation"""
        
        prompt = PROMPT_TEMPLATE_LETTRE.format(
            nom=infos.nom,
            profil=infos.profil_defaut,
            experience=f"{infos.experiences[0]['poste']} chez {infos.experiences[0]['entreprise']}",
            poste=analyse_annonce['poste'],
            entreprise=analyse_annonce['entreprise'],
            competences=', '.join(analyse_annonce.get('competences_cles', [])),
            mission=analyse_annonce.get('mission_principale', '')
        )

        response = self.client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=MAX_TOKENS_LETTRE,
            temperature=TEMPERATURE,
            system=SYSTEM_PROMPT_LETTRE,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = response.content[0].text
        
        import json
        try:
            # Extraire le JSON si entouré de ```json
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0].strip()
            return json.loads(response_text)
        except:
            return {
                'paragraphe_1': 'Paragraphe 1 non généré',
                'paragraphe_2': 'Paragraphe 2 non généré',
                'paragraphe_3': 'Paragraphe 3 non généré',
                'conclusion': 'Conclusion non générée'
            }
    
    def generer_lettre_motivation_spontanee(self, infos: InfosPersonnelles, analyse_entreprise: Dict) -> Dict[str, str]:
        """Génère une lettre de motivation pour candidature spontanée"""
        
        prompt = PROMPT_TEMPLATE_LETTRE_SPONTANEE.format(
            nom=infos.nom,
            profil=infos.profil_defaut,
            experience=f"{infos.experiences[0]['poste']} chez {infos.experiences[0]['entreprise']}",
            entreprise=analyse_entreprise['entreprise'],
            secteur=analyse_entreprise.get('secteur', ''),
            activites=', '.join(analyse_entreprise.get('activites_principales', [])),
            valeurs=analyse_entreprise.get('valeurs', ''),
            technologies=analyse_entreprise.get('technologies', ''),
            poste_cible=analyse_entreprise['poste'],
            besoins=analyse_entreprise.get('besoins_potentiels', '')
        )

        response = self.client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=MAX_TOKENS_LETTRE,
            temperature=TEMPERATURE,
            system=SYSTEM_PROMPT_LETTRE,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = response.content[0].text
        
        import json
        try:
            # Extraire le JSON si entouré de ```json
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0].strip()
            return json.loads(response_text)
        except:
            return {
                'paragraphe_1': 'Paragraphe 1 non généré',
                'paragraphe_2': 'Paragraphe 2 non généré',
                'paragraphe_3': 'Paragraphe 3 non généré',
                'conclusion': 'Conclusion non générée'
            }
    
    def generer_topo_entretien(self, annonce_text: str, analyse_annonce: Dict, infos: InfosPersonnelles) -> str:
        """Génère un topo de préparation d'entretien"""
        
        # Préparer le profil candidat
        profil_candidat = f"""
Profil: {infos.profil_defaut}

Expériences principales:
"""
        for exp in infos.experiences[:2]:
            profil_candidat += f"- {exp['poste']} chez {exp['entreprise']} ({exp['periode']})\n"
        
        profil_candidat += f"\nCompétences:\n"
        profil_candidat += f"- Scientific AI: {infos.competences_scientific_ai}\n"
        profil_candidat += f"- Simulation: {infos.competences_simulation}\n"
        profil_candidat += f"- Generative AI: {infos.competences_generative_ai}\n"
        profil_candidat += f"- Informatique: {infos.competences_informatique}\n"
        
        prompt = PROMPT_TEMPLATE_TOPO.format(
            poste=analyse_annonce['poste'],
            entreprise=analyse_annonce['entreprise'],
            competences=', '.join(analyse_annonce.get('competences_cles', [])),
            mission=analyse_annonce.get('mission_principale', ''),
            annonce_text=annonce_text[:MAX_ANNONCE_LENGTH],
            profil_candidat=profil_candidat
        )
        
        response = self.client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=MAX_TOKENS_TOPO,
            temperature=TEMPERATURE,
            system=SYSTEM_PROMPT_TOPO,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.content[0].text.strip()
    
    def generer_questions_techniques(self, annonce_text: str, analyse_annonce: Dict, infos: InfosPersonnelles) -> str:
        """Génère des questions techniques d'entretien avec réponses"""
        
        # Préparer un résumé des expériences
        experiences_resume = ""
        for exp in infos.experiences[:2]:
            experiences_resume += f"- {exp['poste']} chez {exp['entreprise']}\n"
            for mission in exp['missions'][:3]:
                experiences_resume += f"  • {mission}\n"
        
        # Préparer les compétences
        competences_techniques = f"""
Scientific AI: {infos.competences_scientific_ai}
Simulation: {infos.competences_simulation}
Generative AI: {infos.competences_generative_ai}
Informatique: {infos.competences_informatique}
"""
        
        prompt = PROMPT_TEMPLATE_QUESTIONS_TECH.format(
            nb_questions=NB_QUESTIONS_TECHNIQUES,
            poste=analyse_annonce['poste'],
            entreprise=analyse_annonce['entreprise'],
            competences=', '.join(analyse_annonce.get('competences_cles', [])),
            annonce_text=annonce_text[:MAX_ANNONCE_LENGTH],
            experiences_resume=experiences_resume,
            competences_techniques=competences_techniques
        )
        
        response = self.client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=MAX_TOKENS_QUESTIONS_TECH,
            temperature=TEMPERATURE,
            system=SYSTEM_PROMPT_QUESTIONS_TECH,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.content[0].text.strip()
    
    def generer_questions_personnalite(self, annonce_text: str, analyse_annonce: Dict, infos: InfosPersonnelles) -> str:
        """Génère des questions de personnalité avec réponses STAR"""
        
        # Préparer un résumé des expériences
        experiences_resume = ""
        for exp in infos.experiences:
            experiences_resume += f"\n{exp['poste']} chez {exp['entreprise']} ({exp['periode']}):\n"
            for mission in exp['missions'][:2]:
                experiences_resume += f"- {mission}\n"
        
        prompt = PROMPT_TEMPLATE_QUESTIONS_PERSO.format(
            nb_questions=NB_QUESTIONS_PERSONNALITE,
            entreprise=analyse_annonce['entreprise'],
            poste=analyse_annonce['poste'],
            annonce_text=annonce_text[:MAX_ANNONCE_LENGTH],
            nom=infos.nom,
            experiences_resume=experiences_resume
        )
        
        response = self.client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=MAX_TOKENS_QUESTIONS_PERSO,
            temperature=TEMPERATURE,
            system=SYSTEM_PROMPT_QUESTIONS_PERSO,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.content[0].text.strip()


class GenerateurLaTeX:
    """Génère les fichiers LaTeX à partir des templates"""
    
    @staticmethod
    def get_bullet_symbol() -> str:
        """Retourne la commande LaTeX pour le bullet sélectionné"""
        bullets = {
            "blacksquare": r"$\blacksquare$",
            "bullet": r"$\bullet$",
            "diamond": r"$\diamond$",
            "triangleright": r"$\triangleright$",
            "circ": r"$\circ$",
            "star": r"$\star$",
            "checkmark": r"\checkmark",
            "rightarrow": r"$\rightarrow$",
            "dash": r"---"
        }
        return bullets.get(BULLET_STYLE, r"$\bullet$")
    
    @staticmethod
    def escape_latex(text: str) -> str:
        """Échappe les caractères spéciaux LaTeX"""
        replacements = {
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '~': r'\textasciitilde{}',
            '^': r'\textasciicircum{}',
        }
        for char, replacement in replacements.items():
            text = text.replace(char, replacement)
        return text
    
    @staticmethod
    def colorize_mission_title(mission_text: str) -> str:
        """Colore le titre des missions (texte avant ':') en bleu foncé"""
        # Si la coloration est désactivée, retourner le texte tel quel
        if not COLORIZE_MISSION_TITLES:
            return mission_text
        
        # Chercher le pattern "Titre : Description"
        if ' : ' in mission_text or ' :' in mission_text:
            # Séparer au premier ':'
            parts = mission_text.split(':', 1)
            if len(parts) == 2:
                title = parts[0].strip()
                description = parts[1].strip()
                # Colorer le titre en bleu foncé et le mettre en gras
                return f"\\textcolor{{darkblue}}{{\\textbf{{{title}}}}} : {description}"
        
        return mission_text
    
    @staticmethod
    def generer_cv(infos: InfosPersonnelles, profil_adapte: str, output_path: str):
        """Génère le CV LaTeX"""
        
        # Choisir le bon template selon la configuration
        if CV_TEMPLATE == "2colonnes":
            template_file = TEMPLATES_DIR / 'cv_template_2col.tex'
        else:
            template_file = TEMPLATES_DIR / 'cv_template.tex'
        
        # Lire le template
        with open(template_file, 'r', encoding='utf-8') as f:
            template = f.read()
        
        # Adapter le template selon le format choisi
        if CV_FORMAT == "1page":
            cv_margins = CV_MARGINS_1PAGE
            parskip = LATEX_PARSKIP_1PAGE
            header_spacing = HEADER_SPACING_1PAGE
            vspace_exp = VSPACE_BETWEEN_EXPERIENCES_1PAGE
            vspace_form = VSPACE_BETWEEN_FORMATIONS_1PAGE
            vspace_proj = VSPACE_BETWEEN_PROJETS_1PAGE
        else:  # 2pages
            cv_margins = CV_MARGINS_2PAGES
            parskip = LATEX_PARSKIP_2PAGES
            header_spacing = HEADER_SPACING_2PAGES
            vspace_exp = VSPACE_BETWEEN_EXPERIENCES_2PAGES
            vspace_form = VSPACE_BETWEEN_FORMATIONS_2PAGES
            vspace_proj = VSPACE_BETWEEN_PROJETS_2PAGES
        
        # Remplacer les paramètres dans le template
        template = template.replace('{CV_MARGINS}', cv_margins)
        template = template.replace('{PARSKIP}', parskip)
        template = template.replace('{HEADER_SPACING}', header_spacing)
        template = template.replace('{FONT_SIZE_BASE}', FONT_SIZE_BASE)
        template = template.replace('{FONT_SIZE_NAME}', FONT_SIZE_NAME)
        template = template.replace('{FONT_SIZE_TITLE}', FONT_SIZE_TITLE)
        template = template.replace('{FONT_SIZE_SECTION}', FONT_SIZE_SECTION)
        template = template.replace('{BULLET_SYMBOL}', GenerateurLaTeX.get_bullet_symbol())
        
        # Générer les sections avec les espacements appropriés
        experiences_tex = GenerateurLaTeX._generer_experiences(infos.experiences, vspace_exp)
        formations_tex = GenerateurLaTeX._generer_formations(infos.formations, vspace_form)
        certifications_tex = GenerateurLaTeX._generer_certifications(infos.certifications)
        projets_tex = GenerateurLaTeX._generer_projets(infos.projets, vspace_proj)
        langues_tex = GenerateurLaTeX._generer_langues(infos.langues)
        
        # Générer la section compétences selon le mode
        if MODE_PROFIL == "specifique":
            # Mode spécifique : utiliser les champs hardcodés
            competences_section = GenerateurLaTeX._generer_competences_specifique(infos)
        else:
            # Mode générique : utiliser la liste de compétences dynamique
            competences_section = GenerateurLaTeX._generer_competences_generique(infos.competences)
        
        # Remplacer les placeholders (en échappant les caractères spéciaux LaTeX)
        telephone = infos.telephone if infos.telephone and infos.telephone.strip() else '+33 X XX XX XX XX'
        replacements = {
            '{NOM}': GenerateurLaTeX.escape_latex(infos.nom),
            '{TITRE}': GenerateurLaTeX.escape_latex(infos.titre),
            '{LOCALISATION}': GenerateurLaTeX.escape_latex(infos.localisation),
            '{EMAIL}': infos.email,  # Email pas besoin d'échapper
            '{TELEPHONE}': telephone,
            '{LINKEDIN}': infos.linkedin,  # URL pas besoin d'échapper
            '{LINKEDIN_TEXT}': infos.linkedin.replace('https://', '').replace('http://', ''),
            '{PROFIL}': GenerateurLaTeX.escape_latex(profil_adapte),
            '{EXPERIENCES}': experiences_tex,  # Déjà échappé dans _generer_experiences
            '{FORMATIONS}': formations_tex,  # Déjà échappé dans _generer_formations
            '{CERTIFICATIONS}': certifications_tex,
            '{PROJETS}': projets_tex,
            '{COMPETENCES_SCIENTIFIC_AI}': GenerateurLaTeX.escape_latex(infos.competences_scientific_ai),
            '{COMPETENCES_SIMULATION}': GenerateurLaTeX.escape_latex(infos.competences_simulation),
            '{COMPETENCES_GENERATIVE_AI}': GenerateurLaTeX.escape_latex(infos.competences_generative_ai),
            '{COMPETENCES_INFORMATIQUE}': GenerateurLaTeX.escape_latex(infos.competences_informatique),
            '{COMPETENCES_SECTION}': competences_section,  # Section complète pour mode générique
            '{LANGUES}': langues_tex,
        }
        
        cv_content = template
        for key, value in replacements.items():
            cv_content = cv_content.replace(key, value)
        
        # Écrire le fichier
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(cv_content)
    
    @staticmethod
    def generer_lettre(infos: InfosPersonnelles, analyse_annonce: Dict, 
                       contenu_lettre: Dict, output_path: str):
        """Génère la lettre de motivation LaTeX"""
        
        # Lire le template
        template_file = TEMPLATES_DIR / 'lettre_motivation_template.tex'
        with open(template_file, 'r', encoding='utf-8') as f:
            template = f.read()
        
        # Date actuelle
        date_fr = datetime.now().strftime("%d/%m/%Y")
        
        # Remplacer les placeholders (en échappant les caractères spéciaux LaTeX)
        telephone = infos.telephone if infos.telephone and infos.telephone.strip() else '+33 X XX XX XX XX'
        replacements = {
            '{NOM}': GenerateurLaTeX.escape_latex(infos.nom),
            '{LOCALISATION}': GenerateurLaTeX.escape_latex(infos.localisation),
            '{EMAIL}': infos.email,
            '{TELEPHONE}': telephone,
            '{LINKEDIN}': infos.linkedin,
            '{ENTREPRISE}': GenerateurLaTeX.escape_latex(analyse_annonce.get('entreprise', 'Entreprise')),
            '{DATE}': date_fr,
            '{POSTE}': GenerateurLaTeX.escape_latex(analyse_annonce.get('poste', 'Poste')),
            '{PARAGRAPHE_1}': GenerateurLaTeX.escape_latex(contenu_lettre.get('paragraphe_1', '')),
            '{PARAGRAPHE_2}': GenerateurLaTeX.escape_latex(contenu_lettre.get('paragraphe_2', '')),
            '{PARAGRAPHE_3}': GenerateurLaTeX.escape_latex(contenu_lettre.get('paragraphe_3', '')),
            '{CONCLUSION}': GenerateurLaTeX.escape_latex(contenu_lettre.get('conclusion', '')),
        }
        
        lettre_content = template
        for key, value in replacements.items():
            lettre_content = lettre_content.replace(key, value)
        
        # Écrire le fichier
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(lettre_content)
    
    @staticmethod
    def _generer_experiences(experiences: List[Dict], vspace: str = "0.15cm") -> str:
        """Génère la section expériences"""
        tex = ""
        for i, exp in enumerate(experiences):
            poste = GenerateurLaTeX.escape_latex(exp['poste'])
            entreprise = GenerateurLaTeX.escape_latex(exp['entreprise'])
            periode = GenerateurLaTeX.escape_latex(exp['periode'])
            tex += f"\\cvitem{{{poste} -- {entreprise}}}{{{periode}}}\n"
            for mission in exp['missions']:
                mission_escaped = GenerateurLaTeX.escape_latex(mission)
                # Colorer le titre de la mission (avant ':') en bleu
                mission_colored = GenerateurLaTeX.colorize_mission_title(mission_escaped)
                tex += f"\\cvsubitem{{{mission_colored}}}\n"
            if i < len(experiences) - 1:
                tex += f"\n\\vspace{{{vspace}}}\n\n"
        return tex
    
    @staticmethod
    def _generer_formations(formations: List[Dict], vspace: str = "0.15cm") -> str:
        """Génère la section formations"""
        tex = ""
        for i, form in enumerate(formations):
            diplome = GenerateurLaTeX.escape_latex(form['diplome'])
            periode = GenerateurLaTeX.escape_latex(form['periode'])
            etablissement = GenerateurLaTeX.escape_latex(form['etablissement'])
            tex += f"\\cvitem{{{diplome}}}{{{periode}}}\n"
            tex += f"\\textit{{{etablissement}}}\n"
            for detail in form['details']:
                detail_escaped = GenerateurLaTeX.escape_latex(detail)
                tex += f"\\cvsubitem{{{detail_escaped}}}\n"
            if i < len(formations) - 1:
                tex += f"\n\\vspace{{{vspace}}}\n\n"
        return tex
    
    @staticmethod
    def _generer_certifications(certifications: List[Dict]) -> str:
        """Génère la section certifications"""
        if CV_TEMPLATE == "2colonnes":
            # Format compact pour 2 colonnes
            tex = ""
            for cert in certifications:
                titre = GenerateurLaTeX.escape_latex(cert['titre'])
                date = GenerateurLaTeX.escape_latex(cert['date'])
                tex += f"\\textbf{{{titre}}} \\\\\n{{\\small {date}}} \\\\[0.2cm]\n"
            return tex
        else:
            # Format classique
            tex = ""
            for cert in certifications:
                titre = GenerateurLaTeX.escape_latex(cert['titre'])
                date = GenerateurLaTeX.escape_latex(cert['date'])
                tex += f"\\cvitem{{{titre}}}{{{date}}}\n\n"
            return tex
    
    @staticmethod
    def _generer_projets(projets: List[Dict], vspace: str = "0.3cm") -> str:
        """Génère la section projets"""
        tex = ""
        for i, proj in enumerate(projets):
            titre = GenerateurLaTeX.escape_latex(proj['titre'])
            description = GenerateurLaTeX.escape_latex(proj['description'])
            competences = GenerateurLaTeX.escape_latex(proj['competences'])
            
            # Titre du projet
            tex += f"\\textbf{{{titre}}}\\\\\n"
            # Description
            tex += f"{description}\\\\\n"
            # Compétences (en italique et plus petit)
            tex += f"{{\\small \\textit{{Compétences :}} {competences}}}\n"
            
            if i < len(projets) - 1:
                tex += f"\n\\vspace{{{vspace}}}\n\n"
        return tex
    
    @staticmethod
    def _generer_langues(langues: List[Dict]) -> str:
        """Génère la section langues"""
        if CV_TEMPLATE == "2colonnes":
            # Format compact pour 2 colonnes
            tex = ""
            for lang in langues:
                langue = GenerateurLaTeX.escape_latex(lang['langue'])
                niveau = GenerateurLaTeX.escape_latex(lang['niveau'])
                tex += f"\\textbf{{{langue}}} \\\\\n{{\\small {niveau}}} \\\\[0.2cm]\n"
            return tex
        else:
            # Format classique
            tex = ""
            for lang in langues:
                langue = GenerateurLaTeX.escape_latex(lang['langue'])
                niveau = GenerateurLaTeX.escape_latex(lang['niveau'])
                tex += f"{langue} : {niveau} \\\\\n"
            return tex
    
    @staticmethod
    def _generer_competences_specifique(infos: InfosPersonnelles) -> str:
        """Génère la section compétences en mode spécifique (catégories hardcodées)"""
        # Cette section sera remplacée directement dans le template
        # via les placeholders individuels
        return ""
    
    @staticmethod
    def _generer_competences_generique(competences: List[Dict]) -> str:
        """Génère la section compétences en mode générique (catégories dynamiques)"""
        if not competences:
            return "\\textit{Aucune compétence listée}"
        
        tex = ""
        for i, comp in enumerate(competences):
            categorie = GenerateurLaTeX.escape_latex(comp['categorie'])
            contenu = GenerateurLaTeX.escape_latex(comp['contenu'])
            
            if CV_TEMPLATE == "2colonnes":
                # Format compact pour 2 colonnes
                tex += f"\\skillgroup{{{categorie}}}{{{contenu}}}\n"
            else:
                # Format classique
                tex += f"\\textbf{{{categorie} :}}\n{contenu}\n\n"
        
        return tex


class CompillateurPDF:
    """Compile les fichiers LaTeX en PDF"""
    
    @staticmethod
    def compiler(tex_file: str) -> bool:
        """Compile un fichier .tex en PDF"""
        try:
            # Utiliser le chemin complet de pdflatex
            pdflatex_path = "/Library/TeX/texbin/pdflatex"
            
            # Compiler N fois pour les références (défini dans config.py)
            for _ in range(LATEX_COMPILE_PASSES):
                result = subprocess.run(
                    [pdflatex_path, "-interaction=nonstopmode", tex_file],
                    capture_output=True,
                    text=True,
                    cwd=os.path.dirname(tex_file) or '.'
                )
                
                if result.returncode != 0 and DEBUG_MODE:
                    print(f"Erreur lors de la compilation de {tex_file}")
                    print(result.stdout)
                    return False
            
            print(f"✓ {tex_file} compilé avec succès")
            return True
            
        except Exception as e:
            print(f"Erreur: {e}")
            return False


def main():
    """Fonction principale"""
    
    print("=" * 60)
    print("  GÉNÉRATEUR AUTOMATIQUE DE CV ET LETTRE DE MOTIVATION")
    print("=" * 60)
    print()
    
    # 1. Vérifier la clé API
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ Erreur: La variable d'environnement ANTHROPIC_API_KEY n'est pas définie")
        print("   Vérifiez votre fichier .env ou exportez: export ANTHROPIC_API_KEY='votre-clé'")
        sys.exit(1)
    
    # 2. Déterminer le mode : annonce ou candidature spontanée
    mode = MODE_GENERATION
    
    # Si un argument "--spontanee" est passé, passer en mode spontané
    if len(sys.argv) > 1 and sys.argv[1] == "--spontanee":
        mode = "spontanee"
        if len(sys.argv) > 2:
            url_input = sys.argv[2]
        else:
            url_input = input("URL du site web de l'entreprise: ").strip()
        if len(sys.argv) > 3:
            poste_cible = sys.argv[3]
        else:
            poste_cible = input(f"Poste visé (défaut: {POSTE_CIBLE_SPONTANEE}): ").strip() or POSTE_CIBLE_SPONTANEE
    else:
        # Mode annonce
        if len(sys.argv) > 1 and sys.argv[1] != "--spontanee":
            url_input = sys.argv[1]
        else:
            url_input = input("URL de l'annonce de poste: ").strip()
        poste_cible = None
    
    if not url_input:
        print("❌ URL requise")
        sys.exit(1)
    
    # Afficher le mode
    if mode == "spontanee":
        print(f"📌 Mode: Candidature spontanée")
        print(f"🎯 Poste cible: {poste_cible}")
        print()
    else:
        print(f"📌 Mode: Réponse à une annonce")
        print()
    
    print()
    print(MSG_CHARGEMENT_INFOS)
    
    # 3. Charger les informations statiques
    infos = ParseurInfosStatiques.parse('infos_statique.txt')
    print(f"   ✓ Informations de {infos.nom} chargées")
    
    # 4. Scraper le contenu (annonce ou site web)
    print()
    if mode == "spontanee":
        print("🔍 Scraping du site web de l'entreprise...")
    else:
        print(MSG_SCRAPING)
    
    scraper = ScraperAnnonce()
    contenu_text = scraper.scraper(url_input)
    
    if not contenu_text:
        print(f"❌ Impossible de scraper {'le site web' if mode == 'spontanee' else 'l\'annonce'}")
        sys.exit(1)
    
    print(f"   ✓ Contenu récupéré ({len(contenu_text)} caractères)")
    
    # 5. Analyser avec l'IA
    print()
    ia = GenerateurIA(api_key)
    
    if mode == "spontanee":
        print(f"🤖 Analyse de l'entreprise avec Claude ({CLAUDE_MODEL})...")
        analyse = ia.analyser_entreprise(contenu_text, poste_cible)
        print(f"   ✓ Entreprise: {analyse['entreprise']}")
        print(f"   ✓ Secteur: {analyse.get('secteur', 'N/A')}")
        print(f"   ✓ Poste visé: {analyse['poste']}")
    else:
        print(MSG_ANALYSE_IA.format(model=CLAUDE_MODEL))
        analyse = ia.analyser_annonce(contenu_text)
        print(f"   ✓ Poste: {analyse['poste']}")
        print(f"   ✓ Entreprise: {analyse['entreprise']}")
    
    # 6. Générer le profil adapté
    print()
    print(MSG_GENERATION_PROFIL)
    if mode == "spontanee":
        profil_adapte = ia.generer_profil_adapte_spontanee(infos.profil_defaut, analyse, infos)
    else:
        profil_adapte = ia.generer_profil_adapte(infos.profil_defaut, analyse, infos)
    print("   ✓ Profil personnalisé généré")
    
    # 7. Générer la lettre de motivation
    print()
    print(MSG_GENERATION_LETTRE)
    if mode == "spontanee":
        contenu_lettre = ia.generer_lettre_motivation_spontanee(infos, analyse)
    else:
        contenu_lettre = ia.generer_lettre_motivation(infos, analyse)
    print("   ✓ Lettre de motivation générée")
    
    # 7b. Générer le topo de préparation d'entretien
    print()
    print("📚 Génération du topo de préparation d'entretien...")
    topo_entretien = ia.generer_topo_entretien(contenu_text, analyse, infos)
    print("   ✓ Topo d'entretien généré")
    
    # 7c. Générer les questions techniques
    print()
    print(f"🔧 Génération de {NB_QUESTIONS_TECHNIQUES} questions techniques...")
    questions_techniques = ia.generer_questions_techniques(contenu_text, analyse, infos)
    print("   ✓ Questions techniques générées")
    
    # 7d. Générer les questions de personnalité
    print()
    print(f"💭 Génération de {NB_QUESTIONS_PERSONNALITE} questions de personnalité...")
    questions_personnalite = ia.generer_questions_personnalite(contenu_text, analyse, infos)
    print("   ✓ Questions de personnalité générées")
    
    # 8. Créer le dossier de candidature
    print()
    print(MSG_CREATION_DOSSIER)
    
    # Nom du dossier : Poste_Entreprise_Date
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    poste_clean = re.sub(r'[^a-zA-Z0-9]', '_', analyse['poste'])[:30]
    entreprise_clean = re.sub(r'[^a-zA-Z0-9]', '_', analyse['entreprise'])[:20]
    
    folder_name = f"{poste_clean}_{entreprise_clean}_{timestamp}"
    folder_path_obj = ROOT_DIR / OUTPUT_FOLDER / folder_name
    
    # Créer le dossier
    folder_path_obj.mkdir(parents=True, exist_ok=True)
    folder_path = str(folder_path_obj)  # Convertir en string pour compatibilité
    print(f"   ✓ Dossier créé: {OUTPUT_FOLDER}/{folder_name}/")
    
    # 9. Créer les fichiers LaTeX dans le dossier
    print()
    print(MSG_CREATION_LATEX)
    
    cv_filename = os.path.join(folder_path, FILENAME_CV)
    lettre_filename = os.path.join(folder_path, FILENAME_LETTRE)
    
    GenerateurLaTeX.generer_cv(infos, profil_adapte, cv_filename)
    print(f"   ✓ {FILENAME_CV} créé")
    
    GenerateurLaTeX.generer_lettre(infos, analyse, contenu_lettre, lettre_filename)
    print(f"   ✓ {FILENAME_LETTRE} créé")
    
    # 10. Sauvegarder le contenu original (annonce ou site web)
    if mode == "spontanee":
        source_filename = os.path.join(folder_path, "site_entreprise_original.txt")
        titre_source = "SITE WEB DE L'ENTREPRISE"
    else:
        source_filename = os.path.join(folder_path, FILENAME_ANNONCE)
        titre_source = "ANNONCE ORIGINALE"
    
    with open(source_filename, 'w', encoding='utf-8') as f:
        f.write(f"Type: {'Candidature spontanée' if mode == 'spontanee' else 'Réponse à annonce'}\n")
        f.write(f"URL: {url_input}\n")
        f.write(f"Date de scraping: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        f.write("=" * 60 + "\n\n")
        f.write(contenu_text)
    print(f"   ✓ {titre_source.lower()} sauvegardée")
    
    # 11. Sauvegarder l'analyse
    analyse_filename = os.path.join(folder_path, FILENAME_ANALYSE)
    with open(analyse_filename, 'w', encoding='utf-8') as f:
        f.write(f"Type: {'Candidature spontanée' if mode == 'spontanee' else 'Réponse à annonce'}\n")
        f.write(f"Poste: {analyse['poste']}\n")
        f.write(f"Entreprise: {analyse['entreprise']}\n")
        
        if mode == "spontanee":
            f.write(f"Secteur: {analyse.get('secteur', 'N/A')}\n\n")
            f.write("Activités principales:\n")
            for act in analyse.get('activites_principales', []):
                f.write(f"  - {act}\n")
            f.write(f"\nValeurs: {analyse.get('valeurs', 'N/A')}\n")
            f.write(f"Technologies: {analyse.get('technologies', 'N/A')}\n")
            f.write(f"Besoins potentiels: {analyse.get('besoins_potentiels', 'N/A')}\n")
        else:
            f.write(f"Mission principale: {analyse.get('mission_principale', 'N/A')}\n\n")
            f.write("Compétences clés:\n")
            for comp in analyse.get('competences_cles', []):
                f.write(f"  - {comp}\n")
        
        f.write(f"\nMots-clés: {analyse.get('mots_cles', 'N/A')}\n")
    print(f"   ✓ {FILENAME_ANALYSE} sauvegardée")
    
    # 11b. Sauvegarder le topo d'entretien
    topo_filename = os.path.join(folder_path, "preparation_entretien.txt")
    with open(topo_filename, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("  PRÉPARATION D'ENTRETIEN\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Type: {'Candidature spontanée' if mode == 'spontanee' else 'Réponse à annonce'}\n")
        f.write(f"Poste: {analyse['poste']}\n")
        f.write(f"Entreprise: {analyse['entreprise']}\n")
        f.write(f"Date de génération: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        f.write("\n" + "=" * 80 + "\n\n")
        f.write(topo_entretien)
    print(f"   ✓ preparation_entretien.txt sauvegardée")
    
    # 11c. Sauvegarder les questions techniques
    questions_tech_filename = os.path.join(folder_path, "questions_techniques.txt")
    with open(questions_tech_filename, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write(f"  QUESTIONS TECHNIQUES D'ENTRETIEN ({NB_QUESTIONS_TECHNIQUES} questions)\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Type: {'Candidature spontanée' if mode == 'spontanee' else 'Réponse à annonce'}\n")
        f.write(f"Poste: {analyse['poste']}\n")
        f.write(f"Entreprise: {analyse['entreprise']}\n")
        f.write(f"Date de génération: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        f.write("\n" + "=" * 80 + "\n\n")
        f.write(questions_techniques)
    print(f"   ✓ questions_techniques.txt sauvegardée")
    
    # 11d. Sauvegarder les questions de personnalité
    questions_perso_filename = os.path.join(folder_path, "questions_personnalite.txt")
    with open(questions_perso_filename, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write(f"  QUESTIONS DE PERSONNALITÉ ({NB_QUESTIONS_PERSONNALITE} questions)\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Type: {'Candidature spontanée' if mode == 'spontanee' else 'Réponse à annonce'}\n")
        f.write(f"Poste: {analyse['poste']}\n")
        f.write(f"Entreprise: {analyse['entreprise']}\n")
        f.write(f"Date de génération: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        f.write("\n" + "=" * 80 + "\n\n")
        f.write(questions_personnalite)
    print(f"   ✓ questions_personnalite.txt sauvegardée")
    
    # 12. Compiler en PDF
    if AUTO_COMPILE_PDF:
        print()
        print(MSG_COMPILATION)
        
        CompillateurPDF.compiler(cv_filename)
        CompillateurPDF.compiler(lettre_filename)
    
    # 13. Fin
    print()
    print("=" * 60)
    print("✅ GÉNÉRATION TERMINÉE AVEC SUCCÈS!")
    print("=" * 60)
    print()
    if mode == "spontanee":
        print(f"📌 Type: Candidature spontanée")
        print(f"🎯 Poste visé: {analyse['poste']}")
    else:
        print(f"📌 Type: Réponse à annonce")
    print()
    print(f"📂 Tous les fichiers sont dans:")
    print(f"   {folder_path}/")
    print()
    print(f"📄 Fichiers générés:")
    print(f"   CV & Lettre de motivation:")
    print(f"      ✓ cv.pdf")
    print(f"      ✓ lettre_motivation.pdf")
    print(f"   Préparation d'entretien:")
    print(f"      ✓ preparation_entretien.txt")
    print(f"      ✓ questions_techniques.txt ({NB_QUESTIONS_TECHNIQUES} questions avec réponses)")
    print(f"      ✓ questions_personnalite.txt ({NB_QUESTIONS_PERSONNALITE} questions STAR)")
    print(f"   Informations de référence:")
    if mode == "spontanee":
        print(f"      ✓ site_entreprise_original.txt")
    else:
        print(f"      ✓ annonce_originale.txt")
    print(f"      ✓ analyse_poste.txt")
    print()


if __name__ == "__main__":
    main()

