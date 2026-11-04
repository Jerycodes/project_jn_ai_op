"""
tests/test_rechner.py – automatische Tests für die Geschäftslogik (rechner.py)
===============================================================================
Selbstständige Arbeit, Modul AI Operations (FHNW HSW, HS26) – Jeremy Nathan
Projektaufgabe 1.2 «DevOps Cloud»: Phase Test automatisieren (Reflexionsfolie Lektion 4).

Ein Test ist eine Funktion, deren Name mit «test_» beginnt. Sie ruft eine Funktion des
Programms mit bekannten Werten auf und behauptet mit «assert», was herauskommen muss.
Stimmt die Behauptung nicht, meldet pytest den Test als gescheitert.

Die Erwartungswerte sind das Rechenbeispiel aus dem Bericht (Anhang 5): Mac mit 16 GB
Arbeitsspeicher, Quantisierung Q4_K_M, Kontextfenster 8192 Tokens, Modell Qwen3 8B.

Ausführen (aus dem Projektordner, venv aktiviert, Pakete aus requirements-dev.txt):
    pytest

KI-Deklaration (Hilfsmittelverzeichnis, Merkblatt HSW-FHNW)
    Erstellt am 2026-11-04 mit Unterstützung von Claude (Anthropic; Modell Claude Fable 5.1,
    genutzt über die Claude-Desktop-App). Vorgaben, Prüfung und Test: Jeremy Nathan.
"""

from Code.katalog import MODELL_KATALOG
from Code.rechner import (benoetigter_speicher_gb, berechne_empfehlungen, bewerte,
                          gewichte_gb, kv_cache_gb, max_parameter_mrd, nutzbarer_speicher)

QWEN3_8B = next(m for m in MODELL_KATALOG if m.name == "Qwen3 8B")


# --- Schritt 1: nutzbarer Speicher -------------------------------------------------

def test_nutzbarer_speicher_macos_16gb():
    """macOS gibt der GPU 2/3 des Arbeitsspeichers frei: 16 GB -> 10.67 GB, Typ unified."""
    nutzbar, typ = nutzbarer_speicher(16, "macos", None)
    assert round(nutzbar, 2) == 10.67
    assert typ == "unified"


def test_nutzbarer_speicher_grafikkarte():
    """Separate Grafikkarte: Grafikspeicher minus 0.5 GB Reserve, Typ vram."""
    assert nutzbarer_speicher(32, "windows", 12) == (11.5, "vram")


def test_nutzbarer_speicher_cpu():
    """Ohne Grafikkarte unter Windows/Linux: 75 % des Arbeitsspeichers, Typ ram."""
    assert nutzbarer_speicher(16, "linux", None) == (12.0, "ram")


# --- Schritte 2 bis 4: Bedarf, Bewertung, Faustregel ------------------------------

def test_bedarf_qwen3_8b():
    """Gewichte 4.95 GB + KV-Cache 1.125 GB + Overhead 0.75 GB = 6.83 GB (Formeln 3 bis 5)."""
    assert round(gewichte_gb(QWEN3_8B.parameter_mrd, "Q4_K_M"), 2) == 4.95
    assert kv_cache_gb(QWEN3_8B, 8192) == 1.125
    assert round(benoetigter_speicher_gb(QWEN3_8B, "Q4_K_M", 8192), 2) == 6.83


def test_bewertung_schwellen():
    """Anteil am nutzbaren Speicher: bis 70 % optimal, bis 90 % passt, bis 100 % knapp, darüber zu gross."""
    assert bewerte(7.0, 10.0) == "optimal"
    assert bewerte(9.0, 10.0) == "passt"
    assert bewerte(9.5, 10.0) == "knapp"
    assert bewerte(10.1, 10.0) == "zu gross"
    assert bewerte(1.0, 0.0) == "zu gross"   # kein nutzbarer Speicher: keine Division durch null


def test_faustregel_max_parameter():
    """(10.67 GB - 0.75 GB) * 8 / 4.84 = 16.4 Mrd. Parameter (Formel 2)."""
    nutzbar, _ = nutzbarer_speicher(16, "macos", None)
    assert round(max_parameter_mrd(nutzbar, "Q4_K_M"), 1) == 16.4


# --- Hauptfunktion: das Beispiel aus dem Bericht ----------------------------------

def test_berechne_empfehlungen_beispiel_bericht():
    """Mac 16 GB, Q4_K_M, 8192 Tokens: Qwen3 8B ist die beste Wahl, 4 Modelle passen, 4 sind zu gross."""
    e = berechne_empfehlungen(16, "macos", None, 100, 1, "Q4_K_M", 8192)
    assert e["speichertyp"] == "unified"
    assert e["nutzbarer_speicher_gb"] == 10.67
    assert e["max_parameter_mrd"] == 16.4
    assert e["optimale_parameter_mrd"] == 11.5
    assert e["beste_wahl"] == "Qwen3 8B"
    assert len(e["passend"]) == 4
    assert len(e["zu_gross"]) == 4


def test_kein_modell_passt():
    """2 GB Arbeitsspeicher ohne Grafikkarte, F16: nichts passt, beste_wahl ist None, Hinweis vorhanden."""
    e = berechne_empfehlungen(2, "linux", None, 100, 1, "F16", 8192)
    assert e["passend"] == []
    assert e["beste_wahl"] is None
    assert any("Kein Modell" in h for h in e["hinweise"])