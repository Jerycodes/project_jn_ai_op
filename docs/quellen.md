# Quellenverzeichnis – LLM Requirements Calculator

Alle externen Quellen des Projekts, gebündelt nach Herkunft, mit Link, Abrufdatum und der Stelle,
an der sie verwendet werden. Die Nummern Q1–Q8 stehen so auch in den Kopfkommentaren der Code-Dateien.
Abschnitt 4 enthält die fertigen Einträge im APA-7-Format für das Literaturverzeichnis des Berichts.

Stand: 2026-10-07 · alle Links an diesem Tag geprüft.

---

## 1. Modulmaterial (primäre Quelle)

| Nr. | Quelle | Verwendet für | Wo im Projekt |
|---|---|---|---|
| Q7 | Slides «Projektaufgabe DevOps – Lokal» (1_1.pdf), Folien 3–9 | Aufbau der Aufgabe: Programm mit Eingabe/Ausgabe, venv, Ordner `Code`, FastAPI-Endpunkt, uvicorn, Test unter `/docs` | `cli.py`, `main.py`, README |
| Q7 | Beispielcode des Dozenten (3_1 DevOps – Umsetzung – Beispiel: `Code/main.py`, `primzahl-info.ipynb`, `test_API.ipynb`, `requirements.txt`) | Vorlage für Struktur und Stil: Pydantic-Schemas, `@app.post`, `response_model`, Programm mit `input()`/`print()` | `main.py`, `cli.py` |
| Q7 | Slides «1.2 DevOps» (2_01.pdf), Folien 6–9 | DevOps-Phasen Plan bis Monitor – Einordnung der Umsetzung im Bericht | Bericht Kapitel 1 |
| Q7 | Slides «1.1 Software-Entwicklungsprozess» (1_01.pdf), Folie 14 | Ziel der Arbeit (Programm mit Input/Output, «nach aussen» über API); Beispiele aus dem Vorsemester als Vorbild für die Web-Oberfläche | `static/`, Erklärungsdokument, Bericht Kapitel 1 |
| Q7 | Slides «Projektaufgabe DevOps – Cloud» (2_1.pdf), Folien 3–9 | Ausblick Aufgabe 1.2: Git, `.gitignore`, GitHub, render.com, Startbefehl mit `--host 0.0.0.0 --port $PORT` | Erklärungsdokument; später Bericht Kapitel 2 |
| – | Merkblatt HSW-FHNW «Einsatz von KI-Tools» | Regeln für KI-Einsatz, Hilfsmittelverzeichnis (Anhang 2), Eigenständigkeitserklärung | `docs/hilfsmittel.md`, Bericht |
| – | Vorlage für die Projektarbeit (5_Vorlage für die Projektarbeit.docx) | Struktur und Seitenlimits des Berichts | Bericht |

Alle im Moodle-Kurs «AI Operations HS26 | FHNW» (Dozent Roman Brun).

## 2. llama.cpp (GitHub, ggml-org)

| Nr. | Quelle | Link | Verwendet für | Wo |
|---|---|---|---|---|
| Q1 | Pull Request #1684 «k-quants» (ikawrakow, 3. Juni 2023) | https://github.com/ggml-org/llama.cpp/pull/1684 | Bits pro Gewicht der Quantisierungstypen, 7B-Dateigrössen (Herleitung Q4_K_M 4.84, Q5_K_M 5.67, Q6_K 6.57), Zusammensetzung der _M-Varianten | `katalog.py`, QUANTISIERUNG_BITS |
| Q2 | Datei `ggml/src/ggml-common.h` (Block-Layouts) | https://github.com/ggml-org/llama.cpp/blob/master/ggml/src/ggml-common.h | Exakte Bits pro Gewicht: Q8_0 = 34 Bytes / 32 Gewichte = 8.5; Q4_K 4.5, Q5_K 5.5, Q6_K 6.5625 (Kontrolle) | `katalog.py` |
| Q4 | Discussion #2182 «Adjust VRAM/RAM split on Apple Silicon» (dr3murr, 11. Juli 2023) | https://github.com/ggml-org/llama.cpp/discussions/2182 | Anteil des Unified Memory, den macOS der GPU freigibt: 2/3, ab mehr als 32 GB 3/4; `sysctl iogpu.wired_limit_mb` | `rechner.py`, UNIFIED_* |

## 3. Hugging Face

