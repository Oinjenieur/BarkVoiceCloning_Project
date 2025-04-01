# Bark Voice Cloning - Implémentation Offline

Ce projet fournit une implémentation autonome et offline de Bark, un système de clonage vocal très expressif avec support multilingue et capacités avancées de génération d'effets vocaux.

## Caractéristiques

- 🎙️ **Clonage vocal de haute qualité** - Reproduit fidèlement les caractéristiques vocales avec une expressivité exceptionnelle
- 🌍 **Support étendu multilingue** - Support pour plus de 10 langues dont français, anglais, espagnol, allemand, chinois, et plus
- 🔊 **Effets sonores uniques** - Capacité d'ajouter des rires, respirations et émotions dans la voix générée
- 💻 **Mode offline complet** - Fonctionne entièrement hors ligne une fois les modèles téléchargés
- 🖥️ **Interface graphique intuitive** - Utilisation simplifiée grâce à une interface graphique conviviale
- 🔧 **Interface en ligne de commande** - Pour une utilisation dans des scripts ou l'automatisation

## Installation

### Prérequis

- Python 3.8+ 
- Git
- [PyTorch](https://pytorch.org/get-started/locally/) (idéalement avec support CUDA pour les performances GPU)

### Installation standard

1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/votrenom/BarkVoiceCloning_Project.git
   cd BarkVoiceCloning_Project
   ```

2. Installez les dépendances et téléchargez les modèles :
   ```bash
   # Sous Windows
   setup_models.bat
   
   # Sous Linux/Mac
   pip install -r requirements.txt
   python -m src.download_models
   ```

## Utilisation

### Interface graphique

Pour lancer l'interface graphique :

```bash
# Sous Windows
run_gui.bat

# Sous Linux/Mac
python -m src.gui
```

L'interface vous guidera à travers le processus de clonage vocal :
1. Sélectionnez un fichier audio de référence
2. Entrez le texte à synthétiser
3. Choisissez la langue et les options
4. Ajoutez des effets spéciaux (rires, respirations, émotions) si souhaité
5. Cliquez sur "Cloner la voix"

### Ligne de commande

Pour utiliser l'interface en ligne de commande :

```bash
python -m src.bark_cli --ref chemin/vers/audio.wav --text "Texte à synthétiser" --lang fr
```

Options disponibles :
- `--ref` : Chemin vers l'audio de référence (obligatoire)
- `--text` : Texte à synthétiser (obligatoire)
- `--lang` : Code langue (fr, en, es, de, etc.), par défaut "fr"
- `--output` : Chemin du fichier de sortie (optionnel)
- `--model-dir` : Répertoire des modèles (optionnel)

Options spécifiques à Bark :
- `--laughter` : Ajouter des rires aléatoires
- `--breathing` : Ajouter des respirations aléatoires
- `--emotion` : Ajouter une émotion spécifique (neutral, happy, sad, angry, excited, concerned)

## Structure du projet

```
BarkVoiceCloning_Project/
├── models/                   # Répertoire pour les modèles téléchargés
├── src/
│   ├── standalone_bark.py    # Implémentation principale
│   ├── bark_cli.py           # Interface ligne de commande
│   ├── download_models.py    # Script de téléchargement des modèles
│   ├── gui.py                # Interface graphique
│   └── __init__.py           # Initialisation du package
├── requirements.txt          # Dépendances Python
├── setup_models.bat          # Script d'installation pour Windows
├── run_gui.bat               # Script de lancement GUI pour Windows
└── README.md                 # Documentation
```

## Performances

Bark offre d'excellentes performances de clonage vocal avec des capacités uniques :
- **Similarité vocale** : 87-91%
- **Expressivité** : Très élevée (la meilleure parmi les modèles comparés)
- **Inférence GPU** : ~0.9x temps réel
- **Support multilingue** : Plus de 10 langues
- **Capacités uniques** : Sons non-verbaux, émotions, rires, respirations

## Fonctionnalités spéciales

Bark se distingue par sa capacité à générer des effets vocaux spéciaux :

1. **Rires** : Ajoutez des rires naturels à la synthèse vocale
2. **Respirations** : Incluez des sons de respiration pour une voix plus naturelle
3. **Émotions** : Contrôlez l'émotion de la voix (joie, colère, tristesse, etc.)
4. **Sons non-verbaux** : Générez des hum, hésitations et autres sons vocaux

## Dépannage

Si vous rencontrez des problèmes :

1. **Les modèles ne se téléchargent pas** :
   - Vérifiez votre connexion internet
   - Les modèles sont volumineux (environ 5GB), assurez-vous d'avoir suffisamment d'espace

2. **Erreurs lors du clonage** :
   - Assurez-vous que le fichier audio de référence est de bonne qualité
   - Vérifiez que les modèles sont correctement téléchargés

3. **Performances lentes** :
   - Utilisez un GPU avec CUDA si possible
   - Pour le CPU, attendez-vous à des temps de génération plus longs

## Licence

Ce projet est basé sur Bark, veuillez consulter la licence de Bark pour plus d'informations. 