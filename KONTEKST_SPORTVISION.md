# Kompletny kontekst projektu SportVision

Aktualizacja: 10 listopada 2026

Ten plik jest przekazaniem projektu pomiędzy komputerami i rozmowami z Codexem. Ma pozwolić nowemu asystentowi szybko zrozumieć cel pracy, aktualny kod, decyzje projektowe, historię, ograniczenia, sposób współpracy z autorem oraz najbliższy plan. Kod i lokalna baza są ostatecznym źródłem prawdy, jeśli później pojawi się rozbieżność z tym opisem.

## Instrukcja startowa dla nowego Codexa

Po otwarciu projektu na nowym laptopie należy wysłać Codexowi następującą wiadomość:

> Kontynuujemy pracę inżynierską SportVision. Najpierw niczego nie zmieniaj. Przeczytaj w całości KONTEKST_SPORTVISION.md i README.md. Następnie sprawdź git status, strukturę projektu oraz aktualny kod w main.py, database.py i football_api.py. Nie czytaj, nie pokazuj i nie modyfikuj zawartości .env. Podsumuj stan projektu po polsku i zaproponuj jeden mały następny krok. Projekt ma pozostać prosty, krótki i możliwy do samodzielnego wyjaśnienia na obronie.

## 1. Tożsamość projektu

- Nazwa: SportVision.
- Typ: lokalna aplikacja internetowa.
- Charakter: projekt i praca inżynierska.
- Autor: Szymon Lechowski.
- Kierunek: Informatyka i Inżynieria Danych.
- Uczelnia: Uniwersytet Przyrodniczy w Poznaniu.
- Planowany termin ukończenia i obrony: około lipca 2027, do potwierdzenia z uczelnią.
- Polski temat pracy: „Projekt aplikacji do pobierania, przetwarzania i wizualizacji danych z API serwisów sportowych”.
- Angielski temat pracy: „Design of an application for fetching, processing, and visualizing data from sports service APIs”.
- Repozytorium: https://github.com/szymon204/SportVision.git
- Główna gałąź: `main`.
- Stary katalog na pierwszym komputerze: `A:\PracaInzynierska\SportVision`.

## 2. Najważniejsza wizja

SportVision ma być prostą aplikacją do pobierania, lokalnego przechowywania, przetwarzania i wizualizacji historycznych danych piłkarskich. Aplikacja pobiera dane z API-Football, zapisuje je w jednym pliku SQLite, samodzielnie oblicza statystyki i prezentuje wyniki w przeglądarce.

Projekt nie ma być systemem komercyjnym ani rozwiązaniem „dla NASA”. Ma być wystarczająco rozbudowany, aby wykazać pracę inżynierską, ale na tyle prosty, żeby autor rozumiał go w całości i potrafił samodzielnie wyjaśnić na seminarium oraz obronie.

Najważniejsze wartości projektu:

1. Prostota.
2. Czytelność kodu.
3. Mała liczba technologii i plików.
4. Działanie lokalne i offline po pobraniu danych.
5. Stabilny zestaw danych historycznych.
6. Rozwój małymi, sprawdzanymi krokami.
7. Nauka autora, a nie bezrefleksyjne generowanie kodu.

## 3. Problem i cel pracy

### Problem

Dane piłkarskie są dostępne w wielu serwisach, ale bywają rozproszone, wymagają internetu i nie zawsze są przedstawione w formie wygodnej do prostego porównania. Projekt pokazuje, jak dane z zewnętrznego API można pobrać, uporządkować, zapisać lokalnie, przetworzyć i zwizualizować w jednej aplikacji.

### Cel główny

Celem pracy jest zaprojektowanie i wykonanie prostej aplikacji internetowej, która:

- pobiera drużyny i zakończone mecze z zewnętrznego API,
- zapisuje dane w lokalnej bazie SQLite,
- oblicza tabelę ligową i inne statystyki,
- udostępnia widoki lig i drużyn,
- umożliwia porównanie zespołów,
- po imporcie danych działa bez internetu.

### Użytkownik docelowy

Użytkownikiem jest kibic piłki nożnej lub osoba ucząca się analizy danych sportowych, która chce w prosty sposób sprawdzić tabelę, wyniki, formę i podstawowe porównanie drużyn. Nie jest to narzędzie bukmacherskie ani profesjonalny system skautingowy.

### Własny wkład autora

API jedynie dostarcza surowe dane. Własnym wkładem autora są:

- określenie wymagań i zakresu,
- wybór prostej architektury,
- projekt trzech tabel bazy danych,
- połączenie z API-Football,
- mapowanie identyfikatorów API na lokalne identyfikatory,
- zabezpieczenie przed duplikatami,
- obliczanie tabeli ligowej z wyników meczów,
- obliczanie goli, formy i porównania drużyn,
- budowanie widoków HTML i stylów CSS,
- przygotowanie działania offline,
- testowanie, dokumentowanie i przygotowanie prezentacji.

## 4. Świadomie ograniczony zakres

