# Guia técnico e relatório de implementação da proposta V4

## 1. Objetivo deste arquivo

Este documento mapeia os arquivos usados pela aplicação Sales Engineer AI V2, registra o que foi implementado para a proposta NexusPay V4 e indica onde alterar cada comportamento.

Raiz do projeto:

```text
C:\Users\POPULOS\Documents\Codex\2026-09-23\re\outputs\sales-engineer-v2
```

Nos caminhos abaixo, `./` representa essa raiz.

## 2. Resultado atual

A aplicação local transforma uma reunião, requisitos e regras de governança em um estado JSON estruturado e gera um DOCX sobre o template neutro da POPULOS.

O fluxo atual possui:

- geração opcional com Gemini;
- modo determinístico sem IA;
- catálogo Akamai controlado;
- skill global e contratos por função;
- seleção condicional de produtos;
- matriz de rastreabilidade;
- critérios de aceite;
- decisões internas que bloqueiam emissão;
- compositor DOCX determinístico;
- verificação estado versus DOCX;
- whitelist institucional vinculada ao hash do template;
- testes de regressão contra truncamento e perda de conteúdo.

## 3. Materiais da proposta NexusPay V4

### Material inicial

| Conteúdo | Caminho |
|---|---|
| Transcrição, requisitos, escopo e decisões em Word | `./data/source-material/NexusPay-Material-Fonte-v4.docx` |
| Estado original usado como base | `./data/proposals/20260923-e54ccb6.json` |
| Estado estruturado final da V4 | `./data/proposals/nexuspay-competitive-v4.json` |
| Transformação do caso NexusPay | `./sales_engineer/demo_case_nexuspay_v2.py` |
| Script reproduzível da V4 | `./scripts/generate_nexuspay_v4.py` |

### Saídas

| Conteúdo | Caminho |
|---|---|
| Proposta final V4 | `./data/generated/POPULOS-Proposta-Tecnica-NexusPay-Competitiva-v4.docx` |
| Proposta V3 anterior | `./data/generated/POPULOS-Proposta-Tecnica-NexusPay-Competitiva-v3.docx` |
| Material-fonte para auditoria | `./data/source-material/NexusPay-Material-Fonte-v4.docx` |

## 4. Mapa da aplicação

### Inicialização e interface

| Arquivo | Responsabilidade |
|---|---|
| `./app.py` | Servidor HTTP local e rotas da API. |
| `./run.ps1` | Cria o ambiente virtual, instala dependências e inicia o servidor. |
| `./requirements.txt` | Dependências Python. |
| `./web/index.html` | Estrutura da interface web. |
| `./web/app.js` | Fluxos da interface, chamadas à API e renderização dos dados. |
| `./web/styles.css` | Estilos visuais da aplicação. |

### Domínio e orquestração

| Arquivo | Responsabilidade |
|---|---|
| `./sales_engineer/service.py` | Orquestra criação, demonstração com IA, atualização, aprovação e geração do DOCX. |
| `./sales_engineer/pipeline.py` | Implementa as etapas Discovery, Arquitetura, QA técnico, Redação, QA comercial, Repair e Documento. |
| `./sales_engineer/store.py` | Persistência local das propostas em JSON. |
| `./sales_engineer/ai.py` | Cliente Gemini, tentativas, reparo de JSON e configuração por variáveis de ambiente. |
| `./sales_engineer/skill_loader.py` | Carrega a skill de autoria para os prompts. |

### Conhecimento e seleção técnica

| Arquivo | Responsabilidade |
|---|---|
| `./sales_engineer/catalog.py` | Catálogo permitido de produtos Akamai e capacidades. |
| `./sales_engineer/demo_case_nexuspay_v2.py` | Estado competitivo do caso NexusPay, produtos, escopo, riscos, ondas e critérios. |
| `./sales_engineer/manifest.py` | Geração do manifesto de blocos do documento. |

### Documento e validação

