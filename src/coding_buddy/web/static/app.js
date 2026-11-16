const TOLERANCE = 2;
const COND = {
  without_codebook: { short: "CO", label: "Code only" },
  with_codebook: { short: "CB", label: "+ Codebook" },
};

const $ = (sel, root = document) => root.querySelector(sel);
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
const fmt = (x) => (Number.isInteger(x) ? String(x) : x.toFixed(1));
const signSvg = () => $("#tpl-sign").innerHTML;
const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;

const arrowSvg = (down) =>
  `<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M6 ${down ? "1.5v8.2M2.6 6.4 6 9.8l3.4-3.4" : "10.5V2.3M2.6 5.6 6 2.2l3.4 3.4"}" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>`;

const state = { data: null, script: null, mode: "compare", run: 0 };

/* ---------------- Classification ---------------- */

function classify(finding, truthLine) {
  if (!finding.hit) return { ...finding, verdict: "alarm" };
  return { ...finding, verdict: finding.explained ? "hit" : "wrong-cause", offset: truthLine - finding.line };
}

function verdictPlates(f) {
  if (f.verdict === "hit" || f.verdict === "wrong-cause") {
    let html = f.verdict === "hit"
      ? `<span class="plate plate-hit">Right line · right cause</span>`
      : `<span class="plate plate-yellow" title="Points at the injected line but does not name the real cause">Right line · wrong cause</span>`;
    if (f.offset) {
      const n = Math.abs(f.offset);
      html += `<span class="plate plate-distance" title="The injected error is ${n} line${n > 1 ? "s" : ""} ${f.offset > 0 ? "below" : "above"}">${arrowSvg(f.offset > 0)}${n} line${n > 1 ? "s" : ""}</span>`;
    }
    return html;
  }
  if (f.verdict === "alarm") return `<span class="plate plate-miss">False alarm</span>`;
  return "";
}

/* ---------------- Code renderer ---------------- */

/**
 * cols: [{ label, findings: [{line, category, explanation, verdict?, offset?}] }]
 * One table keeps every column registered on the same source lines.
 */
function renderCode(code, cols, truthLine = null) {
  const lines = code.replace(/\n$/, "").split("\n");
  const byLine = cols.map((c) => {
    const m = new Map();
    for (const f of c.findings) {
      const ln = Math.min(Math.max(1, f.line), lines.length);
      if (!m.has(ln)) m.set(ln, []);
      m.get(ln).push(f);
    }
    return m;
  });

  const table = document.createElement("table");
  table.className = "code" + (reducedMotion ? "" : " animate");
  const span = cols.length + 2;
  let html = "";
  if (cols.length > 1) {
    html += `<thead class="code-colhead"><tr><th></th>${cols.map((c) => `<th title="${esc(c.label)}"><span class="cond-plate cond-${c.key}">${esc(COND[c.key]?.short ?? "")}</span></th>`).join("")}<th></th></tr></thead>`;
  }
  html += "<tbody>";
  let order = 0;
  lines.forEach((text, i) => {
    const n = i + 1;
    const isTruth = n === truthLine;
    const signs = byLine.map((m) => {
      const fs = m.get(n);
      if (!fs) return `<td class="sg"></td>`;
      const d = order++ * 70;
      return `<td class="sg" style="--d:${d}ms">${signSvg().replace("<svg", `<svg style="--d:${d}ms"`)}${fs.length > 1 ? `<span class="sign-count">${fs.length}</span>` : ""}</td>`;
    });
    html += `<tr class="line${isTruth ? " is-truth" : ""}"><td class="ln">${isTruth ? `<span title="Injected error">${n}</span>` : n}</td>${signs.join("")}<td class="src">${esc(text) || " "}</td></tr>`;

    const any = byLine.some((m) => m.has(n));
    if (any) {
      const cells = cols.map((c, ci) => {
        const fs = byLine[ci].get(n);
        if (!fs) return cols.length > 1 ? `<div class="note-empty">${esc(c.label)}: no sign here</div>` : "";
        return fs
          .map(
            (f) => `<div class="note" style="--d:${order * 70}ms">
              <div class="note-head">${cols.length > 1 ? `<span class="note-cond cond-${c.key}">${esc(c.label)}</span>` : ""}<span class="note-cat">${esc(f.category)}</span>${verdictPlates(f)}</div>
              <p>${esc(f.explanation)}</p></div>`
          )
          .join("");
      });
      html += `<tr class="notes"><td colspan="${span}"><div class="notes-grid${cols.length > 1 ? " two" : ""}">${cells.join("")}</div></td></tr>`;
    }
  });
  html += "</tbody>";
  table.innerHTML = html;
  return table;
}

