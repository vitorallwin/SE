// Bancada: cliente da API em lab_server.py. Nenhum dado do caso é montado com innerHTML.

const CODES = {
  "GATE-INSUMO": "insumo insuficiente",
  "GATE-CATALOGO": "fora do catálogo",
  "DECISAO-ABERTA": "decisão interna pendente",
  "APROVACAO-CITACAO": "citação da aprovação",
  "APROVACAO-CAMPOS": "campos da aprovação",
  "SLA-APLICACAO": "aplicação do SLA",
  "DATA-SEM-ORIGEM": "data sem origem",
  "VIABILIDADE": "viabilidade e caminho",
  "SEMANAS": "semanas do cronograma",
  "PRONTIDAO": "prontidão do evento",
  "CONFLITO-PADRAO": "conflito com padrão",
  "TEXTO-SLOT": "texto do template",
  "ID-INTERNO": "ID interno no texto",
  "PRODUTO": "produto ou onda",
  "COBERTURA": "cobertura do insumo",
  "ESCOPO": "escopo",
  "FORMATO": "formato (schema)",
  "JSON-INVALIDO": "JSON ilegível",
  "OUTRO": "outros",
};
const LEGIT = new Set(["GATE-INSUMO", "GATE-CATALOGO", "DECISAO-ABERTA"]);
const FEAS = { fits: "cabe", partially_fits: "cabe parcialmente", does_not_fit: "não cabe", conditional: "condicional" };
const AUTHOR = { A: "Gemini", "B-api": "Claude (API)", "C-local": "IA local", manual: "manual", B: "—" };

const state = { status: null, runs: [], current: null, selected: null, poll: null };
const $ = (id) => document.getElementById(id);

function h(tag, attrs = {}, ...children) {
  const el = document.createElement(tag);
  for (const [key, value] of Object.entries(attrs || {})) {
    if (value === false || value == null) continue;
    if (key === "class") el.className = value;
    else if (key.startsWith("on")) el.addEventListener(key.slice(2), value);
    else if (key === "style") el.style.cssText = value;
    else el.setAttribute(key, value === true ? "" : value);
  }
  for (const child of children.flat()) {
    if (child == null || child === false) continue;
    el.append(child instanceof Node ? child : document.createTextNode(String(child)));
  }
  return el;
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    headers: options.body ? { "Content-Type": "application/json" } : undefined,
    body: options.body ? JSON.stringify(options.body) : undefined,
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.error || `HTTP ${response.status}`);
  return data;
}

function toast(message) {
  const el = $("toast");
  el.textContent = message;
  el.classList.add("show");
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => el.classList.remove("show"), 3200);
}

const when = (iso) => (iso ? new Date(iso).toLocaleString("pt-BR", { dateStyle: "short", timeStyle: "short" }) : "");
const kb = (n) => (n > 1024 * 1024 ? `${(n / 1048576).toFixed(1)} MB` : `${Math.max(1, Math.round(n / 1024))} KB`);
const brDate = (iso) => (iso ? iso.split("-").reverse().join("/") : "—");

/* Masthead */
function renderEngine() {
  const s = state.status;
  const a = s.authors;
  $("engine").replaceChildren(
    ...[["Motor", s.engine_version], ["Regras", `v${s.rules_version}`], ["Template", s.template_version]].map(([k, v]) =>
      h("div", {}, h("dt", {}, k), h("dd", {}, v))),
    h("div", {}, h("dt", {}, "Autores"), h("dd", {},
      ...[["gemini", "Gemini"], ["claude", "Claude"], ["local", "IA local"]].map(([key, label], i) => h("span", {
        title: a[key].configured ? `${a[key].model} · chave: ${a[key].key_source}` : "sem chave no .env",
        style: i ? "margin-left:12px" : "" }, h("span", { class: `dot ${a[key].configured ? "on" : ""}` }), label)))),
  );
}

