"""
cli.py – Ein-/Ausgabe im Terminal (CLI = Command Line Interface)
=================================================================
Selbstständige Arbeit, Modul AI Operations (FHNW HSW, HS26) – Jeremy Nathan

Diese Datei ist die «Benutzerseite» für das Terminal: Sie stellt Fragen (input),
übergibt die Antworten an die Geschäftslogik in rechner.py und gibt das Ergebnis
lesbar aus (print). Sie rechnet selbst nichts – das ist Absicht: Die API in main.py
macht dasselbe über HTTP und nutzt genau dieselbe Logik.

Ausführen (aus dem Projektordner, nicht aus «Code»):
    python -m Code.cli
Enter ohne Eingabe übernimmt den Standardwert in eckigen Klammern.

KI-Deklaration (Hilfsmittelverzeichnis, Merkblatt HSW-FHNW)
    Erstellt am 2026-10-07 mit Unterstützung von Claude (Anthropic; Modell Claude Fable 5.1,
    genutzt über die Claude-Desktop-App). Vorgaben, Entscheidungen (Thema, Struktur,
    Sprache, Umfang), Prüfung und Test: Jeremy Nathan.

Quellen (Nummerierung gilt im ganzen Projekt)
    [Q7] Modul-Slides «Projektaufgabe DevOps – Lokal» (1_1.pdf, Folie 5: Programm mit Eingabe
         und Ausgabe) und Beispielcode des Dozenten (primzahl-info.ipynb mit input()/print()),
         Moodle AI Operations HS26
"""

from Code.katalog import QUANTISIERUNG_BITS
from Code.rechner import berechne_empfehlungen


def frage(text: str, standard: str) -> str:
    """Fragt einen Wert ab; Enter ohne Eingabe übernimmt den Standardwert."""
    antwort = input(f"{text} [{standard}]: ").strip()
    return antwort if antwort else standard


def eingaben_abfragen() -> dict:
    """Stellt alle Fragen und liefert die Antworten als Dictionary mit den Parameternamen der Logik."""
    betriebssystem = frage("Betriebssystem (macos / windows / linux)", "macos").lower()
    ram_gb = float(frage("Arbeitsspeicher (RAM) in GB", "16"))

    if betriebssystem == "macos":
        vram_gb = None   # Apple Silicon: Die GPU nutzt den Arbeitsspeicher, es gibt keine separate Grafikkarte
    else:
        vram = float(frage("Grafikspeicher (VRAM) der separaten Grafikkarte in GB, 0 = keine", "0"))
        vram_gb = vram if vram > 0 else None

    return {
        "ram_gb": ram_gb,
        "betriebssystem": betriebssystem,
        "vram_gb": vram_gb,
        "freier_speicher_gb": float(frage("Freier Platz auf der Festplatte in GB", "100")),
        "anzahl_modelle": int(frage("Anzahl Modelle, die auf der Festplatte liegen sollen", "1")),
        "quantisierung": frage(f"Quantisierung {' / '.join(QUANTISIERUNG_BITS)}", "Q4_K_M").upper(),
        "kontextfenster": int(frage("Kontextfenster in Tokens", "8192")),
    }


def ergebnis_ausgeben(e: dict) -> None:
    """Gibt das Dictionary aus berechne_empfehlungen() als lesbare Tabelle aus."""
    wort = "Grafikspeicher" if e["speichertyp"] == "vram" else "Arbeitsspeicher"
    print(f"\nNutzbarer {wort} für das Modell: {e['nutzbarer_speicher_gb']} GB ({e['speichertyp']})")
    print(f"Faustregel: max. {e['max_parameter_mrd']} Mrd. Parameter, optimal {e['optimale_parameter_mrd']} Mrd.")
    print(f"Beste Wahl: {e['beste_wahl']}\n")

    print(f"{'Bewertung':<10}{'Modell':<16}{'Mrd. Param.':>12}{'braucht':>11}{'Datei':>10}  Festplatte")
    for m in e["passend"] + e["zu_gross"]:
        festplatte = "reicht" if m["passt_auf_festplatte"] else "zu wenig Platz"
        print(f"{m['bewertung']:<10}{m['name']:<16}{m['parameter_mrd']:>12.2f}"
              f"{m['benoetigter_speicher_gb']:>8.1f} GB{m['dateigroesse_gb']:>7.1f} GB  {festplatte}")

    if e["hinweise"]:
        print("\nHinweise:")
        for h in e["hinweise"]:
            print(f"- {h}")


def main() -> None:
    """Ablauf: fragen -> rechnen -> ausgeben."""
    print("LLM Requirements Calculator – welches KI-Modell läuft auf deinem Computer?\n")
    eingaben = eingaben_abfragen()
    ergebnis = berechne_empfehlungen(**eingaben)   # ** entpackt das Dictionary zu benannten Argumenten
    ergebnis_ausgeben(ergebnis)


if __name__ == "__main__":
    main()
