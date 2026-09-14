from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from football_api import (
    get_api_matches,     # Pobiera mecze wskazanej ligi.
    get_api_teams,       # Pobiera drużyny wskazanej ligi.
    test_api_connection  # Sprawdza połączenie z API.
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
    match_exists,
    add_default_leagues
)

app = FastAPI(title="SportVision")

create_tables() #tworzenie tabel

add_default_leagues() #dodanie lig

def calculate_standings(teams, matches):
    # Tutaj zapiszemy statystyki wszystkich drużyn.
    standings = {}

    # Tworzy pusty zestaw statystyk dla każdej drużyny.
    for team in teams:
        standings[team["name"]] = {
            "team_id": team["id"],
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
def home(league_id: int = 1):
    # Pobiera wszystkie ligi z lokalnej bazy.
    leagues = get_leagues()

    # Pobiera wszystkie drużyny przed filtrowaniem.
    all_teams = get_teams()

    # Pobiera wszystkie mecze przed filtrowaniem.
    all_matches = get_matches()

    # Tutaj zapiszemy drużyny należące do wybranej ligi.
    teams = []

    # Wybiera tylko drużyny z odpowiednim league_id.
    for team in all_teams:
        if team["league_id"] == league_id:
            teams.append(team)

    # Tutaj zapiszemy mecze należące do wybranej ligi.
    matches = []

    # Wybiera tylko mecze z odpowiednim league_id.
    for football_match in all_matches:
        if football_match["league_id"] == league_id:
            matches.append(football_match)
        # Oblicza tabelę ligową na podstawie drużyn i wyników.
    standings = calculate_standings(teams, matches)

        # Tutaj powstaną opcje widoczne na liście lig.
    league_options = ""

    # Domyślna nazwa używana dla niepoprawnego ID.
    selected_league_name = "Nieznana liga"

    # Przechodzi przez wszystkie dostępne ligi.
    for league in leagues:
        # Domyślnie opcja nie jest zaznaczona.
        selected_attribute = ""

        # Zaznacza aktualnie wybraną ligę.
        if league["id"] == league_id:
            selected_attribute = "selected"
            selected_league_name = league["name"]

        # Dodaje ligę jako opcję formularza HTML.
        league_options += f"""
        <option value="{league['id']}" {selected_attribute}>
            {league['name']}
        </option>
        """

    # Tutaj powstanie kod HTML zawierający wiersze tabeli.
    standings_rows = ""

    # Numeruje drużyny, zaczynając od pierwszego miejsca.
    for position, standing in enumerate(standings, start=1):
        # Dodaje jeden wiersz z wynikami drużyny.
        standings_rows += f"""
        <tr>
            <td>{position}</td>
            <td><a href="/teams/{standing['team_id']}">{standing['team']}</a></td>
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
            <td><a href="/teams/{team['id']}">{team['name']}</a></td>
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

                                .league-form {{
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    margin-bottom: 25px;
                                }}

                select,
                button {{
                    padding: 10px;
                    border: 1px solid #cccccc;
                    border-radius: 5px;
                    font-size: 16px;
                }}

                button {{
                    background-color: #1f7a4d;
                    color: white;
                    border: none;
                    cursor: pointer;
                }}
            </style>
        </head>

        <body>
            <h1>SportVision</h1>
                <form class="league-form" method="get" action="/">
                <label for="league_id">Wybierz ligę:</label>

                <select id="league_id" name="league_id">
                    {league_options}
                </select>

                <button type="submit">Pokaż</button>
            </form>

            <h2>Dostępne ligi</h2>

            <table>
                <tr>
                    <th>ID</th>
                    <th>Nazwa ligi</th>
                    <th>Kraj</th>
                </tr>

                {rows}
            </table>
            <h2>Drużyny – {selected_league_name}</h2>

            <table>
                <tr>
                    <th>ID</th>
                    <th>Nazwa drużyny</th>
                    <th>Liga</th>
                </tr>

                {team_rows}
            </table>
            <h2>Tabela ligowa – {selected_league_name}</h2>

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
            <h2>Mecze – {selected_league_name}</h2>

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
            <h2>Gole drużyn – {selected_league_name}</h2>

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

@app.post("/api/import-teams/{league_api_id}")
def import_teams(league_api_id: int, season: int = 2024):
    # Szuka lokalnego ID ligi na podstawie ID z API.
    local_league_id = get_league_id_by_api_id(league_api_id)

    # Przerywa import, jeżeli liga nie istnieje lokalnie.
    if local_league_id is None:
        return {
            "message": "Wybrana liga nie istnieje w lokalnej bazie."
        }

    # Pobiera drużyny wybranej ligi i sezonu.
    api_teams = get_api_teams(league_api_id, season)

    # Informuje, jeżeli API nie zwróciło drużyn.
    if not api_teams:
        return {
            "message": "Nie pobrano drużyn z API.",
            "teams_received": 0
        }

    # Przechodzi przez wszystkie otrzymane drużyny.
    for item in api_teams:
        # Pobiera właściwe dane drużyny z odpowiedzi API.
        team = item["team"]

        # Zapisuje drużynę w lokalnej bazie SQLite.
        add_team(
            team["id"],
            team["name"],
            local_league_id
        )

    # Zwraca podsumowanie zakończonego importu.
    return {
        "message": "Import drużyn zakończony.",
        "league_api_id": league_api_id,
        "season": season,
        "teams_received": len(api_teams)
    }

@app.post("/api/import-matches/{league_api_id}")
def import_matches(league_api_id: int, season: int = 2024):
    # Szuka lokalnego ID ligi na podstawie ID z API.
    local_league_id = get_league_id_by_api_id(league_api_id)

    # Przerywa import, jeżeli liga nie istnieje lokalnie.
    if local_league_id is None:
        return {
            "message": "Wybrana liga nie istnieje w lokalnej bazie."
        }

    # Pobiera mecze wybranej ligi i sezonu.
    api_matches = get_api_matches(league_api_id, season)

    # Informuje, jeżeli API nie zwróciło meczów.
    if not api_matches:
        return {
            "message": "Nie pobrano meczów z API.",
            "matches_received": 0
        }

    # Liczy poprawnie zapisane mecze.
    added_matches = 0

    # Liczy pominięte mecze oraz duplikaty.
    skipped_matches = 0

    # Przechodzi przez każdy mecz otrzymany z API.
    for item in api_matches:
        # Pobiera podstawowe informacje o spotkaniu.
        fixture = item["fixture"]

        # Pomija mecze, które nie zostały zakończone.
        if fixture["status"]["short"] != "FT":
            continue

        # Pobiera zewnętrzne identyfikatory obu drużyn.
        home_api_id = item["teams"]["home"]["id"]
        away_api_id = item["teams"]["away"]["id"]

        # Zamienia identyfikatory API na lokalne ID.
        home_team_id = get_team_id_by_api_id(home_api_id)
        away_team_id = get_team_id_by_api_id(away_api_id)

        # Pomija mecz, jeżeli którejś drużyny nie ma w bazie.
        if home_team_id is None or away_team_id is None:
            skipped_matches += 1
            continue

        # Pobiera datę bez godziny i strefy czasowej.
        match_date = fixture["date"][:10]

        # Pomija mecz, jeżeli jest już zapisany.
        if match_exists(match_date, home_team_id, away_team_id):
            skipped_matches += 1
            continue

        # Zapisuje zakończony mecz w lokalnej bazie.
        add_match(
            fixture["id"],             # ID meczu nadane przez API.
            local_league_id,           # Lokalne ID wybranej ligi.
            season,                    # Wybrany sezon.
            match_date,                # Data rozegrania meczu.
            home_team_id,              # Lokalne ID gospodarza.
            away_team_id,              # Lokalne ID gościa.
            item["goals"]["home"],      # Gole gospodarza.
            item["goals"]["away"]       # Gole gościa.
        )

        # Zwiększa licznik zapisanych spotkań.
        added_matches += 1

    # Zwraca podsumowanie importu.
    return {
        "message": "Import meczów zakończony.",
        "league_api_id": league_api_id,
        "season": season,
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

@app.get("/teams/{team_id}/summary")
def team_summary(team_id: int):
    # Pobiera wszystkie drużyny z lokalnej bazy.
    teams = get_teams()

    # Pobiera wszystkie zapisane mecze.
    matches = get_matches()

    # Oblicza aktualne statystyki drużyn.
    standings = calculate_standings(teams, matches)

    # Tutaj zapiszemy znalezioną drużynę.
    selected_team = None

    # Szuka drużyny o identyfikatorze podanym w adresie.
    for team in teams:
        if team["id"] == team_id:
            selected_team = team
            break

    # Kończy działanie, jeżeli drużyna nie istnieje.
    if selected_team is None:
        return {
            "message": "Nie znaleziono drużyny."
        }

    # Tutaj zapiszemy statystyki wybranej drużyny.
    selected_statistics = None

    # Szuka statystyk na podstawie nazwy drużyny.
    for standing in standings:
        if standing["team"] == selected_team["name"]:
            selected_statistics = standing
            break

    # Tutaj powstanie lista meczów wybranej drużyny.
    selected_matches = []

    # Przechodzi przez wszystkie zapisane mecze.
    for football_match in matches:
        # Sprawdza, czy drużyna była gospodarzem.
        played_at_home = (
            football_match["home_team_name"] == selected_team["name"]
        )

        # Sprawdza, czy drużyna była gościem.
        played_away = (
            football_match["away_team_name"] == selected_team["name"]
        )

        # Dodaje mecz, jeśli uczestniczyła w nim wybrana drużyna.
        if played_at_home or played_away:
            selected_matches.append(football_match)

    # Zwraca dane drużyny, jej statystyki i rozegrane mecze.
    return {
        "team": selected_team,
        "statistics": selected_statistics,
        "matches": selected_matches
    }

@app.get("/teams/{team_id}", response_class=HTMLResponse)
def team_page(team_id: int):
    # Wykorzystuje działający endpoint do pobrania danych drużyny.
    summary = team_summary(team_id)

    # Wyświetla prosty komunikat, jeżeli drużyna nie istnieje.
    if "message" in summary:
        return HTMLResponse(
            content="<h1>Nie znaleziono drużyny</h1>",
            status_code=404
        )

    # Wyciąga podstawowe dane z przygotowanego podsumowania.
    team = summary["team"]
    statistics = summary["statistics"]
    matches = summary["matches"]

    # Tutaj powstaną wiersze tabeli z meczami.
    match_rows = ""

    # Przechodzi przez mecze wybranej drużyny.
    for football_match in matches:
        # Sprawdza, czy wybrana drużyna grała jako gospodarz.
        played_at_home = (
            football_match["home_team_name"] == team["name"]
        )

        # Ustala przeciwnika i miejsce rozegrania meczu.
        if played_at_home:
            opponent = football_match["away_team_name"]
            location = "Dom"
            team_goals = football_match["home_goals"]
            opponent_goals = football_match["away_goals"]
        else:
            opponent = football_match["home_team_name"]
            location = "Wyjazd"
            team_goals = football_match["away_goals"]
            opponent_goals = football_match["home_goals"]

        # Ustala tekst i kolor rezultatu.
        if team_goals > opponent_goals:
            result = "Wygrana"
            result_class = "win"
        elif team_goals < opponent_goals:
            result = "Porażka"
            result_class = "loss"
        else:
            result = "Remis"
            result_class = "draw"

        # Dodaje jeden mecz do tabeli.
        match_rows += f"""
        <tr>
            <td>{football_match['match_date']}</td>
            <td>{opponent}</td>
            <td>{location}</td>
            <td>{team_goals} : {opponent_goals}</td>
            <td class="{result_class}">{result}</td>
        </tr>
        """

    # Zwraca gotową stronę HTML wybranej drużyny.
    return f"""
    <!DOCTYPE html>
    <html lang="pl">
        <head>
            <meta charset="UTF-8">
            <title>{team['name']} – SportVision</title>

            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 40px;
                    background-color: #f4f6f8;
                    color: #202124;
                }}

                .container {{
                    max-width: 1000px;
                    margin: 0 auto;
                }}

                .back-link {{
                    color: #1f7a4d;
                    text-decoration: none;
                }}

                .cards {{
                    display: flex;
                    flex-wrap: wrap;
                    gap: 15px;
                    margin: 25px 0;
                }}

                .card {{
                    min-width: 120px;
                    padding: 20px;
                    background-color: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 8px #dddddd;
                    text-align: center;
                }}

                .card strong {{
                    display: block;
                    margin-top: 8px;
                    font-size: 24px;
                    color: #1f7a4d;
                }}

                table {{
                    width: 100%;
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

                .win {{
                    color: green;
                    font-weight: bold;
                }}

                .draw {{
                    color: #b26a00;
                    font-weight: bold;
                }}

                .loss {{
                    color: #c62828;
                    font-weight: bold;
                }}
            </style>
        </head>

        <body>
            <div class="container">
                <a class="back-link" href="/?league_id={team['league_id']}">
                    ← Powrót do ligi
                </a>
                <h1>{team['name']}</h1>
                <p>Liga: {team['league_name']}</p>

                <div class="cards">
                    <div class="card">
                        Mecze
                        <strong>{statistics['played']}</strong>
                    </div>

                    <div class="card">
                        Punkty
                        <strong>{statistics['points']}</strong>
                    </div>

                    <div class="card">
                        Wygrane
                        <strong>{statistics['won']}</strong>
                    </div>

                    <div class="card">
                        Gole
                        <strong>{statistics['goals_for']}</strong>
                    </div>
                </div>

                <h2>Mecze drużyny</h2>

                <table>
                    <tr>
                        <th>Data</th>
                        <th>Przeciwnik</th>
                        <th>Miejsce</th>
                        <th>Wynik</th>
                        <th>Rezultat</th>
                    </tr>

                    {match_rows}
                </table>
            </div>
        </body>
    </html>
    """

@app.get("/comparison")
def compare_teams(first_team_id: int, second_team_id: int):
    # Nie pozwala porównywać drużyny z samą sobą.
    if first_team_id == second_team_id:
        return {
            "message": "Wybierz dwie różne drużyny."
        }

    # Pobiera podsumowanie pierwszej drużyny.
    first_team_summary = team_summary(first_team_id)

    # Pobiera podsumowanie drugiej drużyny.
    second_team_summary = team_summary(second_team_id)

    # Sprawdza, czy pierwsza drużyna istnieje.
    if "message" in first_team_summary:
        return {
            "message": "Nie znaleziono pierwszej drużyny."
        }

    # Sprawdza, czy druga drużyna istnieje.
    if "message" in second_team_summary:
        return {
            "message": "Nie znaleziono drugiej drużyny."
        }

    # Pobiera podstawowe dane pierwszej drużyny.
    first_team = first_team_summary["team"]

    # Pobiera podstawowe dane drugiej drużyny.
    second_team = second_team_summary["team"]

    # Nie pozwala porównywać drużyn z różnych lig.
    if first_team["league_id"] != second_team["league_id"]:
        return {
            "message": "Drużyny muszą należeć do tej samej ligi."
        }

    # Pobiera statystyki pierwszej drużyny.
    first_statistics = first_team_summary["statistics"]

    # Pobiera statystyki drugiej drużyny.
    second_statistics = second_team_summary["statistics"]

    # Ustala drużynę mającą więcej punktów.
    if first_statistics["points"] > second_statistics["points"]:
        points_leader = first_team["name"]
    elif second_statistics["points"] > first_statistics["points"]:
        points_leader = second_team["name"]
    else:
        points_leader = "Remis"

    # Zwraca dane potrzebne do późniejszego wykresu.
    return {
        "league": first_team["league_name"],
        "first_team": {
            "id": first_team["id"],
            "name": first_team["name"],
            "statistics": first_statistics
        },
        "second_team": {
            "id": second_team["id"],
            "name": second_team["name"],
            "statistics": second_statistics
        },
        "points_leader": points_leader
    }

#python -m uvicorn main:app --reload
