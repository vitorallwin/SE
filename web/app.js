const state = {
  health: null,
  proposals: [],
  activeTab: "overview",
  wizardStep: 1,
  draft: { products: ["app_api_protector", "edge_dns"] },
};

const PRODUCTS = {
  edge_dns: ["Edge DNS", "DNS autoritativo global e resiliente"],
  app_api_protector: ["App & API Protector", "WAF, APIs e proteção DDoS na borda"],
  malware_protection: ["Malware Protection", "Inspeção de uploads e políticas de arquivo"],
  alb: ["Application Load Balancer", "Balanceamento global e failover"],
  ip_accelerator: ["IP Accelerator", "Aceleração e disponibilidade TCP/UDP"],
  bot_manager: ["Bot Manager Premier", "Detecção e resposta a automação maliciosa"],
};

const $ = (selector, root = document) => root.querySelector(selector);
const esc = (value = "") => String(value).replace(/[&<>'"]/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;","'":"&#39;",'"':"&quot;"}[char]));
const fmtDate = value => value ? new Intl.DateTimeFormat("pt-BR", {day:"2-digit", month:"short", year:"numeric"}).format(new Date(value)) : "Sem data";
const statusLabel = value => ({draft:"Rascunho", review:"Em revisão", approved:"Aprovada", blocked:"Bloqueada"}[value] || value);
const initials = name => name.split(/\s+/).slice(0,2).map(word => word[0]).join("").toUpperCase();

async function api(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    headers: {"Content-Type":"application/json", ...(options.headers || {})},
  });
  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new Error(data.error || `Erro HTTP ${response.status}`);
  }
  if (response.status === 204) return null;
  return response.json();
}

function toast(message, error = false) {
  const el = $("#toast");
  el.textContent = message;
  el.className = `toast show${error ? " error" : ""}`;
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => el.className = "toast", 3200);
}

function shell(content, active = "proposals", crumb = "Propostas") {
  const ai = state.health?.ai || {};
  return `
    <div class="shell">
      <aside class="sidebar">
        <a class="brand" href="#/"><div class="brand-mark">SE</div><div><strong>Sales Engineer</strong><span>Proposal Studio</span></div></a>
        <div class="nav-label">WORKSPACE</div>
        <nav class="nav" aria-label="Navegação principal">
          <a class="${active === "proposals" ? "active" : ""}" href="#/"><span class="nav-icon">▦</span><span>Propostas</span></a>
          <a class="${active === "new" ? "active" : ""}" href="#/new"><span class="nav-icon">＋</span><span>Nova proposta</span></a>
          <a class="${active === "knowledge" ? "active" : ""}" href="#/knowledge"><span class="nav-icon">◇</span><span>Base técnica</span></a>
          <a class="${active === "settings" ? "active" : ""}" href="#/settings"><span class="nav-icon">⚙</span><span>Configurações</span></a>
        </nav>
        <div class="side-bottom">
          <div class="engine">
            <div class="engine-top"><strong>${ai.configured ? esc(ai.model) : "Motor de demonstração"}</strong><span class="dot ${ai.configured ? "" : "off"}"></span></div>
            <p>${ai.configured ? "Gemini conectado por variável de ambiente." : "Fluxo completo sem chamadas externas."}</p>
          </div>
        </div>
      </aside>
      <main class="main" id="main">
        <header class="topbar"><div class="breadcrumb">Workspace / <strong>${esc(crumb)}</strong></div><div class="top-actions"><a class="btn btn-small" href="#/settings">${ai.configured ? "Gemini ativo" : "Modo demo"}</a><a class="btn btn-primary btn-small" href="#/new">＋ Nova proposta</a></div></header>
        <div class="content">${content}</div>
      </main>
    </div>`;
}

function loading() {
  $("#app").innerHTML = shell(`<div class="loading"><div><div class="spinner"></div>Carregando workspace…</div></div>`);
}

async function loadCommon() {
  const [health, proposals] = await Promise.all([api("/api/health"), api("/api/proposals")]);
  state.health = health;
  state.proposals = proposals.items;
}

