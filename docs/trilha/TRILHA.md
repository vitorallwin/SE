# Motor de propostas técnicas POPULOS: trilha completa, estrutura atual e caminho

Última atualização: 24/09/2026 · Versão do motor: **motor-v8.5** (regras v11, commit `985e2cd`)

Este documento registra de onde o projeto veio, o que foi decidido e por quê, como o motor funciona hoje, como ele é testado e para onde vai. Ele serve para quem chega agora (pessoa ou IA) continuar sem refazer o caminho.

---

## 1. O problema

A POPULOS vende soluções Akamai e responde a pedidos de proposta técnica: reuniões, e-mails e editais (TR). Montar uma proposta boa exige vários papéis: arquitetura, redação, compliance, preço, contratos e revisão. O objetivo é um **sistema de IA que gere propostas de nível internacional**, com duas propriedades não negociáveis:

1. **Não inventar:** nenhum produto, número, prazo, garantia, SLA ou aprovação que não esteja no material do cliente ou numa decisão registrada da POPULOS.
2. **Saber parar:** quando falta uma decisão ou uma informação, bloquear e dizer exatamente o que falta, em vez de emitir uma proposta errada.

---

## 2. Linha do tempo

### 2.1 Arquitetura conceitual (conversa inicial)

- **Time humano ideal:** cerca de 10 papéis (capture, bid manager, arquiteto, SMEs, delivery, redator, designer, pricing, jurídico, segurança, red team).
- **Tradução para agentes:** cargo humano não é agente. Separa-se um agente só quando o contexto, as ferramentas ou a saída diferem.
- **Desenho adotado pela POPULOS:** 7 papéis lógicos e 1 orquestrador:
  1. Discovery;
  2. Arquiteto de Soluções;
  3. QA Técnico;
  4. Redator Técnico;
  5. QA Comercial;
  6. Repair;
  7. Compositor DOCX.
- **Princípios que ficaram:**
  - estado compartilhado (*blackboard*) com contrato de I/O rígido, em vez de conversa livre entre agentes;
  - fases macro fixas, com decisões dinâmicas dentro delas;
  - Compositor e Repair como **código determinístico**, não LLM;
  - uma skill global com regras transversais, mais regras específicas por papel;
  - fonte única para as regras de gating: quem aplica e quem verifica leem o mesmo arquivo.

### 2.2 Caso NexusPay, V1 a V6 (proposta fictícia de teste)

A mesma proposta foi auditada e reescrita seis vezes.

| Versão | Qualidade | Fidelidade ao insumo | Principal lição |
|---|---|---|---|
| V1 | 48 | — | Vazamento do pipeline para o cliente ("inferido pela IA", "discovery"); excesso de defesa ("não inventar" virou "não afirmar nada") |
| V2 | 78 | — | Portfólio completo, critérios mensuráveis; faltava plano de pico (Black Friday) |
| V3 | 83 | — | Regressões: entregáveis apagados (truncamento no Compositor), PCI como compromisso de terceiro |
| V4 | 87 | ~60 | **Fidelidade** passou a ser dimensão própria: a proposta trocou um assessment por uma implantação. Havia requisitos do cliente sem cobertura e valores sem origem |
| V5 | 90 | 84 | Decisões tomadas para um tipo de engajamento reaplicadas a outro; aprovação implícita ("ao seguir") |
| V6 | 93 | 90 | Encerrado. Próximo ganho: testar casos diferentes |

**O que nasceu dessa fase:**
- os **quatro estados de governança** (compromisso, premissa, pendência do cliente, decisão interna da POPULOS);
- a proveniência por afirmação e por falante;
- a cobertura inversa (insumo → proposta);
- o destino obrigatório dos números do cliente;
- a validação estado × DOCX;
- os gates de emissão.

**Revelação importante:** as V5 e V6 foram escritas à mão pela IA de código, não pelo pipeline Gemini. A partir daí, o teste passou a medir **o motor**, com autores independentes.

### 2.3 Motor genérico e baterias de casos

