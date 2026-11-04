# LLM Requirements Calculator

Welches lokale Sprachmodell (LLM) läuft auf meinem Computer? Das Programm nimmt Hardware-Angaben
entgegen und liefert passende Modelle mit Speicherbedarf, Bewertung und bester Wahl.

Selbstständige Arbeit im Modul **AI Operations** (BSc Business AI, FHNW Hochschule für Wirtschaft, HS26) – Jeremy Nathan.
Projektaufgabe 1.1 «DevOps lokal»: Programm → API → Oberfläche. Projektaufgabe 1.2 «DevOps Cloud»: Git und GitHub,
automatische Tests, Pipeline, Betrieb auf render.com. Der Bericht dazu liegt separat (Vorlage des Dozenten); diese README
ist die technische Kurzanleitung zum Code.

## Eingabe und Ausgabe

| Eingabe | Ausgabe |
|---|---|
| Arbeitsspeicher (RAM) in GB · Betriebssystem · optional Grafikspeicher (VRAM) einer separaten Grafikkarte · freier Platz auf der Festplatte · Anzahl Modelle · Quantisierung · Kontextfenster | Für das Modell nutzbarer Arbeits-/Grafikspeicher · maximale und optimale Modellgrösse (Faustregel) · beste Wahl · alle Modelle des Katalogs mit benötigtem Speicher, Dateigrösse, Bewertung (optimal / passt / knapp / zu gross) und Festplatten-Prüfung · Hinweise |

Begriffe, konsequent im ganzen Projekt: **Arbeitsspeicher (RAM)** = Speicher, in dem das Modell liegt, während es
rechnet · **Grafikspeicher (VRAM)** = Arbeitsspeicher einer separaten Grafikkarte · **Festplatte** = dauerhafter Platz für die Modelldatei.

## Schnellstart

Voraussetzung: Python 3.14, Visual Studio Code. Alle Befehle im Projektordner `project_jn_ai_op` ausführen.

```bash
python3 -m venv .venv                 # einmalig: virtuelle Umgebung anlegen
source .venv/bin/activate             # jede Terminal-Sitzung (Windows: .\.venv\Scripts\activate)
pip install -r requirements.txt       # einmalig: FastAPI, uvicorn, pydantic (nur für die API nötig)
pip install -r requirements-dev.txt   # zusätzlich für die Tests: pytest, httpx2 (Aufgabe 1.2; nicht auf render)
```

| Was | Befehl | Dann |
|---|---|---|
| Terminal-Programm (Schritt 1) | `python -m Code.cli` | Fragen beantworten, Enter = Standardwert |
| API (Schritt 2) | `uvicorn Code.main:app --reload --reload-dir Code` | `http://127.0.0.1:8000/docs` → POST /empfehlung → Try it out → Execute |
| Oberfläche (Schritt 3) | gleicher Server | `http://127.0.0.1:8000/` → Beispiel wählen oder Werte eingeben |
| Tests (Aufgabe 1.2) | `pytest` | 17 Tests aus `tests/`, Ergebnis «17 passed» |

Server stoppen: `Ctrl + C`. Die Pakete braucht nur die API; das Terminal-Programm läuft mit der Standardbibliothek.

## Aufbau

```
project_jn_ai_op/
├── .venv/                  virtuelle Umgebung (lokal, nicht versioniert)
├── .gitignore              was Git nicht versioniert (.venv, __pycache__, lokale Exporte …)
├── .python-version         3.14 – Python-Version für render.com und die Pipeline
├── .github/workflows/
│   └── tests.yml           Pipeline: GitHub Actions führt pytest bei jedem Push und Pull Request aus
├── requirements.txt        Pakete für den Betrieb (API), Versionen fix – das installiert render
├── requirements-dev.txt    zusätzlich für Entwicklung und Tests: pytest, httpx2
├── pytest.ini              Einstellungen für pytest (Projektordner importierbar, Tests in tests/)
├── CHANGELOG.md            Änderungen je Version (1.0.0, 1.1.0, 1.1.1)
├── README.md               diese Datei
├── docs/                   quellen.md · hilfsmittel.md · arbeitsjournal.md (Grundlage für den Bericht)
├── tests/
│   ├── test_rechner.py     8 Tests der Geschäftslogik (Rechenbeispiel aus dem Bericht)
│   └── test_api.py         9 Tests der API mit dem TestClient von FastAPI
└── Code/
    ├── __init__.py         macht «Code» zum Package, beschreibt die Schichten
    ├── katalog.py          Daten: Quantisierungen, Klasse Modell, Modellkatalog (8 Modelle, je mit Quelle)
    ├── rechner.py          Geschäftslogik: Rechenfunktionen, berechne_empfehlungen()
    ├── cli.py              Ein-/Ausgabe Terminal: fragen → rechnen → ausgeben
    ├── main.py             Ein-/Ausgabe API: Pydantic-Schemas, POST /empfehlung, GET /health, liefert static/ aus
    └── static/             Oberfläche: index.html (Struktur), style.css (Gestaltung), app.js (ruft die API auf)
```