/* Run list */
function renderRuns() {
  const list = $("runs");
  if (!state.runs.length) {
    list.replaceChildren(h("li", { class: "runs-empty" }, "Nenhuma execução ainda."));
    return;
  }
  list.replaceChildren(...state.runs.map((run) => h("li", {},
    h("button", { class: "run", type: "button", "aria-current": state.current?.id === run.id ? "true" : "false", onclick: () => openRun(run.id) },
      h("span", { class: "run-name" }, run.name),
      h("span", { class: "pips", "aria-label": `${run.attempts} de ${run.limit} tentativas` },
        ...Array.from({ length: run.limit }, (_, i) => h("span", { class: `pip ${i < run.attempts ? "used" : ""}` }))),
      h("span", { class: "run-meta" }, h("span", { class: `tag v-${run.verdict.key}` }, run.verdict.label), " ", when(run.created_at)),
    ))));
}

async function loadRuns() {
  state.runs = await api("/api/runs");
  renderRuns();
}

/* Sheet */
async function openRun(id, { keepSelection = false } = {}) {
  const run = await api(`/api/runs/${id}`);
  const changed = state.current?.id !== id;
  state.current = run;
  if (changed || !keepSelection || state.selected > run.attempt_log.length) state.selected = run.attempt_log.length || null;
  if (location.hash !== `#${id}`) history.replaceState(null, "", `#${id}`);
  renderSheet();
  renderRuns();
  schedulePoll();
  if (changed) $("sheet").focus({ preventScroll: true });
}

function schedulePoll() {
  clearTimeout(state.poll);
  if (state.current?.job?.state === "running") {
    state.poll = setTimeout(async () => {
      const before = state.current.attempt_log.length;
      await openRun(state.current.id, { keepSelection: true }).catch(() => {});
      if (state.current.attempt_log.length !== before) state.selected = state.current.attempt_log.length, renderSheet();
      if (state.current.job?.state !== "running") { loadRuns(); toast(`Autor terminou: ${state.current.verdict.label}`); }
    }, 3000);
  }
}

function attemptKind(entry) {
  const comp = entry.composition?.status;
  if (comp === "emitted") return ["emitted", "Emitida"];
  if (comp === "blocked_by_composer") return ["failed", "Compositor bloqueou"];
  const codes = entry.codes || [];
  if (codes.length && codes.every((c) => LEGIT.has(c))) return ["blocked", "Bloqueio legítimo"];
  return ["violations", `${entry.errors_count} violaç${entry.errors_count === 1 ? "ão" : "ões"}`];
}

