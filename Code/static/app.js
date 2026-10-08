/* =====================================================================
   app.js – Verhalten der Web-Oberfläche
   =====================================================================
   Selbstständige Arbeit, Modul AI Operations (FHNW HSW, HS26) – Jeremy Nathan
   Projektaufgabe 1.1 «DevOps lokal», Schritt 3: Oberfläche für Endkunden.

   Was passiert hier?
   1. Bedienhilfen: Info-Knöpfe («i») auf-/zuklappen, Beispiele laden,
      Grafikkarten-Schalter, Eingaben im Browser merken
   2. Formular auslesen und als JSON an die API schicken (POST /empfehlung)
   3. Antwort der API in HTML umwandeln (Beste Wahl, Kennzahlen, Modell-Liste)

   Die Oberfläche kennt KEINE Rechenlogik – sie ruft nur die API in Code/main.py auf.
   So bleibt Code/rechner.py die einzige Stelle, an der gerechnet wird:
       Browser (diese Datei)  ->  POST /empfehlung (main.py)  ->  rechner.py  ->  katalog.py

   Begriffe (konsequent, damit nichts verwechselt wird):
   - Arbeitsspeicher (RAM)  = schneller Speicher, in dem das Modell beim Rechnen liegt
   - Grafikspeicher (VRAM)  = Arbeitsspeicher einer separaten Grafikkarte
   - Festplatte             = dauerhafter Speicherplatz für die Modelldatei

   KI-Deklaration (Hilfsmittelverzeichnis, Merkblatt HSW-FHNW)
   Erstellt am 2026-10-07 mit Unterstützung von Claude (Anthropic; Modell Claude Fable 5.1,
   genutzt über die Claude-Desktop-App) auf Basis einer früheren, von Jeremy Nathan
   geprüften Version. Vorgaben (Aufbau, Begriffe, Gestaltung), Prüfung und Test: Jeremy Nathan.

   Quelle: [Q7] Modul-Slides 1_01, Folie 14 «Beispiele Vorsemester» (CamCalculator,
   Zeiterfassung) als Vorbild für eine Web-Oberfläche mit Formular und Ergebnis.
   Keine externen Bibliotheken: reines HTML, CSS und JavaScript (fetch-API des Browsers).
   ===================================================================== */

