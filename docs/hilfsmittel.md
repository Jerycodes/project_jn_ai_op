# Hilfsmittelverzeichnis (Anhang 2 des Berichts)

Gemäss «HSW-FHNW Merkblatt Einsatz von KI-Tools»: Jedes Hilfsmittel wird mit Verwendung und betroffenen
Stellen deklariert; die eigene intellektuelle Leistung muss erkennbar bleiben. Diese Datei ist die
laufende Fassung – die Tabelle in Abschnitt 1 wird 1:1 in Anhang 2 des Berichts übernommen und bei
jeder Änderung an beiden Orten nachgeführt.

Stand: 2026-10-08 (identisch mit Anhang 2 in `Bericht_AI_Operations_Jeremy_Nathan.docx`)

---

## 1. Hilfsmittelverzeichnis (Format des Merkblatts)

| Hilfsmittel | Verwendung | Betroffene Stellen |
|---|---|---|
| Claude (Anthropic), Modell Claude Fable 5.1, genutzt über die Claude-Desktop-App mit Zugriff auf den Projektordner | Brainstorming und Bewertung von Themenideen; der Entscheid für den LLM Requirements Calculator wurde von mir getroffen | Themenwahl; Kapitel 1 |
| Claude (Anthropic) | Zusammenfassen und Erklären der Modul-Slides, des Beispielcodes und des Merkblatts als Lernunterstützung; Erklärungsdokument zur verwendeten Technik | Keine direkten Textstellen; Vorbereitung |
| Claude (Anthropic) | Erstellung des Programmcodes nach meinen Vorgaben (Thema, Ein- und Ausgaben, Schichten Daten/Logik/Ein-Ausgabe, Sprache, Umfang): `Code/katalog.py`, `rechner.py`, `cli.py`; Recherche und Belegung der Zahlen mit Quellen | Gesamter Programmcode (Stand 07.10.2026); Kapitel 1 |
| Claude (Anthropic) | Erstellung der API (`Code/main.py`) und der `requirements.txt` nach dem Muster des Dozentenbeispiels; Abklärung der Paketversionen für Python 3.14 | `Code/main.py`, `requirements.txt`; Kapitel 1 |
| Claude (Anthropic) | Erstellung der Web-Oberfläche (`Code/static/`) nach meinen Vorgaben zu Aufbau, Begriffen und Gestaltung; Anpassungen nach meinen Rückmeldungen (z. B. Grafikkarten-Schalter bei macOS gesperrt) | `Code/static/index.html`, `style.css`, `app.js`; Screenvideo Kapitel 1 |
| Claude (Anthropic) | Textentwurf für README, Quellenverzeichnis (APA 7), Hilfsmittelverzeichnis, Arbeitsjournal und Kapitel 1 sowie Erstellung von Abbildung 1; von mir geprüft und überarbeitet | `README.md`, `docs/`, Kapitel 1, Abbildung 1, Anhang 2, Literaturverzeichnis |
| FastAPI, automatische Dokumentation unter `/docs` (Swagger UI) | Testen der API-Endpunkte ohne eigenes Testprogramm | Screenvideo Kapitel 1 |
| Visual Studio Code, Terminal (zsh), Python 3.14, pip, venv | Entwicklungsumgebung, Ausführen und Testen | Gesamte Umsetzung |

## 2. Eigenleistung (was ich selbst gemacht und entschieden habe)

- Themenwahl: Idee und Entscheid für den LLM Requirements Calculator, roter Faden für die weiteren Aufgaben (AzureML, SecurityOps, Supply Chain)
- Projekt aufgesetzt: Ordner, virtuelle Umgebung (Python 3.14), Ordner `Code`, Pakete installiert
- Entscheide: Neuaufbau von Grund auf; Begriffe (Arbeitsspeicher / Grafikspeicher / Festplatte); Schichtenaufteilung in vier Dateien; Umfang (8 Modelle, zwei Endpunkte); Sprache Deutsch; Slides als primäre Quelle, wenige externe Quellen
- Prüfung: Code Schritt für Schritt nachvollzogen, Programm im Terminal, API unter `/docs` und Oberfläche im Browser getestet; Fehler und Verbesserungen zurückgemeldet (Grafikkarten-Frage bei macOS, Darstellung der Oberfläche)
- Bericht: Text in eigenen Worten überarbeitet, Screenvideo erstellt, Quellen geprüft

## 3. So wird die KI-Nutzung im Bericht angegeben

- **Anhang 2:** Tabelle aus Abschnitt 1 übernehmen (gleiche Spalten wie im Merkblatt)
- **Literaturverzeichnis (APA 7):** Anthropic. (2026). *Claude Fable 5.1* [Grosses Sprachmodell]. https://claude.ai
- **Kurzbeleg im Text:** (Anthropic, 2026) an den Stellen, die mit KI erstellt oder überarbeitet wurden, z. B.: «Der Programmcode wurde mit Unterstützung von Claude erstellt (Anthropic, 2026) und von mir geprüft und angepasst; die Verwendung ist in Anhang 2 deklariert.»
- **Grafiken:** «Abbildung 1: Aufbau des Programms in drei Schichten und Richtung der Abhängigkeiten (eigene Darstellung, erstellt mit Unterstützung von Claude; Anthropic, 2026)» – so steht es im Bericht
- **Code-Dateien:** Jede Datei trägt im Kopfkommentar die KI-Deklaration
- **Eigenständigkeitserklärung (Anhang 1):** unterschreiben; sie bestätigt genau die Punkte oben
- Falls die HSW einen eigenen Zitierleitfaden mit KI-Beispiel hat, geht dieser vor