| Arquivo | Responsabilidade |
|---|---|
| `./sales_engineer/neutral_template_builder.py` | Compositor principal do template neutro POPULOS. |
| `./sales_engineer/document_validation.py` | Normalização e comparação dos campos visíveis do estado contra o DOCX final. |
| `./sales_engineer/institutional_policy.py` | Validação do template e blocos institucionais por SHA-256. |
| `./sales_engineer/modular_docx_builder.py` | Compositor modular anterior, mantido como referência. |
| `./sales_engineer/docx_builder.py` | Compositor legado anterior. |

### Templates e política institucional

| Arquivo | Responsabilidade |
|---|---|
| `./assets/proposal_neutral_template.docx` | Template aprovado atualmente usado para geração. |
| `./assets/institutional_whitelist.json` | Versão, hash do template e hashes dos blocos institucionais. |
| `./assets/akamai_template.docx` | Template Akamai anterior, mantido como referência. |

### Testes

| Arquivo | Responsabilidade |
|---|---|
| `./tests/test_pipeline.py` | Pipeline, catálogo, governança, composição, normalização, whitelist e regressões. |
| `./tests/test_store.py` | Persistência local. |

## 5. Skills e regras

### Skill principal

```text
./skills/akamai-proposal-authoring/SKILL.md
```

Define o objetivo, regras obrigatórias, workflow e contrato de saída.

### Referências da skill

| Arquivo | Conteúdo |
|---|---|
| `./skills/akamai-proposal-authoring/references/global-rules.md` | Estados de governança, fontes, bloqueios e linguagem proibida. |
| `./skills/akamai-proposal-authoring/references/agent-contracts.md` | Papel e critério de pronto de cada função. |
| `./skills/akamai-proposal-authoring/references/solution-gating.md` | Regras compartilhadas de seleção dos produtos. |
| `./skills/akamai-proposal-authoring/references/section-model.md` | Estrutura e semântica das seções da proposta. |
| `./skills/akamai-proposal-authoring/agents/openai.yaml` | Metadados da skill para integração com agentes. |

## 6. Agentes lógicos atuais

O desenho possui sete funções mais o orquestrador:

1. **Triagem e Discovery** — normaliza a reunião, classifica fatos e cria requisitos.
2. **Arquiteto de Soluções** — avalia o catálogo e cria decisões técnicas.
3. **QA Técnico** — valida rastreabilidade, viabilidade e critérios de aceite.
4. **Redator Técnico** — escreve o conteúdo orientado ao cliente.
5. **QA Comercial** — valida compromissos, garantia, SLA, licenças e linguagem.
6. **Repair** — executa somente reparos mecânicos autorizados.
7. **Compositor** — transforma o estado aprovado em DOCX por código.
8. **Orquestrador** — controla sequência, gates humanos e bloqueios.

### Limitação importante

Na demonstração atual, essas funções são contratos lógicos. O método `create_ai_demo()` em `service.py` utiliza:

1. uma chamada Gemini para gerar a reunião;
2. uma chamada Gemini que representa conjuntamente Discovery, Arquiteto e Redator;
3. uma chamada Gemini de crítico final;
4. código determinístico para validação e documento.

Ainda não existem sete execuções LLM isoladas com handoffs persistidos individualmente.

## 7. Fluxo real da V4

```text
Reunião simulada
    ↓
Entradas originais
    ├── transcript
    ├── requirements_input
    ├── scope_input
    └── assumptions_input
    ↓
Estado inicial gerado por IA
    ↓
build_nexuspay_v2()
    ├── decisões de produtos
    ├── arquitetura
    ├── rastreabilidade
    ├── escopo e entregáveis
    ├── riscos
    ├── plano de evento
    └── critérios de aceite
    ↓
Decisões do caso
    ├── garantia de 90 dias
    └── licenças fornecidas pela POPULOS
    ↓
build_neutral_template_docx()
    ↓
Gates de emissão
    ├── decisão interna resolvida
    ├── template autorizado por hash
    ├── capacidade de campos e tabelas
    ├── placeholders e vocabulário interno
    ├── estado normalizado versus DOCX
    └── pacote DOCX válido
    ↓
Proposta V4
```

