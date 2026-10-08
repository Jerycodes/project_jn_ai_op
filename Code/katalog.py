"""
katalog.py – Daten-Schicht des LLM Requirements Calculators
============================================================
Selbstständige Arbeit, Modul AI Operations (FHNW HSW, HS26) – Jeremy Nathan

Hier liegen ausschliesslich DATEN und ihre Beschreibung:
    - QUANTISIERUNG_BITS   Bits pro Gewicht je Quantisierungsformat
    - Modell               Klasse: ein Modell mit seinen Architekturwerten
    - MODELL_KATALOG       Liste der Modelle, die der Rechner kennt

Keine Berechnung, keine Ein-/Ausgabe. Wer Daten ändern will (neues Modell, anderer
Wert), muss nur diese Datei anfassen. Später könnte der Katalog aus einer JSON-Datei
oder Datenbank geladen werden – ohne Änderung an rechner.py.

KI-Deklaration (Hilfsmittelverzeichnis, Merkblatt HSW-FHNW)
    Erstellt am 2026-10-07 mit Unterstützung von Claude (Anthropic; Modell Claude Fable 5.1,
    genutzt über die Claude-Desktop-App). Vorgaben, Entscheidungen (Thema, Struktur,
    Sprache, Umfang), Prüfung und Test: Jeremy Nathan.

Quellen (abgerufen am 2026-10-07; Nummerierung gilt im ganzen Projekt)
    [Q1] llama.cpp, Pull Request #1684 «k-quants» (Bits pro Gewicht der Quantisierungstypen,
         Dateigrössen des 7B-Modells, Zusammensetzung der _M-Varianten):
         https://github.com/ggml-org/llama.cpp/pull/1684
    [Q2] llama.cpp / ggml, Datei ggml-common.h (Block-Layouts Q8_0, Q4_K, Q5_K, Q6_K ->
         exakte Bits pro Gewicht): https://github.com/ggml-org/llama.cpp/blob/master/ggml/src/ggml-common.h
    [Q3] Hugging Face Blog «Llama 3.1 – 405B, 70B & 8B …», Abschnitt Inference Memory
         Requirements (Tabelle KV-Cache in FP16, Kontrollrechnung für die KV-Cache-Formel):
         https://huggingface.co/blog/llama31
    [Q5] Modellarchitekturen: config.json der jeweiligen Modellseite auf Hugging Face
         (Felder num_hidden_layers, num_key_value_heads, head_dim) – Link pro Modell im Katalog
    [Q6] Parameterzahlen: Hugging Face Model Hub, Feld «safetensors.total» der jeweiligen
         Modellseite (API: https://huggingface.co/api/models/<Repo>)
"""

from dataclasses import dataclass

# ---------------------------------------------------------------------------
# 1) Quantisierungen
# ---------------------------------------------------------------------------

# Effektive Bits pro Gewicht (bpw) je Quantisierung (GGUF-Format von llama.cpp).
# Q8_0 und F16 sind exakt [Q2]: Q8_0 = 34 Bytes pro 32 Gewichte = 8.5 bpw.
# Q4_K_M, Q5_K_M, Q6_K sind aus den 7B-Dateigrössen in [Q1] abgeleitet
# (Modell LLaMA-7B mit 6.738 Mrd. Parametern [Q6]):
#     bpw = Dateigrösse_GiB * 2^30 * 8 / Parameter
#     Q4_K_M: 3.80 GiB -> 4.84   Q5_K_M: 4.45 GiB -> 5.67   Q6_K: 5.15 GiB -> 6.57
# Kontrolle: Q6_K exakt laut Block-Layout = 6.5625 bpw [Q2] – die Herleitung aus der
# Dateigrösse (6.57) bestätigt den Rechenweg; verwendet wird der exakte Wert 6.56.
# Die _M-Varianten sind grösser als der reine Typ (Q4_K = 4.5 bpw), weil ein Teil der
# Tensoren mit Q6_K gespeichert wird [Q1].
QUANTISIERUNG_BITS: dict[str, float] = {
    "Q4_K_M": 4.84,   # Standard-Empfehlung: kleine Datei, gute Qualität
    "Q5_K_M": 5.67,   # etwas grösser, etwas bessere Qualität
    "Q6_K": 6.56,     # nahe an der Originalqualität
    "Q8_0": 8.5,      # praktisch verlustfrei, fast doppelt so gross wie Q4_K_M
    "F16": 16.0,      # unkomprimiert (16 Bit pro Gewicht)
}

# ---------------------------------------------------------------------------
# 2) Klasse Modell
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Modell:
    """
    Ein Modell im Katalog. frozen=True: Die Werte sind nach dem Anlegen unveränderlich,
    ein Katalogeintrag kann also nicht versehentlich überschrieben werden.
    Architekturwerte stammen aus der config.json des Modells [Q5].
    """
    name: str
    parameter_mrd: float   # Parameter in Milliarden [Q6]
    layer: int             # num_hidden_layers
    kv_heads: int          # num_key_value_heads (bei Grouped-Query Attention kleiner als die Attention-Heads)
    head_dim: int          # head_dim (= hidden_size / num_attention_heads)
    quelle: str            # Link zur config.json

    def kv_kb_pro_token(self) -> float:
        """
        KV-Cache pro Token in KB – eine Eigenschaft der Architektur, darum hier bei den Daten.
        Pro Layer werden für jeden KV-Head ein Key- und ein Value-Vektor (Faktor 2) mit
        head_dim Werten à 2 Bytes (float16) gespeichert.
        Beispiel Llama 3.1 8B: 2 * 32 * 8 * 128 * 2 Bytes = 131'072 Bytes = 128 KB.
        Kontrolle mit [Q3]: «1k Tokens» (1'024) -> 0.125 GB = 128 KB * 1'024 / 1'024 / 1'024.
        """
        return 2 * self.layer * self.kv_heads * self.head_dim * 2 / 1024

# ---------------------------------------------------------------------------
# 3) Modellkatalog – ein Eintrag pro Zeile, Quelle pro Zeile
# ---------------------------------------------------------------------------

MODELL_KATALOG: list[Modell] = [
    Modell("Llama 3.2 1B",   1.24,  16, 8,  64,  "https://huggingface.co/meta-llama/Llama-3.2-1B/blob/main/config.json"),
    Modell("Llama 3.2 3B",   3.21,  28, 8,  128, "https://huggingface.co/meta-llama/Llama-3.2-3B/blob/main/config.json"),
    Modell("Llama 3.1 8B",   8.03,  32, 8,  128, "https://huggingface.co/meta-llama/Llama-3.1-8B/blob/main/config.json"),
    Modell("Qwen3 8B",       8.19,  36, 8,  128, "https://huggingface.co/Qwen/Qwen3-8B/blob/main/config.json"),
    Modell("Phi-4 14B",      14.66, 40, 10, 128, "https://huggingface.co/microsoft/phi-4/blob/main/config.json"),
    Modell("Qwen3 14B",      14.77, 40, 8,  128, "https://huggingface.co/Qwen/Qwen3-14B/blob/main/config.json"),
    Modell("Qwen3 32B",      32.76, 64, 8,  128, "https://huggingface.co/Qwen/Qwen3-32B/blob/main/config.json"),
    Modell("Llama 3.3 70B",  70.55, 80, 8,  128, "https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct/blob/main/config.json"),
]