function dashboard() {
  const items = state.proposals;
  const review = items.filter(item => item.status === "review").length;
  const approved = items.filter(item => item.status === "approved").length;
  const avg = items.filter(item => item.quality_score != null).reduce((sum,item) => sum + item.quality_score, 0) / Math.max(1, items.filter(item => item.quality_score != null).length);
  const content = `
    <div class="page-head"><div><p class="eyebrow">CENTRAL DE PROPOSTAS</p><h1>Propostas técnicas</h1><p class="subtitle">Da descoberta ao documento final, com evidência e aprovação em cada etapa.</p></div><a class="btn btn-primary" href="#/new">＋ Criar proposta</a></div>
    <section class="stats" aria-label="Indicadores">
      ${stat("Propostas ativas", items.filter(i => i.status !== "approved").length, "em construção ou revisão", "↗")}
      ${stat("Aguardando revisão", review, "portão humano", "⌁")}
      ${stat("Aprovadas", approved, "histórico local", "✓")}
      ${stat("Qualidade média", avg ? Math.round(avg) : "—", "score técnico e comercial", "◇")}
    </section>
    <section class="panel">
      <div class="panel-head"><div><h2>Workspace</h2><p>${items.length} proposta${items.length === 1 ? "" : "s"} no ambiente local</p></div><div class="toolbar"><label class="search"><span>⌕</span><input id="search" aria-label="Buscar propostas" placeholder="Buscar cliente ou oportunidade"></label><select id="status-filter" class="select" aria-label="Filtrar status"><option value="">Todos os status</option><option value="draft">Rascunho</option><option value="review">Em revisão</option><option value="approved">Aprovada</option><option value="blocked">Bloqueada</option></select></div></div>
      <div id="proposal-list" class="proposal-list">${proposalRows(items)}</div>
    </section>`;
  $("#app").innerHTML = shell(content);
  $("#search").addEventListener("input", filterRows);
  $("#status-filter").addEventListener("change", filterRows);
}

function stat(label, value, note, icon) {
  return `<article class="stat"><div class="stat-top"><span>${esc(label)}</span><span class="stat-icon">${icon}</span></div><div class="stat-value">${esc(value)}</div><div class="stat-note">${esc(note)}</div></article>`;
}

function proposalRows(items) {
  if (!items.length) return `<div class="empty"><strong>Nenhuma proposta encontrada</strong>Crie a primeira proposta para iniciar o pipeline.</div>`;
  return items.map(item => `
    <a class="proposal-row" href="#/proposal/${esc(item.id)}">
      <div class="client-cell"><div class="avatar">${esc(initials(item.client_name))}</div><div><strong>${esc(item.client_name)}</strong><small>${esc(item.code)} · ${esc(item.opportunity)}</small></div></div>
      <div class="product-tags">${item.products.slice(0,3).map(key => `<span class="mini-tag">${esc(PRODUCTS[key]?.[0] || key)}</span>`).join("")}</div>
      <div class="meta-cell"><span class="badge ${esc(item.status)}">${esc(statusLabel(item.status))}</span><small>Atualizada ${fmtDate(item.updated_at)}</small></div>
      <div class="score">${item.quality_score ?? "—"}<small>/100</small><div class="progress-mini"><i style="width:${Number(item.progress || 0)}%"></i></div></div>
      <button class="kebab" aria-label="Abrir proposta">›</button>
    </a>`).join("");
}

function filterRows() {
  const query = $("#search").value.trim().toLowerCase();
  const status = $("#status-filter").value;
  const items = state.proposals.filter(item => (!query || `${item.client_name} ${item.opportunity} ${item.code}`.toLowerCase().includes(query)) && (!status || item.status === status));
  $("#proposal-list").innerHTML = proposalRows(items);
}

function wizard() {
  const step = state.wizardStep;
  const content = `<div class="wizard"><div class="page-head"><div><p class="eyebrow">NOVA PROPOSTA</p><h1>Preparar proposta Akamai</h1><p class="subtitle">Organize os insumos antes de executar o pipeline.</p></div></div><div class="wizard-grid">${wizardNav(step)}<section class="form-card" id="wizard-card">${wizardBody(step)}</section></div></div>`;
  $("#app").innerHTML = shell(content, "new", "Nova proposta");
  bindWizard();
}

