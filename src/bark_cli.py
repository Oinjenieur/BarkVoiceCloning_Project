#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import sys
from pathlib import Path

# Ajouter le répertoire parent au chemin
sys.path.append(str(Path(__file__).parent.parent))

# Importer notre module StandaloneBark
from src.standalone_bark import StandaloneBark

def main():
    """Interface en ligne de commande pour Bark"""
    parser = argparse.ArgumentParser(
        description="Clonage vocal offline avec Bark",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "--ref", 
        required=True, 
        help="Chemin vers l'audio de référence"
    )
    
    parser.add_argument(
        "--text", 
        required=True, 
        help="Texte à synthétiser"
    )
    
    parser.add_argument(
        "--lang", 
        default="fr", 
        help="Code langue (fr, en, es, de, etc.)"
    )
    
    parser.add_argument(
        "--output", 
        default=None, 
        help="Nom du fichier de sortie"
    )
    
    parser.add_argument(
        "--model-dir", 
        default=None, 
        help="Répertoire des modèles"
    )
    
    # Options spécifiques à Bark
    parser.add_argument(
        "--laughter", 
        action="store_true",
        help="Ajouter des rires aléatoires"
    )
    
    parser.add_argument(
        "--breathing", 
        action="store_true",
        help="Ajouter des respirations aléatoires"
    )
    
    parser.add_argument(
        "--emotion", 
        choices=["neutral", "happy", "sad", "angry", "excited", "concerned"],
        default=None,
        help="Ajouter une émotion spécifique"
    )
    
    args = parser.parse_args()
    
    # Vérifier que l'audio de référence existe
    if not os.path.exists(args.ref):
        print(f"Erreur: Le fichier audio '{args.ref}' n'existe pas.")
        sys.exit(1)
    
    # Initialiser Bark
    try:
        print("Initialisation de Bark...")
        bark = StandaloneBark(model_dir=args.model_dir)
        
        # Cloner la voix
        print(f"Clonage de la voix depuis '{args.ref}'...")
        
        # Si des effets sont demandés, utiliser la méthode avec effets
        if args.laughter or args.breathing or args.emotion:
            fichier_sortie = bark.generate_with_effects(
                args.ref, 
                args.text, 
                output_file=args.output,
                language=args.lang,
                add_laughter=args.laughter,
                add_breathing=args.breathing,
                emotion=args.emotion
            )
        else:
            # Sinon utiliser la méthode standard
            fichier_sortie = bark.clone_voice(
                args.ref, 
                args.text, 
                output_file=args.output,
                language=args.lang
            )
        
        if fichier_sortie:
            print(f"Audio généré avec succès: {fichier_sortie}")
        else:
            print("Échec de la génération audio.")
            sys.exit(1)
            
    except Exception as e:
        print(f"Erreur lors de l'exécution: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 