/* ---------------- Benchmark ---------------- */

function caseRuns(cond, script) {
  return state.data.results.runs[cond].map((run) => run.find((r) => r.script === script));
}

function tally(cond, c) {
  const runs = caseRuns(cond, c.script);
  if (c.bug) {
    const found = runs.filter((r) => r.found).length;
    const expl = runs.filter((r) => r.explained).length;
    const level = expl === runs.length ? "full" : found === 0 ? "none" : "part";
    return `<span class="tally" data-level="${level}" title="${COND[cond].label}: correctly explained in ${expl} of ${runs.length} runs, located in ${found}">${expl}/${runs.length}<small>${COND[cond].short}</small></span>`;
  }
  const fa = runs.reduce((a, r) => a + r.false_alarms, 0);
  return `<span class="tally" data-level="${fa ? "alarm" : "clean"}" title="${COND[cond].label}: ${fa} false alarm${fa === 1 ? "" : "s"} over ${runs.length} runs">${fa} FA<small>${COND[cond].short}</small></span>`;
}

function renderGantry() {
  const { summary, repeats } = state.data.results;
  const wo = summary.without_codebook;
  const wc = summary.with_codebook;
  const buggy = state.data.cases.filter((c) => c.bug);
  const sign = (cls, name, s, cond) => {
    const lanes = buggy
      .map((c) => {
        const runs = caseRuns(cond, c.script);
        const share = runs.filter((r) => r.explained).length / runs.length;
        return `<span class="lane${share ? " is-on" : ""}" title="${esc(c.script)}: cause named in ${Math.round(share * 100)}% of runs"><i style="width:${share * 100}%"></i><b>${esc(c.script.slice(0, 2))}</b></span>`;
      })
      .join("");
    return `<div class="dsign ${cls}">
      <div class="dsign-dest">
        <span class="dsign-name">${name}</span>
        <span class="dsign-detail">errors correctly explained${repeats > 1 ? `, mean of ${repeats} runs` : ""}</span>
        <span class="dsign-detail">right line ${fmt(s.found)} / ${s.n_bugs} · ${fmt(s.false_alarms)} false alarm${s.false_alarms === 1 ? "" : "s"}</span>
      </div>
      <div class="dsign-figure" aria-label="${fmt(s.explained)} of ${s.n_bugs}"><span class="n">${fmt(s.explained)}</span><span class="of">/ ${s.n_bugs}</span></div>
      <div class="lanes" aria-label="Cause named, per injected script">${lanes}</div>
    </div>`;
  };
  $("#gantry").innerHTML = sign("dsign-blue", "Code only", wo, "without_codebook") + sign("dsign-green", "Code + codebook", wc, "with_codebook");
  const lineClause =
    wo.found === wc.found
      ? `both find the line in ${fmt(wc.found)}`
      : `it finds the line in ${fmt(wo.found)} without the codebook and ${fmt(wc.found)} with it`;
  const causeClause =
    wc.explained === wo.explained
      ? `the codebook does not change how often it names the cause (${fmt(wc.explained)})`
      : `it names the cause in ${fmt(wc.explained)} with the codebook and ${fmt(wo.explained)} without`;
  $("#bench-title").textContent = `On ${wc.n_bugs} injected errors, ${lineClause}; ${causeClause}.`;
  const n = state.data.cases.length;
  const clean = state.data.cases.filter((c) => !c.bug).length;
  $("#bench-meta").innerHTML = `Small experiment on synthetic data: ${n} R scripts, ${n - clean} with one injected error each and ${clean} clean controls. Model <code>${esc(state.data.results.model)}</code>, temperature 0, ${repeats} run${repeats > 1 ? "s" : ""} per condition. A sign within ±${TOLERANCE} lines of the injected error is on the right line; it has the right cause when its explanation names the real variable, code or rule.`;
}

function renderList() {
  const ul = $("#script-list");
  ul.innerHTML = state.data.cases
    .map((c) => {
      const kind = c.bug ? `${c.bug.category.replaceAll("_", " ")}${c.bug.needs_codebook ? " · needs codebook" : ""}` : "clean control";
      return `<li><button type="button" class="script" data-script="${esc(c.script)}" aria-current="${c.script === state.script}">
        <span class="script-file">${esc(c.script).replaceAll("_", "_<wbr>")}</span>
        <span class="script-kind">${esc(kind)}</span>
        <span class="tallies">${tally("without_codebook", c)}${tally("with_codebook", c)}</span>
      </button></li>`;
    })
    .join("");
}

