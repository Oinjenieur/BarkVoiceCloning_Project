#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import logging
import subprocess
import argparse
import shutil
from pathlib import Path

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def download_bark_models(output_dir=None):
    """
    Télécharge les modèles nécessaires pour Bark Voice Cloning.
    
    Args:
        output_dir: Répertoire de sortie pour les modèles
    """
    # Définir le répertoire de sortie par défaut si non fourni
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
    
    # S'assurer que les répertoires existent
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, "speaker_embeddings"), exist_ok=True)
    
    logger.info(f"Téléchargement des modèles Bark dans: {output_dir}")
    
    # Définir la variable d'environnement pour le répertoire des modèles
    os.environ["BARK_MODEL_DIR"] = str(output_dir)
    
    try:
        # Importer et précharger les modèles Bark
        logger.info("Téléchargement des modèles Bark...")
        try:
            from bark import preload_models
            preload_models()
            logger.info("Modèles Bark téléchargés avec succès")
        except ImportError:
            logger.error("Bark n'est pas installé. Installez-le d'abord avec 'pip install git+https://github.com/suno-ai/bark.git'")
            return False
        
        logger.info("Téléchargement des données NLTK...")
        download_nltk_data()
        
        return True
    except Exception as e:
        logger.error(f"Erreur lors du téléchargement des modèles: {e}")
        return False

def download_nltk_data():
    """Télécharge les données NLTK nécessaires pour Bark."""
    try:
        import nltk
        nltk.download('punkt')
        logger.info("Données NLTK téléchargées avec succès")
    except Exception as e:
        logger.error(f"Erreur lors du téléchargement des données NLTK: {e}")

def ensure_bark_installed():
    """S'assure que Bark est installé, sinon tente de l'installer."""
    try:
        import bark
        logger.info("Bark est déjà installé")
        return True
    except ImportError:
        logger.warning("Bark n'est pas installé, tentative d'installation...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                "git+https://github.com/suno-ai/bark.git"
            ])
            logger.info("Bark a été installé avec succès")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Erreur lors de l'installation de Bark: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description="Télécharge les modèles pour Bark Voice Cloning")
    parser.add_argument(
        "--output-dir", 
        type=str, 
        help="Répertoire de sortie pour les modèles"
    )
    
    args = parser.parse_args()
    
    # S'assurer que Bark est installé
    if not ensure_bark_installed():
        logger.error("Impossible d'installer Bark. Vérifiez votre connexion internet et les permissions.")
        sys.exit(1)
        
    # Télécharger les modèles
    success = download_bark_models(args.output_dir)
    
    if success:
        logger.info("Tous les modèles ont été téléchargés avec succès")
    else:
        logger.error("Des erreurs se sont produites lors du téléchargement des modèles")
        sys.exit(1)

if __name__ == "__main__":
    main() 