### Zakres aktualny

- pięć najważniejszych lig europejskich,
- dane historyczne oznaczone sezonem `2024`, czyli zasadniczo sezon 2024/2025,
- drużyny i zakończone mecze,
- tabela ligowa,
- lista wyników,
- wykres strzelonych goli,
- strona drużyny,
- forma z pięciu ostatnich spotkań,
- porównanie dwóch drużyn z tej samej ligi,
- logotypy lig i herby drużyn,
- lokalne uruchamianie na Windowsie,
- działanie offline na wcześniej zapisanych danych.

### Elementy celowo poza zakresem

- wyniki na żywo,
- automatyczne odświeżanie danych,
- przewidywanie wyników i sztuczna inteligencja,
- system bukmacherski,
- konta użytkowników i logowanie,
- role i uprawnienia,
- płatności,
- publiczny hosting i chmura,
- osobna aplikacja mobilna,
- rozbudowany frontend JavaScript,
- PostgreSQL, ORM i migracje,
- Docker i mikroserwisy,
- dokładne odtworzenie każdego ligowego regulaminu ustalania kolejności.

Te ograniczenia są świadomą decyzją projektową. Można je opisać w rozdziale o ograniczeniach i dalszym rozwoju.

## 5. Dlaczego projekt rozpoczęto ponownie

Pierwsza wersja SportVision powstawała w sierpniu 2026. Korzystała lub miała korzystać z PostgreSQL, SQLAlchemy, Alembica i rozbudowanej struktury katalogów. Autor uznał, że projekt stał się zbyt trudny do pełnego zrozumienia i wyjaśnienia.

3 września 2026 podjęto decyzję o rozpoczęciu uproszczonej wersji od zera. Nowa wersja wykorzystuje zwykły moduł `sqlite3`, kilka plików Pythona i prosty HTML generowany bezpośrednio przez FastAPI. Stary kod nie był przenoszony do nowej aplikacji.

Najważniejsza lekcja: architektura pracy inżynierskiej ma odpowiadać faktycznym wymaganiom, a nie maksymalnej liczbie technologii.

## 6. Technologie i uzasadnienie

### Python

Obsługuje logikę aplikacji. Ma czytelną składnię i umożliwia wykonanie projektu w małej liczbie plików. Autor zawodowo pracuje głównie w środowisku low-code związanym z C#, dlatego wyjaśnienia powinny często porównywać konstrukcje Pythona do C#.

### FastAPI

Rejestruje endpointy, waliduje proste parametry i automatycznie udostępnia Swagger pod `/docs`. Dekoratory `@app.get` i `@app.post` są zbliżone znaczeniem do atrybutów `HttpGet` i `HttpPost`.

### Uvicorn

Jest lokalnym serwerem HTTP uruchamiającym obiekt `app` z pliku `main.py`.

### SQLite

Nie wymaga instalowania serwera bazodanowego. Cała baza znajduje się w jednym pliku `data/sportvision.db`, który można skopiować na inny komputer. To główny powód odejścia od PostgreSQL.

### requests

Wysyła żądania HTTP do API-Football i pobiera pliki herbów.

### python-dotenv

Wczytuje klucz API z lokalnego pliku `.env`, który nie trafia do GitHuba.

### HTML i CSS

HTML tworzy tabele, formularze, linki i wykresy. CSS odpowiada za wygląd. Nie ma frameworka JavaScript ani osobnego procesu budowania frontendu.

## 7. Architektura

Najkrótszy opis architektury:

```text
Przeglądarka
    |
    | żądanie HTTP GET lub POST
    v
FastAPI i logika w main.py
    |                       |
    | odczyt i zapis        | import internetowy
    v                       v
database.py             football_api.py
    |                       |
    v                       v
SQLite                  API-Football
data/sportvision.db

Pliki CSS i PNG są udostępniane z katalogu static.
```

### Zwykłe przeglądanie

1. Użytkownik otwiera `http://127.0.0.1:8000`.
2. Przeglądarka wysyła `GET /`.
3. FastAPI uruchamia funkcję `home`.
4. Funkcja pobiera ligi, drużyny i mecze przez `database.py`.
5. `database.py` wykonuje zapytania `SELECT` w SQLite.
6. `main.py` filtruje dane i oblicza statystyki.
7. `main.py` składa HTML i zwraca go do przeglądarki.
8. Przeglądarka pobiera CSS i grafiki z `/static`.

W tym przepływie internetowe API nie jest używane.

### Import danych

1. Użytkownik uruchamia endpoint importu w Swaggerze.
2. `main.py` wywołuje funkcję z `football_api.py`.
3. `football_api.py` odczytuje lokalny klucz z `.env`.
4. `requests` wysyła zapytanie do API-Football.
5. Odpowiedź JSON wraca jako struktury Pythona.
6. `main.py` wybiera potrzebne pola i mapuje identyfikatory.
7. `database.py` zapisuje rekordy w SQLite.

W tym przepływie potrzebny jest internet.

