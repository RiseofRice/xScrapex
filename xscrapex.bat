@echo off
REM xScrapex Windows Launcher
REM This batch file makes it easy to run xScrapex on Windows

echo xScrapex - Twitter/X Scraper
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if dependencies are installed
python -c "import requests, bs4, colorama" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Try to install win10toast if not already installed
python -c "import win10toast" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Windows notifications support...
    pip install win10toast
)

REM Check if username was provided
if "%1"=="" (
    echo Usage: xscrapex.bat [username] [interval]
    echo.
    echo Examples:
    echo   xscrapex.bat elonmusk
    echo   xscrapex.bat elonmusk 120
    echo.
    pause
    exit /b 1
)

REM Run the scraper
if "%2"=="" (
    python xscrapex.py %1
) else (
    python xscrapex.py %1 --interval %2
)
