# SportVision — kontekst projektu dla kolejnych rozmów Codex

> Stan na 13 października 2026 r. Ten plik jest trwałym skrótem ustaleń z
> wcześniejszych rozmów Codex prowadzonych na komputerze PC. Ma pozwolić
> kontynuować projekt na laptopie bez odtwarzania architektury od zera.

## Najważniejsza zasada projektu

SportVision jest pracą inżynierską. Celem jest **prosty, czytelny i działający
projekt wystarczający do obrony**, a nie rozbudowany system produkcyjny.

- Odpowiadaj i opisuj zmiany po polsku.
- Pracuj małymi krokami i krótko wyjaśniaj, co się zmieniło.
- Nie dodawaj technologii ani zależności, które nie są potrzebne.
- Nie odczytuj, nie pokazuj i nie zapisuj do repozytorium pliku `.env`.
- Przed większą zmianą sprawdź Git; po sensownym etapie wykonaj czytelny commit.

## Stan migracji

- Laptop: `C:\Users\Admin\Documents\SportVision`
- Zdalne repozytorium: `https://github.com/szymon204/SportVision.git`
- Gałąź: `main`
- Aktualny commit: `807cafbafbc8b1635af4d368466495fb44633065`
- Ostatni commit przed migracją: `Clean up main page code comments`

Kod z GitHuba jest na laptopie. Historyczny czat Codex z PC pozostaje dostępny
zdalnie, ale nie dało się go technicznie przekazać do lokalnej listy czatów,
ponieważ funkcja Handoff nie została udostępniona dla tego połączenia.
Ten plik nie jest pełnym zapisem rozmowy — jest jej użytecznym, wersjonowanym
kontekstem dla dalszej pracy.

## Architektura

```text
start.bat / uvicorn
        -> FastAPI (main.py)
        -> SQLite (database.py, data/sportvision.db)
        -> HTML generowany w Pythonie + static/style.css

Ręczny import przez endpointy FastAPI
        -> API-Football (football_api.py)
        -> SQLite
```

### Pliki

- `main.py` — aplikacja FastAPI, endpointy, generowanie HTML, tabela ligowa,
  strony drużyn i porównanie.
- `database.py` — SQLite: tworzenie tabel i operacje na ligach, drużynach oraz
  meczach.
- `football_api.py` — wyłącznie pobieranie drużyn i meczów z API-Football.
- `static/style.css` — wygląd aplikacji.
- `static/logos/` — lokalne logotypy lig i drużyn.
- `download_team_logos.py` — narzędzie do pobierania logotypów.
- `start.bat` — lokalne uruchomienie aplikacji.

## Dane i działanie offline

Przy zwykłym wejściu na stronę aplikacja **nie korzysta z internetu**. Odczytuje
ligi, drużyny i mecze z lokalnej bazy SQLite.

Podczas startu automatycznie wykonywane są tylko:

1. utworzenie pliku bazy i tabel, gdy ich nie ma;
2. dodanie pięciu podstawowych lig, gdy ich jeszcze nie ma.

Drużyny i mecze nie są importowane automatycznie. Import jest świadomy i
ręczny, przez endpointy:

- `POST /api/import-teams/{league_api_id}`
- `POST /api/import-matches/{league_api_id}`

Plik `data/sportvision.db` nie jest w GitHubie, bo `.gitignore` ignoruje
`*.db`. Oznacza to, że pełna wersja demonstracyjna z już zaimportowanymi danymi
wymaga bezpiecznego skopiowania tego jednego pliku z PC albo ponownego importu
po utworzeniu lokalnego `.env` z kluczem API. Nie umieszczaj klucza w Git.

## Model danych

SQLite zawiera trzy tabele:

- `league`: lokalne `id`, identyfikator `api_id`, nazwa i kraj;
- `team`: lokalne `id`, `api_id`, nazwa i `league_id`;
- `football_match`: `api_id`, liga, sezon, data, gospodarze/goście i wynik.

Ważne: `id` to identyfikator lokalny SQLite, a `api_id` pochodzi z
API-Football. W adresach strony, np. `league_id=4`, używane jest lokalne ID.

## Funkcje dostępne w aktualnej wersji

- pięć głównych lig europejskich;
- import drużyn i zakończonych meczów z API-Football;
- lokalna baza SQLite i praca offline po imporcie;
- tabela ligowa obliczana z wyników;
- wybór ligi i liczby widocznych meczów (10, 30 lub wszystkie);
- strona drużyny, statystyki i forma z pięciu ostatnich meczów;
- porównanie dwóch drużyn z tej samej ligi;
- lokalne logotypy i niebieski motyw.

## Endpointy

- `GET /` — strona główna;
- `GET/POST /leagues`, `GET/POST /teams`, `GET/POST /matches` — proste API
  lokalnych danych;
- `POST /api/import-teams/{league_api_id}` — ręczny import drużyn;
- `POST /api/import-matches/{league_api_id}` — ręczny import meczów;
- `GET /standings` — tabela ligowa jako dane;
- `GET /teams/{team_id}/summary` — dane drużyny i jej mecze;
- `GET /teams/{team_id}` — strona HTML drużyny;
- `GET /comparison` i `GET /compare` — porównanie drużyn.

## Ustalenia do obrony

- Nie importujemy danych automatycznie: ogranicza to zależność od internetu,
  klucza API i limitów zewnętrznego serwisu.
- Na prezentację najlepiej korzystać z gotowej, lokalnej bazy SQLite.
- Aplikacja ma celowo prostą architekturę: FastAPI + SQLite + HTML/CSS,
  bez zbędnego frontendu ani dodatkowej infrastruktury.
- Historycznie komplet danych obejmował 5 lig, 98 drużyn i 1755 meczów;
  traktuj tę liczbę jako opis poprzedniej bazy z PC, a nie gwarancję dla
  bieżącego laptopa bez pliku `sportvision.db`.

## Pierwszy krok przy kolejnej rozmowie

1. Przeczytaj ten plik i `README.md`.
2. Sprawdź `git status` przed zmianami.
3. Sprawdź, czy istnieje `data/sportvision.db`; jeśli nie, nie zakładaj, że
   aplikacja ma już drużyny i wyniki.
4. Zaproponuj jedną małą, uzasadnioną zmianę albo test — bez rozbudowywania
   projektu ponad potrzeby pracy inżynierskiej.