## 8. Alterações implementadas

### Compositor

- `_set_rows()` agora falha quando a quantidade excede a capacidade fixa.
- `_set_rows_dynamic()` insere parágrafos excedentes sem apagar conteúdo.
- Listas inseridas copiam a numeração nativa do template.
- Bullets digitados manualmente foram removidos.
- Escopo e entregáveis usam inserção dinâmica.
- Objetivos, exclusões, premissas e critérios também aceitam expansão controlada.
- Dimensionamento, cronograma e responsabilidades possuem assertivas de capacidade.
- A seção 3.1 passou a mostrar capacidades por produto, evitando ficar limitada a DNS.
- Prolexic aparece como recomendado com modalidade de implantação pendente.
- A garantia aparece uma vez como compromisso formal e uma explicação complementar não duplicada.
- A referência genérica ao TR foi removida dos critérios de aceite.
- O plano de evento foi movido para a descrição da solução.

### Estado NexusPay

- Objetivos foram reescritos com verbo e referências REQ ao final.
- REQ-07 foi criado para prontidão de Black Friday e Pix Day.
- O plano foi dividido em onda prioritária pré-evento e onda pós-evento.
- O resultado de planejamento ficou como `cabe parcialmente`.
- AAP e Bot Manager foram priorizados antes do freeze.
- Prolexic permaneceu condicionado a conectividade, roteamento e modelo operacional.
- A redação PCI foi alterada para apoio na obtenção da documentação junto à Akamai.
- A premissa de licenças passou a declarar fornecimento pela POPULOS.
- O critério de performance perdeu a frase interna sobre promessa comercial anterior.
- Garantia de 90 dias e revenda POPULOS são decisões exclusivas do caso NexusPay.

### Gates e auditoria

- Foi criado `document_validation.py`.
- A comparação normaliza Unicode, espaços, quebras, hifenização, aspas e numeração.
- O documento é bloqueado se escopo, entregável, exclusão, critério ou plano de evento desaparecer.
- Foi criado `institutional_policy.py`.
- A whitelist registra versão do template, SHA-256 completo e hashes dos blocos:
  - Sobre a POPULOS;
  - SLA;
  - confidencialidade.
- Alterar o template sem atualizar a whitelist bloqueia a emissão.

### Regressões cobertas

- truncamento silencioso de listas;
- perda de entregáveis;
- ausência de GTM e Ion na frente 3.1;
- mudança não autorizada do template;
- divergência entre estado e DOCX;
- bullets digitados;
- garantia duplicada;
- decisões internas não resolvidas.

## 9. Onde alterar cada comportamento

### Adicionar ou alterar produto Akamai

1. Edite `./sales_engineer/catalog.py`.
2. Edite o gating em `./skills/akamai-proposal-authoring/references/solution-gating.md`.
3. Se necessário, ajuste os agrupamentos de frentes em `_fronts()` dentro de `neutral_template_builder.py`.
4. Adicione testes em `./tests/test_pipeline.py`.

### Alterar regras gerais

Edite:

```text
./skills/akamai-proposal-authoring/references/global-rules.md
```

Não duplique a mesma regra nas skills individuais.

### Alterar o papel de um agente

Edite:

```text
./skills/akamai-proposal-authoring/references/agent-contracts.md
```

Depois confira se `pipeline.py` e `service.py` implementam o contrato descrito.

### Alterar a estrutura da proposta

1. Atualize `section-model.md`.
2. Atualize `neutral_template_builder.py`.
3. Atualize o template DOCX se a mudança for visual.
4. Atualize os testes.

### Alterar o template

Arquivo:

```text
./assets/proposal_neutral_template.docx
```

Após qualquer alteração, atualize obrigatoriamente:

```text
./assets/institutional_whitelist.json
```

O hash completo pode ser obtido com:

```powershell
Get-FileHash .\assets\proposal_neutral_template.docx -Algorithm SHA256
```

Os hashes dos blocos precisam ser recalculados conforme os seletores implementados em `institutional_policy.py`.

### Alterar o caso NexusPay

Edite:

