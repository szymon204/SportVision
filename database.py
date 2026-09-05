import sqlite3
from pathlib import Path  # budowanie ścieżki niezaleznie od miejsca projektu

DATA_DIRECTORY = Path(__file__).parent / "data"  # wskazanie katalogu data obok database.py
DATABASE_PATH = DATA_DIRECTORY / "sportvision.db"  # określenie lokalizacji bazy (jeden plik).

def create_tables():
    DATA_DIRECTORY.mkdir(exist_ok=True)  # tworzenie folderu data, jeśli jeszcze nie istnieje

    connection = sqlite3.connect(DATABASE_PATH)  # otwiera bazę, jak plik nie istnieje to SQLite automatycznie go tworzy

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS league (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        api_id INTEGER UNIQUE NOT NULL,
        name TEXT NOT NULL,
        country TEXT
        )
        """
    )

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS team (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        api_id INTEGER UNIQUE NOT NULL,
        name TEXT NOT NULL,
        league_id INTEGER NOT NULL,
        FOREIGN KEY (league_id) REFERENCES league(id)
        )
        """
    )

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS football_match (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            api_id INTEGER UNIQUE NOT NULL,
            league_id INTEGER NOT NULL,
            season INTEGER NOT NULL,
            match_date TEXT NOT NULL,
            home_team_id INTEGER NOT NULL,
            away_team_id INTEGER NOT NULL,
            home_goals INTEGER NOT NULL,
            away_goals INTEGER NOT NULL,
            FOREIGN KEY (league_id) REFERENCES league(id),
            FOREIGN KEY (home_team_id) REFERENCES team(id),
            FOREIGN KEY (away_team_id) REFERENCES team(id)
        )
        """
    )

    connection.commit()  # commit zapisuje zmiany
    connection.close()  # zamknięcię połączenia


def get_leagues():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row  # powoduje, że kolumny można odczytywać po nazwach, a nie tylko pozycjach.

    rows = connection.execute(
        """
        SELECT id, api_id, name, country
        FROM league
        ORDER BY name
        """
    ).fetchall()  # pobiera wszystkie znalezione rekordy

    connection.close()

    return [dict(row) for row in rows]  # zmienia rekordy SQLite na zwykłe słowniki Pythona, które FastAPI potrafi zwrócić jako JSON.


def add_league(api_id: int, name: str, country: str):
    connection = sqlite3.connect(DATABASE_PATH)

    connection.execute(
        """
        INSERT OR IGNORE INTO league (api_id, name, country)
        VALUES (?, ?, ?)
        """,
        (api_id, name, country)
    )

    connection.commit()
    connection.close()

def add_team(api_id: int, name: str, league_id: int):
    connection = sqlite3.connect(DATABASE_PATH)

    connection.execute("PRAGMA foreign_keys = ON")  # sprawdzanie czy podane league_id rzeczywiście istnieje w tabeli lig.

    connection.execute(
        """
        INSERT OR IGNORE INTO team (api_id, name, league_id)
        VALUES (?, ?, ?)
        """,
        (api_id, name, league_id)
    )

    connection.commit()
    connection.close()

def get_teams():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    rows = connection.execute(
        """
        SELECT
            team.id,
            team.api_id,
            team.name,
            team.league_id,
            league.name AS league_name
        FROM team
        JOIN league ON team.league_id = league.id
        ORDER BY team.name
        """
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]


def add_match(
    api_id: int,
    league_id: int,
    season: int,
    match_date: str,
    home_team_id: int,
    away_team_id: int,
    home_goals: int,
    away_goals: int
):
    connection = sqlite3.connect(DATABASE_PATH)
    connection.execute("PRAGMA foreign_keys = ON")

    connection.execute(
        """
        INSERT OR IGNORE INTO football_match (
            api_id,
            league_id,
            season,
            match_date,
            home_team_id,
            away_team_id,
            home_goals,
            away_goals
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            api_id,
            league_id,
            season,
            match_date,
            home_team_id,
            away_team_id,
            home_goals,
            away_goals
        )
    )

    connection.commit()
    connection.close()


def get_matches():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    rows = connection.execute(
        """
        SELECT
            football_match.id,
            football_match.api_id,
            football_match.season,
            football_match.match_date,
            home_team.name AS home_team_name,
            away_team.name AS away_team_name,
            football_match.home_goals,
            football_match.away_goals,
            league.name AS league_name
        FROM football_match
        JOIN league
            ON football_match.league_id = league.id
        JOIN team AS home_team
            ON football_match.home_team_id = home_team.id
        JOIN team AS away_team
            ON football_match.away_team_id = away_team.id
        ORDER BY football_match.match_date DESC
        """
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]
