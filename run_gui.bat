@echo off
echo Bark Voice Cloning - Interface Graphique
echo ========================================

REM Verifier que Python est installe
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python n'est pas installe ou n'est pas dans le PATH
    echo Veuillez installer Python 3.8 ou superieur depuis https://www.python.org/
    pause
    exit /b 1
)

REM Verifier que les modeles sont installes
if not exist "models" (
    echo Les modeles ne sont pas installes.
    echo Executez d'abord setup_models.bat pour telecharger les modeles requis.
    pause
    exit /b 1
)

echo Demarrage de l'interface graphique...
python -m src.gui

echo.
echo L'interface graphique s'est fermee.
echo Appuyez sur une touche pour quitter...
pause > nul 