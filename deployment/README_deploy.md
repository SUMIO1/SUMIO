# Deployment aplikacji

Żeby zdeployować naszą aplikację, musimy przygotować plik wykonywalny `sumio.exe`. Pozwoli to na uruchomienie
naszej aplikacji na systemie operacyjnym Windows.

Plik wykonywalny przygotowany będzie za pomocą biblioteki [PyInstaller](https://pyinstaller.org/en/stable/).

Aby stworzyć taki plik, należy wykonać poniższe kroki.

# Przygotowanie środowiska

Najpierw należy upewnić się, że wykonało się wszystkie kroki z pliku [README_dev.md](./README_deploy).
Konfigurację należy przeprowadzić do punktu "Instalacja w trybie edycji" włącznie.

Po tym kroku powinniśmy mieć przygotowanie środowisko wirtualne dla Pythona.

# Instalacja [PyInstallera](https://pyinstaller.org/en/stable/) 

Aby wykonać ten krok, w konsoli należy wywołać komendę
```
pip install --upgrade pyinstaller
```

# Utworzenie pliku `sumio.exe`

Upewnij się, że znajdujesz się w folderze `deployment`. Jeśli nie, przejdź tam z pomocą komendy `cd`.
Jest to o tyle ważne, że pliki powstałe podczas generacji pliku wykonywalnego domyślnie zapisywane są w
bieżącym katalogu roboczym.

Ostatnim krokiem jest wywołanie jednej z dwóch komend:
1. ```python -m PyInstaller .\sumio.spec``` - komenda podstawowa. Skrupulatnie wypisuje informacje na wyjściu standardowym   

2. ```python -m PyInstaller --log-level ERROR .\sumio.spec``` - komenda uproszczona. Raportowanie ogranicza się do błędów.

Po zakończeniu procedury w katalogu `dist` pojawi się plik wykonywalny.