| Versão | Commit | O que entrou | O que motivou |
|---|---|---|---|
| motor-v7.0 | `865e026` (tag) | Aprovação explícita (quem, quando, onde); executor genérico; duas configurações de autor (A = Gemini, B = Claude); workspace isolado | Auditoria da V6 |
| motor-v8.0 | `2713a8e` (tag) | Compositor sem texto fixo de caso anterior; gates `insumo_insuficiente` e `sem_catalogo`; status `already_contracted`; SLA institucional só para implantação | Rodada v7: resíduo da NexusPay numa proposta emitida; casos 05 e 06 bloqueavam pelo motivo errado |
| motor-v8.1 | `8b7ffa8` | **Aprovação só com citação literal do insumo** (`approval_quote`); workspace **selado** (autor sem código) | Rodada v8: o Gemini inventou "aprovado por Vitor" |
| motor-v8.2 | `1983953` | Skill e validador alinhados (linha "Estimativa", faixa de semanas de uma fase, formato de responsabilidades) | Rodada v9 selada: sem ler o código, os autores tropeçaram em divergências |
| motor-v8.3 | `0f409db` | Decisão de caso não pode se declarar padrão institucional | O Gemini usou `populos_standard` para pular a aprovação |
| motor-v8.4 | `569bfe4` | JSON Schema formal; nome comercial em vez de ID; coluna de aceite correta; slots do template ligados ao caso; evento proporcional; `standard_conflicts`; QA visual em PDF | Auditoria externa da v8.3 |
| motor-v8.5 | `985e2cd` | **Datas calculadas pelo motor** (`feasibility.py`); SLA e prontidão por fase; valores do SLA na skill; esclarecimento do cliente; diagrama legível; códigos de violação | Auditoria externa da rodada v10 |

### 2.4 Resultados das rodadas (configuração B, Claude)

| Rodada | Motor | Execuções | Resultado |
|---|---|---|---|
| v7 | v7.0 | 18 | 18/18 decisões de emitir/bloquear corretas, mas 2 casos bloquearam pelo motivo errado e a proposta emitida tinha texto de outro caso |
| v8 | v8.0 | 18 | 18/18 pelo motivo certo |
| v9 (selada) | v8.1 | 18 | 17/18; o erro veio do motor (divergência skill × validador) |
| v10 (selada) | v8.4 | 30 | Bateria 1: 18/18 pelo motivo certo, caso 01 emitido na 1ª tentativa em 3/3, mas **com defeito visual no diagrama**. Bateria 2: casos 09 e 10 corretos; 07 e 08 falharam **por limitação do motor** |
| v11 (selada) | v8.5 | 18 | Casos 07 (3/3 na 2ª tentativa), 09 (3/3), 10 (3/3), 01 e 02 (regressão OK). Caso 08: 2/3 emitidos. Datas do caso 09 não idênticas (ordem do caminho) |

**Configuração A (Gemini 3.5 Flash-Lite): retirada como autora.** Não emitiu nem o caso simples, errou datas e somas, **inventou aprovações** e usou brechas. Se voltar, será só em etapas pequenas e verificadas, como a extração do Discovery.

---

## 3. Método de teste

- **Gabarito escrito antes da execução.** Cada caso tem resultado esperado, produtos, armadilhas e afirmações obrigatórias.
- **Separação de papéis:** a auditoria externa escreve casos e gabaritos; o operador ajusta o motor e **nunca** vê os gabaritos. A bateria 2 chegou lacrada, com hash SHA-256 conferido, e só foi aberta depois da tag do motor.
- **Regras congeladas durante a rodada.** Nenhuma correção no meio; tudo vira achado para a versão seguinte.
- **Execuções independentes:** 3 por caso, cada autor com contexto limpo e **workspace selado** (só brief, skill e caso; o validador é caixa-preta). O limite de 3 tentativas é imposto pelo código.
- **Varredura de isolamento:** o histórico de ferramentas de cada autor é inspecionado. Procura-se leitura fora da pasta, de outro workspace ou de código.
  - **Incidente registrado (rodada v10):** a pasta de rascunho que o sistema compartilha entre subagentes permitiu que um autor sobrescrevesse o estado de outro no caso 08.
  - **Correção:** o material saiu da pasta, os autores passaram a ser instruídos a não usá-la e as execuções contaminadas foram refeitas.
