"""
rechner.py – Geschäftslogik des LLM Requirements Calculators
=============================================================
Selbstständige Arbeit, Modul AI Operations (FHNW HSW, HS26) – Jeremy Nathan

Hier wird GERECHNET – sonst nichts: keine Daten (siehe katalog.py), keine Ein-/Ausgabe
(siehe cli.py bzw. main.py). Alle Funktionen sind «rein»: gleiche Eingabe -> gleiche
Ausgabe, kein input(), kein print(). Dadurch sind sie einzeln testbar und von Terminal
und API gleich verwendbar.

Was macht das Programm?
    Eingabe:  Hardware eines Computers (Arbeitsspeicher, Betriebssystem, optional
              Grafikspeicher, freier Platz auf der Festplatte, Anzahl Modelle,
              Quantisierung, Kontextfenster)
    Ausgabe:  Welche lokalen Sprachmodelle (LLMs) darauf laufen – mit benötigtem
              Arbeitsspeicher, Dateigrösse, Bewertung, bester Wahl sowie maximaler
              und optimaler Modellgrösse (Faustregel)

Begriffe (konsequent, damit nichts verwechselt wird)
    Arbeitsspeicher (RAM)  = schneller Speicher, in dem das Modell liegt, WÄHREND es rechnet
    Grafikspeicher (VRAM)  = Arbeitsspeicher einer separaten Grafikkarte
    Festplatte             = dauerhafter Speicherplatz für die Modelldatei

Rechenweg in vier Schritten
    1. Nutzbarer Speicher:  Grafikspeicher, Unified Memory (macOS) oder Arbeitsspeicher (CPU)
    2. Bedarf pro Modell:   Gewichte + KV-Cache + Overhead
    3. Bewertung:           Anteil am nutzbaren Speicher -> optimal / passt / knapp / zu gross
    4. Faustregel:          grösstes bzw. optimales Modell in Mrd. Parametern

KI-Deklaration (Hilfsmittelverzeichnis, Merkblatt HSW-FHNW)
    Erstellt am 2026-10-07 mit Unterstützung von Claude (Anthropic; Modell Claude Fable 5.1,
    genutzt über die Claude-Desktop-App). Vorgaben, Entscheidungen (Thema, Struktur,
    Sprache, Umfang), Prüfung und Test: Jeremy Nathan. Externe Zahlen sind mit Quelle
    belegt; Werte ohne Quelle sind eigene, gekennzeichnete Annahmen.

Quellen (abgerufen am 2026-10-07; Nummerierung gilt im ganzen Projekt)
    [Q4] llama.cpp, Discussion #2182 (Anteil des Unified Memory, den macOS der GPU auf
         Apple Silicon standardmässig freigibt: 2/3, ab >32 GB 3/4; sysctl iogpu.wired_limit_mb):
         https://github.com/ggml-org/llama.cpp/discussions/2182
    Weitere Quellen (Q1–Q3, Q5, Q6) siehe katalog.py, Q7 siehe cli.py.
"""

from Code.katalog import MODELL_KATALOG, QUANTISIERUNG_BITS, Modell

# ---------------------------------------------------------------------------
# 1) Parameter der Berechnung – jede Zahl hat eine Quelle oder ist als Annahme markiert
# ---------------------------------------------------------------------------

# Anteil des Arbeitsspeichers (Unified Memory), den macOS der GPU auf Apple Silicon
# standardmässig freigibt: 2/3; bei mehr als 32 GB Arbeitsspeicher 3/4 [Q4].
UNIFIED_ANTEIL_KLEIN = 2 / 3
UNIFIED_ANTEIL_GROSS = 3 / 4
UNIFIED_GRENZE_GB = 32