function wizardNav(step) {
  return `<aside class="wizard-nav">${[[1,"Cliente"],[2,"Solução"],[3,"Contexto"],[4,"Revisão"]].map(([n,label]) => `<div class="wizard-step ${step === n ? "active" : ""}"><i>${n}</i><span>${label}</span></div>`).join("")}</aside>`;
}

function field(name, label, value = "", attrs = "", full = false) {
  return `<div class="field ${full ? "full" : ""}"><label for="${name}">${label}</label><input id="${name}" name="${name}" value="${esc(value)}" ${attrs}></div>`;
}

function textarea(name, label, value = "", help = "") {
  return `<div class="field full"><label for="${name}">${label}</label><textarea id="${name}" name="${name}">${esc(value)}</textarea>${help ? `<small>${esc(help)}</small>` : ""}</div>`;
}

function wizardBody(step) {
  const d = state.draft;
  if (step === 1) return `<h2>Identificação da oportunidade</h2><p>Dados usados na capa, no controle interno e no histórico da proposta.</p><form id="wizard-form"><div class="fields">${field("client_name","Cliente",d.client_name || "","required placeholder=\"Razão social ou nome de referência\"")}${field("opportunity","Oportunidade",d.opportunity || "","required placeholder=\"Ex.: Proteção de aplicações públicas\"")}${field("owner","Responsável",d.owner || "Sales Engineering")}${field("due_date","Data desejada",d.due_date || "","type=\"date\"")}</div>${footer(1)}</form>`;
  if (step === 2) return `<h2>Soluções Akamai</h2><p>Selecione os componentes que devem aparecer na arquitetura e no documento.</p><form id="wizard-form"><div class="product-grid">${Object.entries(PRODUCTS).map(([key,[name,desc]]) => `<label class="product-option"><input type="checkbox" name="products" value="${key}" ${d.products?.includes(key) ? "checked" : ""}><span class="product-box"><strong>${esc(name)}</strong><span>${esc(desc)}</span></span></label>`).join("")}</div>${footer(2)}</form>`;
  if (step === 3) return `<h2>Contexto técnico</h2><p>Quanto melhor o contexto, maior a confiança da descoberta e da matriz de cobertura.</p><form id="wizard-form"><div class="fields">${textarea("transcript","Ata ou transcrição",d.transcript || "","Cole a transcrição completa ou um resumo fiel da reunião.")}${textarea("requirements","Requisitos conhecidos",d.requirements || "","Um requisito por linha ou separado por ponto e vírgula.")}${textarea("scope","Escopo esperado",d.scope || "")}${textarea("assumptions","Premissas e restrições",d.assumptions || "")}</div>${footer(3)}</form>`;
  return `<h2>Revisar insumos</h2><p>Confira o resumo. O pipeline poderá ser executado em seguida.</p><div class="review-summary"><div class="review-row"><span>Cliente</span><strong>${esc(d.client_name)}</strong></div><div class="review-row"><span>Oportunidade</span><strong>${esc(d.opportunity)}</strong></div><div class="review-row"><span>Soluções</span><strong>${(d.products || []).map(key => esc(PRODUCTS[key]?.[0] || key)).join(", ")}</strong></div><div class="review-row"><span>Contexto</span><strong>${d.transcript ? `${d.transcript.length} caracteres de ata` : "Sem ata — será sinalizado como pergunta aberta"}</strong></div><div class="review-row"><span>Geração</span><strong>${state.health?.ai?.configured ? `Gemini ${esc(state.health.ai.model)}` : "Motor determinístico de demonstração"}</strong></div></div><div class="form-footer"><button class="btn" id="prev" type="button">← Voltar</button><button class="btn btn-primary" id="create" type="button">Criar e abrir proposta →</button></div>`;
}

function footer(step) {
  return `<div class="form-footer">${step > 1 ? `<button class="btn" id="prev" type="button">← Voltar</button>` : `<a class="btn" href="#/">Cancelar</a>`}<button class="btn btn-primary" type="submit">Continuar →</button></div>`;
}

