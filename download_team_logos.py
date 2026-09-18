from pathlib import Path

import requests

from database import get_teams


# Określa folder, w którym zapiszemy herby drużyn.
LOGO_DIRECTORY = Path(__file__).parent / "static" / "logos" / "teams"

# Tworzy folder wraz z brakującymi folderami nadrzędnymi.
LOGO_DIRECTORY.mkdir(parents=True, exist_ok=True)

# Pobiera wszystkie drużyny z lokalnej bazy SQLite.
teams = get_teams()

# Przechodzi kolejno przez każdą drużynę.
for team in teams:
    # Pobiera identyfikator drużyny używany przez API-Football.
    team_api_id = team["api_id"]

    # Buduje lokalną ścieżkę, np. static/logos/teams/42.png.
    logo_path = LOGO_DIRECTORY / f"{team_api_id}.png"

    # Pomija logo, jeżeli zostało już wcześniej pobrane.
    if logo_path.exists():
        continue

    # Buduje adres grafiki na podstawie api_id drużyny.
    logo_url = (
        f"https://media.api-sports.io/football/teams/{team_api_id}.png"
    )

    try:
        # Pobiera grafikę z limitem oczekiwania wynoszącym 10 sekund.
        response = requests.get(logo_url, timeout=10)

        # Zgłasza błąd, jeżeli serwer nie zwrócił poprawnej odpowiedzi.
        response.raise_for_status()

        # Zapisuje pobraną grafikę jako lokalny plik PNG.
        logo_path.write_bytes(response.content)

        print(f"Pobrano logo: {team['name']}")

    except requests.RequestException:
        # Nie zatrzymuje całego skryptu, jeśli zabraknie jednego logo.
        print(f"Nie udało się pobrać logo: {team['name']}")

print("Zakończono pobieranie herbów drużyn.")