# Eigene Annahmen (keine Quelle; bewusst einfach gehalten und leicht anpassbar):
VRAM_RESERVE_GB = 0.5      # Grafiktreiber/Bildschirm belegen etwas Grafikspeicher
RAM_ANTEIL_CPU = 0.75      # CPU-Inferenz: 75 % des Arbeitsspeichers fürs Modell, Rest fürs System
OVERHEAD_GB = 0.75         # Rechenpuffer der Inferenz-Software (llama.cpp, Ollama, LM Studio)
SCHWELLE_OPTIMAL = 0.70    # <= 70 % des nutzbaren Speichers belegt -> «optimal»
SCHWELLE_PASST = 0.90      # <= 90 % -> «passt»; <= 100 % -> «knapp»; darüber «zu gross»
OPTIMAL_FAKTOR = 0.70      # «optimale» Modellgrösse = 70 % der theoretisch maximalen

# ---------------------------------------------------------------------------
# 2) Rechenschritte – kleine Funktionen, jede macht genau eine Sache
# ---------------------------------------------------------------------------

def nutzbarer_speicher(ram_gb: float, betriebssystem: str, vram_gb: float | None) -> tuple[float, str]:
    """
    Wie viel Speicher steht dem Modell beim Rechnen zur Verfügung – und welcher?
      1. Separate Grafikkarte angegeben -> Grafikspeicher minus Treiber-Reserve, Typ «vram»
      2. macOS (Apple Silicon)          -> Anteil des Arbeitsspeichers [Q4],        Typ «unified»
      3. Sonst (CPU rechnet)            -> Anteil des Arbeitsspeichers (Annahme),  Typ «ram»
    Rückgabe: (nutzbare_gb, speichertyp)
    """
    if vram_gb is not None and vram_gb > 0:
        return max(vram_gb - VRAM_RESERVE_GB, 0.0), "vram"
    if betriebssystem == "macos":
        anteil = UNIFIED_ANTEIL_KLEIN if ram_gb <= UNIFIED_GRENZE_GB else UNIFIED_ANTEIL_GROSS
        return ram_gb * anteil, "unified"
    return ram_gb * RAM_ANTEIL_CPU, "ram"


def gewichte_gb(parameter_mrd: float, quantisierung: str) -> float:
    """
    Speicherbedarf der Modellgewichte in GB – entspricht ungefähr der Dateigrösse auf der Festplatte.
    Formel: Parameter (Mrd.) * Bits pro Gewicht / 8.   Beispiel: 8.03 * 4.84 / 8 = 4.86 GB
    """
    return parameter_mrd * QUANTISIERUNG_BITS[quantisierung] / 8


def kv_cache_gb(modell: Modell, kontextfenster: int) -> float:
    """
    Speicherbedarf des KV-Caches in GB für das gewünschte Kontextfenster.
    Formel: Tokens * KB pro Token / 1024 / 1024.   Beispiel: 8192 * 128 KB = 1.0 GB
    """
    return kontextfenster * modell.kv_kb_pro_token() / 1024 / 1024


def benoetigter_speicher_gb(modell: Modell, quantisierung: str, kontextfenster: int) -> float:
    """Gesamtbedarf im Arbeits- bzw. Grafikspeicher = Gewichte + KV-Cache + Overhead."""
    return gewichte_gb(modell.parameter_mrd, quantisierung) + kv_cache_gb(modell, kontextfenster) + OVERHEAD_GB


def bewerte(benoetigt_gb: float, nutzbar_gb: float) -> str:
    """Anteil am nutzbaren Speicher -> «optimal», «passt», «knapp» oder «zu gross»."""
    if nutzbar_gb <= 0:
        return "zu gross"
    anteil = benoetigt_gb / nutzbar_gb
    if anteil <= SCHWELLE_OPTIMAL:
        return "optimal"
    if anteil <= SCHWELLE_PASST:
        return "passt"
    if anteil <= 1.0:
        return "knapp"
    return "zu gross"


def max_parameter_mrd(nutzbar_gb: float, quantisierung: str) -> float:
    """
    Faustregel: grösstes Modell (Mrd. Parameter), dessen Gewichte in den nutzbaren Speicher
    passen – ohne KV-Cache. Umkehrung von gewichte_gb():  (nutzbar - Overhead) * 8 / bpw
    """
    frei = max(nutzbar_gb - OVERHEAD_GB, 0.0)
    return frei * 8 / QUANTISIERUNG_BITS[quantisierung]

