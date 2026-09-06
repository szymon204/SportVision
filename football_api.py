import os

import requests
from dotenv import load_dotenv


BASE_URL = "https://v3.football.api-sports.io"

load_dotenv()


def test_api_connection():
    api_key = os.getenv("API_FOOTBALL_KEY")

    if not api_key:
        return {
            "connected": False,
            "message": "Nie znaleziono klucza API."
        }

    try:
        response = requests.get(
            f"{BASE_URL}/countries",
            headers={
                "x-apisports-key": api_key
            },
            timeout=10
        )

        response.raise_for_status()
        data = response.json()

    except requests.RequestException:
        return {
            "connected": False,
            "message": "Nie udało się połączyć z API."
        }

    if data.get("errors"):
        return {
            "connected": False,
            "message": "API odrzuciło zapytanie."
        }

    return {
        "connected": True,
        "countries": data.get("results", 0)
    }

def get_premier_league_teams():
    api_key = os.getenv("API_FOOTBALL_KEY")

    if not api_key:
        return []

    try:
        response = requests.get(
            f"{BASE_URL}/teams",
            headers={
                "x-apisports-key": api_key
            },
            params={
                "league": 39, #identyfikator Premier League
                "season": 2024
            },
            timeout=10
        )

        response.raise_for_status()
        data = response.json()

    except requests.RequestException:
        return []

    if data.get("errors"):
        return []

    return data.get("response", [])

def get_premier_league_matches():
    # Pobiera klucz API z lokalnego pliku .env.
    api_key = os.getenv("API_FOOTBALL_KEY")

    # Kończy działanie, jeżeli nie znaleziono klucza.
    if not api_key:
        return []

    try:
        # Wysyła zapytanie o mecze Premier League w sezonie 2024/2025.
        response = requests.get(
            f"{BASE_URL}/fixtures",
            headers={
                # Przekazuje klucz w wymaganym nagłówku.
                "x-apisports-key": api_key
            },
            params={
                # 39 jest identyfikatorem Premier League.
                "league": 39,
                # Sezon 2024 oznacza rozgrywki 2024/2025.
                "season": 2024
            },
            # Przerywa oczekiwanie po maksymalnie 30 sekundach.
            timeout=30
        )

        # Zgłasza błąd, jeżeli serwer zwrócił niepoprawny status HTTP.
        response.raise_for_status()

        # Zamienia odpowiedź JSON na dane Pythona.
        data = response.json()

    except requests.RequestException:
        # Zwraca pustą listę, gdy wystąpi problem z połączeniem.
        return []

    # Sprawdza, czy API zgłosiło błąd w treści odpowiedzi.
    if data.get("errors"):
        return []

    # Zwraca listę meczów albo pustą listę.
    return data.get("response", [])