| Nr. | Quelle | Link | Verwendet für | Wo |
|---|---|---|---|---|
| Q3 | Blog «Llama 3.1 – 405B, 70B & 8B with multilinguality and long context» (Schmid et al., 23. Juli 2024), Abschnitt «Inference Memory Requirements» | https://huggingface.co/blog/llama31 | Kontrollrechnung der KV-Cache-Formel: 8B → 0.125 GB pro 1k Tokens = 128 KB/Token; 70B → 0.313 GB | `katalog.py`, `Modell.kv_kb_pro_token()` |
| Q5 | config.json der Modelle (Felder `num_hidden_layers`, `num_key_value_heads`, `head_dim`) | siehe Tabelle unten | Architekturwerte für den KV-Cache | `katalog.py`, MODELL_KATALOG |
| Q6 | Modellseiten, Angabe «safetensors.total» (API `https://huggingface.co/api/models/<Repo>`) | siehe Tabelle unten | Parameterzahlen in Milliarden | `katalog.py`, MODELL_KATALOG |
| Q6 | Modellseite `huggyllama/llama-7b` | https://huggingface.co/huggyllama/llama-7b | 6.738 Mrd. Parameter des 7B-Modells für die Herleitung der Bits pro Gewicht (Q1) | `katalog.py` |

Modelle im Katalog (Werte am 2026-10-07 abgerufen; die Llama-Seiten verlangen ein Hugging-Face-Konto mit Freigabe):

| Modell | Repo (config.json + Parameterzahl) | Layer | KV-Heads | Head-Dim | Parameter |
|---|---|---|---|---|---|
| Llama 3.2 1B | https://huggingface.co/meta-llama/Llama-3.2-1B | 16 | 8 | 64 | 1'235'814'400 |
| Llama 3.2 3B | https://huggingface.co/meta-llama/Llama-3.2-3B | 28 | 8 | 128 | 3'212'749'824 |
| Llama 3.1 8B | https://huggingface.co/meta-llama/Llama-3.1-8B | 32 | 8 | 128 | 8'030'261'248 |
| Qwen3 8B | https://huggingface.co/Qwen/Qwen3-8B | 36 | 8 | 128 | 8'190'735'360 |
| Phi-4 14B | https://huggingface.co/microsoft/phi-4 | 40 | 10 | 128 (= 5120 / 40) | 14'659'507'200 |
| Qwen3 14B | https://huggingface.co/Qwen/Qwen3-14B | 40 | 8 | 128 | 14'768'307'200 |
| Qwen3 32B | https://huggingface.co/Qwen/Qwen3-32B | 64 | 8 | 128 | 32'762'123'264 |
| Llama 3.3 70B | https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct | 80 | 8 | 128 | 70'553'706'496 |

## 4. FastAPI

| Nr. | Quelle | Link | Verwendet für | Wo |
|---|---|---|---|---|
| Q8 | FastAPI-Dokumentation, Tutorial: «First Steps», «Request Body», «Static Files» (Sebastián Ramírez) | https://fastapi.tiangolo.com/tutorial/ | App-Objekt, Doku unter `/docs`, Request-Body als Pydantic-Klasse, Ausliefern der Oberfläche | `main.py` |

Pydantic und uvicorn werden in diesem Tutorial mitbehandelt und darum nicht separat zitiert.

## 5. Eigene Annahmen (keine Quelle, im Code als solche markiert)

| Wert | Bedeutung | Wo |
|---|---|---|
| 0.5 GB | Reserve des Grafiktreibers im Grafikspeicher | `rechner.py`, VRAM_RESERVE_GB |
| 75 % | Anteil des Arbeitsspeichers bei CPU-Inferenz | `rechner.py`, RAM_ANTEIL_CPU |
| 0.75 GB | Overhead der Inferenz-Software (Rechenpuffer) | `rechner.py`, OVERHEAD_GB |
| 70 % / 90 % | Schwellen für «optimal» und «passt» | `rechner.py`, SCHWELLE_* |
| 70 % | optimale Modellgrösse als Anteil der maximalen | `rechner.py`, OPTIMAL_FAKTOR |

---

## 6. Literaturverzeichnis nach APA 7 (zum Übernehmen in den Bericht)

Kurzbelege im Text: (Brun, 2026e, Folie 6) · (Kawrakow, 2023) · (ggml-org, 2026) · (dr3murr, 2023) · (Schmid et al., 2024) · (Meta, 2024a) · (Qwen Team, 2025c) · (Microsoft, 2024) · (huggyllama, 2023) · (Ramírez, o. D.) · (Anthropic, 2026)

Anthropic. (2026). *Claude Fable 5.1* [Grosses Sprachmodell]. https://claude.ai

Brun, R. (2026a). *DevOps – Umsetzung – Beispiel* [Beispielcode]. Modul AI Operations HS26, FHNW Hochschule für Wirtschaft. Moodle.

