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

def get_api_teams(league_api_id: int, season: int):
    # Pobiera klucz API zapisany lokalnie.
    api_key = os.getenv("API_FOOTBALL_KEY")

    # Kończy działanie, jeżeli nie znaleziono klucza.
    if not api_key:
        return []

    try:
        # Wysyła zapytanie o drużyny wybranej ligi i sezonu.
        response = requests.get(
            f"{BASE_URL}/teams",
            headers={
                "x-apisports-key": api_key
            },
            params={
                "league": league_api_id,
                "season": season
            },
            timeout=10
        )

        # Zgłasza błąd dla niepoprawnego statusu HTTP.
        response.raise_for_status()

        # Zamienia odpowiedź JSON na dane Pythona.
        data = response.json()

    except requests.RequestException:
        # Zwraca pustą listę w przypadku problemu z połączeniem.
        return []

    # Sprawdza, czy API zgłosiło błąd w odpowiedzi.
    if data.get("errors"):
        return []

    # Zwraca listę drużyn otrzymanych z API.
    return data.get("response", [])

def get_api_matches(league_api_id: int, season: int):
    # Pobiera klucz API zapisany lokalnie.
    api_key = os.getenv("API_FOOTBALL_KEY")

    # Kończy działanie, jeżeli nie znaleziono klucza.
    if not api_key:
        return []

    try:
        # Wysyła zapytanie o mecze wybranej ligi i sezonu.
        response = requests.get(
            f"{BASE_URL}/fixtures",
            headers={
                "x-apisports-key": api_key
            },
            params={
                "league": league_api_id,
                "season": season
            },
            timeout=30
        )

        # Zgłasza błąd dla niepoprawnego statusu HTTP.
        response.raise_for_status()

        # Zamienia odpowiedź JSON na dane Pythona.
        data = response.json()

    except requests.RequestException:
        # Zwraca pustą listę w przypadku problemu z połączeniem.
        return []

    # Sprawdza, czy API zgłosiło błąd w odpowiedzi.
    if data.get("errors"):
        return []

    # Zwraca listę meczów otrzymanych z API.
    return data.get("response", [])