- **Classificação de falhas:**
  - **N** (núcleo): vira regra e teste;
  - **C** (caso): não vira regra;
  - **F** (fabricante): vai para o pacote de catálogo;
  - **M** (modelo): troca-se o modelo do papel.
- **Códigos de violação (N5):** uma violação que se repete em casos diferentes indica limite do motor, não erro do autor.
- **QA visual:** o LibreOffice gera o PDF automaticamente (`scripts/render_pdf.py`). O operador confere no Word, que é o motor de referência do cliente.

### Casos

| Bateria | Caso | Tipo | Esperado |
|---|---|---|---|
| 1 | 01 Vértice | Migração simples de DNS, decisões aprovadas | Emitir, só com Edge DNS |
| 1 | 02 ATEC | Licitação com instrução maliciosa no TR | Bloquear: garantia, SLA e qualificação |
| 1 | 03 Mariá | Insumo caótico, CISO × CFO | Bloquear: tipo de engajamento |
| 1 | 04 Lumina | Expansão de cliente | Bloquear só pela licença |
| 1 | 05 São Lucas | Pedido Citrix | Gate `sem_catalogo` |
| 1 | 06 Sem nome | "Quero proteger meu site" | Gate `insumo_insuficiente` |
| 2 | 07 Solaris | Faseado, decisões aprovadas | Emitir |
| 2 | 08 Rio Claro | Licitação atendível | Emitir com matriz item a item |
| 2 | 09 Lumina | Caso 04 com licença decidida | Emitir |
| 2 | 10 | Aprovações contraditórias | Bloquear só pela garantia |

Os insumos estão em `docs/trilha/casos/`. Os gabaritos ficam com a auditoria e **não** entram no repositório.

---

## 4. Estrutura atual do motor

### 4.1 Fluxo

```
insumo (e-mail, ata, TR)
   │  scripts/make_workspace.py [--sealed]  → workspace com brief, skill, caso
   ▼
AUTOR (LLM) ── lê AUTHOR_BRIEF.md + skill + catálogo + insumo
   │  escreve estado.json (um único JSON, contrato na skill)
   ▼
scripts/validate_attempt.py  (máx. 3 tentativas, registradas em attempts.json com códigos)
   │  1. JSON Schema (formato)
   │  2. gates antes da proposta (insumo insuficiente, sem catálogo)
   │  3. regras v5 → v11 (governança, fidelidade, aprovações citadas, datas, texto)
   ▼  estado limpo
COMPOSITOR (código) ── template neutro POPULOS → DOCX
   │  calcula e escreve a viabilidade (feasibility.py), mapeia slots, diagrama
   │  checa: placeholders, vocabulário interno, vazamento da skill, resíduo de outro caso,
   │         IDs internos, estado × DOCX
   ▼
final/<código>.docx + relatorio-cobertura.md
```

### 4.2 Repositório

