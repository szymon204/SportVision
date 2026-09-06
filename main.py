from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from football_api import (
    get_premier_league_matches,  # Pobiera mecze z API.
    get_premier_league_teams,    # Pobiera drużyny z API.
    test_api_connection          # Sprawdza połączenie z API.
)
from database import (
    add_league,
    add_match,
    add_team,
    create_tables,
    get_leagues,
    get_matches,
    get_teams,
    get_league_id_by_api_id,
    get_team_id_by_api_id,
    match_exists
)

app = FastAPI(title="SportVision")

create_tables()

def calculate_standings(teams, matches):
    # Tutaj zapiszemy statystyki wszystkich drużyn.
    standings = {}

    # Tworzy pusty zestaw statystyk dla każdej drużyny.
    for team in teams:
        standings[team["name"]] = {
            "team": team["name"],
            "played": 0,
            "won": 0,
            "drawn": 0,
            "lost": 0,
            "goals_for": 0,
            "goals_against": 0,
            "goal_difference": 0,
            "points": 0
        }

    # Przechodzi przez wszystkie mecze zapisane w bazie.
    for football_match in matches:
        # Pobiera statystyki gospodarza i gościa.
        home = standings.get(football_match["home_team_name"])
        away = standings.get(football_match["away_team_name"])

        # Pomija mecz, jeżeli którejś drużyny nie ma na liście.
        if home is None or away is None:
            continue

        # Pobiera liczbę goli z danego meczu.
        home_goals = football_match["home_goals"]
        away_goals = football_match["away_goals"]

        # Zwiększa liczbę rozegranych meczów obu drużyn.
        home["played"] += 1
        away["played"] += 1

        # Dodaje gole strzelone i stracone przez gospodarza.
        home["goals_for"] += home_goals
        home["goals_against"] += away_goals

        # Dodaje gole strzelone i stracone przez gościa.
        away["goals_for"] += away_goals
        away["goals_against"] += home_goals

        # Sprawdza, czy wygrał gospodarz.
        if home_goals > away_goals:
            home["won"] += 1
            home["points"] += 3
            away["lost"] += 1

        # Sprawdza, czy wygrał gość.
        elif away_goals > home_goals:
            away["won"] += 1
            away["points"] += 3
            home["lost"] += 1

        # Jeżeli nikt nie wygrał, mecz zakończył się remisem.
        else:
            home["drawn"] += 1
            away["drawn"] += 1
            home["points"] += 1
            away["points"] += 1

    # Zamienia słownik drużyn na zwykłą listę.
    standings_list = list(standings.values())

    # Oblicza różnicę bramek każdej drużyny.
    for team in standings_list:
        team["goal_difference"] = (
            team["goals_for"] - team["goals_against"]
        )

    # Sortuje drużyny według punktów, bilansu i strzelonych goli.
    standings_list.sort(
        key=lambda team: (
            team["points"],
            team["goal_difference"],
            team["goals_for"]
        ),
        reverse=True
    )

    # Zwraca gotową tabelę ligową.
    return standings_list

