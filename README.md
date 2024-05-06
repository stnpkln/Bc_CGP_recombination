# Bakalářská práce

Praktická část bakalářské práce s názvem "Využití operátoru křížení v kartézském genetickém programování"

## Spuštění automatických testů
- v `/src` spustit `python -m unittest`

## Generování dokumentace
- v rootovém adresáři spustit `./generate-docs.sh`

## Spouštění experimentů
- v souboru `/src/experiment.py`:
	- odkomentovat getCGPdata() (zakomentováno kvůli chybnému frameworku pdocs, který jinak spouští při generování dokumentace experimenty)
	- lze přenastavit parametry běhů, popsáno v souboru
- spustit `python experiment.py`
- výstupy experimentů budou v souborech `data-general.csv` a `data-run-details.csv`

## Zpracování dat
- soubor `/src/graphs/data_visualizer`
- spustit `python data_visualizer.py`, `data-general.csv` a `data-run-details.csv` musí být v adresáři ze kterého se spouští
- skript vygeneruje grafy ve formátu pdf a tabulku csv se zpracovanými daty jednotlivých algoritmů

Autor: Petr Bromnik
Vedoucí práce: Ing. Martin Hurta
Datum: Duben 2024