## 8. Struktura projektu

```text
SportVision/
|-- .git/
|-- .gitignore
|-- .env                      lokalny sekret, nie jest w Git
|-- .venv/                    lokalne środowisko, nie jest w Git
|-- __pycache__/              automatyczny cache, nie jest w Git
|-- data/
|   `-- sportvision.db        lokalna baza, nie jest w Git
|-- static/
|   |-- style.css
|   `-- logos/
|       |-- leagues/          5 logo lig
|       `-- teams/            98 herbów drużyn
|-- main.py
|-- database.py
|-- football_api.py
|-- download_team_logos.py
|-- requirements.txt
|-- start.bat
|-- README.md
`-- KONTEKST_SPORTVISION.md
```

### Odpowiedzialność plików

- `main.py`: obiekt FastAPI, endpointy, obliczenia, filtrowanie i generowanie HTML.
- `database.py`: ścieżka bazy, tworzenie tabel i wszystkie zapytania SQLite.
- `football_api.py`: komunikacja z API-Football.
- `download_team_logos.py`: pobieranie brakujących herbów na podstawie `api_id`.
- `static/style.css`: wspólny wygląd strony głównej, strony drużyny i porównania.
- `static/logos`: grafiki działające offline.
- `start.bat`: uruchomienie serwera i przeglądarki dwuklikiem.
- `requirements.txt`: zależności Pythona.
- `README.md`: krótka instrukcja dla człowieka.
- `KONTEKST_SPORTVISION.md`: pełne przekazanie kontekstu dla człowieka i Codexa.

## 9. Lokalna baza danych

Ścieżka jest budowana względem pliku `database.py`, dlatego nie zależy od litery dysku ani katalogu uruchomienia:

```text
data/sportvision.db
```

### Tabela league

- `id`: lokalny klucz główny SQLite.
- `api_id`: unikalny identyfikator ligi z API-Football.
- `name`: nazwa ligi.
- `country`: kraj.

### Tabela team

- `id`: lokalny klucz główny drużyny.
- `api_id`: unikalny identyfikator drużyny z API.
- `name`: nazwa drużyny.
- `league_id`: klucz obcy do `league.id`.

### Tabela football_match

- `id`: lokalny klucz główny meczu.
- `api_id`: unikalny identyfikator meczu z API.
- `league_id`: lokalny identyfikator ligi.
- `season`: sezon przekazany podczas importu.
- `match_date`: data w formacie `RRRR-MM-DD`.
- `home_team_id`: lokalny identyfikator gospodarza.
- `away_team_id`: lokalny identyfikator gościa.
- `home_goals`: gole gospodarza.
- `away_goals`: gole gościa.

### Lokalne ID i api_id

`id` nadaje SQLite i aplikacja używa go do lokalnych relacji. `api_id` pochodzi z API-Football i pozwala powiązać dane z usługą zewnętrzną oraz nazwą pliku logo.

Brak lokalnego ID `2` w tabeli lig nie oznacza błędu. `AUTOINCREMENT` nie wykorzystuje ponownie numeru rekordu, który wcześniej usunięto.

### Tworzenie bazy

Podczas importu `main.py` wykonywane są:

```python
create_tables()
add_default_leagues()
```

Jeżeli plik bazy nie istnieje, SQLite tworzy pustą bazę i trzy tabele. Następnie aplikacja dodaje pięć podstawowych lig. Drużyny i mecze nie importują się automatycznie.

## 10. Aktualne dane

Stan lokalnej bazy sprawdzony 10 listopada 2026:

- 5 lig,
- 98 drużyn,
- 1755 meczów,
- sezon zapisany jako `2024`,
- rozmiar bazy około 116 KB.

| Liga | Lokalne ID | ID API | Drużyny | Mecze |
|---|---:|---:|---:|---:|
| Premier League | 1 | 39 | 20 | 380 |
| La Liga | 3 | 140 | 20 | 380 |
| Bundesliga | 4 | 78 | 19 | 308 |
| Serie A | 5 | 135 | 20 | 380 |
| Ligue 1 | 6 | 61 | 19 | 307 |

Bundesliga i Ligue 1 mają po jednej dodatkowej drużynie oraz spotkania związane z barażami zwrócone przez API. Nie jest to uszkodzenie SQLite. Można kiedyś dodać filtr, ale nie jest to konieczne do podstawowego zakresu pracy.

## 11. Obsługiwane ligi

Lista jest zdefiniowana w `DEFAULT_LEAGUES` w `database.py`:

```python
(39, "Premier League", "England")
(140, "La Liga", "Spain")
(78, "Bundesliga", "Germany")
(135, "Serie A", "Italy")
(61, "Ligue 1", "France")
```

Dodanie Ekstraklasy wymagałoby głównie dopisania jednej ligi, potwierdzenia jej `api_id`, wykonania istniejących importów, pobrania herbów i dodania logo ligi. Nie wymaga nowej architektury. Jest to opcja, a nie obowiązkowy element pracy.

