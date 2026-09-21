from pathlib import Path #udostępnianie folderu static.
from fastapi.staticfiles import StaticFiles #udostępnianie folderu static.
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from football_api import (get_api_matches, get_api_teams, test_api_connection)
from database import (add_league, add_match, add_team, create_tables, get_leagues, get_matches, get_teams, get_league_id_by_api_id, get_team_id_by_api_id, match_exists, add_default_leagues)

STATIC_DIRECTORY = Path(__file__).parent / "static" #wskazuje folder CSS niezależnie od miejsca uruchomienia programu.

app = FastAPI(title="SportVision")

#udostępnia pliki CSS pod adresem /static.
#odczytanie folderu static.
app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIRECTORY),
    name="static"
)

create_tables() #tworzenie tabel

add_default_leagues() #dodanie lig

def calculate_standings(teams, matches):
    # Tutaj zapiszemy statystyki wszystkich drużyn.
    standings = {}

    # Tworzy pusty zestaw statystyk dla każdej drużyny.
    for team in teams:
        standings[team["name"]] = {
            "team_id": team["id"], #każdy wiersz przechowuje team id do otwarcia strony drużyny.
            "team_api_id": team["api_id"], #każdy wiersz przechowuje team api id potrzebne do znalezienia herbu.
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
def home(league_id: int = 1, liczba_meczow: int = 10):
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

    if liczba_meczow == 0: #0 - użytkownik chce zobaczyć wszystkie mecze
        ostatnie_mecze = matches
        naglowek_meczow = "Wszystkie mecze"
    else:
        ostatnie_mecze = matches[:liczba_meczow]
        naglowek_meczow = f"{liczba_meczow} ostatnich meczów"

        # Tutaj powstaną opcje widoczne na liście lig.
    league_options = ""

    # Domyślna nazwa używana dla niepoprawnego ID.
    selected_league_name = "Nieznana liga"

    # Przechowuje identyfikator API potrzebny do znalezienia pliku logo.
    selected_league_api_id = 39

    # Przechodzi przez wszystkie dostępne ligi.
    for league in leagues:
        # Domyślnie opcja nie jest zaznaczona.
        selected_attribute = ""

        # Zaznacza aktualnie wybraną ligę.
        if league["id"] == league_id:
            selected_attribute = "selected"
            selected_league_name = league["name"]
            selected_league_api_id = league["api_id"]

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
            <td>
                <a
                    class="team-table-link"
                    href="/teams/{standing['team_id']}"
                >
                    <img
                        class="table-team-logo"
                        src="/static/logos/teams/{standing['team_api_id']}.png"
                        alt=""
                    >
                    <span>{standing['team']}</span>
                </a>
            </td>
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

    # Tutaj powstaną wiersze tabeli z ostatnimi meczami.
    wiersze_meczow = ""

    # Tworzy wiersz tabeli dla każdego wybranego meczu.
    for mecz in ostatnie_mecze:
        wiersze_meczow += f"""
        <tr>
            <td>{mecz['match_date']}</td>
            <td>{mecz['home_team_name']}</td>
            <td>{mecz['home_goals']} : {mecz['away_goals']}</td>
            <td>{mecz['away_team_name']}</td>
            <td>{mecz['league_name']}</td>
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
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>SportVision</title>
            <link rel="stylesheet" href="/static/style.css">
        </head>

        <body class="home-page">
            <div class="home-container">
                <header class="hero">
                    <h1>SportVision</h1>
                </header>

                <section class="summary-cards">
                    <div class="summary-card">
                        <span>Dostępne ligi</span>
                        <strong>{len(leagues)}</strong>
                    </div>
                    <div class="summary-card">
                        <span>Drużyny w lidze</span>
                        <strong>{len(teams)}</strong>
                    </div>
                    <div class="summary-card">
                        <span>Rozegrane mecze</span>
                        <strong>{len(matches)}</strong>
                    </div>
                </section>

                <div class="home-actions">
                    <form class="league-form" method="get" action="/">
                        <label for="league_id">Wybierz ligę:</label>
                        <select id="league_id" name="league_id">
                            {league_options}
                        </select>
                        <input
                            type="hidden"
                            name="liczba_meczow"
                            value="{liczba_meczow}"
                        >
                        <button type="submit">Pokaż</button>
                    </form>

                    <a
                        class="comparison-link"
                        href="/compare?league_id={league_id}"
                    >
                        Porównaj drużyny
                    </a>
                </div>

                <h2 class="league-heading">
                    <img
                        class="league-logo"
                        src="/static/logos/leagues/{selected_league_api_id}.png"
                        alt="Logo ligi {selected_league_name}"
                    >
                    Tabela ligowa – {selected_league_name}
                </h2>

                <div class="table-wrapper">
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
                </div>

                <h2>Gole drużyn – {selected_league_name}</h2>
                <div class="chart">
                    {chart_rows}
                </div>

                <h2>{naglowek_meczow} - {selected_league_name}</h2>
                <div class="table-wrapper">
                    <table>
                        <tr>
                            <th>Data</th>
                            <th>Gospodarz</th>
                            <th>Wynik</th>
                            <th>Gość</th>
                            <th>Liga</th>
                        </tr>
                        {wiersze_meczow}
                    </table>
                </div>
                <div class="match-limit">
                    <span>Pokaż mecze:</span>
                    <a href="/?league_id={league_id}&liczba_meczow=10">10</a>
                    <a href="/?league_id={league_id}&liczba_meczow=30">30</a>
                    <a href="/?league_id={league_id}&liczba_meczow=0">Wszystkie</a>
                </div>
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

    # Tutaj zapiszemy wyniki pięciu ostatnich meczów.
    forma = []

        # Sprawdza pięć ostatnich spotkań wybranej drużyny.
    for mecz in matches[:5]:
        # Sprawdza, czy wybrana drużyna była gospodarzem.
        czy_gospodarz = mecz["home_team_name"] == team["name"]

        # Pobiera gole właściwej drużyny i jej przeciwnika.
        if czy_gospodarz:
            gole_druzyny = mecz["home_goals"]
            gole_przeciwnika = mecz["away_goals"]
        else:
            gole_druzyny = mecz["away_goals"]
            gole_przeciwnika = mecz["home_goals"]

        # Forma z 5 ostatnich meczy rezultat.
        if gole_druzyny > gole_przeciwnika:
            forma.append('<span class="win">W</span>') #dodaje zieloną literę W przy użyciu klasy CSS "win".
        elif gole_druzyny < gole_przeciwnika:
            forma.append('<span class="loss">P</span>') #czerwona litera P przy użyciu klasy CSS "loss".
        else:
            forma.append('<span class="draw">R</span>') #pomarańczowa litera R przy użyciu klasy CSS "draw".

    # Łączy litery w jeden napis, na przykład: W W R P W.
    tekst_formy = " ".join(forma)

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
            <link rel="stylesheet" href="/static/style.css">
        </head>

        <body class="team-page">
            <div class="container">
                <a class="back-link" href="/?league_id={team['league_id']}">
                    ← Powrót do ligi
                </a>
                <div class="team-header">
                    <img
                        class="team-logo"
                        src="/static/logos/teams/{team['api_id']}.png"
                        alt="Herb drużyny {team['name']}"
                    >

                    <div>
                        <h1>{team['name']}</h1>
                        <p>Liga: {team['league_name']}</p>
                    </div>
                </div>

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

                    <div class="card">
                        Forma (5 meczów)
                        <strong>{tekst_formy}</strong>
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

@app.get("/compare", response_class=HTMLResponse)
def comparison_page(
    league_id: int = 1,
    first_team_id: int = 0,
    second_team_id: int = 0
):
    # Pobiera wszystkie ligi z lokalnej bazy.
    leagues = get_leagues()

    # Pobiera wszystkie drużyny przed filtrowaniem.
    all_teams = get_teams()

    # Tutaj zapiszemy drużyny wybranej ligi.
    league_teams = []

    # Wybiera drużyny należące do wskazanej ligi.
    for team in all_teams:
        if team["league_id"] == league_id:
            league_teams.append(team)

    # Tutaj powstaną opcje wyboru ligi.
    league_options = ""

    # Domyślna nazwa dla niepoprawnego ID ligi.
    selected_league_name = "Nieznana liga"

    # Buduje listę lig widoczną w formularzu.
    for league in leagues:
        # Domyślnie opcja nie jest zaznaczona.
        selected_attribute = ""

        # Zaznacza aktualnie wybraną ligę.
        if league["id"] == league_id:
            selected_attribute = "selected"
            selected_league_name = league["name"]
            selected_league_api_id = league["api_id"]

        # Dodaje ligę do elementu select.
        league_options += f"""
        <option value="{league['id']}" {selected_attribute}>
            {league['name']}
        </option>
        """

    # Dodaje początkową opcję pierwszej drużyny.
    first_team_options = """
    <option value="0">Wybierz pierwszą drużynę</option>
    """

    # Dodaje początkową opcję drugiej drużyny.
    second_team_options = """
    <option value="0">Wybierz drugą drużynę</option>
    """

    # Buduje listy drużyn należących do wybranej ligi.
    for team in league_teams:
        # Sprawdza, czy jest to wybrana pierwsza drużyna.
        first_selected = ""

        if team["id"] == first_team_id:
            first_selected = "selected"

        # Sprawdza, czy jest to wybrana druga drużyna.
        second_selected = ""

        if team["id"] == second_team_id:
            second_selected = "selected"

        # Dodaje drużynę do pierwszego pola wyboru.
        first_team_options += f"""
        <option value="{team['id']}" {first_selected}>
            {team['name']}
        </option>
        """

        # Dodaje drużynę do drugiego pola wyboru.
        second_team_options += f"""
        <option value="{team['id']}" {second_selected}>
            {team['name']}
        </option>
        """

    # Wyświetla instrukcję przed wyborem dwóch drużyn.
    comparison_html = """
    <p class="information">
        Wybierz dwie drużyny, aby zobaczyć porównanie.
    </p>
    """

    # Tworzy porównanie dopiero po wybraniu obu drużyn.
    if first_team_id > 0 and second_team_id > 0:
        # Wykorzystuje działający endpoint porównania.
        comparison = compare_teams(
            first_team_id,
            second_team_id
        )

        # Wyświetla komunikat, jeśli porównanie jest niemożliwe.
        if "message" in comparison:
            comparison_html = f"""
            <p class="error">{comparison['message']}</p>
            """

        else:
            # Pobiera dane i statystyki pierwszej drużyny.
            first_team = comparison["first_team"]
            first_statistics = first_team["statistics"]

            # Pobiera dane i statystyki drugiej drużyny.
            second_team = comparison["second_team"]
            second_statistics = second_team["statistics"]

            # Określa statystyki pokazywane na wykresach.
            metrics = [
                ("Punkty", "points"),
                ("Wygrane", "won"),
                ("Gole strzelone", "goals_for")
            ]

            # Tutaj powstaną kolejne sekcje wykresu.
            metric_rows = ""

            # Tworzy wykres dla każdej statystyki.
            for metric_name, metric_key in metrics:
                # Pobiera wartość pierwszej drużyny.
                first_value = first_statistics[metric_key]

                # Pobiera wartość drugiej drużyny.
                second_value = second_statistics[metric_key]

                # Znajduje większą wartość potrzebną do skali.
                maximum_value = max(
                    first_value,
                    second_value,
                    1
                )

                # Oblicza szerokość pierwszego słupka w procentach.
                first_width = first_value / maximum_value * 100

                # Oblicza szerokość drugiego słupka w procentach.
                second_width = second_value / maximum_value * 100

                # Dodaje jedną porównywaną statystykę.
                metric_rows += f"""
                <section class="metric">
                    <h3>{metric_name}</h3>

                    <div class="bar-label">
                        <span>{first_team['name']}</span>
                        <strong>{first_value}</strong>
                    </div>

                    <div class="bar-track">
                        <div
                            class="bar first-bar"
                            style="width: {first_width}%"
                        ></div>
                    </div>

                    <div class="bar-label">
                        <span>{second_team['name']}</span>
                        <strong>{second_value}</strong>
                    </div>

                    <div class="bar-track">
                        <div
                            class="bar second-bar"
                            style="width: {second_width}%"
                        ></div>
                    </div>
                </section>
                """

            # Buduje kompletne podsumowanie porównania.
            comparison_html = f"""
            <div class="comparison-result">
                <h2>
                    {first_team['name']} vs {second_team['name']}
                </h2>

                <p>
                    Więcej punktów:
                    <strong>{comparison['points_leader']}</strong>
                </p>

                {metric_rows}
            </div>
            """

    # Zwraca kompletną stronę HTML.
    return f"""
    <!DOCTYPE html>
    <html lang="pl">
        <head>
            <meta charset="UTF-8">
            <meta
                name="viewport"
                content="width=device-width, initial-scale=1"
            >
            <title>Porównanie drużyn – SportVision</title>
            <link rel="stylesheet" href="/static/style.css">
        </head>

        <body class="comparison-page">
            <div class="container">
                <a
                    class="back-link"
                    href="/?league_id={league_id}"
                >
                    ← Powrót do ligi
                </a>

                <h1>Porównanie drużyn</h1>

                <h2>1. Wybierz ligę</h2>

                <form class="comparison-form" method="get" action="/compare">
                    <select name="league_id">
                        {league_options}
                    </select>

                    <button type="submit">
                        Pokaż drużyny
                    </button>
                </form>

                <h2>2. Wybierz drużyny z ligi {selected_league_name}</h2>

                <form class="comparison-form" method="get" action="/compare">
                    <input
                        type="hidden"
                        name="league_id"
                        value="{league_id}"
                    >

                    <select name="first_team_id">
                        {first_team_options}
                    </select>

                    <select name="second_team_id">
                        {second_team_options}
                    </select>

                    <button type="submit">
                        Porównaj
                    </button>
                </form>

                {comparison_html}
            </div>
        </body>
    </html>
    """

#python -m uvicorn main:app --reload