Abhängigkeiten laufen nur in eine Richtung – die Logik kennt weder Terminal noch API, die Daten kennen die Logik nicht:

```
cli.py  ──┐
          ├──►  rechner.py  ──►  katalog.py
main.py ──┘
   ▲
static/app.js (Browser, per fetch an POST /empfehlung)
```

## Rechenweg (Kurzform, Details und Quellen im Code)

1. **Nutzbarer Speicher** – `rechner.nutzbarer_speicher()`: Grafikspeicher minus Reserve; auf macOS der Anteil des Arbeitsspeichers, den das System der GPU freigibt (2/3, ab 32 GB 3/4); sonst 75 % des Arbeitsspeichers (CPU).
2. **Bedarf pro Modell** – Gewichte (Parameter × Bits pro Gewicht / 8, zugleich Dateigrösse) + KV-Cache (Tokens × KB pro Token, aus der Modellarchitektur) + 0.75 GB Overhead.
3. **Bewertung** – Anteil am nutzbaren Speicher: ≤ 70 % optimal · ≤ 90 % passt · ≤ 100 % knapp · darüber zu gross. Beste Wahl = grösstes Modell mit optimal/passt, das auch auf die Festplatte passt.
4. **Faustregel** – maximale Modellgrösse = (nutzbar − Overhead) × 8 / Bits pro Gewicht; optimal = 70 % davon.

Jede Zahl ist in `katalog.py` bzw. `rechner.py` entweder mit Quelle belegt oder als eigene Annahme markiert.

## API

| Methode | Pfad | Zweck |
|---|---|---|
| POST | `/empfehlung` | Hardware (JSON) → Empfehlungen (JSON); Schemas `HardwareAnfrage` / `Empfehlung` in `main.py` |
| GET | `/health` | Lebenszeichen `{"status": "ok"}` |
| GET | `/` und `/static/…` | Oberfläche (nicht in `/docs` gelistet) |

Beispiel:

```bash
curl -X POST http://127.0.0.1:8000/empfehlung -H "Content-Type: application/json" \
  -d '{"ram_gb": 36, "betriebssystem": "macos", "freier_speicher_gb": 200, "anzahl_modelle": 2, "quantisierung": "Q4_K_M", "kontextfenster": 8192}'
```

Antwort (gekürzt): `{"speichertyp": "unified", "nutzbarer_speicher_gb": 27.0, "max_parameter_mrd": 43.4, "optimale_parameter_mrd": 30.4, "beste_wahl": "Qwen3 32B", "passend": [...], "zu_gross": [...], "hinweise": [...]}`.
Ungültige Eingaben (z. B. `ram_gb: -1`) beantwortet die API mit Status 422 und einer Feldliste.

## Aufgabe 1.2: Git, GitHub, Tests, Pipeline und render.com

Öffentlich erreichbar: https://llm-requirements-calculator.onrender.com (Oberfläche) · `/docs` (API) · `/health` (Lebenszeichen).
Repository: https://github.com/Jerycodes/project_jn_ai_op

### Branch-Modell (Gitflow)

| Zweig | Zweck | Geht auf render? |
|---|---|---|
| `main` | Produktion; jeder Stand trägt ein Tag (`v1.0.0`, `v1.1.0`, `v1.1.1`) | ja, automatisch bei jedem Push |
| `develop` | Sammelzweig für fertige, geprüfte Features | nein |
| `feature/<thema>` | eine Funktion pro Zweig; zweigt von `develop` ab und mündet dort wieder ein | nein |
| `release/<version>` | Version fertig machen (Nummer, Changelog), dann nach `main` und zurück nach `develop` | nein |
| `hotfix/<version>` | Korrektur ab `main`; danach nach `main` und nach `develop` | nein |

