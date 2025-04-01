import torch
import numpy as np
import os
import soundfile as sf
from pathlib import Path
import sys

# Imports spécifiques à Bark
try:
    from bark import SAMPLE_RATE, generate_audio, preload_models
    from bark.generation import generate_text_semantic, generate_voice
except ImportError:
    print("Bark n'est pas installé. Installez-le avec 'pip install -r requirements.txt'")
    sys.exit(1)

class StandaloneBark:
    def __init__(self, model_dir=None):
        """
        Initialise le système de clonage vocal Bark
        
        Args:
            model_dir: Chemin vers le répertoire des modèles (optionnel)
        """
        # Configurer le répertoire des modèles si fourni
        if model_dir:
            os.environ["BARK_MODEL_DIR"] = str(Path(model_dir))
        
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Initialisation de Bark sur {self.device}...")
        
        # Précharger les modèles
        try:
            preload_models()
            print("Modèles Bark chargés avec succès")
        except Exception as e:
            print(f"Erreur lors du chargement des modèles: {e}")
            sys.exit(1)
    
    def clone_voice(self, reference_audio, text, output_file=None, language="fr"):
        """
        Clone une voix à partir d'un fichier audio de référence
        
        Args:
            reference_audio: Chemin vers le fichier audio de référence
            text: Texte à synthétiser
            output_file: Chemin du fichier de sortie (optionnel)
            language: Code de langue (auto, en, fr, de, etc.)
        """
        print(f"Clonage de voix en cours pour: {text}")
        
        # Adaptation pour les langues
        if language != "en":
            # Ajouter préfixe de langue pour le multilingue
            text = f"[{language.upper()}]{text}"
            
        try:
            # Générer l'audio
            audio_array = generate_audio(
                text,
                history_prompt=reference_audio,
                output_full=True
            )
            
            # Générer un nom de fichier de sortie si non spécifié
            if output_file is None:
                base_name = os.path.basename(reference_audio).split('.')[0]
                output_file = f"output_{base_name}_{language}.wav"
            
            # Enregistrer l'audio généré
            sf.write(output_file, audio_array, SAMPLE_RATE)
            print(f"Audio généré avec succès: {output_file}")
            
            return output_file
        except Exception as e:
            print(f"Erreur lors du clonage vocal: {e}")
            return None
    
    def languages_supported(self):
        """Liste des langues supportées par Bark"""
        return [
            "en",  # Anglais
            "zh",  # Chinois
            "fr",  # Français
            "de",  # Allemand
            "it",  # Italien
            "ja",  # Japonais
            "ko",  # Coréen
            "pl",  # Polonais
            "pt",  # Portugais
            "ru",  # Russe
            "es",  # Espagnol
            "tr",  # Turc
        ]
        
    def generate_with_effects(self, reference_audio, text, output_file=None, language="fr", 
                             add_laughter=False, add_breathing=False, emotion=None):
        """
        Génère du texte avec des effets spéciaux (rires, respirations, émotions)
        
        Args:
            reference_audio: Chemin vers l'audio de référence
            text: Texte à synthétiser
            output_file: Chemin du fichier de sortie (optionnel)
            language: Code de langue
            add_laughter: Ajouter des rires (sous forme de balises [laughter])
            add_breathing: Ajouter des respirations (sous forme de balises [breathing])
            emotion: Émotion à ajouter (excited, sad, happy, etc.)
        """
        # Transformer le texte pour inclure les effets spéciaux
        modified_text = text
        
        # Ajouter les balises d'émotion si spécifiées
        if emotion:
            modified_text = f"[{emotion}] {modified_text}"
            
        # Ajouter des balises de rire si demandé
        if add_laughter:
            # Ajouter des balises de rire à des positions aléatoires (simpliste)
            sentences = modified_text.split(". ")
            for i in range(len(sentences)):
                if np.random.random() < 0.3:  # 30% de chance par phrase
                    sentences[i] = sentences[i] + " [laughter]"
            modified_text = ". ".join(sentences)
        
        # Ajouter des balises de respiration si demandé
        if add_breathing:
            # Ajouter des balises de respiration à des positions aléatoires
            sentences = modified_text.split(". ")
            for i in range(len(sentences)):
                if np.random.random() < 0.2:  # 20% de chance par phrase
                    sentences[i] = sentences[i] + " [breathing]"
            modified_text = ". ".join(sentences)
        
        # Utiliser la méthode standard pour générer l'audio
        return self.clone_voice(reference_audio, modified_text, output_file, language) 