```text
./sales_engineer/demo_case_nexuspay_v2.py
```

Depois execute:

```powershell
& "C:\Users\POPULOS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" .\scripts\generate_nexuspay_v4.py
```

### Alterar garantia ou modelo de licenciamento do caso

Edite os objetos `warranty` e `license_supply` em:

```text
./scripts/generate_nexuspay_v4.py
```

Não coloque esses valores como padrão global.

### Alterar diretamente uma proposta salva

Os estados ficam em:

```text
./data/proposals/
```

Depois de editar um JSON, gere novamente o DOCX. Prefira alterar o gerador ou a aplicação para que a mudança seja reproduzível.

## 10. Executar a aplicação

No PowerShell:

```powershell
Set-Location "C:\Users\POPULOS\Documents\Codex\2026-09-23\re\outputs\sales-engineer-v2"
$env:GEMINI_API_KEY="SUA_CHAVE"
$env:GEMINI_MODEL="gemini-3.5-flash-lite"
.\run.ps1
```

Abra:

```text
http://localhost:8010
```

Sem `GEMINI_API_KEY`, o pipeline determinístico continua disponível.

## 11. Executar os testes

Com o runtime usado neste ambiente:

```powershell
& "C:\Users\POPULOS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m unittest discover -s tests -v
```

Resultado atual esperado:

```text
14 testes aprovados
```

Também é possível validar a sintaxe:

```powershell
& "C:\Users\POPULOS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m compileall -q sales_engineer tests scripts
```

## 12. Regenerar a V4

```powershell
Set-Location "C:\Users\POPULOS\Documents\Codex\2026-09-23\re\outputs\sales-engineer-v2"
& "C:\Users\POPULOS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" .\scripts\generate_nexuspay_v4.py
```

Esse comando atualiza:

```text
./data/proposals/nexuspay-competitive-v4.json
./data/generated/POPULOS-Proposta-Tecnica-NexusPay-Competitiva-v4.docx
```

## 13. Estado dos dados e segurança

- A chave Gemini é lida apenas da variável `GEMINI_API_KEY`.
- A chave não deve ser colocada no código, JSON da proposta, navegador ou documentação.
- A chave compartilhada durante o teste deve ser rotacionada antes de qualquer uso fora do ambiente demonstrativo.
- Supabase não está implementado; a persistência atual é local em JSON.
- Autenticação e segregação por usuário ainda não estão implementadas.
- Os dados da NexusPay são fictícios.

## 14. Pendências técnicas conhecidas

### Agentes ainda não são processos isolados

Os sete agentes são contratos lógicos. Para auditoria completa, implementar handoffs persistidos:

```text
data/handoffs/<proposal-id>/01-discovery.json
data/handoffs/<proposal-id>/02-architecture.json
data/handoffs/<proposal-id>/03-technical-qa.json
data/handoffs/<proposal-id>/04-writing.json
data/handoffs/<proposal-id>/05-commercial-qa.json
data/handoffs/<proposal-id>/06-repair.json
data/handoffs/<proposal-id>/07-document-manifest.json
```

Cada arquivo deve registrar entrada, saída, agente, modelo, skill, timestamp, hash e resultado do gate.

### Manifesto

O compositor atual usa diretamente o estado estruturado. O script da V4 limpa o manifesto herdado para evitar que um manifesto antigo pareça representar a versão atual. O próximo passo é reconstruir o manifesto após cada transformação e validar manifesto versus estado.

### Template e índices

O compositor ainda utiliza posições conhecidas do template para vários campos. As assertivas impedem truncamento silencioso, mas uma grande reestruturação do DOCX pode exigir atualização dos índices e seletores.

### Renderização

O Microsoft Word foi adotado como motor visual de referência neste ambiente. O renderer empacotado baseado em LibreOffice não encontrou `soffice.exe` nesta máquina. Se o cliente utilizar outro motor, deve existir uma matriz de compatibilidade visual.

### Produção

Antes de produção ainda são necessários:

- autenticação;
- banco de dados e versionamento transacional;
- armazenamento de artefatos;
- fila de execução;
- observabilidade;
- RAG com documentação oficial e versionada da Akamai;
- gestão segura de segredos;
- aprovação e assinatura das decisões internas;
- testes de concorrência e recuperação.

## 15. Checklist antes de entregar uma proposta

- [ ] Reunião ou TR anexado e classificado.
- [ ] Requisitos numerados.
- [ ] Produtos ligados a requisitos.
- [ ] Produtos excluídos não aparecem na arquitetura principal.
- [ ] Promessa ligada a componente, escopo e aceite.
- [ ] Garantia aprovada para a oportunidade.
- [ ] Modelo de fornecimento aprovado para a oportunidade.
- [ ] Pendências do cliente possuem consequência explícita.
- [ ] Nenhuma decisão interna está aberta.
- [ ] Template corresponde ao hash autorizado.
- [ ] Estado versus DOCX passou sem divergências.
- [ ] Zero placeholders e linguagem interna.
- [ ] Testes automatizados verdes.
- [ ] DOCX renderizado no motor de referência.
- [ ] Todas as páginas inspecionadas visualmente.

## 16. Proposta V5 (regras v5)

A V5 responde ao feedback consolidado da V4. A principal mudança é o tipo de engajamento: o insumo exclui a "implementação prática de infraestrutura nesta fase de descoberta", então a V5 contrata apenas a **Fase 1 (Assessment e Desenho)** e apresenta a implantação em ondas como **Fase 2 opcional** (seção 6.3).

### Arquivos novos ou alterados

| Arquivo | Conteúdo |
|---|---|
| `./sales_engineer/demo_case_nexuspay_v5.py` | Estado da V5: requisitos REQ-01 a REQ-10 com origem, números do cliente com destino, cobertura inversa, Fase 2 opcional. |
| `./sales_engineer/proposal_rules.py` | Validador das regras v5 (engajamento, soma de semanas, ondas, opcionais, proveniência, números, estimativas, mascaramento no SIEM). |
| `./scripts/generate_nexuspay_v5.py` | Resolve as decisões do caso e gera estado, DOCX e relatório de cobertura. |
| `./tests/test_v5_rules.py` | 25 testes de regressão, com testes negativos para cada gate. |
| `./skills/akamai-proposal-authoring/references/lexicon.json` | Léxico único de termos internos e termos sem tradução, lido pelo código. |
| `./sales_engineer/document_validation.py` | Léxico, detector de 8 palavras copiadas da skill e cobertura da Fase 2 no gate estado × DOCX. |
| `./sales_engineer/neutral_template_builder.py` | Textos por caso (`document_text`), frentes e diagrama só com recomendados, seção de opções, Fase 2 opcional, critérios de referência e títulos inseridos com a formatação do template. |
| `global-rules.md` / `solution-gating.md` | Regras de fidelidade v5; linhas de GTM, ALB (por requisição), Prolexic, Ion e Account Protector. |

As regras v5 só se aplicam a estados com `rules_version >= 5`. Estados antigos (V2 a V4 e o pipeline da aplicação) continuam gerando como antes, exceto pelas mudanças de texto do compositor. Por isso, `generate_nexuspay_v4.py` não reproduz mais o DOCX V4 auditado byte a byte.

### Gerar a V5

```powershell
& "C:\Users\POPULOS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" .\scripts\generate_nexuspay_v5.py
```

Saídas: `data/proposals/nexuspay-competitive-v5.json`, `data/generated/POPULOS-Proposta-Tecnica-NexusPay-Competitiva-v5.docx` e `data/generated/NexusPay-v5-relatorio-cobertura.md`.

### Decisões de teste do caso (confirmar)

Registradas em `CASE_DECISIONS` no script da V5, válidas somente para a NexusPay: engajamento `phased`, estimativa da Fase 1 de 4 a 6 semanas, garantia de 90 dias e revenda POPULOS.

### Pendências conhecidas

