#!/usr/bin/env python3
"""
Génération en batch depuis un fichier d'URLs
Solution pragmatique pour traiter des offres de n'importe quelle plateforme
"""

import os
import sys
import time
import subprocess
from pathlib import Path


def lire_urls(fichier: str) -> list:
    """Lit les URLs depuis un fichier texte"""
    urls = []
    
    if not os.path.exists(fichier):
        print(f"❌ Fichier non trouvé: {fichier}")
        return urls
    
    with open(fichier, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Ignorer les lignes vides et commentaires
            if line and not line.startswith('#'):
                if line.startswith('http'):
                    urls.append(line)
    
    return urls


def generer_pour_url(url: str, index: int, total: int) -> bool:
    """Génère CV/LM pour une URL"""
    print(f"\n{'='*80}")
    print(f"📄 [{index}/{total}] Traitement de l'offre")
    print(f"🔗 {url}")
    print(f"{'='*80}\n")
    
    try:
        cmd = ['python3', 'generateur_cv_lettre.py', url]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Génération réussie!")
            return True
        else:
            print(f"❌ Erreur lors de la génération")
            if result.stderr:
                print(f"   {result.stderr[:200]}")
            return False
    
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False


def main():
    print("="*80)
    print("  GÉNÉRATION EN BATCH DEPUIS FICHIER D'URLs")
    print("="*80)
    print()
    
    # Déterminer le fichier d'URLs
    if len(sys.argv) > 1:
        fichier_urls = sys.argv[1]
    else:
        fichier_urls = "urls_a_traiter.txt"
    
    print(f"📁 Fichier d'URLs: {fichier_urls}")
    print()
    
    # Lire les URLs
    urls = lire_urls(fichier_urls)
    
    if not urls:
        print("❌ Aucune URL trouvée dans le fichier")
        print()
        print("💡 Format du fichier:")
        print("   # Commentaire (lignes commençant par #)")
        print("   https://www.linkedin.com/jobs/view/123456")
        print("   https://www.welcometothejungle.com/fr/companies/xxx/jobs/yyy")
        print("   https://www.apec.fr/candidat/offres-emploi.html?id=zzz")
        print()
        sys.exit(1)
    
    print(f"✅ {len(urls)} URL(s) trouvée(s)")
    print()
    
    # Confirmation
    print("⚠️  La génération en batch va:")
    print(f"   - Traiter {len(urls)} offres")
    print(f"   - Appeler l'API Claude ~{len(urls) * 4} fois")
    print(f"   - Prendre environ {len(urls) * 2} minutes")
    print(f"   - Coûter environ {len(urls) * 0.20}€")
    print()
    
    confirmation = input("Confirmer? (oui/non): ").strip().lower()
    
    if confirmation not in ['oui', 'o', 'yes', 'y']:
        print("\n❌ Génération annulée")
        sys.exit(0)
    
    # Générer pour chaque URL
    resultats = []
    
    for i, url in enumerate(urls, 1):
        success = generer_pour_url(url, i, len(urls))
        resultats.append({'url': url, 'success': success})
        
        # Pause entre les générations
        if i < len(urls):
            print(f"\n⏱️  Pause de 3 secondes...")
            time.sleep(3)
    
    # Résumé
    print("\n" + "="*80)
    print("  RÉSUMÉ GÉNÉRATION EN BATCH")
    print("="*80)
    print()
    
    reussies = sum(1 for r in resultats if r['success'])
    echouees = len(resultats) - reussies
    
    print(f"✅ Réussies: {reussies}/{len(resultats)}")
    print(f"❌ Échouées: {echouees}/{len(resultats)}")
    
    if echouees > 0:
        print("\n❌ URLs échouées:")
        for r in resultats:
            if not r['success']:
                print(f"   - {r['url']}")
    
    print()
    print(f"📂 Tous les dossiers sont dans: ./candidatures/")
    print()


if __name__ == "__main__":
    main()
