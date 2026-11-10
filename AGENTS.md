# Zasady pracy z projektem SportVision

Te instrukcje obowiązują każdego asystenta pracującego w tym repozytorium.

## Źródła prawdy

1. Najpierw przeczytaj w całości `KONTEKST_SPORTVISION.md` i `README.md`.
2. Aktualny kod, lokalna baza i stan Git opisują bieżący stan wykonania.
3. `KONTEKST_SPORTVISION.md` opisuje wizję, zakres, historię i sposób współpracy.
4. Jeżeli kod i dokumentacja są rozbieżne, wskaż różnicę. Nie poprawiaj jej automatycznie.
5. Jeżeli informacji nie ma w projekcie ani w wypowiedzi użytkownika, napisz: „Brak potwierdzonej informacji w kontekście projektu” i zapytaj użytkownika.
6. Nie przedstawiaj przypuszczenia jako faktu. Rozdzielaj potwierdzone fakty, wnioski i propozycje.

## Bezpieczeństwo

- Nie czytaj, nie pokazuj i nie modyfikuj zawartości `.env`.
- Możesz wyłącznie sprawdzić, czy `.env` istnieje.
- Nigdy nie wypisuj ani nie zapisuj klucza API.
- Nie dodawaj `.env`, plików `.db`, `.venv` ani `__pycache__` do Git.
- Nie wykonuj destrukcyjnych poleceń Git.
- Nie wykonuj commita ani push bez wyraźnego polecenia użytkownika.
- Nie korzystaj z internetu, jeśli nie jest potrzebny do zadania lub użytkownik tego zabronił.

## Styl projektu

- Odpowiadaj po polsku.
- Projekt ma pozostać prosty, krótki i wystarczający do pracy inżynierskiej.
- Nie dodawaj technologii, zależności, frameworków ani warstw bez potwierdzonej potrzeby.
- Preferuj najmniejszą zmianę rozwiązującą konkretny problem.
- Nie przebudowuj architektury bez wyraźnej zgody użytkownika.
- Przed większą zmianą opisz problem, pliki, zakres i prostsze alternatywy oraz zaczekaj na zgodę.
- Domyślnie pozwól użytkownikowi pisać kod samodzielnie. Edytuj automatycznie, gdy wyraźnie o to poprosi.
- Nowy kod wyjaśniaj prostym językiem, odnosząc Python do C# i low-code.
- Dodawaj krótkie komentarze do istotnych nowych linii, ale nie komentuj oczywistości wielokrotnie.
- Po zmianie sprawdź składnię, odpowiednie widoki i `git diff`.
- Po dniu pracy przypomnij o aktualizacji historii projektu.

## Tryb nauki

Przy omawianiu funkcji odpowiedz na cztery pytania:

1. Co ją uruchamia?
2. Jakie dane otrzymuje?
3. Co robi z danymi?
4. Co zwraca?

Blok nauki zakończ krótkim pytaniem ABCD. Po odpowiedzi użytkownika podaj prawidłową odpowiedź i wyjaśnienie.

