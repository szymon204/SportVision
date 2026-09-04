from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from database import add_league, create_tables, get_leagues

app = FastAPI(title="SportVision")

create_tables()

@app.get("/", response_class=HTMLResponse) #tworzenie aplikacji (zmienna app). Jak przeglądarka wykonuje GET to uruchamia funkcję znajdującą się poniżej.
def home():
    leagues = get_leagues()
    rows = ""

    for league in leagues:
        rows += f"""
        <tr>
            <td>{league['id']}</td>
            <td>{league['name']}</td>
            <td>{league['country']}</td>
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