function renderViewer() {
  const c = state.data.cases.find((x) => x.script === state.script);
  $("#viewer-title").textContent = c.script;
  $("#truth").innerHTML = c.bug
    ? `<span class="plate plate-truth">Injected · line ${c.bug.line}</span><p>${esc(c.bug.description)}</p>`
    : `<span class="plate plate-quiet">Clean control</span><p>No injected error. Every sign on this script is a false alarm under the strict scoring.</p>`;

  const conds = state.mode === "compare" ? ["without_codebook", "with_codebook"] : [state.mode];
  const cols = conds.map((cond) => {
    const r = caseRuns(cond, c.script)[state.run];
    return {
      key: cond,
      label: COND[cond].label,
      findings: r.findings.map((f) => classify(f, c.bug?.line)),
    };
  });
  const host = $("#bench-code");
  host.replaceChildren(renderCode(c.code, cols, c.bug?.line ?? null));
  const target = host.querySelector(".is-truth") ?? host.querySelector(".notes")?.previousElementSibling;
  host.scrollTop = target ? Math.max(0, target.offsetTop - host.clientHeight / 3) : 0;
}

function setupBenchmark() {
  const res = state.data.results;
  if (!res) {
    $("#bench-title").textContent = "No benchmark results yet";
    $("#bench-meta").innerHTML = `Run <code>uv run coding-buddy --repeats 3</code> to create <code>results/results.json</code>, then reload this page.`;
    $("#gantry").hidden = true;
    $("#work").hidden = true;
    return;
  }
  $("#model-plate").textContent = `benchmark · ${res.model}`;
  $("#model-plate").title = "Model used for the benchmark results. Live review shows its own model.";
  // Deep link: ?script=05 opens that script, ?mode=with_codebook picks the condition.
  const params = new URLSearchParams(location.search);
  const wanted = params.get("script");
  state.script = (wanted && state.data.cases.find((c) => c.script.startsWith(wanted))?.script) || state.data.cases[0].script;
  if (["compare", "without_codebook", "with_codebook"].includes(params.get("mode"))) {
    state.mode = params.get("mode");
    $("#mode-group").querySelectorAll("button").forEach((b) => b.setAttribute("aria-checked", String(b.dataset.mode === state.mode)));
  }
  $("#run-select").innerHTML = Array.from({ length: res.repeats }, (_, i) => `<option value="${i}">Run ${i + 1} of ${res.repeats}</option>`).join("");
  $("#run-select").closest(".select-wrap").hidden = res.repeats < 2;
  renderGantry();
  renderList();
  renderViewer();

  $("#script-list").addEventListener("click", (e) => {
    const btn = e.target.closest(".script");
    if (!btn) return;
    state.script = btn.dataset.script;
    document.querySelectorAll(".script").forEach((b) => b.setAttribute("aria-current", String(b === btn)));
    renderViewer();
  });
  $("#script-list").addEventListener("keydown", (e) => {
    if (!["ArrowDown", "ArrowUp"].includes(e.key)) return;
    const items = [...document.querySelectorAll(".script")];
    const i = items.indexOf(document.activeElement);
    if (i < 0) return;
    e.preventDefault();
    const next = items[(i + (e.key === "ArrowDown" ? 1 : -1) + items.length) % items.length];
    next.focus();
    next.click();
  });
  $("#mode-group").addEventListener("click", (e) => {
    const btn = e.target.closest("button[data-mode]");
    if (!btn) return;
    state.mode = btn.dataset.mode;
    $("#mode-group").querySelectorAll("button").forEach((b) => b.setAttribute("aria-checked", String(b === btn)));
    renderViewer();
  });
  $("#run-select").addEventListener("change", (e) => {
    state.run = Number(e.target.value);
    renderViewer();
  });
}

/* ---------------- Live review ---------------- */

function syncGutter() {
  const ta = $("#editor");
  const n = Math.max(1, ta.value.split("\n").length);
  $("#editor-gutter").textContent = Array.from({ length: n }, (_, i) => i + 1).join("\n");
  ta.style.height = "auto";
  ta.style.height = ta.scrollHeight + "px";
  const hint = $("#editor-hint");
  hint.classList.remove("is-error");
  hint.textContent = `${n} line${n === 1 ? "" : "s"} · ${ta.value.length.toLocaleString()} / 20,000 characters`;
}