function bindWizard() {
  const form = $("#wizard-form");
  if (form) form.addEventListener("submit", event => {
    event.preventDefault();
    saveWizard(form);
    if (state.wizardStep === 2 && !state.draft.products.length) return toast("Selecione ao menos uma solução Akamai.", true);
    state.wizardStep += 1;
    wizard();
  });
  $("#prev")?.addEventListener("click", () => { if (form) saveWizard(form); state.wizardStep -= 1; wizard(); });
  $("#create")?.addEventListener("click", createProposal);
}

function saveWizard(form) {
  const data = new FormData(form);
  if (state.wizardStep === 2) state.draft.products = data.getAll("products");
  else for (const [key,value] of data.entries()) state.draft[key] = value;
}

async function createProposal() {
  const button = $("#create");
  button.disabled = true; button.textContent = "Criando…";
  try {
    const proposal = await api("/api/proposals", {method:"POST", body:JSON.stringify(state.draft)});
    state.wizardStep = 1; state.draft = {products:["app_api_protector","edge_dns"]};
    location.hash = `#/proposal/${proposal.id}`;
    toast("Proposta criada.");
  } catch (error) { toast(error.message, true); button.disabled = false; button.textContent = "Criar e abrir proposta →"; }
}

async function detail(id) {
  loading();
  try {
    const proposal = await api(`/api/proposals/${id}`);
    renderDetail(proposal);
  } catch (error) { toast(error.message, true); location.hash = "#/"; }
}

function renderDetail(p) {
  const internalPending = Object.entries(p.governance || {}).filter(([,d]) => d?.state === "populos_internal_decision" && !d?.value);
  const content = `
    <section class="detail-head">
      <div class="detail-title"><div><p class="eyebrow">${esc(p.code)}</p><h1>${esc(p.client_name)}</h1><p class="subtitle">${esc(p.opportunity)}</p><div class="meta-line"><span>Responsável: ${esc(p.owner)}</span><span>Criada ${fmtDate(p.created_at)}</span><span class="badge ${esc(p.status)}">${esc(statusLabel(p.status))}</span></div></div><div class="detail-actions"><button class="btn" id="run">▶ Executar pipeline</button><button class="btn" id="download" ${internalPending.length ? "disabled" : ""}>⇩ Gerar DOCX</button>${p.status !== "approved" ? `<button class="btn btn-primary" id="approve">Aprovar</button>` : ""}</div></div>
      <div class="pipeline">${p.stages.map((s,i) => `<div class="stage ${esc(s.status)}"><div class="stage-dot">${s.status === "done" ? "✓" : i+1}</div><span>${esc(s.label)}</span></div>`).join("")}</div>
    </section>
    <div class="tabs" role="tablist">${[["overview","Visão geral"],["discovery","Discovery"],["architecture","Arquitetura"],["traceability","Rastreabilidade"],["document","Documento"]].map(([key,label]) => `<button class="tab ${state.activeTab === key ? "active" : ""}" data-tab="${key}">${label}</button>`).join("")}</div>
    <div id="tab-content">${detailTab(p)}</div>`;
  $("#app").innerHTML = shell(content, "proposals", p.client_name);
  document.querySelectorAll(".tab").forEach(btn => btn.addEventListener("click", () => { state.activeTab = btn.dataset.tab; renderDetail(p); }));
  $("#run")?.addEventListener("click", () => runPipeline(p.id));
  $("#download")?.addEventListener("click", () => downloadDocx(p.id));
  $("#approve")?.addEventListener("click", () => approve(p.id));
  $("#set-warranty")?.addEventListener("click", () => setWarranty(p));
  $("#set-supply")?.addEventListener("click", () => setSupply(p));
}

function detailTab(p) {
  if (state.activeTab === "discovery") return discoveryTab(p);
  if (state.activeTab === "architecture") return architectureTab(p);
  if (state.activeTab === "traceability") return traceTab(p);
  if (state.activeTab === "document") return documentTab(p);
  return overviewTab(p);
}

