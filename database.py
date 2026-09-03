import sqlite3
from pathlib import Path #budowanie ścieżki niezaleznie od miejsca projektu

DATA_DIRECTORY = Path(__file__).parent / "data" #wskazanie katalogu data obok database.py
DATABASE_PATH = DATA_DIRECTORY / "sportvision.db" #określenie lokalizacji bazy (jeden plik).

def create_tables():
    DATA_DIRECTORY.mkdir(exist_ok=True) #tworzenie folderu data, jeśli jeszcze nie istnieje

    connection = sqlite3.connect(DATABASE_PATH) #otwiera bazę, jak plik nie istnieje to SQLite automatycznie go tworzy

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

    connection.commit() #commit zapisuje zmiany
    connection.close() #zamknięcię połączenia

def get_leagues():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row #powoduje, że kolumny można odczytywać po nazwach, a nie tylko pozycjach.

    rows = connection.execute(
        """
        SELECT id, api_id, name, country
        FROM league
        ORDER BY name
        """
    ).fetchall() #pobiera wszystkie znalezione rekordy

    connection.close()

    return [dict(row) for row in rows] #zmienia rekordy SQLite na zwykłe słowniki Pythona, które FastAPI potrafi zwrócić jako JSON.


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