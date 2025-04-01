#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import threading

# Ajouter le répertoire parent au chemin
sys.path.append(str(Path(__file__).parent.parent))

# Importer notre module StandaloneBark
from src.standalone_bark import StandaloneBark

class BarkGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Configuration de la fenêtre principale
        self.title("Bark Voice Cloning - Interface Graphique")
        self.geometry("700x650")
        self.minsize(650, 600)
        
        # Configuration du style
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Helvetica", 11))
        self.style.configure("TLabel", font=("Helvetica", 11))
        self.style.configure("Header.TLabel", font=("Helvetica", 14, "bold"))
        
        # Initialisation des variables
        self.ref_audio_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.model_dir = tk.StringVar(value=str(Path(__file__).parent.parent / "models"))
        self.language = tk.StringVar(value="fr")
        
        # Variables spécifiques à Bark
        self.add_laughter = tk.BooleanVar(value=False)
        self.add_breathing = tk.BooleanVar(value=False)
        self.emotion = tk.StringVar(value="")
        
        # Création des composants
        self._create_widgets()
        
        # Instance de Bark (sera initialisée lors du premier clonage)
        self.bark = None
        self.is_processing = False
        
    def _create_widgets(self):
        """Crée tous les widgets de l'interface"""
        # Cadre principal
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre
        header = ttk.Label(main_frame, text="Bark Voice Cloning", style="Header.TLabel")
        header.pack(pady=(0, 20))
        
        # Section 1: Sélection de l'audio de référence
        ref_frame = ttk.LabelFrame(main_frame, text="Audio de référence", padding=10)
        ref_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(ref_frame, text="Fichier audio:").pack(anchor="w")
        
        ref_path_frame = ttk.Frame(ref_frame)
        ref_path_frame.pack(fill=tk.X, pady=5)
        
        ref_entry = ttk.Entry(ref_path_frame, textvariable=self.ref_audio_path)
        ref_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        browse_btn = ttk.Button(ref_path_frame, text="Parcourir", command=self._browse_ref_audio)
        browse_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Section 2: Texte à synthétiser
        text_frame = ttk.LabelFrame(main_frame, text="Texte à synthétiser", padding=10)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.text_entry = tk.Text(text_frame, height=5, width=50, wrap=tk.WORD)
        self.text_entry.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Section 3: Options générales
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding=10)
        options_frame.pack(fill=tk.X, pady=10)
        
        # Sélection de la langue
        lang_frame = ttk.Frame(options_frame)
        lang_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(lang_frame, text="Langue:").pack(side=tk.LEFT)
        
        languages = [
            ("Français", "fr"), 
            ("Anglais", "en"), 
            ("Espagnol", "es"),
            ("Allemand", "de"), 
            ("Italien", "it"), 
            ("Japonais", "ja"),
            ("Chinois", "zh"),
            ("Russe", "ru"),
            ("Portugais", "pt"),
            ("Polonais", "pl"),
        ]
        
        lang_combo = ttk.Combobox(lang_frame, textvariable=self.language, state="readonly", width=15)
        lang_combo['values'] = [f"{name} ({code})" for name, code in languages]
        lang_combo.current(0)
        lang_combo.pack(side=tk.LEFT, padx=(5, 0))
        
        # Section 4: Options spécifiques à Bark
        effects_frame = ttk.LabelFrame(main_frame, text="Effets spéciaux (Bark)", padding=10)
        effects_frame.pack(fill=tk.X, pady=10)
        
        # Checkboxes pour les effets
        effects_checkboxes = ttk.Frame(effects_frame)
        effects_checkboxes.pack(fill=tk.X, pady=5)
        
        laughter_check = ttk.Checkbutton(effects_checkboxes, text="Ajouter des rires", variable=self.add_laughter)
        laughter_check.pack(side=tk.LEFT, padx=(0, 20))
        
        breathing_check = ttk.Checkbutton(effects_checkboxes, text="Ajouter des respirations", variable=self.add_breathing)
        breathing_check.pack(side=tk.LEFT)
        
        # Sélection d'émotion
        emotion_frame = ttk.Frame(effects_frame)
        emotion_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(emotion_frame, text="Émotion:").pack(side=tk.LEFT)
        
        emotions = [
            "", "neutral", "happy", "sad", "angry", "excited", "concerned"
        ]
        
        emotion_combo = ttk.Combobox(emotion_frame, textvariable=self.emotion, state="readonly", width=15)
        emotion_combo['values'] = emotions
        emotion_combo.current(0)
        emotion_combo.pack(side=tk.LEFT, padx=(5, 0))
        
        # Fichier de sortie
        output_frame = ttk.Frame(options_frame)
        output_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(output_frame, text="Fichier de sortie:").pack(anchor="w")
        
        output_path_frame = ttk.Frame(output_frame)
        output_path_frame.pack(fill=tk.X, pady=5)
        
        output_entry = ttk.Entry(output_path_frame, textvariable=self.output_path)
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        output_btn = ttk.Button(output_path_frame, text="Parcourir", command=self._browse_output_file)
        output_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Répertoire des modèles
        model_frame = ttk.Frame(options_frame)
        model_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(model_frame, text="Répertoire des modèles:").pack(anchor="w")
        
        model_path_frame = ttk.Frame(model_frame)
        model_path_frame.pack(fill=tk.X, pady=5)
        
        model_entry = ttk.Entry(model_path_frame, textvariable=self.model_dir)
        model_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        model_btn = ttk.Button(model_path_frame, text="Parcourir", command=self._browse_model_dir)
        model_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Section 5: Actions
        actions_frame = ttk.Frame(main_frame)
        actions_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Barre de progression
        self.progress = ttk.Progressbar(actions_frame, mode="indeterminate")
        self.progress.pack(fill=tk.X, pady=(0, 10))
        
        # Boutons
        buttons_frame = ttk.Frame(actions_frame)
        buttons_frame.pack(fill=tk.X)
        
        self.clone_btn = ttk.Button(buttons_frame, text="Cloner la voix", command=self._clone_voice)
        self.clone_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        
        download_btn = ttk.Button(buttons_frame, text="Télécharger modèles", command=self._download_models)
        download_btn.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=(5, 0))
        
        # Zone de log
        log_frame = ttk.LabelFrame(main_frame, text="Journal", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.log_text = tk.Text(log_frame, height=5, width=50, wrap=tk.WORD, state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar pour le log
        scrollbar = ttk.Scrollbar(self.log_text, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
    
    def _browse_ref_audio(self):
        """Sélectionner un fichier audio de référence"""
        filetypes = [
            ("Fichiers audio", "*.wav *.mp3 *.ogg *.flac"),
            ("Tous les fichiers", "*.*")
        ]
        filename = filedialog.askopenfilename(
            title="Sélectionner un fichier audio",
            filetypes=filetypes
        )
        if filename:
            self.ref_audio_path.set(filename)
    
    def _browse_output_file(self):
        """Sélectionner un fichier de sortie"""
        filetypes = [("Fichiers WAV", "*.wav")]
        filename = filedialog.asksaveasfilename(
            title="Enregistrer l'audio généré",
            defaultextension=".wav",
            filetypes=filetypes
        )
        if filename:
            self.output_path.set(filename)
    
    def _browse_model_dir(self):
        """Sélectionner le répertoire des modèles"""
        directory = filedialog.askdirectory(
            title="Sélectionner le répertoire des modèles"
        )
        if directory:
            self.model_dir.set(directory)
    
    def _log(self, message):
        """Ajoute un message au journal"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def _download_models(self):
        """Télécharge les modèles Bark"""
        if self.is_processing:
            return
            
        self.is_processing = True
        self.progress.start()
        self.clone_btn.config(state=tk.DISABLED)
        
        def download_thread():
            try:
                from src.download_models import download_models
                self._log("Téléchargement des modèles Bark en cours...")
                self._log("Cette opération peut prendre plusieurs minutes...")
                output_dir = download_models(self.model_dir.get())
                self._log(f"Modèles téléchargés avec succès dans: {output_dir}")
            except Exception as e:
                self._log(f"Erreur lors du téléchargement des modèles: {e}")
                messagebox.showerror("Erreur", f"Échec du téléchargement: {e}")
            finally:
                self.is_processing = False
                self.progress.stop()
                self.clone_btn.config(state=tk.NORMAL)
        
        threading.Thread(target=download_thread).start()
    
    def _clone_voice(self):
        """Clone la voix à partir du fichier audio de référence"""
        if self.is_processing:
            return
            
        # Valider les entrées
        ref_audio = self.ref_audio_path.get().strip()
        text = self.text_entry.get("1.0", tk.END).strip()
        lang_code = self.language.get().split("(")[-1].split(")")[0].strip()
        output_file = self.output_path.get().strip() or None
        model_dir = self.model_dir.get().strip()
        
        # Options spécifiques à Bark
        add_laughter = self.add_laughter.get()
        add_breathing = self.add_breathing.get()
        emotion = self.emotion.get() if self.emotion.get() else None
        
        if not ref_audio:
            messagebox.showerror("Erreur", "Veuillez sélectionner un fichier audio de référence.")
            return
            
        if not os.path.exists(ref_audio):
            messagebox.showerror("Erreur", f"Le fichier audio '{ref_audio}' n'existe pas.")
            return
            
        if not text:
            messagebox.showerror("Erreur", "Veuillez entrer du texte à synthétiser.")
            return
            
        # Lancer le traitement
        self.is_processing = True
        self.progress.start()
        self.clone_btn.config(state=tk.DISABLED)
        
        def clone_thread():
            try:
                # Initialiser Bark si ce n'est pas déjà fait
                if self.bark is None:
                    self._log("Initialisation de Bark...")
                    self.bark = StandaloneBark(model_dir=model_dir)
                
                # Cloner la voix
                self._log(f"Clonage de la voix depuis '{ref_audio}' en {lang_code}...")
                self._log(f"Texte: '{text}'")
                
                # Si des effets sont demandés, utiliser la méthode avec effets
                if add_laughter or add_breathing or emotion:
                    self._log("Utilisation des effets spéciaux...")
                    
                    if add_laughter:
                        self._log("Ajout de rires")
                    
                    if add_breathing:
                        self._log("Ajout de respirations")
                    
                    if emotion:
                        self._log(f"Émotion: {emotion}")
                    
                    output = self.bark.generate_with_effects(
                        ref_audio,
                        text,
                        output_file=output_file,
                        language=lang_code,
                        add_laughter=add_laughter,
                        add_breathing=add_breathing,
                        emotion=emotion
                    )
                else:
                    # Sinon utiliser la méthode standard
                    output = self.bark.clone_voice(
                        ref_audio,
                        text,
                        output_file=output_file,
                        language=lang_code
                    )
                
                if output:
                    self._log(f"Audio généré avec succès: {output}")
                    messagebox.showinfo("Succès", f"Audio généré avec succès:\n{output}")
                else:
                    self._log("Échec de la génération audio.")
                    messagebox.showerror("Erreur", "Échec de la génération audio.")
                    
            except Exception as e:
                self._log(f"Erreur lors du clonage vocal: {e}")
                messagebox.showerror("Erreur", f"Échec du clonage vocal: {e}")
            finally:
                self.is_processing = False
                self.progress.stop()
                self.clone_btn.config(state=tk.NORMAL)
        
        threading.Thread(target=clone_thread).start()

if __name__ == "__main__":
    app = BarkGUI()
    app.mainloop() 