@app.get("/", response_class=HTMLResponse)  # tworzenie aplikacji (zmienna app). Jak przeglądarka wykonuje GET to uruchamia funkcję znajdującą się poniżej.
def home():
    leagues = get_leagues()
    teams = get_teams()
    matches = get_matches()
        # Oblicza tabelę ligową na podstawie drużyn i wyników.
    standings = calculate_standings(teams, matches)

    # Tutaj powstanie kod HTML zawierający wiersze tabeli.
    standings_rows = ""

    # Numeruje drużyny, zaczynając od pierwszego miejsca.
    for position, standing in enumerate(standings, start=1):
        # Dodaje jeden wiersz z wynikami drużyny.
        standings_rows += f"""
        <tr>
            <td>{position}</td>
            <td>{standing['team']}</td>
            <td>{standing['played']}</td>
            <td>{standing['won']}</td>
            <td>{standing['drawn']}</td>
            <td>{standing['lost']}</td>
            <td>{standing['goals_for']}</td>
            <td>{standing['goals_against']}</td>
            <td>{standing['goal_difference']}</td>
            <td><strong>{standing['points']}</strong></td>
        </tr>
        """
    rows = ""
    team_rows = ""

    for league in leagues:
        rows += f"""
        <tr>
            <td>{league['id']}</td>
            <td>{league['name']}</td>
            <td>{league['country']}</td>
        </tr>
        """

    for team in teams:
        team_rows += f"""
        <tr>
            <td>{team['id']}</td>
            <td>{team['name']}</td>
            <td>{team['league_name']}</td>
        </tr>
        """

    match_rows = ""

    for football_match in matches:
        match_rows += f"""
        <tr>
            <td>{football_match['match_date']}</td>
            <td>{football_match['home_team_name']}</td>
            <td>{football_match['home_goals']} : {football_match['away_goals']}</td>
            <td>{football_match['away_team_name']}</td>
            <td>{football_match['league_name']}</td>
        </tr>
        """
    team_goals = {}

    for team in teams:
        team_goals[team["name"]] = 0

    for football_match in matches:
        team_goals[football_match["home_team_name"]] += football_match["home_goals"]
        team_goals[football_match["away_team_name"]] += football_match["away_goals"]

    max_goals = max(team_goals.values(), default=0)

    chart_rows = ""

    for team_name, goals in team_goals.items():
        if max_goals > 0:
            bar_width = goals / max_goals * 100
        else:
            bar_width = 0

        chart_rows += f"""
        <div class="chart-row">
            <div>{team_name}</div>

            <div class="chart-track">
                <div class="chart-bar" style="width: {bar_width}%"></div>
            </div>

            <div>{goals}</div>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="pl">
        <head>
            <meta charset="UTF-8">
            <title>SportVision</title>

            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 40px;
                    background-color: #f4f6f8;
                }}

                table {{
                    width: 600px;
                    border-collapse: collapse;
                    background-color: white;
                }}

                th, td {{
                    padding: 12px;
                    border: 1px solid #dddddd;
                    text-align: left;
                }}

                th {{
                    background-color: #1f7a4d;
                    color: white;
                }}

                .standings-table {{
                    width: 100%;
                    max-width: 1000px;
                }}

                .standings-table th,
                .standings-table td {{
                    text-align: center;
                }}

                               .standings-table th:nth-child(2),
                .standings-table td:nth-child(2) {{
                    text-align: left;
                }}

                .chart {{
                    width: 600px;
                }}

                .chart-row {{
                    display: grid;
                    grid-template-columns: 120px 1fr 40px;
                    align-items: center;
                    gap: 10px;
                    margin-bottom: 10px;
                }}

                .chart-track {{
                    height: 26px;
                    background-color: #dddddd;
                }}

                .chart-bar {{
                    height: 100%;
                    background-color: #1f7a4d;
                }}
            </style>
        </head>

        <body>
            <h1>SportVision</h1>
            <h2>Dostępne ligi</h2>

            <table>
                <tr>
                    <th>ID</th>
                    <th>Nazwa ligi</th>
                    <th>Kraj</th>
                </tr>

                {rows}
            </table>
            <h2>Drużyny</h2>

            <table>
                <tr>
                    <th>ID</th>
                    <th>Nazwa drużyny</th>
                    <th>Liga</th>
                </tr>

                {team_rows}
            </table>
                        <h2>Tabela ligowa</h2>

            <table class="standings-table">
                <tr>
                    <th>Poz.</th>
                    <th>Drużyna</th>
                    <th>M</th>
                    <th>W</th>
                    <th>R</th>
                    <th>P</th>
                    <th>GS</th>
                    <th>GSr</th>
                    <th>Bilans</th>
                    <th>Pkt</th>
                </tr>

                {standings_rows}
            </table>
            <h2>Mecze</h2>

            <table>
                <tr>
                    <th>Data</th>
                    <th>Gospodarz</th>
                    <th>Wynik</th>
                    <th>Gość</th>
                    <th>Liga</th>
                </tr>

                {match_rows}
            </table>
            <h2>Gole drużyn</h2>

            <div class="chart">
                {chart_rows}
            </div>
        </body>
    </html>
    """

@app.get("/leagues")
def leagues():
    return get_leagues()

@app.post("/leagues")
def create_league(api_id: int, name: str, country: str):
    add_league(api_id, name, country)

    return {
        "message": "Liga została dodana"
    }

@app.post("/teams")
def create_team(api_id: int, name: str, league_id: int):
    add_team(api_id, name, league_id)

    return {
        "message": "Drużyna została dodana"
    }