function overviewTab(p) {
  const events = [...(p.events || [])].reverse().slice(0,8);
  return `<div class="detail-grid"><div class="stack"><section class="card"><div class="card-head"><h2>Saúde da proposta</h2><span class="badge ${esc(p.status)}">${esc(statusLabel(p.status))}</span></div><div class="metric-grid"><div class="metric"><b>${p.progress || 0}%</b><span>pipeline concluído</span></div><div class="metric"><b>${p.quality_score ?? "—"}</b><span>qualidade / 100</span></div><div class="metric"><b>${p.traceability?.length || 0}</b><span>requisitos rastreados</span></div></div></section><section class="card"><div class="card-head"><h2>Resumo da solução</h2></div><p>${esc(p.architecture?.summary || "Execute o pipeline para gerar a recomendação técnica.")}</p><div class="product-tags">${p.products.map(key => `<span class="mini-tag">${esc(PRODUCTS[key]?.[0] || key)}</span>`).join("")}</div></section><section class="card"><div class="card-head"><h2>QA técnico e comercial</h2></div>${qaItems([...(p.qa?.technical || []), ...(p.qa?.commercial || [])])}</section></div><aside class="stack"><section class="card"><div class="card-head"><h3>Perguntas abertas</h3><span class="mini-tag">${p.open_questions?.length || 0}</span></div>${p.open_questions?.length ? p.open_questions.map(q => `<div class="question">${esc(q)}</div>`).join("<div style=\"height:8px\"></div>") : `<p>Nenhuma pendência registrada.</p>`}</section><section class="card"><div class="card-head"><h3>Atividade</h3></div>${events.map(e => `<div class="event">${esc(e.message)}<time>${fmtDate(e.at)}</time></div>`).join("")}</section></aside></div>`;
}

function qaItems(items) {
  if (!items.length) return `<p>O QA será preenchido durante a execução.</p>`;
  return items.map(i => `<div class="qa-item"><span class="severity ${esc(i.severity)}">${i.severity === "info" ? "✓" : "!"}</span><span>${esc(i.message)}</span></div>`).join("");
}

function discoveryTab(p) {
  const d = p.discovery || {};
  return `<div class="detail-grid"><div class="stack"><section class="card"><div class="card-head"><h2>Requisitos identificados</h2><span class="mini-tag">confiança ${Math.round((d.confidence || 0)*100)}%</span></div>${d.requirements?.length ? `<ul>${d.requirements.map(r => `<li><strong>${esc(r.id)}</strong> — ${esc(r.text)}</li>`).join("")}</ul>` : `<p>Execute o pipeline para estruturar requisitos.</p>`}</section><section class="card"><div class="card-head"><h2>Objetivos de negócio</h2></div>${d.business_goals?.length ? `<ul>${d.business_goals.map(esc).map(x => `<li>${x}</li>`).join("")}</ul>` : `<p>Sem objetivos estruturados.</p>`}</section></div><aside class="card"><div class="card-head"><h3>Restrições</h3></div>${d.constraints?.length ? `<ul>${d.constraints.map(esc).map(x => `<li>${x}</li>`).join("")}</ul>` : `<p>Nenhuma restrição estruturada.</p>`}</aside></div>`;
}

function architectureTab(p) {
  const a = p.architecture || {};
  return `<div class="stack"><section class="card"><div class="card-head"><h2>Arquitetura recomendada</h2></div><p>${esc(a.summary || "Execute o pipeline para gerar a arquitetura.")}</p></section><section class="card"><div class="card-head"><h2>Componentes</h2></div><div class="product-grid">${(a.products || []).map(product => `<div class="product-box"><strong>${esc(product.name)}</strong><span>${esc(product.summary)}</span><div class="product-tags" style="margin-top:10px">${product.capabilities.map(c => `<span class="mini-tag">${esc(c)}</span>`).join("")}</div></div>`).join("") || "<p>Sem componentes calculados.</p>"}</div></section><section class="card"><div class="card-head"><h2>Ondas de implementação</h2></div>${(a.implementation_waves || []).map((wave,i) => `<div class="review-row"><span>Onda ${i+1}</span><strong>${esc(wave.name)} · ${esc(wave.duration)}</strong></div>`).join("")}</section></div>`;
}

