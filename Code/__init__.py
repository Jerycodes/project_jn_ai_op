"""
Package «Code» – LLM Requirements Calculator
============================================
Selbstständige Arbeit, Modul AI Operations (FHNW HSW, HS26) – Jeremy Nathan

Aufbau nach Schichten (Separation of Concerns):

    katalog.py   Daten-Schicht      Quantisierungen, Klasse Modell, Modellkatalog
    rechner.py   Geschäftslogik     Rechenfunktionen und berechne_empfehlungen()
    cli.py       Ein-/Ausgabe       Terminal: Fragen stellen, Ergebnis ausgeben
    main.py      Ein-/Ausgabe       API mit FastAPI (Schritt 2)

Abhängigkeiten laufen nur in eine Richtung:
    cli.py / main.py  ->  rechner.py  ->  katalog.py
Die Logik weiss nichts von Terminal oder API; die Daten wissen nichts von der Logik.

Ausführen (immer aus dem Projektordner, nicht aus «Code»):
    python -m Code.cli                                  Terminal-Version
    uvicorn Code.main:app --reload --reload-dir Code    API (ab Schritt 2)

Diese Datei macht den Ordner «Code» zu einem Python-Package, damit die Importe
«from Code.katalog import …» eindeutig funktionieren.
"""