Ablauf eines Features: `git switch -c feature/x` → Test und Code → `pytest` → Commit und `git push -u origin feature/x`
(Pipeline läuft) → Merge nach `develop` (Pull Request oder `git merge`) → manuelle Prüfung lokal mit uvicorn → Release nach `main`.

### Tests (pytest)

- `tests/test_rechner.py`: 8 Tests der Geschäftslogik mit dem Rechenbeispiel aus dem Bericht (Mac 16 GB, Q4_K_M, 8192 Tokens)
- `tests/test_api.py`: 9 Tests der API über den TestClient von FastAPI, ohne laufenden Server: `/health`, gültige Anfrage 200,
  ungültige Anfrage 422, Startseite, Eingabegrenzen
- `pytest.ini`: `pythonpath = .` (Importe wie bei uvicorn), `testpaths = tests`
- Werkzeuge nur für die Entwicklung stehen in `requirements-dev.txt`; render installiert weiterhin nur `requirements.txt`

### Pipeline (GitHub Actions, Continuous Integration)

`.github/workflows/tests.yml`: Bei jedem Push und Pull Request startet GitHub einen Linux-Rechner, installiert Python
(Version aus `.python-version`) und die Pakete aus `requirements-dev.txt` und führt `pytest` aus. Das Ergebnis erscheint als
Häkchen am Commit und im Pull Request. Läufe: https://github.com/Jerycodes/project_jn_ai_op/actions

### Betrieb (render.com, Continuous Deployment)

- Web Service, Region Frankfurt, Instance Free; Build Command `pip install -r requirements.txt`;
  Start Command `uvicorn Code.main:app --host 0.0.0.0 --port $PORT`
- Auto-Deploy «On Commit» auf `main`: Push → Build → Deploy. Beim Umschalten laufen alte und neue Instanz kurz parallel
- Health Check Path `/health`: render schaltet erst um, wenn der neue Server `{"status": "ok"}` liefert
- Python-Version aus `.python-version` (3.14): dieselbe wie lokal und in der Pipeline
- Free-Tarif: nach 15 Minuten ohne Anfrage schläft der Dienst; der nächste Aufruf dauert bis zu einer Minute
- Monitoring im Dashboard: Events (Deploys), Logs (jede Anfrage, wie lokal im Terminal), Metrics

### Versionen und Grenzen der Umsetzung

- Versionen und Tags: `CHANGELOG.md` und https://github.com/Jerycodes/project_jn_ai_op/tags
- Nicht umgesetzt: Staging-Server (die Prüfung vor einem Release erfolgt lokal auf `develop`), Docker (render baut
  aus `requirements.txt` und `.python-version`), statische Code-Analyse

## Dokumentation und Quellen

- `docs/quellen.md` – alle verwendeten Quellen mit Link, Abrufdatum und Verwendungsstelle (APA 7)
- `docs/hilfsmittel.md` – Hilfsmittelverzeichnis (KI-Einsatz) gemäss Merkblatt HSW-FHNW
- `docs/arbeitsjournal.md` – Arbeitsschritte, Entscheidungen, Eigenleistung
- `CHANGELOG.md` – Änderungen je Version
- Jede Code- und Testdatei beginnt mit einem Kopfkommentar: Zweck, KI-Deklaration, Quellen (Q1–Q14)

## Abweichung vom Beispiel des Dozenten

Das Beispiel (`primzahl-info`) legt Logik und API in eine Datei und pinnt `fastapi==0.115.0`, `uvicorn==0.30.6`,
`pydantic==2.9.2`. Dieses Projekt trennt Daten, Logik und Ein-/Ausgabe in vier Dateien und verwendet aktuelle
Paketversionen, weil die gepinnten Versionen unter Python 3.14 nicht installierbar sind (Begründung in `requirements.txt`).
Startbefehl und Ordnerkonvention (`Code/`, `uvicorn Code.main:app`) sind identisch.
