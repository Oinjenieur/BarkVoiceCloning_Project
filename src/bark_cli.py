#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import logging
import json
from pathlib import Path

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Ajouter le répertoire parent au chemin
sys.path.append(str(Path(__file__).parent.parent))

# Importer notre module StandaloneBark
from src.standalone_bark import StandaloneBark

def extract_command(args):
    """Commande pour extraire l'identité vocale d'un fichier audio."""
    try:
        bark = StandaloneBark(model_dir=args.model_dir)
        speaker_id = bark.extract_speaker(
            audio_file=args.audio,
            speaker_id=args.speaker_id
        )
        logger.info(f"Identité vocale extraite avec succès: {speaker_id}")
    except Exception as e:
        logger.error(f"Erreur lors de l'extraction: {e}")
        sys.exit(1)

def generate_command(args):
    """Commande pour générer de l'audio à partir d'un texte."""
    try:
        bark = StandaloneBark(model_dir=args.model_dir)
        output_file = bark.clone_voice(
            text=args.text,
            speaker_id=args.speaker_id,
            audio_file=args.audio,
            output_file=args.output,
            language=args.language,
            temperature=args.temperature
        )
        logger.info(f"Audio généré avec succès: {output_file}")
    except Exception as e:
        logger.error(f"Erreur lors de la génération: {e}")
        sys.exit(1)

def emotion_command(args):
    """Commande pour générer de l'audio avec une émotion spécifiée."""
    try:
        bark = StandaloneBark(model_dir=args.model_dir)
        output_file = bark.generate_voice_with_emotion(
            text=args.text,
            speaker_id=args.speaker_id,
            audio_file=args.audio,
            output_file=args.output,
            language=args.language,
            emotion=args.emotion,
            temperature=args.temperature
        )
        logger.info(f"Audio généré avec succès: {output_file}")
    except Exception as e:
        logger.error(f"Erreur lors de la génération avec émotion: {e}")
        sys.exit(1)

def multilingual_command(args):
    """Commande pour générer de l'audio dans plusieurs langues."""
    try:
        # Charger le fichier JSON contenant les textes
        with open(args.texts_file, 'r', encoding='utf-8') as f:
            texts = json.load(f)
        
        bark = StandaloneBark(model_dir=args.model_dir)
        
        # Créer le répertoire de sortie s'il n'existe pas
        output_dir = args.output_dir or os.path.join(os.getcwd(), "generated_audio")
        os.makedirs(output_dir, exist_ok=True)
        
        # Générer l'audio pour chaque langue
        for lang, text in texts.items():
            output_file = os.path.join(output_dir, f"generated_{lang}.wav")
            logger.info(f"Génération audio pour la langue: {lang}")
            
            bark.clone_voice(
                text=text,
                speaker_id=args.speaker_id,
                audio_file=args.audio,
                output_file=output_file,
                language=lang,
                temperature=args.temperature
            )
            
            logger.info(f"Audio généré pour {lang}: {output_file}")
            
        logger.info(f"Génération multilingue terminée. Fichiers sauvegardés dans: {output_dir}")
        
    except Exception as e:
        logger.error(f"Erreur lors de la génération multilingue: {e}")
        sys.exit(1)

def main():
    """Fonction principale pour l'interface en ligne de commande."""
    
    # Créer le parseur principal
    parser = argparse.ArgumentParser(
        description="Bark Voice Cloning - Interface en ligne de commande"
    )
    subparsers = parser.add_subparsers(dest="command", help="Commande à exécuter")
    
    # Sous-commande pour extraire l'identité vocale
    extract_parser = subparsers.add_parser("extract", help="Extraire l'identité vocale d'un fichier audio")
    extract_parser.add_argument("--audio", required=True, help="Fichier audio de référence")
    extract_parser.add_argument("--speaker-id", help="Identifiant du locuteur (optionnel)")
    extract_parser.add_argument("--model-dir", help="Répertoire des modèles (optionnel)")
    
    # Sous-commande pour générer de l'audio
    generate_parser = subparsers.add_parser("generate", help="Générer de l'audio à partir d'un texte")
    generate_parser.add_argument("--text", required=True, help="Texte à prononcer")
    generate_parser.add_argument("--speaker-id", help="Identifiant du locuteur (optionnel)")
    generate_parser.add_argument("--audio", help="Fichier audio de référence (alternative à speaker-id)")
    generate_parser.add_argument("--output", help="Fichier de sortie (optionnel)")
    generate_parser.add_argument("--language", default="en", help="Code de langue (en, fr, etc.)")
    generate_parser.add_argument("--temperature", type=float, default=0.7, help="Température (0.5-1.0)")
    generate_parser.add_argument("--model-dir", help="Répertoire des modèles (optionnel)")
    
    # Sous-commande pour générer de l'audio avec émotion
    emotion_parser = subparsers.add_parser("emotion", help="Générer de l'audio avec une émotion spécifiée")
    emotion_parser.add_argument("--text", required=True, help="Texte à prononcer")
    emotion_parser.add_argument("--speaker-id", help="Identifiant du locuteur (optionnel)")
    emotion_parser.add_argument("--audio", help="Fichier audio de référence (alternative à speaker-id)")
    emotion_parser.add_argument("--output", help="Fichier de sortie (optionnel)")
    emotion_parser.add_argument("--language", default="en", help="Code de langue (en, fr, etc.)")
    emotion_parser.add_argument("--emotion", required=True, choices=["neutral", "happy", "sad", "angry", "surprised"], 
                            help="Émotion à exprimer")
    emotion_parser.add_argument("--temperature", type=float, default=0.7, help="Température (0.5-1.0)")
    emotion_parser.add_argument("--model-dir", help="Répertoire des modèles (optionnel)")
    
    # Sous-commande pour la génération multilingue
    multilingual_parser = subparsers.add_parser("multilingual", help="Générer de l'audio dans plusieurs langues")
    multilingual_parser.add_argument("--texts-file", required=True, help="Fichier JSON contenant les textes par langue")
    multilingual_parser.add_argument("--speaker-id", help="Identifiant du locuteur (optionnel)")
    multilingual_parser.add_argument("--audio", help="Fichier audio de référence (alternative à speaker-id)")
    multilingual_parser.add_argument("--output-dir", help="Répertoire de sortie (optionnel)")
    multilingual_parser.add_argument("--temperature", type=float, default=0.7, help="Température (0.5-1.0)")
    multilingual_parser.add_argument("--model-dir", help="Répertoire des modèles (optionnel)")
    
    # Analyser les arguments
    args = parser.parse_args()
    
    # Exécuter la commande appropriée
    if args.command == "extract":
        extract_command(args)
    elif args.command == "generate":
        generate_command(args)
    elif args.command == "emotion":
        emotion_command(args)
    elif args.command == "multilingual":
        multilingual_command(args)
    else:
        parser.print_help()
        
if __name__ == "__main__":
    main() 