# Änderungen (Changelog)

Versionsnummern nach dem Muster Hauptversion.Nebenversion.Korrektur (Semantic Versioning).

## 1.1.0 – 2026-11-04
- Arbeitsspeicher bis 4096 GB und Grafikspeicher bis 512 GB in Oberfläche und API (vorher 1024 bzw. 256 GB nur in der Oberfläche, API ohne Obergrenze)
- 17 automatische Tests mit pytest (Geschäftslogik und API), Ordner tests/
- GitHub Actions führt die Tests bei jedem Push und Pull Request aus (.github/workflows/tests.yml)
- requirements-dev.txt für Entwicklung und Tests; Produktion bleibt bei requirements.txt
- Branch-Modell nach Gitflow: main (Produktion auf render.com), develop, feature/*, release/*

## 1.0.0 – 2026-10-08
- Erste Version: Rechner (katalog.py, rechner.py), Terminal (cli.py), API mit FastAPI (main.py), Web-Oberfläche (static/)
- Deployment auf render.com aus dem Zweig main