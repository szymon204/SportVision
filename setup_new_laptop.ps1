[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

# Przechodzi do folderu projektu niezależnie od miejsca uruchomienia skryptu.
Set-Location -LiteralPath $PSScriptRoot

# Zapobiega tworzeniu pomocniczych plików __pycache__ podczas zwykłego uruchamiania.
$env:PYTHONDONTWRITEBYTECODE = "1"

Write-Host "Przygotowanie SportVision na nowym laptopie" -ForegroundColor Cyan

# Wybiera dostępne polecenie uruchamiające Python 3.
if (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonCommand = "py"
    $pythonArguments = @("-3")
}
elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCommand = "python"
    $pythonArguments = @()
}
else {
    throw "Nie znaleziono Pythona. Zainstaluj Python 3 i uruchom skrypt ponownie."
}

# Tworzy środowisko tylko wtedy, gdy jeszcze nie istnieje.
if (-not (Test-Path -LiteralPath ".\.venv\Scripts\python.exe")) {
    Write-Host "Tworzenie lokalnego środowiska .venv..."
    & $pythonCommand @pythonArguments -m venv .venv
}
else {
    Write-Host "Środowisko .venv już istnieje."
}

$venvPython = ".\.venv\Scripts\python.exe"

# Instaluje dokładnie zależności zapisane w requirements.txt.
Write-Host "Instalowanie bibliotek projektu..."
& $venvPython -m pip install -r requirements.txt

# Tworzy folder bazy, ale nie tworzy ani nie nadpisuje samego pliku z danymi.
New-Item -ItemType Directory -Path ".\data" -Force | Out-Null

# Sprawdza import bibliotek bez uruchamiania aplikacji.
& $venvPython -c "import fastapi, uvicorn, requests, dotenv; print('Biblioteki Pythona: OK')"

# Sprawdza wyłącznie obecność prywatnych plików. Nie odczytuje ich zawartości.
if (Test-Path -LiteralPath ".\.env") {
    Write-Host "Plik .env: znaleziony" -ForegroundColor Green
}
else {
    Write-Host "Plik .env: brak - jest potrzebny tylko do importu z API" -ForegroundColor Yellow
}

if (Test-Path -LiteralPath ".\data\sportvision.db") {
    Write-Host "Baza sportvision.db: znaleziona" -ForegroundColor Green
}
else {
    Write-Host "Baza sportvision.db: brak - skopiuj ją ze starego komputera" -ForegroundColor Yellow
}

Write-Host "Przygotowanie środowiska zakończone." -ForegroundColor Cyan
Write-Host "Po skopiowaniu prywatnych plików uruchom start.bat."