function renderSheet() {
  const run = state.current;
  const limit = run.limit;
  const log = run.attempt_log;
  const running = run.job?.state === "running";
  const full = log.length >= limit;
  const authors = state.status.authors;

  const slots = Array.from({ length: limit }, (_, i) => {
    const entry = log[i];
    if (!entry) {
      const live = running && i === log.length;
      return h("div", { class: `slot ${live ? "s-running" : ""}` },
        h("span", { class: "slot-n" }, i + 1),
        h("span", { class: "slot-status" }, live ? "Autor escrevendo…" : "Livre"),
        live ? h("span", { class: "slot-sub" }, run.job.model) : null);
    }
    const [kind, label] = attemptKind(entry);
    return h("button", { type: "button", class: `slot filled s-${kind}`, "aria-pressed": state.selected === i + 1 ? "true" : "false",
      onclick: () => { state.selected = i + 1; renderSheet(); } },
      h("span", { class: "slot-n" }, i + 1),
      h("span", { class: "slot-status" }, label),
      h("span", { class: "slot-sub" }, when(entry.at)),
      h("span", { class: "slot-codes" }, ...(entry.codes || []).map((c) => h("span", { class: `code-chip ${LEGIT.has(c) ? "legit" : ""}` }, c))));
  });

  const authorBtn = (engine, label) => {
    const ok = authors[engine].configured;
    return h("button", { class: "btn", type: "button", disabled: running || full || !ok,
      title: ok ? `Roda até ${limit - log.length} tentativa(s) com ${authors[engine].model}` : `Configure a chave no .env do servidor`,
      onclick: () => startAuthor(engine) }, `Rodar ${label}`);
  };

  const r = run.request;
  const facts = [["Data", brDate(r.proposal_date)], ["Dados", r.data_mode], ["Autor", AUTHOR[r.configuration] || r.configuration],
    ["Modelo", r.author_model], ["Motor", `${r.engine_version} · v${r.rules_version}`], ["Skill", (r.skill_sha256 || "").slice(0, 12)]];

  $("sheet").replaceChildren(
    h("header", { class: "head" },
      h("div", {},
        h("h1", {}, run.name),
        h("div", { class: "head-id" }, run.id, run.pending.code ? ` · ${run.pending.code}` : "", run.pending.client ? ` · ${run.pending.client}` : "")),
      h("span", { class: `stamp v-${run.verdict.key}` }, run.verdict.label),
      h("dl", { class: "facts" }, ...facts.map(([k, v]) => h("div", {}, h("dt", {}, k), h("dd", {}, v || "—"))),
        run.parent ? h("div", {}, h("dt", {}, "Origem"), h("dd", {}, h("button", { class: "parent-link", type: "button", onclick: () => openRun(run.parent) }, run.parent))) : null),
    ),

    renderNextStep(run),

    h("section", { class: "block", "aria-labelledby": "t-attempts" },
      h("div", { class: "block-title" }, h("h2", { id: "t-attempts" }, "Tentativas"), h("span", { class: "aside" }, `${log.length} de ${limit} usadas · limite físico`)),
      h("div", { class: "slots", style: `--limit:${limit}` }, ...slots),
      h("div", { class: "toolbar" },
        authorBtn("claude", "Claude"), authorBtn("gemini", "Gemini"), authorBtn("local", "IA local"),
        h("span", { class: "sep", "aria-hidden": "true" }),
        h("button", { class: "btn", type: "button", disabled: running || full, onclick: () => openDialog("dlg-state") }, "Colar estado.json"),
        h("button", { class: "btn btn-quiet", type: "button", onclick: () => openDialog("dlg-complement") }, "Complementar insumo → nova execução")),
      run.job?.state === "failed" ? h("div", { class: "job-error" }, `Autor falhou: ${run.job.error}`,
        /chave/i.test(run.job.error) ? h("div", { style: "margin-top:8px" }, h("button", { class: "btn", type: "button", onclick: () => $("open-keys").click() }, "Trocar a chave")) : null) : null,
    ),

    renderViolations(log),
    renderPending(run.pending, log.length),
    renderOutputs(run),

    h("section", { class: "block", "aria-labelledby": "t-raw" },
      h("div", { class: "block-title" }, h("h2", { id: "t-raw" }, "Insumo e notas"), h("span", { class: "aside" }, run.sources.join(" · "))),
      h("details", { class: "raw" }, h("summary", {}, `insumo.md · ${run.insumo.length.toLocaleString("pt-BR")} caracteres`), h("pre", { class: "pre" }, run.insumo)),
      run.notes ? h("details", { class: "raw", open: true }, h("summary", {}, "Notas do autor"), h("pre", { class: "pre" }, run.notes)) : null,
    ),
  );
}

const DECISIONS = { warranty: "garantia", license_supply: "fornecimento das licenças", sla: "SLA", sla_applicability: "a quais fases o SLA se aplica",
  engagement_type: "tipo de engajamento", stabilization_buffer: "folga de estabilização antes do evento" };