function resultState(kind, title, body) {
  const icon =
    kind === "error"
      ? `<svg viewBox="0 0 24 22" aria-hidden="true"><path d="M12 1.6 23 20.4H1z" fill="var(--surface)" stroke="var(--sign-red)" stroke-width="2.4" stroke-linejoin="round"/><path d="M8.6 9.4l6.8 6.8M15.4 9.4l-6.8 6.8" stroke="var(--sign-red)" stroke-width="2.2" stroke-linecap="round"/></svg>`
      : kind === "clear"
        ? `<svg viewBox="0 0 24 22" aria-hidden="true"><rect x="1.5" y="1.5" width="21" height="19" rx="3" fill="var(--sign-green)"/><path d="M7 11.4l3.4 3.4L17.4 7.6" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>`
        : `<svg viewBox="0 0 24 22" aria-hidden="true"><path d="M12 1.6 23 20.4H1z" fill="none" stroke="var(--line-strong)" stroke-width="2" stroke-linejoin="round" stroke-dasharray="3 3"/></svg>`;
  return `<div class="state${kind === "error" ? " state-error" : ""}">${icon}<h3>${esc(title)}</h3><p>${body}</p></div>`;
}

function setupLive() {
  const ta = $("#editor");
  const select = $("#example-select");
  select.innerHTML = `<option value="">Choose a script…</option>` + state.data.cases.map((c, i) => `<option value="${i}">${esc(c.script)}</option>`).join("");
  const start = state.data.cases.findIndex((c) => c.script.startsWith("05_"));
  select.value = String(Math.max(0, start));
  ta.value = state.data.cases[Math.max(0, start)].code;
  syncGutter();
  $("#result-body").innerHTML = resultState("empty", "No review yet", "Load an example or paste your own script, then press <strong>Review script</strong>. Signs appear on the lines the model flags.");

  select.addEventListener("change", () => {
    if (select.value === "") return;
    ta.value = state.data.cases[Number(select.value)].code;
    syncGutter();
  });
  ta.addEventListener("input", () => {
    select.value = "";
    syncGutter();
  });
  ta.addEventListener("keydown", (e) => {
    if (e.key === "Tab" && !e.shiftKey && !e.ctrlKey) {
      e.preventDefault();
      ta.setRangeText("  ", ta.selectionStart, ta.selectionEnd, "end");
      syncGutter();
    }
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      $("#review-form").requestSubmit();
    }
  });
  $("#review-form").addEventListener("submit", runReview);
}

async function runReview(e) {
  e.preventDefault();
  const code = $("#editor").value;
  const hint = $("#editor-hint");
  if (!code.trim()) {
    hint.textContent = "The editor is empty. Paste an R script or load an example first.";
    hint.classList.add("is-error");
    $("#editor").focus();
    return;
  }
  const useCodebook = $("#use-codebook").checked;
  const btn = $("#review-btn");
  const pane = $("#result-pane");
  btn.disabled = true;
  btn.querySelector(".btn-label").textContent = "Reviewing…";
  btn.querySelector("kbd")?.replaceWith(Object.assign(document.createElement("span"), { className: "spinner" }));
  pane.setAttribute("aria-busy", "true");
  $("#result-meta").textContent = `${state.data.results?.model ?? "Gemini"} is reading ${code.split("\n").length} lines${useCodebook ? " with the codebook" : ""}`;
  $("#result-body").innerHTML = `<div class="skeleton" aria-hidden="true">${Array.from({ length: 9 }, (_, i) => `<i style="width:${[62, 84, 40, 72, 90, 55, 78, 36, 66][i]}%"></i>`).join("")}</div>`;
  const t0 = performance.now();

  try {
    const res = await fetch("/api/review", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code, use_codebook: useCodebook }),
    });
    const body = await res.json().catch(() => ({}));
    if (!res.ok) {
      const detail = typeof body.detail === "string" ? body.detail : `The server answered ${res.status}.`;
      throw new Error(detail);
    }
    const secs = ((performance.now() - t0) / 1000).toFixed(1);
    const n = body.findings.length;
    $("#result-meta").innerHTML = `<span class="plate plate-mono" style="background:var(--surface-2);color:var(--ink);box-shadow:inset 0 0 0 1px var(--line)">live · ${esc(body.model)}</span><span class="plate ${useCodebook ? "plate-hit" : "plate-quiet"}">${useCodebook ? "With codebook" : "Code only"}</span><span>${secs} s</span>`;
    $("#result-title").textContent = n ? `${n} finding${n === 1 ? "" : "s"}` : "Findings";
    if (!n) {
      $("#result-body").innerHTML = resultState("clear", "No errors found", "The model reported no issue that would change the results. That is not proof the script is correct.");
    } else {
      const wrap = document.createElement("div");
      wrap.className = "code-scroll";
      wrap.append(renderCode(code, [{ key: "live", label: "Review", findings: body.findings }]));
      $("#result-body").replaceChildren(wrap);
    }
  } catch (err) {
    $("#result-title").textContent = "Findings";
    $("#result-meta").textContent = "";
    $("#result-body").innerHTML = resultState(
      "error",
      "The review did not run",
      `${esc(err.message)}<br>Check that the server is running and <code>GEMINI_API_KEY</code> is set in <code>.env</code>, then try again.`
    );
  } finally {
    btn.disabled = false;
    btn.querySelector(".btn-label").textContent = "Review script";
    btn.querySelector(".spinner")?.replaceWith(Object.assign(document.createElement("kbd"), { textContent: "Ctrl ↵" }));
    pane.removeAttribute("aria-busy");
  }
}