(function () {
  "use strict";

  // ---------- Elemente aus dem HTML holen -----------------------------
  const form = document.getElementById("hardware-form");
  const submitBtn = document.getElementById("submit-btn");
  const formError = document.getElementById("form-error");
  const gpuToggle = document.getElementById("gpu_toggle");
  const vramWrapper = document.getElementById("vram-wrapper");
  const results = document.getElementById("results");
  const resultsSub = document.getElementById("results-sub");
  const resultsContent = document.getElementById("results-content");

  // Beispiele, die per Chip geladen werden können
  const PRESETS = {
    macbook: { betriebssystem: "macos",   ram_gb: 36, gpu: false, vram_gb: 8,  freier_speicher_gb: 200, anzahl_modelle: 2, quantisierung: "Q4_K_M", kontextfenster: 8192 },
    gaming:  { betriebssystem: "windows", ram_gb: 32, gpu: true,  vram_gb: 12, freier_speicher_gb: 500, anzahl_modelle: 3, quantisierung: "Q4_K_M", kontextfenster: 8192 },
    laptop:  { betriebssystem: "linux",   ram_gb: 16, gpu: false, vram_gb: 8,  freier_speicher_gb: 60,  anzahl_modelle: 1, quantisierung: "Q4_K_M", kontextfenster: 4096 },
  };

  const OS_NAME = { macos: "macOS", windows: "Windows", linux: "Linux" };

  // Texte und Icons pro Bewertung (Farbe kommt aus dem CSS, Text + Icon aus dieser Tabelle)
  const BEWERTUNG = {
    "optimal":  { klasse: "optimal", text: "Optimal",  icon: "check" },
    "passt":    { klasse: "passt",   text: "Passt",    icon: "check" },
    "knapp":    { klasse: "knapp",   text: "Knapp",    icon: "warn"  },
    "zu gross": { klasse: "zugross", text: "Zu gross", icon: "x"     },
  };

  // Welcher Speicher wird für das Modell genutzt? (Antwort der API: speichertyp)
  const SPEICHERTYP = {
    vram:    { wort: "Grafikspeicher",  titel: "Grafikspeicher (VRAM)", sub: "der separaten Grafikkarte",            erklaerung: "Deine separate Grafikkarte rechnet im eigenen Grafikspeicher – das ist der schnellste Fall." },
    unified: { wort: "Arbeitsspeicher", titel: "Arbeitsspeicher (RAM)", sub: "CPU und GPU teilen ihn sich (Apple Silicon)", erklaerung: "Auf Apple Silicon teilen sich CPU und GPU den Arbeitsspeicher. macOS gibt der GPU rund zwei Drittel bis drei Viertel davon frei." },
    ram:     { wort: "Arbeitsspeicher", titel: "Arbeitsspeicher (RAM)", sub: "der Prozessor rechnet, keine Grafikkarte", erklaerung: "Ohne separate Grafikkarte rechnet der Prozessor im Arbeitsspeicher – das funktioniert, ist aber deutlich langsamer." },
  };

  // Kleine SVG-Icons als Strings (keine Icon-Bibliothek nötig)
  const ICONS = {
    check: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 8.5l3 3 7-7"/></svg>',
    warn:  '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8 2.5l6 11H2z"/><path d="M8 6.5v3M8 12h.01"/></svg>',
    x:     '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M4 4l8 8M12 4l-8 8"/></svg>',
    star:  '<svg viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M8 1.5l2 4.2 4.6.6-3.4 3.2.9 4.6L8 11.8 3.9 14.1l.9-4.6L1.4 6.3 6 5.7z"/></svg>',
    disk:  '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="3" width="12" height="10" rx="2"/><path d="M2 9h12M5 11.5h.01"/></svg>',
    info:  '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="8" cy="8" r="6.2"/><path d="M8 7.2v4M8 5h.01"/></svg>',
  };

  // ---------- Hilfsfunktionen -----------------------------------------
  /** Zahl im Schweizer Format, z. B. 24.1 oder 8'192 */
  function zahl(n, dezimalen) {
    return Number(n).toLocaleString("de-CH", { minimumFractionDigits: dezimalen, maximumFractionDigits: dezimalen });
  }

  /** Text sicher ins HTML einfügen (verhindert, dass Text als HTML interpretiert wird) */
  function esc(text) {
    return String(text).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }

  function badge(bewertung) {
    const b = BEWERTUNG[bewertung] || BEWERTUNG["zu gross"];
    return `<span class="badge badge--${b.klasse}">${ICONS[b.icon]}${b.text}</span>`;
  }

  function icon(name, groesse) {
    return ICONS[name].replace('viewBox="0 0 16 16"', `viewBox="0 0 16 16" width="${groesse}" height="${groesse}"`);
  }

  // ---------- 1. Bedienhilfen -----------------------------------------
  /** Info-Knöpfe: klappen die Erklärung unter dem Feld auf und zu */
  document.querySelectorAll(".info-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const panel = document.getElementById(btn.getAttribute("aria-controls"));
      const offen = btn.getAttribute("aria-expanded") === "true";
      btn.setAttribute("aria-expanded", String(!offen));
      panel.hidden = offen;
    });
  });

  /**
   * Grafikkarten-Schritt an das Betriebssystem anpassen:
   * - macOS (Apple Silicon): keine separate Grafikkarte -> Schalter aus und gesperrt, Hinweis einblenden
   * - Windows/Linux: Schalter frei; VRAM-Feld nur, wenn der Schalter an ist
   */
  function gpuAnzeigeAktualisieren() {
    const istMac = form.querySelector('input[name="betriebssystem"]:checked').value === "macos";
    if (istMac) gpuToggle.checked = false;
    gpuToggle.disabled = istMac;
    document.getElementById("step-gpu").classList.toggle("step--disabled", istMac);
    document.getElementById("gpu-note").classList.toggle("is-hidden", !istMac);
    vramWrapper.classList.toggle("is-hidden", !gpuToggle.checked);
  }
  gpuToggle.addEventListener("change", gpuAnzeigeAktualisieren);

  /** Betriebssystem geändert -> Grafikkarten-Schritt ein-/ausblenden */
  form.querySelectorAll('input[name="betriebssystem"]').forEach((radio) => {
    radio.addEventListener("change", gpuAnzeigeAktualisieren);
  });

  /** Schreibt Werte (Beispiel oder gespeicherte Eingaben) ins Formular */
  function formularSetzen(w) {
    form.querySelector(`input[name="betriebssystem"][value="${w.betriebssystem}"]`).checked = true;
    form.ram_gb.value = w.ram_gb;
    gpuToggle.checked = Boolean(w.gpu);
    form.vram_gb.value = w.vram_gb;
    form.freier_speicher_gb.value = w.freier_speicher_gb;
    form.anzahl_modelle.value = w.anzahl_modelle;
    form.quantisierung.value = w.quantisierung;
    form.kontextfenster.value = w.kontextfenster;
    gpuAnzeigeAktualisieren();
  }

  /** Beispiel-Chips: Werte setzen und direkt berechnen */
  document.querySelectorAll(".chip[data-preset]").forEach((chip) => {
    chip.addEventListener("click", () => {
      formularSetzen(PRESETS[chip.dataset.preset]);
      form.requestSubmit();
    });
  });

  /** Eingaben im Browser merken (falls kein Speicher verfügbar ist, passiert einfach nichts) */
  function eingabenSpeichern(payload) {
    try { localStorage.setItem("llm-calc-eingaben", JSON.stringify({ ...payload, gpu: gpuToggle.checked, vram_gb: form.vram_gb.value })); } catch (e) { /* ignorieren */ }
  }
  function eingabenLaden() {
    try { return JSON.parse(localStorage.getItem("llm-calc-eingaben")); } catch (e) { return null; }
  }

  // ---------- 2. Formular -> JSON -> API --------------------------------
  /** Liest das Formular und baut das JSON, das die API erwartet (siehe HardwareAnfrage in main.py) */
  function formularAuslesen() {
    const daten = new FormData(form);
    return {
      ram_gb: Number(daten.get("ram_gb")),
      betriebssystem: daten.get("betriebssystem"),
      vram_gb: gpuToggle.checked ? Number(daten.get("vram_gb")) : null,   // null = keine separate Grafikkarte
      freier_speicher_gb: Number(daten.get("freier_speicher_gb")),
      anzahl_modelle: Number(daten.get("anzahl_modelle")),
      quantisierung: daten.get("quantisierung"),
      kontextfenster: Number(daten.get("kontextfenster")),
    };
  }

  async function empfehlungAbrufen(payload) {
    const antwort = await fetch("/empfehlung", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (antwort.status === 422) {
      // Pydantic hat die Eingabe abgelehnt – Felder und Meldungen anzeigen
      const fehler = await antwort.json();
      const liste = (fehler.detail || []).map((f) => `${f.loc[f.loc.length - 1]}: ${f.msg}`).join(" · ");
      throw new Error("Ungültige Eingabe – " + liste);
    }
    if (!antwort.ok) throw new Error(`Der Server hat mit Status ${antwort.status} geantwortet.`);
    return antwort.json();
  }

  // ---------- 3. Darstellung der Antwort ------------------------------
  function modellZeile(e, d, typ, anzahlModelle, istBeste) {
    const nutzbar = d.nutzbarer_speicher_gb;
    const anteil = nutzbar > 0 ? (e.benoetigter_speicher_gb / nutzbar) * 100 : 100;
    const stufe = e.bewertung === "knapp" ? "warn" : e.bewertung === "zu gross" ? "bad" : "";
    const disk = e.passt_auf_festplatte
      ? `<span class="model__disk model__disk--ok">${ICONS.disk} Festplatte: ${zahl(e.dateigroesse_gb, 1)} GB Modelldatei – Platz reicht${anzahlModelle > 1 ? ` für ${anzahlModelle} Modelle` : ""}</span>`
      : `<span class="model__disk model__disk--no">${ICONS.disk} Festplatte: ${zahl(e.dateigroesse_gb, 1)} GB Modelldatei – zu wenig freier Platz${anzahlModelle > 1 ? ` für ${anzahlModelle} Modelle` : ""}</span>`;

    return `
      <li class="model ${istBeste ? "model--best" : ""}">
        <div class="model__head">
          <span class="model__name">${esc(e.name)}</span>
          <span class="model__params">${zahl(e.parameter_mrd, 1)} Mrd. Parameter</span>
          ${istBeste ? `<span class="badge badge--best">${ICONS.star}Beste Wahl</span>` : ""}
          ${badge(e.bewertung)}
        </div>
        <div class="model__ram">${typ.wort}: <strong>${zahl(e.benoetigter_speicher_gb, 1)} GB</strong> von ${zahl(nutzbar, 1)} GB</div>
        <div class="model__meter-row">
          <div class="meter ${stufe ? `meter--${stufe}` : ""}" role="img" aria-label="${Math.round(anteil)} Prozent des nutzbaren ${typ.wort}s">
            <div class="meter__fill ${stufe ? `meter__fill--${stufe}` : ""}" style="width:${Math.min(anteil, 100)}%"></div>
          </div>
          <span class="meter__pct">${Math.round(anteil)} %</span>
        </div>
        ${disk}
      </li>`;
  }

  function ergebnisRendern(d, payload) {
    const typ = SPEICHERTYP[d.speichertyp] || SPEICHERTYP.ram;
    const beste = d.passend.find((e) => e.name === d.beste_wahl);

    // Untertitel: Was wurde eingegeben?
    resultsSub.textContent = [
      OS_NAME[payload.betriebssystem],
      `${zahl(payload.ram_gb, 0)} GB Arbeitsspeicher`,
      payload.vram_gb ? `Grafikkarte mit ${zahl(payload.vram_gb, 0)} GB Grafikspeicher`
        : payload.betriebssystem === "macos" ? "Apple Silicon (GPU nutzt den Arbeitsspeicher)" : "keine separate Grafikkarte",
      `${zahl(payload.freier_speicher_gb, 0)} GB frei auf der Festplatte`,
      payload.quantisierung,
      `${zahl(payload.kontextfenster, 0)} Tokens`,
    ].join(" · ");

    // 1) Beste Wahl
    let besteHtml;
    if (beste) {
      besteHtml = `
        <section class="card best">
          <div class="best__eyebrow">Beste Wahl für deinen Computer</div>
          <div class="best__name">${esc(beste.name)}</div>
          <div class="best__meta"><span>${zahl(beste.parameter_mrd, 1)} Mrd. Parameter · ${esc(payload.quantisierung)}</span>${badge(beste.bewertung)}</div>
          <div class="best__facts">
            <div class="fact">
              <div class="fact__label">${typ.wort} beim Rechnen</div>
              <div class="fact__value">${zahl(beste.benoetigter_speicher_gb, 1)} GB</div>
              <div class="fact__sub">von ${zahl(d.nutzbarer_speicher_gb, 1)} GB nutzbar</div>
            </div>
            <div class="fact">
              <div class="fact__label">Festplatte (Modelldatei)</div>
              <div class="fact__value">${zahl(beste.dateigroesse_gb, 1)} GB</div>
              <div class="fact__sub">${beste.passt_auf_festplatte ? "Platz reicht" : "zu wenig freier Platz"}</div>
            </div>
            <div class="fact">
              <div class="fact__label">Davon für den Kontext</div>
              <div class="fact__value">${zahl(beste.kv_cache_gb, 1)} GB</div>
              <div class="fact__sub">${zahl(payload.kontextfenster, 0)} Tokens</div>
            </div>
          </div>
        </section>`;
    } else {
      besteHtml = `
        <section class="card best">
          <div class="best__eyebrow">Ergebnis</div>
          <div class="best__none">Kein Modell aus dem Katalog passt in den nutzbaren ${typ.wort}.</div>
          <div class="best__meta">Versuche eine kleinere Quantisierung (Q4_K_M) oder ein kleineres Kontextfenster.</div>
        </section>`;
    }

    // 2) Kennzahlen
    const statsHtml = `
      <div class="stats">
        <div class="card stat">
          <div class="stat__label">Nutzbarer ${typ.wort} für das Modell</div>
          <div class="stat__value">${zahl(d.nutzbarer_speicher_gb, 1)}<small>GB</small></div>
          <div class="stat__sub">${typ.titel} – ${typ.sub}</div>
        </div>
        <div class="card stat">
          <div class="stat__label">Grösstes mögliches Modell</div>
          <div class="stat__value">${zahl(d.max_parameter_mrd, 0)}<small>Mrd. Parameter</small></div>
          <div class="stat__sub">Faustregel ohne Kontextfenster</div>
        </div>
        <div class="card stat">
          <div class="stat__label">Empfohlene Modellgrösse</div>
          <div class="stat__value">${zahl(d.optimale_parameter_mrd, 0)}<small>Mrd. Parameter</small></div>
          <div class="stat__sub">mit Reserve für Kontext und Tempo</div>
        </div>
      </div>`;

    // 3) Hinweise aus der API (Erklärung zum Speichertyp, Warnungen): blau = Info, gelb = kein Modell passt
    const hinweise = d.hinweise.length ? d.hinweise : [typ.erklaerung];
    const istWarnung = d.beste_wahl === null;
    const calloutHtml = `
      <div class="callout ${istWarnung ? "callout--warn" : ""}" role="note">
        ${icon(istWarnung ? "warn" : "info", 18)}
        <ul>${hinweise.map((h) => `<li>${esc(h)}</li>`).join("")}</ul>
      </div>`;

    // 4) Passende Modelle
    const listeHtml = `
      <section class="card models">
        <h3 class="models__title">Passende Modelle <span class="models__count">${d.passend.length} von ${d.passend.length + d.zu_gross.length} im Katalog</span></h3>
        ${d.passend.length
          ? `<ul class="model-list">${d.passend.map((e) => modellZeile(e, d, typ, payload.anzahl_modelle, e.name === d.beste_wahl)).join("")}</ul>`
          : `<p style="color:var(--text-2)">Keines der Modelle im Katalog passt.</p>`}
      </section>`;

    // 5) Zu grosse Modelle (zugeklappt)
    const zuGrossHtml = d.zu_gross.length ? `
      <section class="card">
        <details class="toobig">
          <summary>Zu gross für deinen Computer (${d.zu_gross.length})</summary>
          <ul class="model-list">${d.zu_gross.map((e) => modellZeile(e, d, typ, payload.anzahl_modelle, false)).join("")}</ul>
        </details>
      </section>` : "";

    resultsContent.innerHTML = besteHtml + statsHtml + calloutHtml + listeHtml + zuGrossHtml;
    results.classList.remove("is-hidden");
    results.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  // ---------- Formular abschicken -------------------------------------
  form.addEventListener("submit", async (ev) => {
    ev.preventDefault();
    formError.classList.add("is-hidden");
    if (!form.checkValidity()) { form.reportValidity(); return; }

    const payload = formularAuslesen();
    submitBtn.disabled = true;
    submitBtn.classList.add("is-loading");
    try {
      const daten = await empfehlungAbrufen(payload);
      ergebnisRendern(daten, payload);
      eingabenSpeichern(payload);
    } catch (fehler) {
      const netz = fehler instanceof TypeError;   // fetch scheitert komplett -> Server nicht erreichbar
      formError.textContent = netz
        ? "Die API ist nicht erreichbar. Läuft der Server? (uvicorn Code.main:app --reload --reload-dir Code)"
        : fehler.message;
      formError.classList.remove("is-hidden");
    } finally {
      submitBtn.disabled = false;
      submitBtn.classList.remove("is-loading");
    }
  });

  // ---------- Start ---------------------------------------------------
  const gespeichert = eingabenLaden();
  if (gespeichert && gespeichert.betriebssystem) {
    formularSetzen({ ...gespeichert, vram_gb: gespeichert.vram_gb || 8 });
  } else {
    gpuAnzeigeAktualisieren();
  }
})();
