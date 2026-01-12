#!/bin/bash
# Script d'installation de Playwright pour scraper WTTJ

echo "============================================================"
echo "  INSTALLATION DE PLAYWRIGHT POUR SCRAPER WTTJ"
echo "============================================================"
echo ""

# Activer l'environnement virtuel
source venv/bin/activate

# Installer Playwright
echo "📦 Installation de Playwright..."
pip install playwright

# Installer le navigateur Chromium
echo "🌐 Installation de Chromium..."
playwright install chromium

echo ""
echo "✅ Installation terminée!"
echo ""
echo "💡 Test rapide:"
echo "   python3 wttj_playwright_scraper.py"
echo ""
