# Hilfsmittelverzeichnis (Anhang 2 des Berichts)

Gemäss «HSW-FHNW Merkblatt Einsatz von KI-Tools». Die Tabelle wird in Anhang 2 des Berichts übernommen
und bei jeder Änderung an beiden Orten nachgeführt.

Stand: 2026-11-04 (Aufgaben 1.1 und 1.2)

---

## 1. Hilfsmittelverzeichnis

| Hilfsmittel | Verwendung | Betroffene Teile der Arbeit |
|---|---|---|
| Claude (Anthropic), Modell Claude Fable 5.1, Claude-Desktop-App | Claude wurde verwendet, um Erklärungen zu den Modulinhalten und zur eingesetzten Technik zu erhalten (API, FastAPI, uvicorn, Git, GitHub, render.com, pytest, GitHub Actions). | Vorbereitung, keine direkten Textstellen |
| Claude (Anthropic) | Claude wurde verwendet, um nach meinen Vorgaben (Thema, Ein- und Ausgaben, Aufbau in Schichten, Sprache, Umfang) den Programmcode, die Web-Oberfläche, die Tests und die Pipeline-Datei zu erstellen. Ich habe den Code geprüft, getestet und Anpassungen zurückgemeldet. | `Code/`, `tests/`, `pytest.ini`, `requirements*.txt`, `.github/workflows/tests.yml`, `CHANGELOG.md`; Kapitel 1 und 2 |
| Claude (Anthropic) | Claude wurde verwendet, um Textentwürfe und Abbildungen für den Bericht und die Projektdokumentation zu erstellen und zu überarbeiten. Die Texte habe ich geprüft und in eigenen Worten angepasst. | Kapitel 1 und 2, Abbildungen, Anhänge, `README.md`, `docs/` |
| FastAPI, Dokumentation unter `/docs` (Swagger UI) | Manuelles Testen der API-Endpunkte, lokal und auf render.com | Screenvideos Kapitel 1 und 2 |
| pytest 9.2.0 mit TestClient von FastAPI (httpx2 2.16.0) | Automatische Tests der Geschäftslogik und der API | `tests/`; Kapitel 2 |
| Git, GitHub (Repository, Pull Request, GitHub Actions) | Versionskontrolle, Branch-Modell, Pipeline | Kapitel 2, Screenvideo Kapitel 2 |
| render.com (Web Service, Free) | Betrieb der API in der Cloud, automatisches Deployment, Health Check, Logs | Kapitel 2, Screenvideo Kapitel 2 |
| Visual Studio Code, Terminal (zsh), Python 3.14, pip, venv | Entwicklungsumgebung, Ausführen und Testen | Gesamte Umsetzung |

## 2. Eigenleistung

Themenwahl und Konzept des Programms (Ein- und Ausgaben, Aufbau in Schichten, Umfang, Begriffe); Einrichten von
Projekt, virtueller Umgebung, Repository, GitHub und render.com; Ausführen aller Git-Befehle (Branches, Commits,
Merges, Tags, Push); Entscheide zu Branch-Modell, Tests, Features, Release, Hotfix und Health Check; Prüfen des Codes
und der Tests, manuelles Testen im Terminal, unter `/docs` (lokal und auf render.com) und in der Oberfläche; Kontrolle der
Pipeline-Läufe und der render-Logs; Überarbeiten aller Texte in eigenen Worten; Screenvideos; Arbeitsjournal.
