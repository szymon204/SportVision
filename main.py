from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from database import (
    add_league,
    add_match,
    add_team,
    create_tables,
    get_leagues,
    get_matches,
    get_teams,
)

app = FastAPI(title="SportVision")

create_tables()

@app.get("/", response_class=HTMLResponse)  # tworzenie aplikacji (zmienna app). Jak przeglądarka wykonuje GET to uruchamia funkcję znajdującą się poniżej.
def home():
    leagues = get_leagues()
    teams = get_teams()
    matches = get_matches()
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


#python -m uvicorn main:app --reload
