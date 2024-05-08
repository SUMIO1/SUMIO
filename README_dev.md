# Rozpoczęcie pracy nad projektem
## Pobranie repozytorium

Aby rozpocząć pracę nad projektem, należy pobrać repozytorium.
Można to zrobić poprzez użycie polecenia `git clone <link do repozytorium>`, lub przez pobranie pliku .zip.

## Środowisko wirtualne

Środowisko wirtualne może być utworzone ręcznie lub automatycznie przy użyciu Pycharma.
Po otwarciu folderu projektu w Pycharmie, pojawi się okno dialogowe z prośbą o utworzenie środowiska wirtualnego.
Należy wybrać bazowy interpreter (Python 3.10) i wczytać zależności z pliku `requirements.txt`.
W przypadku konfiguracji ręcznej należy użyć polecenia 
```
pip install -r ./requirements.txt
```

## Aktywacja wirtualnego środowiska w konsoli

PyCharm automatycznie aktywuje wirtualne środowisko po uruchomieniu konsoli 
(można rozpoznać to po tym, że linijka zaczyna się od słowa `(venv)`). 
Jeśli nie, należy to zrobić ręcznie poprzez wykonanie skryptu `venv/Scripts/activate`.

## Instalacja w trybie edycji

Aby stworzyć link (symlink) do aktualnego katalogu z kodem źródłowym, należy wykonać:
```
pip install -e .
```

## Instalacja pakietów dla deweloperów

W już aktywowanej konsoli należy wpisać komendę 
```
pip install -r ./requirements_dev.txt
``` 
Aby upewnić się, że wszystkie pakiety zostały poprawnie zainstalowane, można użyć komendy
```
pip freeze
```
która wyświetli listę zainstalowanych pakietów.

## Lokalne komendy

Projekt zawiera zestaw narzędzi wspomagających rozwój oprogramowania,
które można wywoływać z poziomu wiersza poleceń:
```
mypy src
```
```
pytest
```
```
tox
```

# Praca na Githubie

## Współpraca repozytorium z Jirą

**Ważne** Każdy task w Jirze ma swój unikalny klucz.
W przypadku naszego projektu klucze te mają następujący format: `SIO-15`, `SIO-4` itp. 
Aby zapewnić współpracę między Jirą a Githubem, należy przestrzegać następujących zasad:
- Nazwa gałęzi musi odpowiadać kluczowi taska w Jirze, np. `SIO-15`.
- Podczas tworzenia commitów należy stosować szablon: `[SIO-15] <twoja wiadomość commita>`. 
Przykłady: `[SIO-15] Add the new shiny feature`, `[SIO-15] Fix a horrible bug`

## Praca na branchach

Tak długo jak posiadacie swoją gałąź na wyłączność,
możecie robić z nią co się żywnie podoba (na własną odpowiedzialność):
- amendować commity
- revertować commity
- usuwać commity
- squashować commity
- force pushować gałąź na Githuba (ostrożnie, nie usuńcie sobie waszej pracy).

Ważne jest tylko to, aby stan gałęzi był poprawny (i najlepiej elegancki, co uprzyjemni code review) podczas wystawiania pull requesta do maina. 

## CI

Każdy commit wypchnięty do repozytorium będzie sprawdzany przez Githuba pod kątem poprawności 
za pomocą CI (Continuous Integration). Więcej informacji na Githubie w zakładce Actions.

## Pull requesty

Po ukończeniu pracy na gałęzi `SIO-15` i stwierdzeniu, że zmiany są gotowe do scalenia z główną gałęzią `main`,
należy utworzyć pull requesta. W pull requestcie należy:
- opisać dokładnie wprowadzone zmiany
- dodać odpowiednie etykiety
- przypisać recenzentów (czy jakie tam obecnie panują ustalenia w zespole).

Aby pull request mógł zostać zaakceptowany i dołączony do głównego brancha, muszą zostać spełnione następujące warunki:
- Wszystkie konwersacje muszą być oznaczone jako "resolved".
- Wszystkie testy muszą zakończyć się sukcesem.
- Co najmniej dwie osoby (zależnie od obecnie panujących ustaleń) muszą zrobić review i zaakceptować pull requesta.
- Branch musi być aktualna w stosunku do głównego brancha.
- W wyjątkowych sytuacjach można użyć opcji 
"Merge without waiting for requirements to be met (bypass branch protections)", 
ale należy tego za wszelką cenę unikać i uprzednio należy skonsultować się z zespołem.

Każdy opisany tutaj krok i wprowadzone reguły / ustalenia itp. jak najbardziej podlegają negocjacji i zmianom.
Nie jestśmy skazani na te zasady w imię zasad. Możemy nimi manipulować i je poprawiać / zmieniać.
