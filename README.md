# Bc_CGP_recombination

Bakalářská práce na téma "Využití operátoru křížení v kartézském genetickém programování"

# Plán
- dořešit TODOčka v kódu ***DONE***
- více protestovat (ověřit validitu výstupu algoritmu) ***DONE***
- nastavit parametry tak aby byly vhodné ? ASI ***DONE*** ?
- experimentovat s klasickým CGP - 1 + lambda ***DONE***
- vyřešit generování dokumentace (nejspíš sphynx) ***DONE***
- vytvořit větve pro algoritmy křížení ***DONE***
- otestovat, zjistit nejlepší parametry
- začít psát bakalářskou práci
   - nadpisy
   - úvod (CGP obecně, CGP křížení...)

## testování
- v /src spustit `python -m unittest`

## dokumentace
- v /docs
- generování: `./generate-docs.sh`

### dotazy:
- volba evolucni strategie ke krizeni 1 a 2
- co vsechno za data bych mel sbirat pro vyhodnocovani za metriky
- je 1e7 fitness evaluaci dostacujici pro metriky (vychazi to asi na 1-2 hodiny max)
   - MOMENTALNE TO VYCHAZI: 400 minut na vsechny funkce * 3 algorytmy * 30 pokusu = 25 dni...
   - u puvodniho clanku pouzili 10e8, ale to by dle mych vypoctu bylo na muj notas az moc