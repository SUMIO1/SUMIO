# Rozpoczęcie pracy nad projektem
## Pobranie repozytorium

Aby rozpocząć pracę nad projektem, należy pobrać repozytorium.
Można to zrobić poprzez użycie polecenia git clone, lub pobranie pliku .zip.

## Środowisko wirtualne

Środowisko wirtualne może być utworzone ręcznie lub automatycznie przy użyciu Pycharma.
Po otwarciu folderu projektu w Pycharmie, pojawi się okno dialogowe z prośbą o utworzenie środowiska wirtualnego.
Należy wybrać bazowy interpreter (Python 3.10) i wczytać zależności z pliku `requirements.txt`.

## Aktywacja wirtualnego środowiska w konsoli

PyCharm automatycznie aktywuje wirtualne środowisko po uruchomieniu konsoli 
(można rozpoznać to po tym, że linijka zaczyna się od słowa `(venv)`). 
Jeśli nie, należy to zrobić ręcznie poprzez wykonanie skryptu `venv/Scripts/activate`.

## Instalacja pakietów dla deweloperów

W już aktywowanej konsoli należy wpisać komendę `pip install -r ./requirements_dev.txt`. 
Aby upewnić się, że wszystkie pakiety zostały poprawnie zainstalowane, można użyć komendy `pip freeze`,
która wyświetli listę zainstalowanych pakietów.

## Lokalne komendy

Projekt zawiera zestaw narzędzi wspomagających rozwój oprogramowania, które można wywoływać:
- `mypy src`,
- `pytest`, 
- `tox`.

## Współpraca repozytorium z Jirą

**Ważne** Każdy task w Jirze ma swój unikalny klucz.
W przypadku naszego projektu klucze te mają następujący format: `SIO-15`, `SIO-4` itp. 
Aby zapewnić współpracę między Jirą a Githubem, należy przestrzegać następujących zasad:

- Nazwa gałęzi musi odpowiadać kluczowi taska w Jirze, np. `SIO-15`.
- Podczas tworzenia commitów należy stosować szablon: `[SIO-15] <twoja wiadomość commita>`.

# Praca na Githubie
## CI

Każdy commit wypchnięty do repozytorium będzie sprawdzany przez Githuba pod kątem poprawności 
za pomocą CI (Continuous Integration). Więcej informacji znajdziesz na Githubie w zakładce Actions.

## Pull requesty

Po ukończeniu pracy na gałęzi `SIO-15` i uzgodnieniu, że zmiany są gotowe do scalenia z główną gałęzią `main`,
należy utworzyć pull request. W pull requestcie należy opisać dokładnie wprowadzone zmiany oraz dodać
odpowiednie etykiety i przypisać recenzentów.

Aby pull request mógł zostać zaakceptowany i dołączony do głównej gałęzi, muszą zostać spełnione następujące warunki:
- Wszystkie konwersacje muszą być oznaczone jako "resolved".
- Wszystkie testy muszą zakończyć się sukcesem.
- Co najmniej dwie osoby muszą zrobić review i zaakceptować pull request.
- Gałąź musi być aktualna w stosunku do głównej gałęzi.
- W wyjątkowych sytuacjach można użyć opcji 
"Merge without waiting for requirements to be met (bypass branch protections)", 
ale należy tego za wszelką cenę unikać i należy skonsultować się z zespołem.

Każdy opisany tutaj krok, wprowadzone zasady / ustalenia itp. jak najbardziej podlegają negocjacji i zmianom.
Nie jestśmy skazani na te zasady w imię zasad, tylko możemy nimi manipulować i je poprawiać / zmieniać.