## 12. API-Football

- Bazowy adres: `https://v3.football.api-sports.io`.
- Nazwa lokalnej zmiennej: `API_FOOTBALL_KEY`.
- Wartość znajduje się wyłącznie w `.env`.
- Klucz nie może znaleźć się w kodzie, repozytorium, dokumentacji, zrzutach ekranu ani odpowiedzi Codexa.
- `get_api_teams` wywołuje endpoint `/teams` z parametrami ligi i sezonu.
- `get_api_matches` wywołuje endpoint `/fixtures` z parametrami ligi i sezonu.
- Limit oczekiwania wynosi 10 sekund dla drużyn i 30 sekund dla meczów.
- Błąd sieci, brak klucza lub błąd zwrócony przez API powoduje obecnie zwrócenie pustej listy.
- Aplikacja importuje tylko spotkania ze statusem `FT`, czyli zakończone.
- Najpierw trzeba importować drużyny, a dopiero później mecze, ponieważ mecz przechowuje lokalne ID gospodarza i gościa.
- Import uruchamia się świadomie przez Swagger; zwykłe wejście na stronę nie zużywa limitu API.

Ceny i limity API mogą się zmieniać. Przed kolejnym dużym importem należy sprawdzić aktualny plan w panelu dostawcy, a nie opierać się na starej notatce cenowej.

## 13. Ochrona przed duplikatami

- `api_id` lig, drużyn i meczów jest unikalne w odpowiednich tabelach.
- `INSERT OR IGNORE` pomija rekord naruszający unikalność.
- `add_default_leagues` najpierw sprawdza istnienie ligi.
- `match_exists` wyszukuje mecz po dacie, gospodarzu i gościu.
- Ponowne uruchomienie importu nie powinno powielać tych samych danych.

## 14. Najważniejsze algorytmy

### Tabela ligowa

Funkcja `calculate_standings(teams, matches)`:

1. Tworzy pusty zestaw statystyk dla każdej drużyny.
2. Przechodzi przez mecze.
3. Zwiększa liczbę rozegranych spotkań obu drużyn.
4. Sumuje gole strzelone i stracone.
5. Przyznaje 3 punkty za zwycięstwo i 1 punkt za remis.
6. Oblicza bilans jako gole strzelone minus gole stracone.
7. Sortuje po punktach, bilansie i golach strzelonych.

To jeden z najważniejszych przykładów własnego przetwarzania danych. Aplikacja nie pobiera gotowej tabeli ligowej z API.

Uproszczenie: algorytm nie odtwarza wszystkich szczegółowych zasad rozstrzygania remisów punktowych w każdej lidze.

### Filtrowanie strony głównej

Funkcja `home(league_id, liczba_meczow)` pobiera wszystkie rekordy, a następnie w Pythonie wybiera drużyny i mecze z właściwym `league_id`. Dopiero po filtrowaniu oblicza tabelę wybranej ligi.

Parametr `liczba_meczow` działa tak:

- `10`: dziesięć najnowszych,
- `30`: trzydzieści najnowszych,
- `0`: wszystkie.

### Wykres goli

Program sumuje gole zdobyte u siebie i na wyjeździe. Największy wynik otrzymuje pasek o szerokości 100%, a pozostałe szerokość proporcjonalną:

```text
szerokość = gole drużyny / największa liczba goli * 100
```

Wykres powstaje w HTML i CSS bez zewnętrznej biblioteki.

### Strona drużyny i forma

`team_summary` znajduje drużynę, jej obliczone statystyki i wszystkie mecze, w których występowała. `team_page` ustala przeciwnika, miejsce meczu, wynik i rezultat z punktu widzenia wybranej drużyny.

Pierwsze pięć spotkań z listy posortowanej malejąco po dacie tworzy formę:

- `W`: wygrana,
- `R`: remis,
- `P`: porażka.

### Porównanie drużyn

Porównywać można dwie różne drużyny z tej samej ligi. Widok pokazuje punkty, zwycięstwa i gole strzelone. Dłuższy pasek odpowiada większej wartości. `max(first_value, second_value, 1)` zabezpiecza dzielenie przed zerem.

## 15. Endpointy

| Metoda | Adres | Cel | Internet |
|---|---|---|---|
| GET | `/` | Strona główna wybranej ligi | nie |
| GET | `/leagues` | Ligi jako JSON | nie |
| POST | `/leagues` | Ręczne dodanie ligi | nie |
| GET | `/teams` | Drużyny jako JSON | nie |
| POST | `/teams` | Ręczne dodanie drużyny | nie |
| GET | `/matches` | Mecze jako JSON | nie |
| POST | `/matches` | Ręczne dodanie meczu | nie |
| POST | `/api/import-teams/{league_api_id}` | Import drużyn | tak |
| POST | `/api/import-matches/{league_api_id}` | Import meczów | tak |
| GET | `/standings` | Obliczone statystyki jako JSON | nie |
| GET | `/teams/{team_id}/summary` | Podsumowanie drużyny jako JSON | nie |
| GET | `/teams/{team_id}` | Strona HTML drużyny | nie |
| GET | `/comparison` | Porównanie jako JSON | nie |
| GET | `/compare` | Strona HTML porównania | nie |