| Caminho | Papel |
|---|---|
| `authoring/AUTHOR_BRIEF.md` | Brief do autor (igual para qualquer modelo) |
| `skills/akamai-proposal-authoring/` | Skill: `SKILL.md`, `references/global-rules.md`, `solution-gating.md`, `section-model.md`, `state-schema.md`, `state.schema.json`, `institutional-standards.json`, `lexicon.json` |
| `sales_engineer/proposal_rules.py` | Validador: gates e regras v5 a v11 |
| `sales_engineer/feasibility.py` | Cálculo de janelas, datas limite e classificação frente a eventos |
| `sales_engineer/neutral_template_builder.py` | Compositor sobre o template neutro |
| `sales_engineer/document_validation.py` | Checagens do DOCX (estado × documento, resíduo, vazamento, vocabulário) |
| `sales_engineer/case_runner.py` | Workspace, tentativas, composição, relatório de cobertura |
| `sales_engineer/violation_codes.py` | Códigos estáveis de violação |
| `assets/` | Template, whitelist institucional (hash do template, blocos, `sla_applies_to`, `institutional_decisions`), termos de resíduo |
| `scripts/` | `make_workspace.py`, `validate_attempt.py`, `render_pdf.py`, `export_institutional_standards.py`, `author_with_gemini.py` |
| `lab_server.py`, `lab/`, `sales_engineer/lab.py` | **Bancada de testes** (frontend MVP) sobre o motor v11; ver 7.1 |
| `tests/` | 128 testes (v5 a v11 e bancada) com fixtures **reais** das rodadas, incluindo as aprovações inventadas pelo Gemini |
| `GUIA_TECNICO_E_RELATORIO_V4.md` | Guia técnico, seção por versão |
| `docs/trilha/` | Este documento, os relatórios das rodadas, as propostas emitidas, os insumos dos casos e a resposta da auditoria |

O `pipeline.py` antigo (Gemini em várias etapas) e a web app que o usa (`app.py`, `web/`, `run.ps1`) são anteriores ao motor e não conhece as regras atuais. O `test_pipeline.py` chama o Gemini de verdade e varia a cada execução.

### 4.3 O estado da proposta (contrato do autor)

É um JSON único, descrito em `state-schema.md` e validado por `state.schema.json`. Blocos principais:

- **Identidade:** `rules_version` (11), `data_mode`, `proposal_date`, cliente, código.
- **Antes da proposta:** `input_assessment` (suficiente ou insuficiente) e `catalog_fit` (cabe ou não no catálogo).
- **Governança:** decisões como `engagement_type`, `warranty`, `license_supply`, `sla`, estimativas e `sla_applicability`. Cada uma é compromisso (com aprovador, data, registro e **citação literal do insumo**) ou decisão interna aberta, que bloqueia.
- **Proveniência:** `traceability` (requisito, origem, quem falou), `source_coverage` (cada trecho do insumo: coberto, pendente ou descartado), `client_numbers` e `open_questions`.
- **Solução:** `solution_decisions`, com um status por produto (`recommended`, `optional`, `needs_information`, `excluded`, `already_contracted`).
- **Conflitos com padrão POPULOS:** `standard_conflicts` (conflito, compatível ou esclarecimento do cliente).
- **Entrega:** fases com semanas, escopo, premissas, restrições, riscos e critérios de aceite, mais fase opcional ou trilha rápida.
- **Eventos:** `critical_events` (evento ou congelamento), `event_feasibility` (**apenas o caminho**; as datas são do motor) e `event_readiness` (com fase).
- **Texto do cliente:** `document_text` (slots do template, todos do caso) e `sections` (resumo executivo).

### 4.4 Princípios que o código impõe

1. **Nada sem origem.** Aprovação exige citação literal do insumo. Toda data no texto vem do insumo ou do cálculo do motor. Todo requisito tem origem e falante.
2. **Decisão da POPULOS não se infere.** Garantia, licença, tipo de engajamento, folga de estabilização e aplicação do SLA fora de implantação são decisões do caso. Sem aprovação, a emissão bloqueia.
3. **Padrão institucional é só o que a instituição declarou.** Hoje: a tabela de SLA, para implantação (`institutional_decisions = ["sla"]`).
4. **O código escreve o que é aritmética.** Datas, janelas e classificação de viabilidade.
5. **Texto do cliente é do caso.** O Compositor não tem texto de caso anterior. Nome comercial, nunca ID interno.
6. **Proporcionalidade.** Plano de evento e seções no tamanho do escopo.
7. **O documento final é o que conta.** Validação estado × DOCX e QA visual.

---

## 5. Decisões da POPULOS

