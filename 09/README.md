# Vlastna uloha na nativne asynchronne programovanie

Vytvorili sme 2 skripty - `[db_reader_async.py, db_reader_sync.py]`, ktore maju rovnaky vystup, robia to iste, ale ich implementacia je rozdielna.

Nasim cielom bolo prechadzat SQLite databazu `capitals.db` a hladat hlavne mesta krajin specifikovanych v poli `COUNTRIES`.

### Struktura databazy:
- Databaza obsahuje jedinu tabulku - `CAPITALS`
- Tabulka `CAPITALS` obsahuje 3 stlpce: [id, country, capital]
- Stlpec `id` je unikatny identifikator pre kazdy riadok
- Stlpec `country` obsahuje nazvy krajin
- Stlpec `capital` obsajuje hlavne mesto pre kazdu krajinu

### Princip cinnosti programu
V programe sa snazime o to, aby sme pomocou koprogramov (generatory v `*_sync.py` verzii a nativne asyncio v `*_async.py` verzii) prehladavali databazu a nachadzali k zadanym krajinam hlavne mesta.

### Priklad vystupu pre db_reader_sync.py:
```bash
One: running
One: Slovakia - Bratislava, time elapsed 243401 [ns]
Two: running
Two: China - Beijing, time elapsed 35937 [ns]
One: running
One: USA - Washington, time elapsed 31426 [ns]
Two: running
Two: Czech Republic - Paha, time elapsed 29021 [ns]
One: running
One: Poland - Warszawa, time elapsed 27920 [ns]
Two: running
Two: Taiwan - Taipei, time elapsed 30631 [ns]
538670 [ns] vs 398336.0 [ns] (app runtime vs sum of partial times)
```

### Priklad vystupu pre db_reader_async.py:
```bash
One: running
Two: running
One: Slovakia - Bratislava, time elapsed 569332 [ns]
Two: China - Beijing, time elapsed 598175 [ns]
One: running
Two: running
One: USA - Washington, time elapsed 611418 [ns]
Two: Czech Republic - Paha, time elapsed 728408 [ns]
One: running
Two: running
One: Poland - Warszawa, time elapsed 776487 [ns]
Two: Taiwan - Taipei, time elapsed 495881 [ns]
2903820 [ns] vs 3779701 [ns] (app runtime vs sum of partial times)
```

### Zhodnotenie
Obidve verzie robia pomerne jednoduche operacie (sql SELECT), pretoze databaza je iba subor vo formate sqlite, takze sme museli prejst z merania v milisekundach na meranie v nanosekundach. \
Pri porovnavani sme zohladnili 2 ukazovatele:
- app runtime
- sum of partial times
Mozeme vidiet, ze pri `async` verzii je `app runtime` o cosi mensi ako suma vsetkych ciastkovych behov. To nam potvrdzuje, ze sme vyhodne zefektivnili vyuzitie CPU, kedze samotny hlavny koprogram `main` bezal pomalsie ako jednotlive volania koprogramu `get_capital`. \
Na druhu stranu, ked sa pozrieme na priklad vystupu `sync` verzie, tak tam mozeme vidiet, ze `app runtime` je vacsi ako `sum of partial times` a teda to nam hovori o tom, ze `main` bezal ovela dlhsie, spustal koprogram `get_capital` a neefektivne cakal, kym dobehne.
