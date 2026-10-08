# Arbeitsjournal – Selbstständige Arbeit AI Operations (HS26)

Zweck: Den Arbeitsprozess nachvollziehbar machen (das Merkblatt sieht vor, dass der Arbeitsprozess auf
Verlangen aufgezeigt wird) und die Bausteine für den Bericht sammeln. Nach jeder Arbeitssitzung ein Eintrag;
was ich selbst gemacht oder entschieden habe steht unter «Eigenleistung», KI-Beiträge unter «KI-Beitrag»
und zusätzlich in `docs/hilfsmittel.md`.

## Screenvideos (separate Dateien, im Bericht mit Dateiname referenziert)

| Kapitel | Inhalt laut Vorlage | Dateiname | Status |
|---|---|---|---|
| 1 DevOps lokal | Aufruf der API und Antwort (relevante Stellen mit Mauszeiger zeigen) | `01_devops_lokal.mp4` | offen |
| 2 DevOps Cloud | GitHub-Repository, Aufruf der API auf render.com und Antwort | `02_devops_cloud.mp4` | offen |
| 3 AzureML | deploytes Modell (Endpoint), Beispielaufruf mit Ergebnissen im Notebook | `03_azureml.mp4` | offen |
| 4 Guardrail | Prompt in Jan.AI, Reaktion der Guardrail, Antwort, Usage/Kosten in LiteLLM | `04_guardrail.mp4` | offen |
| 5 Supply Chain | zu prüfende Files/Codezeilen, Durchführung der Prüfung | `05_supply_chain.mp4` | offen |

---

## Einträge

### 2026-09-15 bis 2026-09-22 – Lektionen 1–2, Themenwahl
- **Eigenleistung:** Modulmaterial gesichtet; Themenkandidaten abgewogen; Entscheid «LLM Requirements Calculator» mit rotem Faden für AzureML (Vorhersage Tokens/s), SecurityOps (Anonymisierung von Geräte-Identifikatoren) und Supply Chain (Prüfung des eigenen Repos).
- **KI-Beitrag:** Brainstorming und Bewertung der Ideen mit Claude.

### 2026-09-26 – Erste Version (Ordner `ai_op_project`, heute Referenz)
- **Eigenleistung:** venv erstellt, Anforderungen formuliert (Code verstehen, alles dokumentieren, Bericht vorbereiten; später: professionelle Oberfläche, klare Begriffe).
- **KI-Beitrag:** Erste Umsetzung mit Logik, API und Web-Oberfläche, README und Doku-Dateien.
- **Entscheid danach:** Neuaufbau von Grund auf, um jeden Teil zu verstehen und sauber zu dokumentieren.

### 2026-10-07 – Neuaufbau Aufgabe 1.1 in `project_jn_ai_op`
- **Eigenleistung:**
  - Neuer Ordner, venv Python 3.14, Ordner `Code` (von `code` umbenannt: Dozentenkonvention `uvicorn Code.main:app`, Gross-/Kleinschreibung auf Linux, `code` ist ein Python-Standardmodul).
  - Vorgaben: Slides als primäre Quelle, wenige ergiebige externe Quellen, KI-Deklaration in jeder Datei, Code nur nach Freigabe, Schritt für Schritt.
  - Entscheide: Thema bestätigt; Deutsch; 8 Modelle; Split in Daten/Logik/Ein-/Ausgabe (vier Dateien); nur `/empfehlung` und `/health`; Oberfläche wie Version 2; Grafikkarten-Schalter bei macOS gesperrt mit Hinweis statt ausgeblendet; Artificial Analysis vorerst nicht verwendet; `.gitignore` und Git erst in Aufgabe 1.2.
  - Tests auf dem eigenen Mac: Terminal (`python -m Code.cli`, u. a. 256 GB / F16 und Q8_0), `pip install`, API unter `/docs` (`/health`, `/empfehlung`), Oberfläche im Browser; Rückmeldung zur Grafikkarten-Frage bei macOS.
