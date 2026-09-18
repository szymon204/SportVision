@echo off

rem Przechodzi do folderu, w ktorym znajduje sie start.bat.
cd /d "%~dp0"

rem Sprawdza, czy srodowisko Pythona jest przygotowane.
if not exist ".venv\Scripts\python.exe" (
    echo Nie znaleziono srodowiska .venv.
    echo Najpierw trzeba przygotowac aplikacje.
    pause
    exit /b 1
)

rem Uruchamia serwer SportVision w osobnym oknie.
start "SportVision - serwer" cmd /k ".venv\Scripts\python.exe -m uvicorn main:app"

rem Daje serwerowi dwie sekundy na uruchomienie.
timeout /t 2 /nobreak >nul

rem Otwiera aplikacje w domyslnej przegladarce.
start "" "http://127.0.0.1:8000"