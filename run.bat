@echo off
echo Starting CurseForge Minecraft Mod Crawler...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

REM Check if dependencies are installed
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo  CurseForge Minecraft Mod Crawler
echo ========================================
echo.
echo Make sure to:
echo 1. Get an API key from https://console.curseforge.com/
echo 2. Enter the API key in the application
echo 3. Configure your search parameters
echo.
echo Starting application...
echo.

python mod_crawler_gui.py

if errorlevel 1 (
    echo.
    echo Application exited with an error.
    pause
)