# ---------------------------------------------------------------------------
# 3) Hauptfunktion – fasst alles zusammen; wird von cli.py und main.py aufgerufen
# ---------------------------------------------------------------------------

def berechne_empfehlungen(ram_gb: float, betriebssystem: str, vram_gb: float | None,
                          freier_speicher_gb: float, anzahl_modelle: int,
                          quantisierung: str, kontextfenster: int) -> dict:
    """
    Rechnet jedes Modell im Katalog durch und liefert ein Dictionary, das sich 1:1 als
    JSON ausgeben lässt (darum ideal für die API).

    Rückgabe-Felder:
        speichertyp, nutzbarer_speicher_gb, max_parameter_mrd, optimale_parameter_mrd,
        beste_wahl, passend (Liste), zu_gross (Liste), hinweise (Liste von Texten)
    """
    nutzbar_gb, speichertyp = nutzbarer_speicher(ram_gb, betriebssystem, vram_gb)
    max_mrd = max_parameter_mrd(nutzbar_gb, quantisierung)

    modelle = []
    for m in MODELL_KATALOG:
        gewichte = gewichte_gb(m.parameter_mrd, quantisierung)
        benoetigt = benoetigter_speicher_gb(m, quantisierung, kontextfenster)
        bewertung = bewerte(benoetigt, nutzbar_gb)
        modelle.append({
            "name": m.name,
            "parameter_mrd": m.parameter_mrd,
            "dateigroesse_gb": round(gewichte, 2),                  # Platz auf der Festplatte pro Modell
            "kv_cache_gb": round(kv_cache_gb(m, kontextfenster), 2),
            "benoetigter_speicher_gb": round(benoetigt, 2),         # Arbeits-/Grafikspeicher beim Rechnen
            "bewertung": bewertung,
            "passt_in_speicher": bewertung != "zu gross",
            "passt_auf_festplatte": gewichte * anzahl_modelle <= freier_speicher_gb,
        })

    modelle.sort(key=lambda e: e["parameter_mrd"], reverse=True)    # grösste zuerst
    passend = [e for e in modelle if e["passt_in_speicher"]]
    zu_gross = [e for e in modelle if not e["passt_in_speicher"]]

    # Beste Wahl: grösstes Modell, das «optimal» oder «passt» ist UND auf die Festplatte passt;
    # sonst das grösste Modell, das überhaupt in den Speicher passt.
    beste_wahl = next((e["name"] for e in passend
                       if e["bewertung"] in ("optimal", "passt") and e["passt_auf_festplatte"]), None)
    if beste_wahl is None and passend:
        beste_wahl = passend[0]["name"]

    hinweise = []
    if speichertyp == "ram":
        hinweise.append("Ohne separate Grafikkarte rechnet der Prozessor – das funktioniert, ist aber deutlich langsamer.")
    if speichertyp == "unified":
        hinweise.append("Apple Silicon: CPU und GPU teilen sich den Arbeitsspeicher; macOS gibt der GPU nur einen Teil davon frei.")
    if kontextfenster >= 32768:
        hinweise.append("Grosses Kontextfenster: Der KV-Cache belegt viel Arbeitsspeicher – ein kleineres Kontextfenster erlaubt grössere Modelle.")
    if not passend:
        hinweise.append("Kein Modell aus dem Katalog passt in den nutzbaren Speicher.")

    return {
        "speichertyp": speichertyp,
        "nutzbarer_speicher_gb": round(nutzbar_gb, 2),
        "max_parameter_mrd": round(max_mrd, 1),
        "optimale_parameter_mrd": round(max_mrd * OPTIMAL_FAKTOR, 1),
        "beste_wahl": beste_wahl,
        "passend": passend,
        "zu_gross": zu_gross,
        "hinweise": hinweise,
    }