function traceTab(p) {
  const rows = p.traceability || [];
  return `<section class="card"><div class="card-head"><div><h2>Matriz de rastreabilidade</h2><p>Requisito → capacidade → evidência → cobertura</p></div><span class="mini-tag">${rows.length} linhas</span></div><div class="trace-wrap"><table><thead><tr><th>ID</th><th>Requisito</th><th>Solução</th><th>Evidência</th><th>Status</th></tr></thead><tbody>${rows.map(row => `<tr><td><strong>${esc(row.requirement_id)}</strong></td><td>${esc(row.requirement)}</td><td>${esc(row.solution)}</td><td>${esc(row.evidence)}</td><td class="coverage">✓ Coberto</td></tr>`).join("") || `<tr><td colspan="5">Execute o pipeline para construir a matriz.</td></tr>`}</tbody></table></div></section>`;
}

function documentTab(p) {
  const governance = p.governance || {};
  const warranty = governance.warranty || {};
  const supply = governance.license_supply || {};
  const blocked = [warranty, supply].some(x => x.state === "populos_internal_decision" && !x.value);
  return `<div class="detail-grid"><div class="stack"><section class="card"><div class="card-head"><h2>Prévia das seções</h2><span class="mini-tag">${p.sections?.length || 0} seções</span></div>${p.sections?.length ? p.sections.map(section => `<div style="padding:14px 0;border-bottom:1px solid var(--line-soft)"><h3>${esc(section.title)}</h3>${section.paragraphs.map(x => `<p>${esc(x)}</p>`).join("")}</div>`).join("") : `<p>A redação será criada durante o pipeline.</p>`}</section></div><aside class="stack"><section class="card"><div class="card-head"><h3>Decisões internas POPULOS</h3><span class="badge ${blocked ? "blocked" : "approved"}">${blocked ? "Emissão bloqueada" : "Resolvidas"}</span></div><div class="review-row"><span>Garantia</span><strong>${esc(warranty.value || "Decisão necessária")}</strong></div><button class="btn" style="width:100%;margin-bottom:10px" id="set-warranty">Definir garantia</button><div class="review-row"><span>Licenças Akamai</span><strong>${esc(supply.value || "Decisão necessária")}</strong></div><button class="btn" style="width:100%" id="set-supply">Definir fornecimento</button></section><section class="card"><div class="card-head"><h3>Documento Akamai</h3></div><p>O DOCX preserva a identidade visual e só é emitido depois dos gates internos.</p><button class="btn btn-primary" style="width:100%" id="download-side" ${blocked ? "disabled" : ""}>⇩ Gerar e baixar DOCX</button></section><section class="card"><div class="card-head"><h3>Portão de aprovação</h3></div><p>${p.status === "approved" ? `Aprovada por ${esc(p.approved_by || "responsável")}.` : "Revise o QA e as pendências antes da aprovação final."}</p></section></aside></div>`;
}

async function saveGovernance(p, governance) {
  try {
    const updated = await api(`/api/proposals/${p.id}`, {method:"PATCH", body:JSON.stringify({governance})});
    renderDetail(updated); toast("Decisão interna registrada.");
  } catch (error) { toast(error.message, true); }
}

function setWarranty(p) {
  const days = window.prompt("Prazo de garantia aprovado pela POPULOS, em dias corridos:");
  if (!days || !/^\d+$/.test(days.trim())) return;
  const governance = structuredClone(p.governance || {});
  governance.warranty = {state:"commitment", value:`A POPULOS corrigirá defeitos diretamente atribuíveis aos serviços executados por ${days.trim()} dias corridos após o aceite final.`, source:"aprovação interna da oportunidade"};
  saveGovernance(p, governance);
}

