@echo off
setlocal
title College Notes RAG Assistant
cd /d "%~dp0"

echo.
echo ============================================
echo     COLLEGE NOTES RAG ASSISTANT
echo ============================================
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo Python was not found.
    echo Please install Python 3.10 or newer, then run START.bat again.
    pause
    exit /b 1
)

if not exist "venv\Scripts\python.exe" (
    echo [1/3] Creating Python environment...
    python -m venv venv
    if errorlevel 1 (
        echo Could not create the Python environment.
        pause
        exit /b 1
    )
)

echo [2/3] Installing required packages...
venv\Scripts\python.exe -m pip install --disable-pip-version-check -r requirements.txt
if errorlevel 1 (
    echo.
    echo Package installation failed. Check your internet connection.
    pause
    exit /b 1
)

if not exist ".env" (
    echo.
    echo FIRST-TIME API KEY SETUP
    echo Get a Groq API key at:
    echo https://console.groq.com/keys
    echo.
    set /p GROQKEY=Paste your Groq API key and press Enter:
    powershell -NoProfile -Command "$k=$env:GROQKEY; Set-Content -Path '.env' -Value ('GROQ_API_KEY=' + $k)"
)

echo [3/3] Starting application...
echo.
venv\Scripts\python.exe -m streamlit run app.py
pause
