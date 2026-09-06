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