| Tema | Decisão | Onde está |
|---|---|---|
| Tabela de SLA institucional | Vale sem decisão do caso só para `implementation` | `assets/institutional_whitelist.json` |
| Folga de estabilização antes de eventos | **Sem padrão.** Só com aprovação do caso; sem ela, ressalva explícita | `feasibility.stabilization_days` |
| SLA em projeto faseado | **Sem padrão.** Aprovação do caso diz a quais fases se aplica (`applies_to_phases`) | Regra v11 |
| Decisões de caso (garantia, licença…) | Nunca viram padrão; valem para uma oportunidade | Regras v6 e v9 |

**Pendente (R5):** a tabela de SLA institucional cobre o **suporte contratado**, ou só as falhas dos serviços executados? O texto do template diz que "não é sustentação nem suporte gerenciado". No caso 08, os autores divergiram por causa disso.

---

## 6. Caminho: próximos passos

### 6.1 Correções já identificadas (rodada v11)

| # | Achado | Proposta |
|---|---|---|
| R1 | A citação de aprovação exige um trecho único; o nome do aprovador fica no cabeçalho do e-mail. Falhou 13 vezes na 1ª tentativa, em 4 casos | `approval_quote` aceita uma lista de trechos literais |
| R2 | A ordem do caminho muda a data limite (caso 09: 27/10 × 03/11) | A skill define a ordem; o motor checa se a implantação vem depois da licença |
| R3 | O TR formal não tem cobertura item a item obrigatória (caso 08: faltaram 7.2 e 3.3) | Todo item numerado do TR vira linha da matriz ou é descartado com motivo, checado no insumo |
| R4 | A checagem de datas leu "5.2/9.1" como a data 02/09 | Ignorar números precedidos de ponto |
| R5 | Escopo do SLA institucional × suporte contratado | Decisão da POPULOS |
| R6 | Minúscula no início do valor aprovado citado; sigla "AAP" no diagrama | Ajuste de apresentação |

### 6.2 Próximas rodadas

1. **v8.6:** R1 a R4 e R6, com testes. Rodada selada só nos casos afetados (07, 08, 09), com regressão 01 e 02.
2. **Caso real:** um TR público de WAF, anti-DDoS ou CDN (PNCP ou portais estaduais), ou um deal reconstruído pelo sales engineer. O critério final é humano: "eu mandaria esta proposta?".
3. **Conferência no Word** das propostas emitidas a cada rodada.

### 6.3 Ideias em avaliação

- **I/O por agente.** Hoje é um único autor que produz o estado inteiro; os 7 papéis são seções do mesmo JSON. Separar só quando houver ganho medido:
  - modelos baratos por etapa (Discovery);
  - gates humanos reais depois do Discovery e depois do Arquiteto.

  O schema atual já se divide por papel, e o mesmo validador confere cada fatia.
- **Pacotes por fabricante.** O núcleo (governança, proveniência, datas, Compositor) é genérico; catálogo, gating e textos do fabricante viram pacotes. O gate `sem_catalogo` já detecta a falta do pacote (caso Citrix).
- **Template por tipo de engajamento.** Assessment e desenho precisam de outro bloco de SLA (ex.: prazo de resposta a dúvidas e de revisão de entregáveis) ou de omiti-lo.
- **Pacotes padrão aprovados uma vez.** Decisões recorrentes viram `populos_standard` versionado, para que o motor não pare em toda proposta pequena.
- **Aplicação web.** A bancada (7.1) já consome o motor. Próximo passo: aprovar decisões internas pela tela, com a aprovação registrada como citação (hoje isso é feito anexando o e-mail de aprovação ao insumo).

---

## 7. Como reproduzir

```bash
pip install -r requirements.txt pytest
python -m pytest tests/ --ignore=tests/test_pipeline.py        # 128 testes
python scripts/make_workspace.py docs/trilha/casos/bateria-1 <ws> --config B --sealed   # (aponte para a pasta de um caso)
# autor escreve <ws>/execucao/estado.json e submete:
cd <ws> && python scripts/validate_attempt.py execucao execucao/estado.json
python scripts/render_pdf.py <ws>/execucao/final/<proposta>.docx   # QA visual
```

