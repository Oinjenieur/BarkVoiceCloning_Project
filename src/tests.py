#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import unittest
import tempfile
import shutil
import logging
from pathlib import Path

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Ajouter le répertoire parent au chemin
sys.path.append(str(Path(__file__).parent.parent))

# Importer nos modules
from src.standalone_bark import StandaloneBark
from src.download_models import download_bark_models, ensure_bark_installed

class TestBarkVoiceCloning(unittest.TestCase):
    """Tests pour le projet Bark Voice Cloning."""
    
    @classmethod
    def setUpClass(cls):
        """Configuration avant tous les tests."""
        # Créer un répertoire temporaire pour les tests
        cls.test_dir = tempfile.mkdtemp()
        cls.model_dir = os.path.join(cls.test_dir, "models")
        cls.audio_dir = os.path.join(cls.test_dir, "audio")
        
        # Créer les sous-répertoires
        os.makedirs(cls.model_dir, exist_ok=True)
        os.makedirs(cls.audio_dir, exist_ok=True)
        
        # Vérifier que Bark est installé
        is_installed = ensure_bark_installed()
        if not is_installed:
            logger.error("Bark n'est pas installé. Les tests ne peuvent pas être exécutés.")
            sys.exit(1)
        
        # Télécharger un petit ensemble de modèles pour les tests
        logger.info("Téléchargement des modèles pour les tests...")
        # Note: Cette opération peut prendre du temps
        download_bark_models(cls.model_dir)
    
    @classmethod
    def tearDownClass(cls):
        """Nettoyage après tous les tests."""
        # Supprimer le répertoire temporaire
        shutil.rmtree(cls.test_dir)
    
    def setUp(self):
        """Configuration avant chaque test."""
        self.bark = StandaloneBark(model_dir=self.model_dir)
        
        # Créer un petit fichier audio test si nécessaire
        self.test_audio = os.path.join(self.audio_dir, "test_audio.wav")
        if not os.path.exists(self.test_audio):
            self._create_test_audio()
    
    def _create_test_audio(self):
        """Crée un fichier audio de test simple."""
        try:
            import numpy as np
            from scipy.io.wavfile import write
            
            # Générer un simple sinus à 440 Hz
            sr = 22050
            duration = 3  # secondes
            t = np.linspace(0, duration, int(sr * duration), endpoint=False)
            signal = 0.5 * np.sin(2 * np.pi * 440 * t)
            
            # Enregistrer au format WAV
            write(self.test_audio, sr, signal.astype(np.float32))
            logger.info(f"Fichier audio de test créé: {self.test_audio}")
        except Exception as e:
            logger.error(f"Erreur lors de la création du fichier audio test: {e}")
            raise
    
    def test_extract_speaker(self):
        """Teste l'extraction de l'identité vocale."""
        try:
            speaker_id = self.bark.extract_speaker(
                audio_file=self.test_audio,
                speaker_id="test_speaker"
            )
            
            # Vérifier que l'ID est correct
            self.assertEqual(speaker_id, "test_speaker")
            
            # Vérifier que le fichier d'embedding existe
            embedding_path = os.path.join(self.model_dir, "speaker_embeddings", f"{speaker_id}.npy")
            self.assertTrue(os.path.exists(embedding_path))
        except Exception as e:
            self.fail(f"L'extraction de l'identité vocale a échoué: {e}")
    
    def test_clone_voice_with_speaker_id(self):
        """Teste le clonage vocal avec un ID de locuteur."""
        try:
            # D'abord extraire l'identité vocale
            speaker_id = self.bark.extract_speaker(
                audio_file=self.test_audio,
                speaker_id="test_speaker"
            )
            
            # Puis générer l'audio
            output_file = os.path.join(self.test_dir, "output.wav")
            result = self.bark.clone_voice(
                text="Ceci est un test de synthèse vocale.",
                speaker_id=speaker_id,
                output_file=output_file,
                language="fr"
            )
            
            # Vérifier que le fichier de sortie existe
            self.assertTrue(os.path.exists(output_file))
            self.assertEqual(result, output_file)
        except Exception as e:
            self.fail(f"Le clonage vocal avec ID de locuteur a échoué: {e}")
    
    def test_clone_voice_with_audio_file(self):
        """Teste le clonage vocal directement avec un fichier audio."""
        try:
            output_file = os.path.join(self.test_dir, "output_direct.wav")
            result = self.bark.clone_voice(
                text="This is a voice cloning test.",
                audio_file=self.test_audio,
                output_file=output_file,
                language="en"
            )
            
            # Vérifier que le fichier de sortie existe
            self.assertTrue(os.path.exists(output_file))
            self.assertEqual(result, output_file)
        except Exception as e:
            self.fail(f"Le clonage vocal direct a échoué: {e}")
    
    def test_generate_voice_with_emotion(self):
        """Teste la génération vocale avec émotion."""
        try:
            # D'abord extraire l'identité vocale
            speaker_id = self.bark.extract_speaker(
                audio_file=self.test_audio,
                speaker_id="test_speaker_emotion"
            )
            
            # Puis générer l'audio avec émotion
            output_file = os.path.join(self.test_dir, "output_emotion.wav")
            result = self.bark.generate_voice_with_emotion(
                text="Je suis très heureux aujourd'hui!",
                speaker_id=speaker_id,
                output_file=output_file,
                language="fr",
                emotion="happy"
            )
            
            # Vérifier que le fichier de sortie existe
            self.assertTrue(os.path.exists(output_file))
            self.assertEqual(result, output_file)
        except Exception as e:
            self.fail(f"La génération vocale avec émotion a échoué: {e}")

if __name__ == "__main__":
    unittest.main() 