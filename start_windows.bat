@echo off
title CyberGuard Universal Launcher
echo ======================================================
echo           CyberGuard - Starting Platform
echo ======================================================

:: Resolve project root directory dynamically
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

:: Check if virtual environment exists
if exist ".venv\Scripts\activate.bat" (
    echo [*] Activating Python virtual environment (.venv)...
    call ".venv\Scripts\activate.bat"
) else if exist "venv\Scripts\activate.bat" (
    echo [*] Activating Python virtual environment (venv)...
    call "venv\Scripts\activate.bat"
) else (
    echo [*] Using system Python...
)

:: Run universal python launcher
python run.py

pause
