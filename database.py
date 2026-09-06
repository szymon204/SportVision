import sqlite3
from pathlib import Path  # budowanie ścieżki niezaleznie od miejsca projektu

DATA_DIRECTORY = Path(__file__).parent / "data"  # wskazanie katalogu data obok database.py
DATABASE_PATH = DATA_DIRECTORY / "sportvision.db"  # określenie lokalizacji bazy (jeden plik).

# Ligi obsługiwane przez naszą aplikację.
DEFAULT_LEAGUES = [
    (39, "Premier League", "England"),
    (140, "La Liga", "Spain"),
    (78, "Bundesliga", "Germany"),
    (135, "Serie A", "Italy"),
    (61, "Ligue 1", "France")
]

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

def add_default_leagues():
    # Otwiera lokalną bazę SQLite.
    connection = sqlite3.connect(DATABASE_PATH)

        # Przechodzi przez dane pięciu obsługiwanych lig.
    for api_id, name, country in DEFAULT_LEAGUES:
        # Sprawdza, czy liga jest już zapisana.
        existing_league = connection.execute(
            """
            SELECT id
            FROM league
            WHERE api_id = ?
            """,
            (api_id,)
        ).fetchone()

        # Dodaje ligę wyłącznie wtedy, gdy jeszcze nie istnieje.
        if existing_league is None:
            connection.execute(
                """
                INSERT INTO league (api_id, name, country)
                VALUES (?, ?, ?)
                """,
                (api_id, name, country)
            )

    # Zapisuje dodane ligi w bazie.
    connection.commit()

    # Zamyka połączenie z bazą.
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


def get_league_id_by_api_id(api_id: int):
    connection = sqlite3.connect(DATABASE_PATH)

    row = connection.execute(
        """
        SELECT id
        FROM league
        WHERE api_id = ?
        """,
        (api_id,)
    ).fetchone()

    connection.close()

    if row is None:
        return None

    return row[0]

def get_team_id_by_api_id(api_id: int):
    # Otwiera lokalną bazę SQLite.
    connection = sqlite3.connect(DATABASE_PATH)

    # Szuka lokalnego ID drużyny na podstawie ID z API.
    row = connection.execute(
        """
        SELECT id
        FROM team
        WHERE api_id = ?
        """,
        # Przecinek tworzy krotkę zawierającą jeden parametr.
        (api_id,)
    ).fetchone()

    # Zamyka połączenie po wykonaniu zapytania.
    connection.close()

    # Zwraca None, jeżeli drużyny nie znaleziono.
    if row is None:
        return None

    # Zwraca lokalne ID znalezionej drużyny.
    return row[0]

def match_exists(match_date: str, home_team_id: int, away_team_id: int):
    # Otwiera lokalną bazę SQLite.
    connection = sqlite3.connect(DATABASE_PATH)

    # Szuka meczu o tej samej dacie, gospodarzu i gościu.
    row = connection.execute(
        """
        SELECT id
        FROM football_match
        WHERE match_date = ?
          AND home_team_id = ?
          AND away_team_id = ?
        LIMIT 1
        """,
        # Przekazuje wartości w miejsce znaków zapytania.
        (match_date, home_team_id, away_team_id)
    ).fetchone()

    # Zamyka połączenie z bazą.
    connection.close()

    # True oznacza, że taki mecz jest już zapisany.
    return row is not None