"""
main.py – Ein-/Ausgabe über eine API (FastAPI)
===============================================
Selbstständige Arbeit, Modul AI Operations (FHNW HSW, HS26) – Jeremy Nathan
Projektaufgabe 1.1 «DevOps lokal», Schritt 2: das Programm als API bereitstellen.

Diese Datei ist die zweite «Benutzerseite» neben cli.py: Statt Fragen im Terminal
nimmt sie eine HTTP-Anfrage mit JSON entgegen, ruft dieselbe Geschäftslogik in
rechner.py auf und gibt das Ergebnis als JSON zurück. Sie rechnet selbst nichts.

Aufbau gemäss Modul-Slides [Q7], Folien 6–9, und Beispielcode des Dozenten:
    - Die Business-Logik ist eine normale Python-Funktion (berechne_empfehlungen in rechner.py)
    - FastAPI stellt sie über einen Endpunkt bereit: @app.post("/empfehlung")
    - Eingabe- und Ausgabe-Schema werden als Pydantic-Klassen definiert; FastAPI prüft
      damit die Daten automatisch und erzeugt die Doku unter /docs
    - uvicorn ist der ASGI-Server, der die App ausführt

Ablauf einer Anfrage:
    Client (Web-Oberfläche unter /, oder /docs) -> uvicorn -> FastAPI -> rechner.py -> JSON zurück

Schritt 3: Dieselbe App liefert unter «/» die Web-Oberfläche für Endkunden aus
(Ordner Code/static: index.html, style.css, app.js). Die Oberfläche ruft POST /empfehlung
auf – es gibt also nur eine Berechnung für Terminal, /docs und Oberfläche.

Ausführen (aus dem Projektordner, venv aktiviert, Pakete aus requirements.txt installiert):
    uvicorn Code.main:app --reload --reload-dir Code
        Code.main:app  = Ordner.Datei:App-Objekt (Konvention des Dozenten)
        --reload       = Server startet bei Codeänderungen automatisch neu
        --reload-dir   = nur den Ordner Code überwachen (sonst reagiert er auch auf .venv)
    Testen: http://127.0.0.1:8000/        -> Web-Oberfläche (Schritt 3)
            http://127.0.0.1:8000/docs    -> technische API-Doku: POST /empfehlung -> «Try it out» -> «Execute»

KI-Deklaration (Hilfsmittelverzeichnis, Merkblatt HSW-FHNW)
    Erstellt am 2026-10-07 mit Unterstützung von Claude (Anthropic; Modell Claude Fable 5.1,
    genutzt über die Claude-Desktop-App). Vorgaben, Entscheidungen (Thema, Struktur,
    Sprache, Umfang), Prüfung und Test: Jeremy Nathan.

Quellen (Nummerierung gilt im ganzen Projekt)
    [Q7] Modul-Slides «Projektaufgabe DevOps – Lokal» (1_1.pdf, Folien 6–9: FastAPI, uvicorn,
         Ordner «Code», Start mit uvicorn Code.main:app, Test unter /docs) und Beispielcode
         des Dozenten (Code/main.py: Pydantic-Schemas, @app.post, response_model),
         Moodle AI Operations HS26 – primäre Quelle
    [Q8] FastAPI-Dokumentation, Tutorial (abgerufen am 2026-10-07): «First Steps» (Start,
         Doku unter /docs), «Request Body» (Eingabe als Pydantic-Klasse) und «Static Files»
         (Ausliefern der Oberfläche): https://fastapi.tiangolo.com/tutorial/
"""

from pathlib import Path
from typing import Literal

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from Code.rechner import berechne_empfehlungen

# Ordner mit der Web-Oberfläche – relativ zu dieser Datei, damit es unabhängig vom
# Arbeitsverzeichnis funktioniert (lokal wie später auf render.com).
STATIC_DIR = Path(__file__).parent / "static"

# Erlaubte Werte als Typen: Alles andere lehnt FastAPI mit Status 422 und Fehlertext ab.
Betriebssystem = Literal["macos", "windows", "linux"]
Quantisierung = Literal["Q4_K_M", "Q5_K_M", "Q6_K", "Q8_0", "F16"]   # muss zu QUANTISIERUNG_BITS in katalog.py passen

# ---------------------------------------------------------------------------
# 1) Eingabe-Schema: Was der Client im Request-Body (JSON) schicken muss
#    Die Feldnamen sind dieselben wie die Parameter von berechne_empfehlungen().
# ---------------------------------------------------------------------------

