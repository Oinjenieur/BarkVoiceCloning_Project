#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import logging
import numpy as np
import torch
import uuid
import datetime
import tempfile
from pathlib import Path
from typing import Optional, Dict, List, Tuple, Union, Any

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class StandaloneBark:
    """Classe principale pour le clonage vocal avec Bark."""
    
    def __init__(self, model_dir: Optional[str] = None):
        """
        Initialisation de l'instance Bark pour le clonage vocal.
        
        Args:
            model_dir: Répertoire des modèles pré-entraînés.
        """
        self.model_dir = model_dir or os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
        self.speaker_embeddings_dir = os.path.join(self.model_dir, "speaker_embeddings")
        
        # S'assurer que les répertoires existent
        os.makedirs(self.model_dir, exist_ok=True)
        os.makedirs(self.speaker_embeddings_dir, exist_ok=True)
        
        self.bark = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        logger.info(f"Initialisation de Bark (appareil: {self.device})")
        logger.info(f"Répertoire des modèles: {self.model_dir}")
        
    def _load_models(self):
        """Charge les modèles Bark si ce n'est pas déjà fait."""
        if self.bark is not None:
            return

        try:
            logger.info("Chargement des modèles Bark...")
            
            from bark import SAMPLE_RATE, generate_audio, preload_models
            from bark.generation import (
                generate_text_semantic,
                preload_models,
            )
            from bark.api import semantic_to_waveform
            from bark import generate_audio, SAMPLE_RATE
            from scipy.io.wavfile import write as write_wav
            
            preload_models()
            
            self.bark_sr = SAMPLE_RATE
            self.generate_audio = generate_audio
            self.generate_text_semantic = generate_text_semantic
            self.semantic_to_waveform = semantic_to_waveform
            self.write_wav = write_wav
            
            logger.info("Modèles Bark chargés avec succès")
            
        except Exception as e:
            logger.error(f"Erreur lors du chargement des modèles Bark: {e}")
            raise
            
    def extract_speaker(self, audio_file: str, speaker_id: Optional[str] = None) -> str:
        """
        Extrait l'identité vocale à partir d'un fichier audio.
        
        Args:
            audio_file: Chemin vers le fichier audio.
            speaker_id: Identifiant du locuteur (généré automatiquement si non fourni).
            
        Returns:
            Identifiant du locuteur.
        """
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Fichier audio non trouvé: {audio_file}")
            
        # Charger les modèles si nécessaire
        self._load_models()
        
        # Générer un ID si non fourni
        if speaker_id is None:
            speaker_id = f"speaker_{uuid.uuid4().hex[:8]}"
            
        try:
            logger.info(f"Extraction de l'identité vocale depuis {audio_file}...")
            
            from bark.generation import generate_text_semantic
            import scipy
            
            # Charger l'audio
            audio, sr = load_audio(audio_file)
            
            # Enregistrer l'embedding
            np.save(
                os.path.join(self.speaker_embeddings_dir, f"{speaker_id}.npy"),
                audio
            )
            
            logger.info(f"Identité vocale extraite et enregistrée sous l'ID: {speaker_id}")
            return speaker_id
            
        except Exception as e:
            logger.error(f"Erreur lors de l'extraction de l'identité vocale: {e}")
            raise
            
    def clone_voice(
        self,
        text: str,
        speaker_id: Optional[str] = None,
        audio_file: Optional[str] = None,
        output_file: Optional[str] = None,
        language: str = "en",
        temperature: float = 0.7,
    ) -> str:
        """
        Clone une voix et génère de l'audio avec le texte fourni.
        
        Args:
            text: Texte à prononcer.
            speaker_id: Identifiant d'une voix précédemment extraite.
            audio_file: Fichier audio de référence (alternative à speaker_id).
            output_file: Chemin de sortie pour l'audio généré.
            language: Code de langue (en, fr, de, es, etc.).
            temperature: Contrôle de la créativité (0.5-1.0).
            
        Returns:
            Chemin vers le fichier audio généré.
        """
        if not speaker_id and not audio_file:
            raise ValueError("Vous devez fournir soit un speaker_id, soit un audio_file")
            
        # Charger les modèles si nécessaire
        self._load_models()
        
        # Si audio_file est fourni, extraire d'abord l'identité vocale
        if audio_file:
            if not speaker_id:
                speaker_id = f"temp_{uuid.uuid4().hex[:8]}"
            speaker_id = self.extract_speaker(audio_file, speaker_id)
            
        # Vérifier que l'embedding existe
        embedding_path = os.path.join(self.speaker_embeddings_dir, f"{speaker_id}.npy")
        if not os.path.exists(embedding_path):
            raise FileNotFoundError(f"Identité vocale non trouvée: {speaker_id}")
            
        # Créer le chemin de sortie si non fourni
        if not output_file:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(
                self.model_dir, 
                f"generated_{speaker_id}_{timestamp}.wav"
            )
            
        try:
            logger.info(f"Génération d'audio pour le texte: '{text}'")
            
            # Charger l'embedding
            history_prompt = np.load(embedding_path)
            
            # Générer l'audio
            audio_array = self.generate_audio(
                text, 
                history_prompt=history_prompt,
                text_temp=temperature,
                waveform_temp=temperature,
                output_full=True
            )
            
            # Enregistrer l'audio
            self.write_wav(output_file, self.bark_sr, audio_array)
            
            logger.info(f"Audio généré et enregistré: {output_file}")
            return output_file
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération audio: {e}")
            raise
            
    def generate_voice_with_emotion(
        self,
        text: str,
        speaker_id: Optional[str] = None,
        audio_file: Optional[str] = None,
        output_file: Optional[str] = None,
        language: str = "en",
        emotion: str = "neutral",
        temperature: float = 0.7,
    ) -> str:
        """
        Génère de l'audio avec émotion spécifiée.
        
        Args:
            text: Texte à prononcer.
            speaker_id: Identifiant d'une voix précédemment extraite.
            audio_file: Fichier audio de référence (alternative à speaker_id).
            output_file: Chemin de sortie pour l'audio généré.
            language: Code de langue (en, fr, de, es, etc.).
            emotion: Émotion (neutral, happy, sad, angry, surprised).
            temperature: Contrôle de la créativité (0.5-1.0).
            
        Returns:
            Chemin vers le fichier audio généré.
        """
        # Ajouter des modificateurs d'émotion au texte
        emotion_prefixes = {
            "neutral": "",
            "happy": "[RIRE] [JOYEUX] ",
            "sad": "[TRISTE] [SOLENNEL] ",
            "angry": "[COLÈRE] [INTENSE] ",
            "surprised": "[SURPRISE] [EXCITÉ] "
        }
        
        if emotion not in emotion_prefixes:
            logger.warning(f"Émotion '{emotion}' non reconnue, utilisation de 'neutral'")
            emotion = "neutral"
            
        modified_text = emotion_prefixes[emotion] + text
        
        # Utiliser la méthode clone_voice standard avec le texte modifié
        return self.clone_voice(
            text=modified_text,
            speaker_id=speaker_id,
            audio_file=audio_file,
            output_file=output_file,
            language=language,
            temperature=temperature
        )
            
# Fonctions utilitaires
def load_audio(file_path, sr=None):
    """Charge un fichier audio avec le bon format pour Bark."""
    try:
        import scipy
        
        # Détecter le format de fichier
        if file_path.endswith('.mp3') or file_path.endswith('.ogg') or file_path.endswith('.flac'):
            try:
                import librosa
                audio, file_sr = librosa.load(file_path, sr=sr)
                return audio, file_sr
            except ImportError:
                logger.warning("librosa non installé, certains formats audio peuvent ne pas être pris en charge")
                
        # Lire le fichier WAV
        file_sr, audio = scipy.io.wavfile.read(file_path)
        audio = audio.astype(np.float32)
        
        # Normaliser
        if audio.ndim > 1:
            audio = audio.mean(axis=1)
        audio = audio / np.max(np.abs(audio))
        
        # Rééchantillonner si nécessaire
        if sr is not None and file_sr != sr:
            from scipy import signal
            audio = signal.resample(audio, int(len(audio) * sr / file_sr))
            file_sr = sr
            
        return audio, file_sr
        
    except Exception as e:
        logger.error(f"Erreur lors du chargement de l'audio: {e}")
        raise 