Swagger jest dostępny pod:

```text
http://127.0.0.1:8000/docs
```

`Method Not Allowed` oznacza zwykle użycie GET dla endpointu POST albo odwrotnie. Błąd `422` oznacza zwykle, że parametr nie pasuje do zadeklarowanego typu.

## 16. Interfejs

Strona główna zawiera:

- wyśrodkowany napis SportVision na niebieskim tle,
- wybór ligi,
- odnośnik do porównania drużyn,
- logo ligi,
- tabelę ligową z herbami i linkami do drużyn,
- wykres strzelonych goli,
- listę 10, 30 lub wszystkich meczów.

Strona drużyny zawiera:

- herb i nazwę,
- ligę,
- liczbę meczów, punktów, zwycięstw i goli,
- kolorową formę z pięciu spotkań,
- tabelę wszystkich meczów drużyny.

Strona porównania zawiera:

- wybór ligi,
- wybór dwóch drużyn,
- walidację błędnego wyboru,
- paski porównujące punkty, zwycięstwa i gole.

Interfejs używa jasnoniebieskiego motywu. CSS ma prostą regułę responsywną dla ekranów węższych niż 700 pikseli. Oznacza to dostosowanie strony do mniejszego ekranu, ale nie oznacza natywnej aplikacji mobilnej.

## 17. Działanie offline

Po imporcie ligi, drużyny i mecze znajdują się w SQLite. CSS i grafiki znajdują się lokalnie w repozytorium. Dlatego zwykłe przeglądanie działa bez WiFi.

Internet jest potrzebny tylko do:

- klonowania lub aktualizacji repozytorium,
- instalacji bibliotek,
- importu nowych danych z API,
- pobierania brakujących herbów.

Klucz API nie jest potrzebny podczas samej prezentacji wcześniej zapisanych danych.

## 18. Uruchamianie

### Pierwsze przygotowanie komputera

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Uruchomienie z terminala

```powershell
python -m uvicorn main:app --reload
```

### Uruchomienie dwuklikiem

Po przygotowaniu `.venv` można dwukrotnie kliknąć `start.bat`. Plik:

1. przechodzi do własnego katalogu,
2. sprawdza obecność `.venv\Scripts\python.exe`,
3. uruchamia Uvicorn w osobnym oknie,
4. czeka dwie sekundy,
5. otwiera `http://127.0.0.1:8000`.

`start.bat` nie jest samodzielnym plikiem EXE. Nie zawiera Pythona ani bibliotek. Na nowym komputerze trzeba jednorazowo przygotować środowisko.

## 19. Najprostsze przeniesienie na nowy laptop

Nie należy kopiować `.venv`. Środowisko wirtualne zawiera ścieżki zależne od starego komputera i powinno zostać odtworzone.

### Część pierwsza: kod przez GitHub

Na starym komputerze:

1. Sprawdzić `git status`.
2. Zatwierdzić i wysłać wszystkie potrzebne zmiany.
3. Potwierdzić, że `main` i `origin/main` są zsynchronizowane.

Na nowym laptopie:

```powershell
git clone https://github.com/szymon204/SportVision.git
cd SportVision
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

GitHub przeniesie kod, README, ten dokument, CSS oraz wszystkie zapisane logo.

### Część druga: dwa pliki poza GitHubem

Osobno, najlepiej pendrivem lub prywatnym zaszyfrowanym dyskiem, skopiować:

```text
.env
data/sportvision.db
```

Na nowym laptopie umieścić je dokładnie w tych samych miejscach względem głównego folderu projektu.

- `.env` jest sekretem i nie wolno wysyłać go do publicznego repozytorium ani wklejać do rozmowy.
- `sportvision.db` jest gotowym zestawem danych offline. Bez niego aplikacja utworzy pustą bazę i doda tylko pięć lig.

### Część trzecia: dokumenty pracy poza repozytorium

Na starym komputerze poza repozytorium znajdują się również:

```text
A:\PracaInzynierska\HistoriaProjektu.docx
A:\PracaInzynierska\Dokumentacja_SportVision.docx
A:\PracaInzynierska\154434_Szymon_Lechowski.docx
A:\PracaInzynierska\INZYNIERKA.txt
A:\PracaInzynierska\Wymagania\
A:\PracaInzynierska\Przykładowe prace\
```

Tych materiałów nie ma w repozytorium SportVision. Najprościej skopiować cały folder `A:\PracaInzynierska` na prywatny dysk lub pendrive. Nie należy publikować dokumentu zawierającego numer albumu w publicznym repozytorium.

### Kontrola po przeniesieniu

1. Uruchomić `start.bat`.
2. Sprawdzić stronę główną każdej ligi.
3. Sprawdzić 10, 30 i wszystkie mecze.
4. Otworzyć stronę drużyny.
5. Porównać dwie drużyny.
6. Wyłączyć WiFi i ponownie sprawdzić widoki.
7. Sprawdzić `git status`.

### Kopia awaryjna na obronę

Na obronę warto mieć:

- sprawdzony laptop,
- folder projektu z gotową bazą,
- odtworzone `.venv`,
- kopię folderu na pendrivie,
- prezentację i pracę również jako PDF,
- zrzuty ekranu najważniejszych widoków,
- aplikację sprawdzoną wcześniej bez internetu.

## 20. Pliki ignorowane przez Git

`.gitignore` pomija:

```text
.venv/
__pycache__/
*.pyc
.env
*.db
```

Znaczenie:

- `.venv`: lokalne biblioteki i interpreter środowiska.
- `__pycache__` i `*.pyc`: automatycznie generowany cache Pythona.
- `.env`: sekret API.
- `*.db`: lokalna baza robocza.

Konsekwencja: samo sklonowanie GitHuba nie daje gotowych danych offline ani klucza API.

## 21. Git i historia wersji

Repozytorium ma jedno aktualne zdalne źródło:

```text
origin  https://github.com/szymon204/SportVision.git
```

Ważniejsze etapy:

- `e47603d`: podstawowa aplikacja FastAPI i SQLite,
- `0a2ef66`: ligi na stronie głównej,
- import drużyn i meczów Premier League,
- obliczanie tabeli i strony drużyn,
- uogólnienie obsługi pięciu lig,
- `145c064`: wizualizacja porównania drużyn,
- `a9d3e78`: przeniesienie stylów do CSS,
- `af50d64`: poprawa strony głównej,
- `cfe3d81`: lokalne uruchamianie i grafiki,
- `7a04ca5`: ograniczenie listy meczów,
- `e38fb15`: forma drużyny,
- `9975db8`: niebieski motyw i wybór 10, 30 lub wszystkich meczów,
- `214d088`: usunięcie powielonej tabeli drużyn,
- `95cf566`: kolory formy,
- `8dac467`: uproszczenie strony głównej,
- `07e82d4`: usunięcie testowego endpointu API i opis przepływu,
- `807cafb`: porządkowanie komentarzy strony głównej.

Przed dużą zmianą należy wykonać bezpieczny commit. Po zakończonym dniu należy zaktualizować historię projektu i zapisać logiczny punkt Git.

## 22. Obecne ograniczenia i dług techniczny

- Brak automatycznych testów jednostkowych i integracyjnych.
- Testowanie odbywało się głównie ręcznie.
- `main.py` jest długi, ponieważ zawiera endpointy, logikę i HTML.
- Dane są filtrowane w Pythonie po pobraniu wszystkich rekordów.
- Obsługa błędów API jest uproszczona i nie zwraca szczegółowej przyczyny.
- Dane dotyczą jednego historycznego sezonu.
- Import nie uruchamia się automatycznie.
- Swagger jest technicznym interfejsem importu.
- Algorytm tabeli nie implementuje wszystkich regulaminów ligowych.
- W danych mogą występować baraże.
- `/standings` zwraca tabelę obliczoną dla wszystkich pobranych drużyn, podczas gdy strona główna poprawnie filtruje wybraną ligę.
- Brak instalatora EXE.
- Brak CI i formalnej automatyzacji testów.
- Komentarze i nazwy są częściowo po polsku, częściowo po angielsku.

Nie należy automatycznie „naprawiać” wszystkich tych elementów. Każda poprawa musi mieć uzasadnienie w zakresie pracy i nie może niepotrzebnie zwiększać architektury.

## 23. Najbliższa rozsądna roadmapa

### Priorytet 1: pewność działania

- dodać kilka prostych testów funkcji `calculate_standings`,
- przetestować brak duplikatów,
- dodać podstawowe testy najważniejszych endpointów,
- wykonać pełny test na nowym laptopie i bez WiFi.

### Priorytet 2: małe uporządkowanie

- poprawić oczywiste wcięcia i komentarze bez przebudowy architektury,
- ewentualnie poprawić komunikaty błędów importu,
- zdecydować, czy filtrować baraże,
- utrzymać krótki README i aktualny kontekst.

### Priorytet 3: praca pisemna

- ustalić z promotorką ostateczny cel i zakres,
- opracować analizę wymagań,
- opisać architekturę i bazę,
- wyjaśnić import i algorytmy,
- opisać testy oraz wyniki,
- przygotować ograniczenia i kierunki rozwoju,
- zebrać zrzuty ekranu i diagramy.

### Priorytet 4: przygotowanie obrony

- nauczyć się trzyminutowego opisu projektu,
- umieć prześledzić przepływ jednej operacji,
- przećwiczyć pytania promotorki,
- przygotować pokaz awaryjny bez internetu,
- przygotować prezentację dopiero po ustaleniu wymagań uczelni.

### Funkcje opcjonalne

- Ekstraklasa,
- lepszy komunikat o pustej bazie,
- prosty przycisk importu zamiast Swaggera,
- przenośny pakiet lub EXE.

Funkcje opcjonalne nie powinny wyprzedzać testów, dokumentacji i zrozumienia istniejącego kodu.

## 24. Proponowana struktura pracy pisemnej

1. Wstęp i cel pracy.
2. Charakterystyka danych sportowych i źródła danych.
3. Analiza wymagań.
4. Projekt architektury i bazy danych.
5. Implementacja aplikacji.
6. Algorytmy przetwarzania i wizualizacji.
7. Testowanie i rezultaty.
8. Ograniczenia oraz możliwe kierunki rozwoju.
9. Podsumowanie.
10. Bibliografia i załączniki.

Ostateczny układ należy zatwierdzić z promotorką.

## 25. Gotowe odpowiedzi na najważniejsze pytania

### Dlaczego ten temat

Łączy zainteresowanie piłką nożną z pełnym procesem informatycznym: pobraniem danych, zapisem, przetwarzaniem i wizualizacją.

### Dlaczego dane historyczne

Są kompletne, stabilne i powtarzalne. Ułatwiają testowanie oraz niezawodną prezentację bez zależności od aktualnych zdarzeń.

### Dlaczego SQLite

Nie wymaga serwera, mieści się w jednym pliku i dobrze pasuje do lokalnej aplikacji demonstracyjnej działającej offline.

### Dlaczego FastAPI

Umożliwia proste endpointy, walidację parametrów i automatyczny Swagger przy małej ilości kodu.

### Dlaczego aplikacja działa offline

Po imporcie widoki czytają dane z lokalnego pliku SQLite, a CSS i grafiki również znajdują się lokalnie.

### Co jest własnym wkładem

Projekt bazy i przepływu danych, integracja, mapowanie ID, ochrona przed duplikatami, algorytm tabeli, forma, porównanie, interfejs, testowanie i dokumentacja.

### Jak sprawdzana jest poprawność

Obecnie głównie przez scenariusze ręczne, kontrolę bazy i porównanie wyników. Docelowo przez mały zestaw testów automatycznych i próbę na czystym komputerze.

### Najważniejsze ograniczenie

Aplikacja wykorzystuje jeden historyczny sezon i nie aktualizuje się automatycznie. Jest to świadomy zakres, nie ukryty błąd.

### Hipoteza badawcza

Praca ma charakter inżynierski i implementacyjny. Najważniejszy jest cel, wymagania oraz sprawdzenie, czy wykonany system je spełnia, a nie tworzenie nowej teorii naukowej.

## 26. Trzyminutowy opis projektu

SportVision jest lokalną aplikacją internetową do analizy historycznych danych piłkarskich. Dane drużyn i zakończonych meczów są pobierane z API-Football, a następnie zapisywane w bazie SQLite. Na podstawie wyników program sam oblicza tabelę ligową, gole, formę drużyn i porównania. FastAPI obsługuje endpointy i generuje strony HTML, `database.py` odpowiada za bazę, a `football_api.py` za komunikację z usługą zewnętrzną. Po wykonaniu importu aplikacja korzysta z lokalnych danych i działa bez internetu. Projekt celowo pozostaje prosty, ponieważ najważniejsze jest pełne zrozumienie kodu i niezawodna prezentacja pracy inżynierskiej.

## 27. Zasady współpracy z Codexem

1. Odpowiadać po polsku.
2. Nie czytać, nie pokazywać i nie modyfikować zawartości `.env`.
3. Nie dodawać zbędnych technologii ani zależności.
4. Preferować najprostsze rozwiązanie spełniające wymaganie.
5. Przed większą zmianą wykonać bezpieczny punkt Git.
6. Pracować małymi krokami i po każdym kroku testować.
7. Wyjaśniać, co zmiana robi, dlaczego jest potrzebna i jak przepływają dane.
8. W nowych fragmentach dodawać krótkie komentarze do większości ważnych linii.
9. Tam, gdzie nie szkodzi to spójności, używać zrozumiałych polskich nazw zmiennych.
10. Nie przepisywać całej architektury bez wyraźnej zgody autora.
11. Nie tworzyć rozwiązania komercyjnego ani nadmiarowej warstwy abstrakcji.
12. Jeśli autor chce pisać sam, podawać dokładne małe kroki zamiast automatycznie edytować kod.
13. Jeśli autor prosi o poprawkę automatyczną, zmieniać tylko wskazany zakres.
14. Po zmianie sprawdzić składnię, główne widoki i `git diff`.
15. Po dniu pracy aktualizować dziennik historii.
16. W nauce kończyć blok krótkim testem ABCD i po odpowiedzi podawać prawidłowy wynik z wyjaśnieniem.
17. Odnosić konstrukcje Pythona do C# i low-code, gdy ułatwia to zrozumienie.

## 28. Kontekst autora i sposób nauki

- Autor pracuje zwykle około dziewięciu godzin dziennie.
- Od października ma również zajęcia weekendowe.
- Na projekt i naukę często ma około jednej godziny dziennie.
- Zawodowo pracuje głównie z rozwiązaniami low-code związanymi z C#.
- Rozumie ogólny przepływ aplikacji, ale chce rozumieć także konkretne fragmenty kodu.
- Duża struktura i nadmiar warstw utrudniają mu naukę.
- Potrzebuje wyjaśnień praktycznych, małych przykładów i powtórek.
- Promotorka nie jest programistką, dlatego na seminarium ważniejsze są cel, problem, zakres, dane, własny wkład i rezultaty niż szczegóły składni.
- Najlepszy tryb nauki: jeden przypadek użycia, fragment kodu, wyjaśnienie czterech pytań i krótki quiz.

Cztery pytania do każdej funkcji:

1. Co ją uruchamia?
2. Jakie dane otrzymuje?
3. Co robi z danymi?
4. Co zwraca?

## 29. Podstawowe odpowiedniki Python i C sharp

| Python lub FastAPI | Przybliżony odpowiednik C# |
|---|---|
| `def` | metoda |
| `list` | `List<T>` |
| `dict` | `Dictionary` lub DTO |
| `None` | `null` |
| `for item in items` | `foreach` |
| `append` | `Add` |
| `items[:5]` | `Take(5)` |
| f-string | interpolacja `$"..."` |
| `@app.get` | `HttpGet` |
| `try/except` | `try/catch` |
| adnotacja `int` | parametr typu `int` z walidacją |

## 30. Podstawowy test po każdej zmianie

1. Uruchomić `python -m py_compile` dla plików Pythona.
2. Uruchomić aplikację i obserwować terminal serwera.
3. Otworzyć stronę główną dla pięciu lig.
4. Sprawdzić 10, 30 i wszystkie mecze.
5. Otworzyć przynajmniej jedną stronę drużyny.
6. Porównać dwie drużyny.
7. Sprawdzić błędny wybór tej samej drużyny.
8. Sprawdzić najważniejsze endpointy GET w Swaggerze.
9. Sprawdzić działanie bez WiFi, jeśli zmiana dotyczy uruchamiania lub danych.
10. Sprawdzić `git diff` przed commitem.

## 31. Typowe błędy

- `Internal Server Error`: wyjątek Pythona; pełna przyczyna jest w terminalu Uvicorna.
- `Method Not Allowed`: właściwy adres, ale zła metoda GET lub POST.
- `no such table`: aplikacja używa pustej lub innej bazy albo tabela nie została utworzona.
- `422 Unprocessable Entity`: parametr nie pasuje do oczekiwanego typu.
- brak CSS: błędny link `/static/style.css` albo brak montowania katalogu `static`.
- brak herbu: brakuje pliku `static/logos/teams/{api_id}.png`.
- pusta strona ligi: nowa baza bez zaimportowanych drużyn i meczów.
- import zwraca zero: brak klucza, brak internetu, limit API albo błąd dostawcy.
- `start.bat` nie działa: brak `.venv` lub bibliotek.

## 32. Co trzeba znać na obronę

Trzeba umieć:

- opisać problem, cel i użytkownika,
- uzasadnić wybór FastAPI i SQLite,
- narysować prosty przepływ danych,
- wyjaśnić różnicę między `id` i `api_id`,
- wyjaśnić kolejność importu,
- prześledzić jeden mecz w `calculate_standings`,
- wyjaśnić działanie offline,
- wskazać własny wkład,
- wskazać ograniczenia bez ukrywania ich,
- uruchomić i pokazać aplikację.

Nie trzeba znać na pamięć:

- numeru każdej linii,
- wszystkich wartości CSS,
- wewnętrznej implementacji FastAPI i Uvicorna,
- całej odpowiedzi JSON API-Football,
- identyfikatorów wszystkich drużyn.

Komentarze w kodzie są pomocą i mogą pozostać w projekcie, ale odpowiedź na obronie powinna wynikać z rozumienia przepływu.

## 33. Stan repozytorium przy tworzeniu tego pliku

Przed utworzeniem dokumentu:

- gałąź: `main`,
- lokalny `main` był zgodny z `origin/main`,
- katalog roboczy był czysty,
- ostatni commit: `807cafb Clean up main page code comments`.

Po dodaniu tego pliku należy wykonać nowy commit i `git push`, aby kontekst był dostępny na nowym laptopie.

## 34. Najważniejsza zasada na dalszy rozwój

Nie należy mierzyć jakości projektu wyłącznie liczbą funkcji lub linii kodu. W tej pracy wartością jest kompletny, działający i zrozumiały przepływ:

```text
zewnętrzne API -> walidacja i mapowanie -> lokalna baza -> obliczenia -> wizualizacja -> test
```

Jeżeli nowa funkcja nie wzmacnia celu pracy, prezentacji, testowalności albo zrozumienia, prawdopodobnie nie jest obecnie potrzebna.
