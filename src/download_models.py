#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path
import subprocess
import tempfile
import shutil

def download_models(output_dir=None):
    """
    Télécharge les modèles Bark
    
    Args:
        output_dir: Répertoire où stocker les modèles
    """
    # Répertoire des modèles par défaut
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / "models"
    else:
        output_dir = Path(output_dir)
    
    # Créer le répertoire s'il n'existe pas
    os.makedirs(output_dir, exist_ok=True)
    print(f"Les modèles seront téléchargés dans: {output_dir}")
    
    # Définir la variable d'environnement pour le répertoire des modèles
    os.environ["BARK_MODEL_DIR"] = str(output_dir)
    
    try:
        # Importer Bark pour télécharger les modèles
        from bark import preload_models
        print("Téléchargement des modèles Bark en cours...")
        preload_models()
        print("Modèles téléchargés avec succès!")
        return output_dir
    
    except ImportError:
        print("Bark n'est pas installé. Installation en cours...")
        
        # Installer Bark si nécessaire
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                "git+https://github.com/suno-ai/bark.git"
            ])
            print("Bark installé avec succès.")
            
            # Réessayer le téléchargement après installation
            from bark import preload_models
            print("Téléchargement des modèles Bark en cours...")
            preload_models()
            print("Modèles téléchargés avec succès!")
            return output_dir
            
        except Exception as e:
            print(f"Erreur lors de l'installation/téléchargement des modèles: {e}")
            return None
    
    except Exception as e:
        print(f"Erreur lors du téléchargement des modèles: {e}")
        return None

def main():
    """Fonction principale pour l'exécution en ligne de commande"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Télécharge les modèles nécessaires pour Bark"
    )
    
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Répertoire de sortie pour les modèles"
    )
    
    args = parser.parse_args()
    download_models(args.output_dir)

if __name__ == "__main__":
    main() 