Brun, R. (2026b). *1.1 Software-Entwicklungsprozess* [Vorlesungsfolien]. Modul AI Operations HS26, FHNW Hochschule für Wirtschaft. Moodle.

Brun, R. (2026c). *1.2 DevOps* [Vorlesungsfolien]. Modul AI Operations HS26, FHNW Hochschule für Wirtschaft. Moodle.

Brun, R. (2026d). *Projektaufgabe DevOps – Cloud* [Vorlesungsfolien]. Modul AI Operations HS26, FHNW Hochschule für Wirtschaft. Moodle.

Brun, R. (2026e). *Projektaufgabe DevOps – Lokal* [Vorlesungsfolien]. Modul AI Operations HS26, FHNW Hochschule für Wirtschaft. Moodle.

dr3murr. (2023, 11. Juli). *Adjust VRAM/RAM split on Apple Silicon* [Diskussion #2182, ggml-org/llama.cpp]. GitHub. https://github.com/ggml-org/llama.cpp/discussions/2182

ggml-org. (2026). *ggml-common.h* [Quellcode, ggml-org/llama.cpp]. GitHub. Abgerufen am 7. Oktober 2026, von https://github.com/ggml-org/llama.cpp/blob/master/ggml/src/ggml-common.h

huggyllama. (2023). *llama-7b* [Modellseite]. Hugging Face. Abgerufen am 7. Oktober 2026, von https://huggingface.co/huggyllama/llama-7b

Kawrakow, I. [ikawrakow]. (2023, 3. Juni). *k-quants* [Pull Request #1684, ggml-org/llama.cpp]. GitHub. https://github.com/ggml-org/llama.cpp/pull/1684

Meta. (2024a). *Llama-3.1-8B* [Modellseite und config.json]. Hugging Face. Abgerufen am 7. Oktober 2026, von https://huggingface.co/meta-llama/Llama-3.1-8B

Meta. (2024b). *Llama-3.2-1B* [Modellseite und config.json]. Hugging Face. Abgerufen am 7. Oktober 2026, von https://huggingface.co/meta-llama/Llama-3.2-1B

Meta. (2024c). *Llama-3.2-3B* [Modellseite und config.json]. Hugging Face. Abgerufen am 7. Oktober 2026, von https://huggingface.co/meta-llama/Llama-3.2-3B

Meta. (2024d). *Llama-3.3-70B-Instruct* [Modellseite und config.json]. Hugging Face. Abgerufen am 7. Oktober 2026, von https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct

Microsoft. (2024). *phi-4* [Modellseite und config.json]. Hugging Face. Abgerufen am 7. Oktober 2026, von https://huggingface.co/microsoft/phi-4

Qwen Team. (2025a). *Qwen3-14B* [Modellseite und config.json]. Hugging Face. Abgerufen am 7. Oktober 2026, von https://huggingface.co/Qwen/Qwen3-14B

Qwen Team. (2025b). *Qwen3-32B* [Modellseite und config.json]. Hugging Face. Abgerufen am 7. Oktober 2026, von https://huggingface.co/Qwen/Qwen3-32B

Qwen Team. (2025c). *Qwen3-8B* [Modellseite und config.json]. Hugging Face. Abgerufen am 7. Oktober 2026, von https://huggingface.co/Qwen/Qwen3-8B

Ramírez, S. (o. D.). *FastAPI – Tutorial – User Guide*. Abgerufen am 7. Oktober 2026, von https://fastapi.tiangolo.com/tutorial/

Schmid, P., Sanseviero, O., Bartolome, A., von Werra, L., Vila, D., Srivastav, V., Sun, M., & Cuenca, P. (2024, 23. Juli). *Llama 3.1 – 405B, 70B & 8B with multilinguality and long context*. Hugging Face. https://huggingface.co/blog/llama31

Hinweise zum Format: Quellen ohne Datum erhalten «o. D.»; bei Webseiten, die sich ändern können, steht das Abrufdatum. Bei mehreren Werken derselben Urheberschaft im gleichen Jahr unterscheiden Buchstaben (a, b, c …) in alphabetischer Reihenfolge der Titel; Titel, die mit einer Zahl beginnen, werden eingeordnet, als wäre die Zahl ausgeschrieben («1.1» → «Eins Punkt Eins», also nach «DevOps …» und vor «Projektaufgabe …»). Die Buchstaben a–e der Brun-Einträge gelten gleich im Erklärungsdokument und im Bericht. Falls die HSW einen eigenen Zitierleitfaden hat, geht dieser vor.