- A interface web e o `pipeline.py` ainda não pedem `engagement_type` nem aplicam as regras v5.
- A nota de fidelidade ainda não é calculada por rubrica; o relatório de cobertura é a base para isso.
- O segundo QA técnico após a redação e o store de decisões por oportunidade continuam no plano.

### Proposta V6 (regras v6)

`./sales_engineer/demo_case_nexuspay_v6.py` parte da V5 e aplica o feedback da V5. `./scripts/generate_nexuspay_v6.py` gera `nexuspay-competitive-v6.json`, o DOCX V6 e `NexusPay-v6-relatorio-cobertura.md`. `./tests/test_v6_rules.py` cobre as regras novas.

Regras v6 (em `_validate_rules_v6`, só para `rules_version >= 6`):

- decisão em `commitment` exige `approved_by`, `approved_at`, `approved_value` igual ao `value` e `engagement_ref` igual ao engajamento vigente; origem com "confirmar" bloqueia;
- o SLA institucional só é emitido se `applies_to` contiver o engajamento;
- cada requisito declara `speakers` (`client`, `vendor`, `input_document`); requisito apoiado só no fabricante exige `hypothesis`;
- entregas e critérios da fase contratada não podem conter termos de `client_scope.forbidden_in_committed`;
- evento crítico com data conhecida exige viabilidade calculada a partir da data da proposta e declarada no sumário;
- a trilha rápida declara a entrada na borda como mudança em produção, com janela, reversão, aprovação, prazo antes do congelamento, a pergunta sobre hostnames já na Akamai, e sem Prolexic.

O compositor agora renderiza todos os parágrafos do resumo executivo, e o gate estado × DOCX passou a cobri-los.

## 17. Motor v7 e rodada de casos diversos

O motor v7 é genérico: não depende de um arquivo Python por caso. O autor (humano, Gemini ou subagente Claude) escreve um estado JSON no formato de `skills/akamai-proposal-authoring/references/state-schema.md`, e o motor valida e compõe.

| Arquivo | Papel |
|---|---|
| `engine_config.json` | Versão do motor, limite de iterações (3), template e modelo de cada configuração. |
| `authoring/AUTHOR_BRIEF.md` | Brief do autor, idêntico nas duas configurações. |
| `sales_engineer/case_runner.py` | Extração do insumo, pacote da skill, validação, registro de tentativas e composição. |
| `scripts/make_workspace.py` | Cria um workspace isolado por execução: motor, skill, brief e um único caso. Sem testes, dados, histórico nem outros casos. |
| `scripts/prepare_run.py` | Cria a pasta da execução com `insumo.md`, `catalog.json` e `request.json`. |
| `scripts/validate_attempt.py` | Submete uma tentativa (`passN.json`, `attempts.json`) e compõe em `final/` quando está limpa. Recusa a partir da 4ª tentativa. |
| `scripts/author_with_gemini.py` | Configuração A: autor via Gemini (requer `GEMINI_API_KEY`). |
| `tests/test_v7_engine.py` | Regras v7 e executor genérico. |

Padrão institucional (`basis: populos_standard`) exige a versão vigente do template, não aprovação por caso. Prazo de licenciamento desconhecido usa `weeks: null` com pergunta aberta e impede a classificação `fits`.

Regras v7 (`_validate_rules_v7`): `data_mode` como flag que não desliga checagem; aprovação explícita com `approved_by`, `approved_at` ISO, `approval_record` e `mode`, sem aprovação implícita nem marcação de teste no texto; estimativa de esforço com dono técnico; critério de aceite próprio para toda opção que toca produção; prazo de licenciamento em toda viabilidade e na trilha rápida.

### Executar um caso

```powershell
python .\scripts\prepare_run.py <pasta-do-insumo> <pasta-da-execução> --config A --date 2026-09-24
python .\scripts\author_with_gemini.py <pasta-da-execução>          # configuração A
# configuração B: subagente Claude com contexto limpo, recebendo só AUTHOR_BRIEF.md e a pasta da execução
```

Resultado por execução: `pass1..3.json`, `attempts.json` (violações da primeira passada e da final), `notes.md` e, quando emitido, `final/` com o DOCX e o relatório de cobertura.

