"""
tests/test_api.py – automatische Tests für die API (main.py)
=============================================================
Selbstständige Arbeit, Modul AI Operations (FHNW HSW, HS26) – Jeremy Nathan
Projektaufgabe 1.2 «DevOps Cloud»: Phase Test automatisieren.

Der TestClient von FastAPI spielt den Browser: Er schickt Anfragen direkt an die App,
ohne dass uvicorn laufen muss. Geprüft wird dasselbe wie manuell unter /docs:
Lebenszeichen, gültige Anfrage mit Antwort 200, ungültige Anfrage mit Status 422.

KI-Deklaration (Hilfsmittelverzeichnis, Merkblatt HSW-FHNW)
    Erstellt am 2026-11-04 mit Unterstützung von Claude (Anthropic; Modell Claude Fable 5.1,
    genutzt über die Claude-Desktop-App). Vorgaben, Prüfung und Test: Jeremy Nathan.

Quelle
    [Q9] FastAPI-Dokumentation, Tutorial «Testing» (abgerufen am 2026-11-04):
         https://fastapi.tiangolo.com/tutorial/testing/
"""

from fastapi.testclient import TestClient

from Code.main import app

client = TestClient(app)

BEISPIEL = {"ram_gb": 16, "betriebssystem": "macos", "vram_gb": None, "freier_speicher_gb": 100,
            "anzahl_modelle": 1, "quantisierung": "Q4_K_M", "kontextfenster": 8192}


def test_health():
    """GET /health antwortet 200 mit {"status": "ok"} (Lebenszeichen für Monitoring und render)."""
    antwort = client.get("/health")
    assert antwort.status_code == 200
    assert antwort.json() == {"status": "ok"}


def test_empfehlung_gueltig():
    """POST /empfehlung mit gültigen Werten: 200 und die Empfehlung aus dem Rechenbeispiel."""
    antwort = client.post("/empfehlung", json=BEISPIEL)
    assert antwort.status_code == 200
    daten = antwort.json()
    assert daten["beste_wahl"] == "Qwen3 8B"
    assert daten["nutzbarer_speicher_gb"] == 10.67
    assert daten["passend"][0]["name"] == "Qwen3 8B"


def test_empfehlung_ungueltiger_ram():
    """ram_gb = -5 verletzt gt=0: Status 422, der Fehlertext nennt das Feld ram_gb, es wird nicht gerechnet."""
    antwort = client.post("/empfehlung", json={**BEISPIEL, "ram_gb": -5})
    assert antwort.status_code == 422
    assert antwort.json()["detail"][0]["loc"] == ["body", "ram_gb"]


def test_empfehlung_ungueltiges_betriebssystem():
    """Ein Wert ausserhalb von macos/windows/linux wird mit 422 abgelehnt."""
    antwort = client.post("/empfehlung", json={**BEISPIEL, "betriebssystem": "amiga"})
    assert antwort.status_code == 422


def test_startseite():
    """GET / liefert die Web-Oberfläche (index.html) mit Status 200."""
    antwort = client.get("/")
    assert antwort.status_code == 200
    assert "<html" in antwort.text.lower()

# --- Feature ram-grenze: Arbeitsspeicher bis 4096 GB, darüber 422 ----------------

def test_ram_ueber_1tb_erlaubt():
    """Grosse Workstations und Server: 2048 GB werden angenommen (vorher Grenze 1024 in der Oberfläche)."""
    antwort = client.post("/empfehlung", json={**BEISPIEL, "ram_gb": 2048})
    assert antwort.status_code == 200
    assert antwort.json()["beste_wahl"] == "Llama 3.3 70B"


def test_ram_ueber_obergrenze_abgelehnt():
    """Mehr als 4096 GB ist kein realistischer Wert: 422, Fehlertext nennt ram_gb."""
    antwort = client.post("/empfehlung", json={**BEISPIEL, "ram_gb": 5000})
    assert antwort.status_code == 422
    assert antwort.json()["detail"][0]["loc"] == ["body", "ram_gb"]


def test_vram_ueber_obergrenze_abgelehnt():
    """Grafikspeicher über 512 GB ist kein realistischer Wert für eine Karte: 422."""
    antwort = client.post("/empfehlung", json={**BEISPIEL, "betriebssystem": "linux", "vram_gb": 600})
    assert antwort.status_code == 422
    assert antwort.json()["detail"][0]["loc"] == ["body", "vram_gb"]


def test_vram_grosse_karte_erlaubt():
    """288 GB (grosse Rechenzentrums-Karte) werden angenommen, Speichertyp vram."""
    antwort = client.post("/empfehlung", json={**BEISPIEL, "betriebssystem": "linux", "vram_gb": 288})
    assert antwort.status_code == 200
    assert antwort.json()["speichertyp"] == "vram"