- **KI-Beitrag (Claude):**
  - Schritt 1: `Code/rechner.py` (Programm mit Eingabe/Ausgabe, Quellen Q1–Q7, geprüfte Links); Korrektur macOS-Grenze auf 32 GB gemäss Quelle.
  - Split: `katalog.py`, `rechner.py`, `cli.py`, `__init__.py`; Ergebnisse gegen die Einzeldatei-Version verglichen (identisch).
  - Schritt 2: `requirements.txt`, `Code/main.py` (FastAPI, zwei Endpunkte); Test mit gültigen und ungültigen Eingaben (422).
  - Schritt 3: `Code/static/` aus Version 2 übernommen und angepasst; `main.py` liefert `/` aus; Prüfung in Hell-/Dunkelmodus und Handy-Breite.
  - Schritt 4a: README, `docs/quellen.md` (APA 7), `docs/hilfsmittel.md`, dieses Journal.

### 2026-10-08 – Dokumentation abgeschlossen (Schritt 4b/4c)
- **KI-Beitrag (Claude):**
  - 4b: Erklärungsdokument `24_ai_operation/Erklaerung_Projekt_und_Technik.docx` + `.pdf` (18 Seiten: Schichten, Weg einer Anfrage, API/HTTP/REST, GET/POST, JSON, FastAPI-Code Schritt für Schritt, Dekorator `@`, Pydantic, uvicorn/ASGI, `/docs`, Oberfläche, venv, DevOps-Bezug, Ausblick 1.2, Glossar, Quellen APA 7); zwei Abbildungen.
  - 4c: Bericht `24_ai_operation/Bericht_AI_Operations_Jeremy_Nathan.docx` aus der Dozenten-Vorlage: Titelblatt, Kapitel 1 (1 Seite, Abbildung 1 mit Beschriftung), Literaturverzeichnis (APA 7) vor Anhang 1, Anhang 1 ohne «Muster», Anhang 2 = Hilfsmittelverzeichnis, Anhang 3/4 als Verzeichnis-Felder, Fusszeile; `_Vorschau.pdf` daneben.
  - `docs/quellen.md`: Slides «Projektaufgabe DevOps – Cloud» ergänzt; Brun-Einträge neu a–e gemäss APA (Titel alphabetisch).
- **Eigenleistung:** Vorgaben für Zielgruppe und Aufbau des Erklärungsdokuments (Zugriff von Handy/iPad), Entscheid Bericht nach Vorlage mit APA 7, Hilfsmittel in Word integriert.
- **Offen:**
  - [ ] Word öffnen → Felder aktualisieren (Inhaltsverzeichnis, Abbildungsverzeichnis; Frage beim Öffnen mit «Ja» beantworten oder Strg/Cmd+A, F9)
  - [ ] Titelblatt: Ort und Datum prüfen (Platzhalter «Olten, 07.10.2026»)
  - [ ] Kapitel 1 in eigenen Worten überarbeiten, Quellen stichprobenartig prüfen (Links in `docs/quellen.md`)
  - [ ] Screenvideo `01_devops_lokal.mp4` aufnehmen (Terminal-Start, `/docs` POST /empfehlung, Antwort, Oberfläche)
  - [ ] Anhang 1 ausdrucken/unterschreiben (Ort, Datum, Unterschrift)
  - [ ] Reflexionsfolien bis 13.10. (MLOps-Prinzipien in den DevOps-Aufgaben; Technical Debt)
  - [ ] Aufgabe 1.2: Git, `.gitignore`, GitHub, render.com

---

## Vorlage für neue Einträge

```
### JJJJ-MM-TT – Kurztitel
- **Eigenleistung:** …
- **KI-Beitrag (Tool):** … (+ Eintrag in hilfsmittel.md)
- **Entscheide:** …
- **Offen:** …
```
