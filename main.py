from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from database import add_league, create_tables, get_leagues

app = FastAPI(title="SportVision")

create_tables()

@app.get("/", response_class=HTMLResponse) #tworzenie aplikacji (zmienna app). Jak przeglądarka wykonuje GET to uruchamia funkcję znajdującą się poniżej.
def home():
    return """
    <!DOCTYPE html>
    <html lang="pl">
        <head>
            <meta charset="UTF-8">
            <title>SportVision</title>
        </head>
        <body>
            <h1>SportVision</h1>
            <p>Moja aplikacja działa.</p>
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