@app.get("/teams")
def teams():
    return get_teams()

@app.post("/matches")
def create_match(
    api_id: int,
    league_id: int,
    season: int,
    match_date: str,
    home_team_id: int,
    away_team_id: int,
    home_goals: int,
    away_goals: int
):
    add_match(
        api_id,
        league_id,
        season,
        match_date,
        home_team_id,
        away_team_id,
        home_goals,
        away_goals
    )

    return {
        "message": "Mecz został dodany"
    }

@app.get("/matches")
def matches():
    return get_matches()

@app.get("/api/test")
def api_test():
    return test_api_connection()

@app.post("/api/import-teams")
def import_teams():
    league_id = get_league_id_by_api_id(39)

    if league_id is None:
        return {
            "message": "Premier League nie istnieje w lokalnej bazie."
        }

    api_teams = get_premier_league_teams()

    for item in api_teams:
        team = item["team"]

        add_team(
            team["id"],
            team["name"],
            league_id
        )

    return {
        "message": "Import drużyn zakończony.",
        "teams_received": len(api_teams)
    }

@app.post("/api/import-matches")
def import_matches():
    # Odszukuje lokalne ID Premier League.
    league_id = get_league_id_by_api_id(39)

    # Przerywa import, jeżeli liga nie istnieje lokalnie.
    if league_id is None:
        return {
            "message": "Premier League nie istnieje w lokalnej bazie."
        }

    # Pobiera mecze Premier League z API.
    api_matches = get_premier_league_matches()

    # Informuje o problemie, jeżeli API nie zwróciło danych.
    if not api_matches:
        return {
            "message": "Nie pobrano meczów z API.",
            "matches_received": 0
        }

    # Liczy poprawnie zapisane mecze.
    added_matches = 0

    # Liczy pominięte mecze i duplikaty.
    skipped_matches = 0

    # Przechodzi kolejno przez każdy mecz zwrócony przez API.
    for item in api_matches:
        # Pobiera podstawowe informacje o spotkaniu.
        fixture = item["fixture"]

        # Pomija mecze, które nie mają statusu zakończonego spotkania.
        if fixture["status"]["short"] != "FT":
            continue

        # Pobiera zewnętrzny identyfikator gospodarza.
        home_api_id = item["teams"]["home"]["id"]

        # Pobiera zewnętrzny identyfikator gościa.
        away_api_id = item["teams"]["away"]["id"]

        # Zamienia zewnętrzne ID gospodarza na lokalne ID.
        home_team_id = get_team_id_by_api_id(home_api_id)

        # Zamienia zewnętrzne ID gościa na lokalne ID.
        away_team_id = get_team_id_by_api_id(away_api_id)

        # Pomija mecz, jeśli którejś drużyny nie ma w bazie.
        if home_team_id is None or away_team_id is None:
            skipped_matches += 1
            continue

        # Pobiera samą datę z pełnego zapisu czasu.
        match_date = fixture["date"][:10]

        # Pomija mecz, który został już wcześniej zapisany.
        if match_exists(match_date, home_team_id, away_team_id):
            skipped_matches += 1
            continue

        # Zapisuje zakończony mecz w lokalnej bazie.
        add_match(
            fixture["id"],             # Identyfikator meczu w API.
            league_id,                 # Lokalne ID ligi.
            2024,                      # Początek sezonu 2024/2025.
            match_date,                # Data spotkania.
            home_team_id,              # Lokalne ID gospodarza.
            away_team_id,              # Lokalne ID gościa.
            item["goals"]["home"],      # Gole gospodarza.
            item["goals"]["away"]       # Gole gościa.
        )

        # Zwiększa licznik zapisanych spotkań.
        added_matches += 1

    # Zwraca krótkie podsumowanie importu.
    return {
        "message": "Import meczów zakończony.",
        "matches_received": len(api_matches),
        "matches_added": added_matches,
        "matches_skipped": skipped_matches
    }

@app.get("/standings")
def standings():
    # Pobiera drużyny z lokalnej bazy SQLite.
    teams = get_teams()

    # Pobiera rozegrane mecze z lokalnej bazy.
    matches = get_matches()

    # Oblicza i zwraca aktualną tabelę ligową.
    return calculate_standings(teams, matches)

#python -m uvicorn main:app --reload