function setSupply(p) {
  const mode = window.prompt("Digite 1 para revenda POPULOS ou 2 para aquisição direta pelo CONTRATANTE:");
  if (!/[12]/.test(mode || "")) return;
  const value = mode === "1" ? "As licenças Akamai serão fornecidas pela POPULOS por meio de revenda autorizada." : "As licenças Akamai serão adquiridas diretamente pelo CONTRATANTE e deverão estar ativas antes da configuração.";
  const governance = structuredClone(p.governance || {});
  governance.license_supply = {state:"commitment", value, source:"aprovação interna da oportunidade"};
  saveGovernance(p, governance);
}

async function runPipeline(id) {
  const btn = $("#run"); btn.disabled = true; btn.textContent = "Executando agentes…";
  try { const proposal = await api(`/api/proposals/${id}/run`, {method:"POST", body:"{}"}); renderDetail(proposal); toast("Pipeline concluído."); }
  catch (error) { toast(error.message, true); btn.disabled = false; btn.textContent = "▶ Executar pipeline"; }
}

function downloadDocx(id) {
  toast("Gerando documento a partir do template Akamai…");
  window.location.href = `/api/proposals/${id}/docx`;
  setTimeout(() => detail(id), 1200);
}

async function approve(id) {
  const approver = window.prompt("Nome de quem aprova esta proposta:");
  if (!approver) return;
  try { const p = await api(`/api/proposals/${id}/approve`, {method:"POST", body:JSON.stringify({approver})}); renderDetail(p); toast("Proposta aprovada."); }
  catch (error) { toast(error.message, true); }
}

function knowledge() {
  const cards = Object.entries(PRODUCTS).map(([key,[name,desc]]) => `<article class="card"><div class="card-head"><h3>${esc(name)}</h3><span class="mini-tag">Akamai</span></div><p>${esc(desc)}</p><div class="meta-line"><span>Fonte: template fornecido</span><span>ID: ${esc(key)}</span></div></article>`).join("");
  $("#app").innerHTML = shell(`<div class="page-head"><div><p class="eyebrow">CONHECIMENTO</p><h1>Catálogo técnico</h1><p class="subtitle">Capacidades usadas pelo arquiteto e pela matriz de rastreabilidade.</p></div></div><div class="product-grid">${cards}</div>`, "knowledge", "Base técnica");
}

function settings() {
  const ai = state.health?.ai || {};
  $("#app").innerHTML = shell(`<div class="page-head"><div><p class="eyebrow">CONFIGURAÇÃO</p><h1>Ambiente local</h1><p class="subtitle">Segredos ficam somente no ambiente do processo.</p></div></div><div class="detail-grid"><section class="card"><div class="card-head"><h2>Motor de IA</h2><span class="badge ${ai.configured ? "approved" : "draft"}">${ai.configured ? "Configurado" : "Modo demo"}</span></div><div class="review-row"><span>Modelo</span><strong>${esc(ai.model || "—")}</strong></div><div class="review-row"><span>Origem da chave</span><strong>${ai.configured ? "Variável de ambiente GEMINI_API_KEY" : "Não configurada"}</strong></div><p>A aplicação não recebe, não salva e não devolve a chave pela interface. Reinicie o servidor após alterar o ambiente.</p></section><aside class="card"><div class="card-head"><h3>Execução</h3></div><p>Local · JSON · sem autenticação</p><p>Para produção, habilite Supabase, autenticação, fila e políticas de acesso.</p></aside></div>`, "settings", "Configurações");
}

async function route() {
  const hash = location.hash || "#/";
  if (!state.health) {
    loading();
    try { await loadCommon(); } catch (error) { toast(error.message, true); return; }
  }
  if (hash === "#/" || hash === "") return dashboard();
  if (hash === "#/new") return wizard();
  if (hash === "#/knowledge") return knowledge();
  if (hash === "#/settings") return settings();
  const match = hash.match(/^#\/proposal\/([a-zA-Z0-9-]+)/);
  if (match) return detail(match[1]);
  location.hash = "#/";
}

document.addEventListener("click", event => {
  if (event.target?.id === "download-side") {
    const match = location.hash.match(/^#\/proposal\/([a-zA-Z0-9-]+)/);
    if (match) downloadDocx(match[1]);
  }
});
window.addEventListener("hashchange", route);
route();