// Traduz o estado da execução em um próximo passo concreto, com o botão certo.
function renderNextStep(run) {
  const log = run.attempt_log, last = log[log.length - 1], left = run.limit - log.length;
  const items = log.flatMap((a) => a.items || []);
  const open = [...new Set(items.filter((i) => i.code === "DECISAO-ABERTA").map((i) => (i.message.match(/aberta: (\w+)/) || [])[1]).filter(Boolean))];
  const openText = open.map((k) => DECISIONS[k] || k).join(", ");
  const lastCodes = new Set(last?.codes || []);
  const btn = (label, onclick, primary) => h("button", { class: `btn ${primary ? "btn-primary" : ""}`, type: "button", onclick }, label);
  const complement = () => openDialog("dlg-complement");
  const repeat = async () => {
    try { const r = await api(`/api/runs/${run.id}/complement`, { method: "POST", body: { text: "" } }); await loadRuns(); await openRun(r.id); toast("Nova execução com o mesmo insumo."); }
    catch (err) { toast(err.message); }
  };
  let text, actions = [];
  if (run.job?.state === "running") text = "O autor está escrevendo. Cada tentativa aparece numa casa acima assim que o validador responde.";
  else if (!log.length) text = "Clique em Rodar Claude ou Rodar Gemini. Se o estado foi escrito fora daqui, use Colar estado.json.";
  else if (run.verdict.key === "emitted") {
    text = "Proposta pronta. Baixe o DOCX (verde, em Saída) e gere o PDF para conferir as páginas.";
  } else if (lastCodes.has("GATE-INSUMO")) {
    text = "O insumo não basta para escrever uma proposta. Leve as perguntas ao cliente abaixo e, com as respostas, use Complementar insumo.";
    actions = [btn("Complementar insumo", complement, true)];
  } else if (lastCodes.has("GATE-CATALOGO")) {
    text = "O pedido está fora do catálogo disponível. O motor precisa do pacote desse fabricante antes de gerar proposta.";
  } else if (open.length && (run.verdict.key === "blocked" || !left)) {
    text = `Falta uma decisão da POPULOS que o autor não pode inventar: ${openText}. Cole o e-mail de quem aprovou (nome, data e o valor aprovado) em Complementar insumo. Uma nova execução começa com isso.`;
    actions = [btn("Complementar insumo com a aprovação", complement, true)];
  } else if (left > 0) {
    text = `O autor errou em ${last.errors_count} ponto(s). Rode o autor de novo: ele recebe as violações e corrige. Restam ${left} tentativa(s).`;
  } else {
    text = "As 3 tentativas acabaram sem proposta. Repita com o mesmo insumo (nova execução) ou complemente o insumo se faltou informação.";
    actions = [btn("Repetir com o mesmo insumo", repeat, true), btn("Complementar insumo", complement)];
  }
  if (lastCodes.has("FORMATO") && run.verdict.key !== "emitted") text += " (FORMATO = o JSON fugiu do schema; é erro do autor, não do caso.)";
  return h("section", { class: "next", "aria-labelledby": "t-next" },
    h("h2", { id: "t-next" }, "O que fazer agora"), h("p", {}, text), actions.length ? h("div", { class: "toolbar" }, ...actions) : null);
}

function renderViolations(log) {
  const entry = log[(state.selected || 0) - 1];
  const title = h("div", { class: "block-title" }, h("h2", { id: "t-viol" }, entry ? `Validador · tentativa ${entry.attempt}` : "Validador"),
    entry ? h("span", { class: "aside" }, `${entry.errors_count} mensage${entry.errors_count === 1 ? "m" : "ns"} · ${entry.codes.length} código${entry.codes.length === 1 ? "" : "s"}`) : null);
  let body;
  if (!entry) body = h("p", { class: "muted" }, "Nenhuma tentativa submetida.");
  else if (!entry.errors.length) body = h("p", { class: "clean" }, entry.composition?.status === "emitted" ? "Nenhuma violação. Proposta composta." : `Nenhuma violação de regra. Compositor: ${entry.composition?.error || "—"}`);
  else {
    const groups = new Map();
    for (const { code, message } of entry.items) {
      if (!groups.has(code)) groups.set(code, []);
      groups.get(code).push(message);
    }
    const order = [...groups.keys()].sort((a, b) => (a.startsWith("GATE") ? -1 : 0) - (b.startsWith("GATE") ? -1 : 0) || groups.get(b).length - groups.get(a).length);
    body = h("div", { class: "ledger" }, ...order.map((code) => h("div", { class: `group ${code.startsWith("GATE") ? "gate" : LEGIT.has(code) ? "legit" : ""}` },
      h("div", { class: "group-code" }, `${code} ×${groups.get(code).length}`, h("small", {}, CODES[code] || "")),
      h("ul", {}, ...groups.get(code).map((m) => h("li", {}, m))))));
  }
  return h("section", { class: "block", "aria-labelledby": "t-viol" }, title, body);
}

