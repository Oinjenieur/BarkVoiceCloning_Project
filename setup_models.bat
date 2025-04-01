@echo off
echo Bark Voice Cloning - Installation et telechargement des modeles
echo ================================================================

REM Verifier que Python est installe
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python n'est pas installe ou n'est pas dans le PATH
    echo Veuillez installer Python 3.8 ou superieur depuis https://www.python.org/
    goto :error
)

REM Verifier que pip est disponible
python -m pip --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo pip n'est pas disponible
    echo Installation de pip...
    python -m ensurepip --upgrade
    if %ERRORLEVEL% NEQ 0 (
        echo Erreur lors de l'installation de pip
        goto :error
    )
)

echo Installation des dependances...
python -m pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo Erreur lors de l'installation des dependances
    goto :error
)

echo Creation des repertoires pour les modeles...
if not exist "models" mkdir models
if not exist "models\speaker_embeddings" mkdir models\speaker_embeddings

echo Telechargement des modeles Bark...
python -m src.download_models --output-dir models
if %ERRORLEVEL% NEQ 0 (
    echo Erreur lors du telechargement des modeles
    goto :error
)

echo.
echo Installation terminee avec succes !
echo Vous pouvez maintenant lancer l'application avec run_gui.bat
goto :end

:error
echo.
echo Une erreur s'est produite lors de l'installation.
echo Veuillez verifier les messages d'erreur ci-dessus.
pause
exit /b 1

:end
echo.
echo Appuyez sur une touche pour fermer cette fenetre...
pause > nul 