## 18. Motor v8: correções da rodada de casos diversos

A rodada v7 (config B, casos 01 a 06, 3 execuções cada) acertou 18/18 decisões de emitir ou bloquear. Ela revelou cinco lacunas do núcleo, corrigidas na v8 (`_pre_proposal_gate` e `_validate_rules_v8`):

| Achado | Correção |
|---|---|
| O compositor tinha texto fixo de um caso anterior ("nuvens", "SOC", "Assessment", "lojistas") | Os slots dependentes do caso não têm mais texto padrão: `document_text` obrigatório, além de `client_roles`, `restrictions`, `assessment_items` e `dimensioning`. `assets/case_residue.json` bloqueia termos de casos anteriores que cheguem ao DOCX sem estar no estado. |
| Insumo insuficiente e pedido fora do catálogo bloqueavam só por falta de decisões | Gates `insumo_insuficiente` (`input_assessment`) e `sem_catalogo` (`catalog_fit`), avaliados antes de qualquer outra regra. |
| Produto já contratado aparecia como excluído | Status `already_contracted`, com `contract_ref`. Aparece como ambiente atual e não pode ser oferecido de novo. |
| Cada autor declarava a aplicabilidade do SLA de um jeito | A instituição declara (`sla_applies_to` na whitelist). Outros engajamentos exigem a decisão aprovada `sla_applicability`. |
| Autor podia rodar o validador fora do contador | O brief proíbe. É uma limitação conhecida: dentro do workspace, isso não pode ser impedido por código. |

O fixture `tests/fixtures/vertice_v8.json` é uma saída real da rodada (caso 01), usada como estado limpo do contrato v8. Os testes estão em `tests/test_v8_engine.py`.

### Motor v8.1 (regras v9)

Na rodada v8, o autor Gemini escreveu decisões "aprovadas por Vitor" que não existem no insumo (garantia de 12 meses no caso 02, licenciamento no caso 04). O validador conferia só o preenchimento dos campos. Na v9, toda decisão de caso em `commitment` cita `approval_quote`, um trecho literal do insumo. O `record_attempt` passa o `insumo.md` ao validador, que confere: a citação existe no insumo, trata da decisão, nomeia o aprovador e contém o valor aprovado. O estado real do Gemini ficou como fixture (`tests/fixtures/lumina_gemini_aprovacao_inventada.json`).

O `make_workspace --sealed` cria um workspace sem o código do motor: só brief, skill, caso e um `validate_attempt.py` que chama o motor fora da pasta. Assim o autor conhece as regras apenas pela skill e pelas mensagens do validador.

### Motor v8.2 e v8.3

- v8.2: na rodada selada (autor sem acesso ao código) apareceram três divergências entre skill e validador. A linha "Estimativa" era sempre recusada; a faixa de semanas de uma fase isolada era tratada como total; o formato de `delivery.responsibilities` passava no validador e derrubava o compositor. As três foram alinhadas.
- v8.3: o Gemini marcou a decisão de licença como `populos_standard` para pular a aprovação. Agora só as decisões listadas em `institutional_decisions` na whitelist (hoje, `sla`) podem usar essa base.

## 19. Arquivos de trabalho fora da aplicação

Estes arquivos ajudaram na geração e auditoria, mas não são necessários para executar a aplicação:

| Arquivo | Finalidade |
|---|---|
| `C:\Users\POPULOS\Documents\Codex\2026-09-23\re\work\create_nexuspay_source_pack.py` | Gera o DOCX de material-fonte. |
| `C:\Users\POPULOS\Documents\Codex\2026-09-23\re\work\export_word_pdf.py` | Exportador auxiliar por Microsoft Word. |
| `C:\Users\POPULOS\Documents\Codex\2026-09-23\re\work\neutral-template\v4-final-render\` | Renderização interna da V4 para QA. |
| `C:\Users\POPULOS\Documents\Codex\2026-09-23\re\work\source-pack-render2\` | Renderização interna do material-fonte. |

Esses artefatos de renderização não devem ser publicados ao cliente.