function renderPending(p, attempts) {
  const title = h("div", { class: "block-title" }, h("h2", { id: "t-pend" }, "Pendências da última tentativa"),
    h("span", { class: "aside" }, "datas calculadas pelo motor"));
  if (!attempts) return h("section", { class: "block", "aria-labelledby": "t-pend" }, title, h("p", { class: "muted" }, "Aparecem depois da primeira tentativa."));
  if (!p.readable) return h("section", { class: "block", "aria-labelledby": "t-pend" }, title, h("p", { class: "muted" }, "A última tentativa não tem um estado legível (JSON inválido ou malformado)."));
  const list = (items, empty, render) => (items.length ? h("ol", {}, ...items.map(render)) : h("p", { class: "muted" }, empty));
  return h("section", { class: "block", "aria-labelledby": "t-pend" }, title,
    h("div", { class: "pending" },
      h("div", {}, h("h3", {}, "Decisões internas abertas"),
        list(p.decisions, "Nenhuma: todas aprovadas ou não aplicáveis.", (d) => h("li", {}, DECISIONS[d.key] || d.key, " ", h("code", {}, d.key), d.state === "populos_internal_decision" ? " · aguardando aprovação" : ` · ${d.state}`, d.value ? ` · proposto: ${fmt(d.value)}` : ""))),
      h("div", {}, h("h3", {}, "Perguntas ao cliente"), list(p.questions, "Nenhuma.", (q) => h("li", {}, q))),
    ),
    ...p.feasibility.map((f) => h("div", { class: "feas" },
      h("div", { class: "feas-head" }, f.event, h("span", { class: `tag v-${f.classification === "fits" ? "emitted" : f.classification === "does_not_fit" ? "failed" : "violations"}` }, FEAS[f.classification] || f.classification)),
      h("div", {}, f.text),
      f.errors.length ? h("div", { class: "muted", style: "margin-top:6px" }, f.errors.join(" · ")) : null)),
  );
}

const fmt = (v) => (typeof v === "object" ? JSON.stringify(v) : String(v));

function renderOutputs(run) {
  const emitted = run.files.some((f) => f.path.endsWith(".docx"));
  const url = (p) => `/api/runs/${run.id}/files/${p.split("/").map(encodeURIComponent).join("/")}`;
  const hasPdf = run.files.some((f) => f.path.endsWith(".pdf"));
  return h("section", { class: "block", "aria-labelledby": "t-out" },
    h("div", { class: "block-title" }, h("h2", { id: "t-out" }, "Saída"),
      emitted ? h("button", { class: "btn", type: "button", disabled: !state.status.pdf, title: state.status.pdf ? "" : "LibreOffice não encontrado no servidor",
        onclick: (e) => renderPdf(e.currentTarget) }, hasPdf ? "Regerar PDF" : "Gerar PDF e páginas") : null),
    h("div", { class: "files" }, ...run.files.map((f) => h("a", { class: `file ${f.path.endsWith(".docx") ? "primary" : ""}`, href: url(f.path) },
      h("span", { class: "mono" }, f.path.replace(/^final\/(render\/)?/, "")), h("small", {}, kb(f.size))))),
    run.pages.length ? h("div", { class: "pages", "aria-label": "Páginas renderizadas pelo LibreOffice" },
      ...run.pages.map((p, i) => h("a", { href: url(p), target: "_blank", rel: "noopener" }, h("img", { src: url(p), alt: `Página ${i + 1}`, loading: "lazy" })))) : null,
    run.pages.length ? h("p", { class: "muted" }, "Render do LibreOffice. A referência para o cliente é o Word.") : null,
  );
}

/* Actions */
async function startAuthor(engine) {
  try {
    state.current = await api(`/api/runs/${state.current.id}/author`, { method: "POST", body: { engine } });
    renderSheet(); schedulePoll(); loadRuns();
    toast("Autor iniciado. As tentativas aparecem aqui conforme o validador responde.");
  } catch (err) { toast(err.message); }
}

async function renderPdf(button) {
  button.disabled = true; button.textContent = "Gerando…";
  try { state.current = await api(`/api/runs/${state.current.id}/pdf`, { method: "POST" }); renderSheet(); }
  catch (err) { toast(err.message); button.disabled = false; button.textContent = "Gerar PDF e páginas"; }
}

function openDialog(id) {
  const dlg = $(id);
  dlg.querySelector("form").reset();
  dlg.querySelectorAll(".form-error").forEach((e) => (e.textContent = ""));
  if (id === "dlg-new") { dlg.querySelector("[name=proposal_date]").value = new Date().toISOString().slice(0, 10); $("drop-list").textContent = ""; }
  dlg.showModal();
}

function bindForm(id, errorId, handler) {
  const form = $(id);
  form.addEventListener("submit", async (event) => {
    if (event.submitter?.value === "cancel") return;
    event.preventDefault();
    const button = event.submitter;
    button.disabled = true;
    try { await handler(form); form.closest("dialog").close(); }
    catch (err) { $(errorId).textContent = err.message; }
    finally { button.disabled = false; }
  });
}