class HardwareAnfrage(BaseModel):
    """Hardware-Angaben des Benutzers. Field(...) = Pflichtfeld; gt/ge/le = erlaubter Bereich."""

    ram_gb: float = Field(..., gt=0, description="Arbeitsspeicher (RAM) in GB – nicht die Festplatte")
    betriebssystem: Betriebssystem = Field(..., description="macos, windows oder linux")
    vram_gb: float | None = Field(None, ge=0, description="Grafikspeicher (VRAM) einer separaten Grafikkarte in GB; leer bei macOS oder ohne Grafikkarte")
    freier_speicher_gb: float = Field(..., ge=0, description="Freier Platz auf der Festplatte in GB")
    anzahl_modelle: int = Field(1, ge=1, le=20, description="Wie viele Modelle gleichzeitig auf der Festplatte liegen sollen")
    quantisierung: Quantisierung = Field("Q4_K_M", description="Quantisierungsformat (GGUF)")
    kontextfenster: int = Field(8192, ge=512, le=262144, description="Kontextfenster in Tokens")

    # Beispiel, das in /docs unter «Try it out» vorausgefüllt ist.
    model_config = {"json_schema_extra": {"examples": [{
        "ram_gb": 36, "betriebssystem": "macos", "vram_gb": None, "freier_speicher_gb": 200,
        "anzahl_modelle": 2, "quantisierung": "Q4_K_M", "kontextfenster": 8192,
    }]}}

# ---------------------------------------------------------------------------
# 2) Ausgabe-Schema: Wie die Antwort (JSON) aufgebaut ist
#    Entspricht 1:1 dem Dictionary, das berechne_empfehlungen() zurückgibt.
# ---------------------------------------------------------------------------

class ModellErgebnis(BaseModel):
    """Ein durchgerechnetes Modell aus dem Katalog."""

    name: str
    parameter_mrd: float = Field(description="Parameter in Milliarden")
    dateigroesse_gb: float = Field(description="Grösse der Modelldatei auf der Festplatte in GB")
    kv_cache_gb: float = Field(description="KV-Cache für das gewünschte Kontextfenster in GB")
    benoetigter_speicher_gb: float = Field(description="Arbeits- bzw. Grafikspeicher beim Rechnen in GB")
    bewertung: Literal["optimal", "passt", "knapp", "zu gross"]
    passt_in_speicher: bool = Field(description="Passt das Modell in den nutzbaren Arbeits-/Grafikspeicher?")
    passt_auf_festplatte: bool = Field(description="Reicht der freie Platz auf der Festplatte für anzahl_modelle?")


class Empfehlung(BaseModel):
    """Gesamtantwort des Calculators."""

    speichertyp: Literal["vram", "unified", "ram"] = Field(description="vram = Grafikspeicher, unified/ram = Arbeitsspeicher")
    nutzbarer_speicher_gb: float = Field(description="Für das Modell nutzbarer Arbeits-/Grafikspeicher in GB")
    max_parameter_mrd: float = Field(description="Faustregel: grösstes Modell, dessen Gewichte passen (ohne KV-Cache)")
    optimale_parameter_mrd: float = Field(description="Faustregel: empfohlene Modellgrösse mit Reserve")
    beste_wahl: str | None = Field(description="Name des empfohlenen Modells; null, wenn keines passt")
    passend: list[ModellErgebnis] = Field(description="Modelle, die in den Speicher passen – grösste zuerst")
    zu_gross: list[ModellErgebnis] = Field(description="Modelle, die nicht passen (zur Information)")
    hinweise: list[str]

# ---------------------------------------------------------------------------
# 3) App und Endpunkte
# ---------------------------------------------------------------------------

app = FastAPI(
    title="LLM Requirements Calculator",
    description="Berechnet aus Hardware-Angaben, welche lokalen Sprachmodelle (LLMs) passen. "
                "Selbstständige Arbeit, Modul AI Operations, FHNW HS26.",
    version="1.0.0",
)


@app.get("/health")
def health() -> dict:
    """Lebenszeichen: Läuft der Server? Nützlich für Monitoring und für render.com (Aufgabe 1.2)."""
    return {"status": "ok"}


@app.post("/empfehlung", response_model=Empfehlung)
def empfehlung(anfrage: HardwareAnfrage) -> Empfehlung:
    """
    Hauptendpunkt: Hardware rein (JSON), Modellempfehlungen raus (JSON).
      1. FastAPI prüft den Request-Body gegen HardwareAnfrage (sonst Status 422).
      2. Die Geschäftslogik wird mit den geprüften Werten aufgerufen.
      3. Das Ergebnis wird gegen Empfehlung geprüft und als JSON gesendet.
    """
    ergebnis = berechne_empfehlungen(**anfrage.model_dump())   # Dictionary -> benannte Argumente
    return Empfehlung(**ergebnis)


# ---------------------------------------------------------------------------
# 4) Web-Oberfläche (Schritt 3): statische Dateien ausliefern
# ---------------------------------------------------------------------------

@app.get("/", include_in_schema=False)
def startseite() -> FileResponse:
    """Startseite = Code/static/index.html. include_in_schema=False: erscheint nicht in /docs."""
    return FileResponse(STATIC_DIR / "index.html")


# Alles unter /static (style.css, app.js) wird direkt aus dem Ordner ausgeliefert.
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
