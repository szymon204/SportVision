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