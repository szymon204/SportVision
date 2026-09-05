from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from database import add_league, add_team, create_tables, get_leagues, get_teams

app = FastAPI(title="SportVision")

create_tables()

@app.get("/", response_class=HTMLResponse) #tworzenie aplikacji (zmienna app). Jak przeglądarka wykonuje GET to uruchamia funkcję znajdującą się poniżej.
def home():
    leagues = get_leagues()
    teams = get_teams()
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

    return{
        "message": "Drużyna została dodana"
    }

@app.get("/teams")
def teams():
    return get_teams()

#python -m uvicorn main:app --reload