# SportVision

SportVision to prosta aplikacja internetowa służąca do prezentowania i porównywania statystyk drużyn piłkarskich.

Projekt powstaje jako praca inżynierska. Jego głównym założeniem jest czytelność kodu, lokalne przechowywanie danych oraz możliwość działania bez internetu po wcześniejszym pobraniu danych.

## Najważniejsze funkcje

- obsługa pięciu najważniejszych lig europejskich,
- pobieranie drużyn i meczów z API-Football,
- zapisywanie danych w lokalnej bazie SQLite,
- wyświetlanie tabeli ligowej,
- prezentowanie wyników meczów,
- wykres liczby strzelonych goli,
- strony ze statystykami drużyn,
- porównywanie dwóch drużyn,
- działanie offline na wcześniej zapisanych danych.

## Technologie

- Python,
- FastAPI,
- SQLite,
- HTML,
- CSS,
- API-Football.

## Uruchomienie projektu

### 1. Utworzenie środowiska wirtualnego

W terminalu PowerShell, w głównym folderze projektu, wykonaj:

```powershell
python -m venv .venv
```

### 2. Aktywowanie środowiska

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Instalacja bibliotek

```powershell
pip install -r requirements.txt
```

### 4. Konfiguracja klucza API

W głównym folderze projektu należy utworzyć lokalny plik `.env` i umieścić w nim klucz API-Football.

Plik `.env` nie jest wysyłany do repozytorium GitHub.

### 5. Uruchomienie aplikacji

```powershell
uvicorn main:app --reload
```

Po uruchomieniu aplikacja jest dostępna pod adresem:

```text
http://127.0.0.1:8000
```

Dokumentacja endpointów FastAPI znajduje się pod adresem:

```text
http://127.0.0.1:8000/docs
```

## Działanie bez internetu

Po pobraniu danych z API ligi, drużyny i mecze są zapisywane w lokalnej bazie SQLite.

Internet jest potrzebny podczas importowania nowych danych. Przeglądanie wcześniej pobranych danych nie wymaga połączenia z internetem.

## Najważniejsze pliki

- `main.py` – endpointy FastAPI, obliczenia statystyk i strony HTML,
- `database.py` – tworzenie i obsługa bazy SQLite,
- `football_api.py` – pobieranie danych z API-Football,
- `static/style.css` – wygląd aplikacji,
- `requirements.txt` – lista wymaganych bibliotek.

## Status projektu

Projekt jest rozwijany małymi krokami. Obecna wersja działa lokalnie i wykorzystuje dane historyczne z sezonu 2024/2025.