const b64 = (file) => new Promise((resolve, reject) => {
  const reader = new FileReader();
  reader.onload = () => resolve(reader.result.split(",")[1]);
  reader.onerror = reject;
  reader.readAsDataURL(file);
});

bindForm("form-new", "new-error", async (form) => {
  const data = new FormData(form);
  const files = await Promise.all([...form.files.files].map(async (f) => ({ name: f.name, content: await b64(f) })));
  const run = await api("/api/runs", { method: "POST", body: {
    name: data.get("name"), proposal_date: data.get("proposal_date"), data_mode: data.get("data_mode"), text: data.get("text"), files } });
  await loadRuns(); await openRun(run.id);
  toast("Execução criada. Rode um autor ou cole um estado.");
});

bindForm("form-state", "state-error", async (form) => {
  const text = form.state.value;
  try { JSON.parse(text); } catch (err) { throw new Error(`JSON inválido: ${err.message}`); }
  state.current = await api(`/api/runs/${state.current.id}/attempts`, { method: "POST", body: { state: text } });
  state.selected = state.current.attempt_log.length;
  renderSheet(); loadRuns();
  toast(`Tentativa ${state.selected}: ${state.current.verdict.label}`);
});

bindForm("form-complement", "complement-error", async (form) => {
  const run = await api(`/api/runs/${state.current.id}/complement`, { method: "POST", body: { text: form.text.value } });
  await loadRuns(); await openRun(run.id);
  toast("Nova execução criada com o complemento.");
});

const drop = $("drop");
const fileInput = drop.querySelector("input");
const listFiles = () => ($("drop-list").textContent = [...fileInput.files].map((f) => f.name).join(" · "));
fileInput.addEventListener("change", listFiles);
["dragenter", "dragover"].forEach((t) => drop.addEventListener(t, () => drop.classList.add("over")));
["dragleave", "drop"].forEach((t) => drop.addEventListener(t, () => drop.classList.remove("over")));
drop.addEventListener("drop", () => setTimeout(listFiles));

$("new-run").addEventListener("click", () => openDialog("dlg-new"));
const syncLocalFields = () => {
  const form = $("form-keys"), local = form.provider.value === "local", cfg = state.status?.authors?.local || {};
  $("local-fields").hidden = !local;
  if (local) { form.base_url.value ||= cfg.base_url || "https://popai.populos.com.br/v1"; form.model.value ||= cfg.model || "populos"; }
  form.key.placeholder = state.status?.authors?.[form.provider.value]?.configured ? "Deixe vazio para manter a chave atual" : "Clique aqui e aperte Ctrl+V";
};
$("form-keys").provider.addEventListener("change", syncLocalFields);
$("open-keys").addEventListener("click", () => { openDialog("dlg-keys"); $("key-result").textContent = ""; syncLocalFields(); });

$("form-keys").addEventListener("submit", async (event) => {
  if (event.submitter?.value === "cancel") return;
  event.preventDefault();
  const form = event.target, button = event.submitter, result = $("key-result");
  $("keys-error").textContent = ""; result.textContent = "Gravando e testando…"; result.className = "key-result";
  button.disabled = true;
  try {
    const r = await api("/api/keys", { method: "POST", body: { provider: form.provider.value, key: form.key.value, base_url: form.base_url.value, model: form.model.value } });
    form.key.value = "";
    state.status.authors = r.authors; renderEngine();
    if (state.current) renderSheet();
    result.textContent = `${r.check.ok ? "✓" : "✗"} Gravada (${r.length} caracteres): ${r.check.message}.`;
    result.className = `key-result ${r.check.ok ? "ok" : "bad"}`;
  } catch (err) { result.textContent = ""; $("keys-error").textContent = err.message; }
  finally { button.disabled = false; }
});

(async function init() {
  try {
    state.status = await api("/api/status");
    renderEngine();
    await loadRuns();
    const id = location.hash.slice(1);
    if (id && state.runs.some((r) => r.id === id)) await openRun(id);
  } catch (err) { toast(`Servidor indisponível: ${err.message}`); }
})();