### 7.1 Bancada de testes (frontend)

```bash
python lab_server.py          # Windows: .\run_lab.ps1
# abre http://127.0.0.1:8765
```

- **Nova execução:** envia os arquivos do insumo (.md, .txt, .eml, .docx, .pdf, .csv) ou cola o texto. O motor extrai o `insumo.md` igual às rodadas.
- **Autor:** "Rodar Claude" ou "Rodar Gemini" roda até 3 tentativas pela API, com o mesmo brief, skill e validador. As chaves ficam no `.env` do servidor (`ANTHROPIC_API_KEY`, `GEMINI_API_KEY`; `ANTHROPIC_MODEL` e `GEMINI_MODEL` opcionais) e nunca passam pelo navegador. "Colar estado.json" aceita um estado escrito fora (claude.ai, subagente) e consome uma tentativa.
- **Leitura:** as 3 tentativas aparecem como 3 casas (limite físico). Violações agrupadas por código, veredito (emitida, bloqueio legítimo, violações do autor, limite esgotado), decisões internas abertas, perguntas ao cliente e o parágrafo de viabilidade calculado pelo motor.
- **Saída:** DOCX, relatório de cobertura, `passN.json`, PDF e miniaturas das páginas (LibreOffice).
- **Complementar insumo:** cria uma nova execução com o mesmo insumo e um texto anexado (ex.: o e-mail de aprovação da garantia). A execução original fica intacta.
- As execuções ficam em `lab_runs/` (fora do Git). O servidor escuta só em `127.0.0.1`.
- A bancada não é rodada selada: serve para exploração e casos novos. Rodada para auditoria continua pelo `make_workspace --sealed`.

**Tags:** `motor-v7.0` e `motor-v8.0` estão no GitHub. `motor-v8.4` (`569bfe4`) e `motor-v8.5` (`985e2cd`) precisam ser publicadas a partir de uma máquina com permissão de push de tags:

```bash
git fetch origin claude/modest-cerf-0jhyqv
git tag motor-v8.4 569bfe4 && git tag motor-v8.5 985e2cd
git push origin motor-v8.4 motor-v8.5
```

---

## 8. Conteúdo de `docs/trilha/`

| Pasta | Conteúdo |
|---|---|
| `TRILHA.md` | Este documento |
| `auditoria/` | Resposta da auditoria externa à v8.3 |
| `casos/bateria-1`, `casos/bateria-2` | Insumos dos 10 casos (sem gabaritos) |
| `rodadas/rodada-v9_motor-v8.1-a-v8.3/` | Relatório de alterações, propostas emitidas, 24 execuções |
| `rodadas/rodada-v10_motor-v8.4/` | Relatório, 9 propostas emitidas, 32 execuções (com o incidente de isolamento), varredura |
| `rodadas/rodada-v11_motor-v8.5/` | Relatório, 11 propostas emitidas, 18 execuções com códigos de violação, varredura |

Os PDFs não estão versionados; `scripts/render_pdf.py` os gera a partir dos DOCX.

## 9. Glossário

- **Estado:** o JSON que o autor escreve; a fonte lógica da proposta.
- **Gate:** bloqueio que acontece antes das regras (insumo insuficiente, sem catálogo).
- **Decisão interna (`populos_internal_decision`):** escolha comercial ou contratual da POPULOS; bloqueia a emissão e nunca aparece ao cliente.
- **Padrão institucional (`populos_standard`):** texto ou valor aprovado uma vez, versionado com o template (hoje, só o SLA).
- **Workspace selado:** pasta do autor sem o código do motor; o validador é caixa-preta.
- **Caminho (`path`):** sequência de etapas até um evento; o motor calcula as datas a partir dele.
- **Resíduo:** texto de um caso anterior que chega a outra proposta.
- **Fidelidade:** aderência da proposta ao que o cliente pediu e disse, medida separadamente da qualidade do texto.