/* ---------------- Codebook (tiny Markdown renderer for our own file) ---------------- */

function inline(s) {
  return esc(s)
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
}

function renderMarkdown(md) {
  const out = [];
  const lines = md.split("\n");
  for (let i = 0; i < lines.length; i++) {
    const l = lines[i];
    if (/^# /.test(l)) out.push(`<h1 id="codebook-title">${inline(l.slice(2))}</h1>`);
    else if (/^## /.test(l)) out.push(`<h2>${inline(l.slice(3))}</h2>`);
    else if (/^\|/.test(l)) {
      const rows = [];
      while (i < lines.length && /^\|/.test(lines[i])) rows.push(lines[i++]);
      i--;
      const cells = (r) => r.replace(/^\||\|$/g, "").split("|").map((x) => x.trim());
      const [head, , ...body] = rows;
      out.push(`<table><thead><tr>${cells(head).map((h) => `<th scope="col">${inline(h)}</th>`).join("")}</tr></thead><tbody>${body.map((r) => `<tr>${cells(r).map((c) => `<td>${inline(c)}</td>`).join("")}</tr>`).join("")}</tbody></table>`);
    } else if (/^- /.test(l)) {
      const items = [];
      while (i < lines.length && /^(- |  )/.test(lines[i])) {
        if (/^- /.test(lines[i])) items.push(lines[i].slice(2));
        else items[items.length - 1] += " " + lines[i].trim();
        i++;
      }
      i--;
      out.push(`<ul>${items.map((x) => `<li>${inline(x)}</li>`).join("")}</ul>`);
    } else if (l.trim()) {
      let p = l;
      while (i + 1 < lines.length && lines[i + 1].trim() && !/^(#|\||- )/.test(lines[i + 1])) p += " " + lines[++i];
      out.push(`<p>${inline(p)}</p>`);
    }
  }
  return out.join("");
}

async function loadCodebook() {
  const body = $("#codebook-body");
  if (body.dataset.loaded) return;
  try {
    const res = await fetch("/api/codebook");
    body.innerHTML = renderMarkdown((await res.json()).markdown);
    body.dataset.loaded = "1";
  } catch {
    body.innerHTML = `<h1 id="codebook-title">Codebook</h1>` + resultState("error", "Could not load the codebook", "Reload the page to try again.");
  }
}

/* ---------------- Routing ---------------- */

function route() {
  const view = ["benchmark", "live", "codebook"].includes(location.hash.slice(1)) ? location.hash.slice(1) : "benchmark";
  for (const v of ["benchmark", "live", "codebook"]) $(`#view-${v}`).hidden = v !== view;
  document.querySelectorAll(".tab").forEach((t) => (t.dataset.view === view ? t.setAttribute("aria-current", "page") : t.removeAttribute("aria-current")));
  document.title = { benchmark: "Benchmark", live: "Live review", codebook: "Codebook" }[view] + " · Coding Buddy";
  if (view === "codebook") loadCodebook();
}

async function init() {
  window.addEventListener("hashchange", route);
  route();
  try {
    const res = await fetch("/api/benchmark");
    if (!res.ok) throw new Error(`The server answered ${res.status}.`);
    state.data = await res.json();
  } catch (err) {
    $("#bench-title").textContent = "Could not load the benchmark";
    $("#bench-meta").textContent = `${err.message} Start the server with uv run coding-buddy-ui and reload.`;
    $("#work").hidden = true;
    return;
  }
  setupBenchmark();
  setupLive();
}

init();
