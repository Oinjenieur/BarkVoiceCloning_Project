@echo off
echo Bark Voice Cloning - Installation et téléchargement des modèles
echo ======================================================

echo.
echo 1. Installation des dépendances...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo Erreur lors de l'installation des dépendances.
    goto :error
)

echo.
echo 2. Téléchargement des modèles...
python -m src.download_models
if %ERRORLEVEL% NEQ 0 (
    echo Erreur lors du téléchargement des modèles.
    goto :error
)

echo.
echo Installation terminée avec succès !
echo Vous pouvez maintenant lancer l'application avec run_gui.bat
goto :end

:error
echo.
echo Une erreur s'est produite lors de l'installation.
echo Vérifiez les détails ci-dessus et réessayez.

:end
pause 