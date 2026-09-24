# Rodada selada motor-v8.5: relatório para a auditoria

Data: 24/09/2026 · Tag: `motor-v8.5` (commit `985e2cd`) · Regras v11 · Template `2026.09.24-1`
Skill SHA-256: `7c9d6d385644115dee9dbf3fa84ceac69a92ee95943aff5a541ab1b272feeb49`
Autor: configuração B (Claude), workspace selado, limite físico de 3 tentativas. São 18 execuções: bateria 2 (casos 07 a 10) e regressão dos casos 01 e 02.

## 1. O que mudou desde a v8.4

| Item da auditoria | Implementação |
|---|---|
| A1 | Valores da tabela institucional de SLA na skill (`institutional-standards.json`), gerados do template e conferidos por teste |
| A2 e N3 | `sla_applicability.applies_to_phases` e `event_readiness[].phase`; o documento diz a que fase o SLA se aplica |
| N1 e A4 | `feasibility.py`: o autor declara o caminho e o motor calcula janelas, datas limite e classificação. Data sem origem no insumo nem no cálculo bloqueia |
| N2 | Congelamento e folga de estabilização entram na conta. **Não há valor padrão de folga** (decisão da POPULOS): sem aprovação, vira ressalva |
| A3, A5, N4, V1, N5 | Faixa de onda opcional aceita; skill alinhada; `client_clarification`; diagrama quebra linhas; código estável por violação |

## 2. Resultados

| Caso | Esperado (gabarito anterior) | Obtido | Tentativas |
|---|---|---|---|
| 01 Vértice (regressão) | Emitir | **3/3 emitidas** | 1, 1 e 2 (a 2ª tentativa foi por um campo `mode` faltando, erro do autor) |
| 02 ATEC (regressão) | Bloquear | **3/3 bloqueadas** | Garantia, SLA e qualificação. O conflito 30 × 60 dias agora sai como pendência do cliente (N4) |
| 07 Faseado | Emitir até a 2ª tentativa | **3/3 emitidas na 2ª** | Na v8.4 eram todas na 3ª. SLA restrito à Fase 2, como aprovado |
| 08 Licitação | Emitir com matriz item a item | **2/3 emitidas**, 1 bloqueada | Ver R3 e R5 |
| 09 Expansão | Emitir, datas idênticas | **3/3 emitidas**, datas não idênticas | Ver R2 |
| 10 Contraditório | Bloquear só pela garantia | **3/3** | — |

**Critérios da auditoria:**
- Caso 08 emitido com matriz item a item: **parcial.** Foram 2 de 3 emitidas, e a matriz não cita os itens 7.2 e 3.3 do TR.
- Caso 07 até a 2ª tentativa: **atingido (3/3).**
- Datas limite idênticas nas 3 execuções: **não atingido no caso 09** (27/10, 27/10 e 03/11). Ver R2.

**Isolamento:** 18/18 execuções sem nenhuma sinalização. Nenhuma leitura de código, de outro workspace ou da pasta compartilhada.

**Texto:** nenhum ID interno nas 11 propostas emitidas. O parágrafo de viabilidade vem do motor em todos os casos com evento. Os diagramas estão legíveis nos casos 07, 08 e 09 (V1 conferido no PDF).

## 3. Códigos de violação na 1ª tentativa (N5)

| Código | Ocorrências | Casos | Leitura |
|---|---|---|---|
| DECISAO-ABERTA | 14 | 02, 08, 10 | Bloqueios legítimos |
| **APROVACAO-CITACAO** | **13** | **07, 08, 09, 10** | **Sistemático: limite do motor (R1)** |
| APROVACAO-CAMPOS | 2 | 01, 09 | Autor (campo `mode` esquecido) |
| DATA-SEM-ORIGEM | 1 | 02 | Falso positivo do motor (R4) |

## 4. Achados para a próxima versão

**R1. A citação de aprovação exige um trecho único (alto, sistemático).**
- Nos e-mails, o nome do aprovador fica no cabeçalho e o texto aprovado fica no corpo.
- A regra exige os dois num trecho contínuo, e 13 primeiras tentativas falharam assim.
- **Correção:** `approval_quote` aceita uma lista de trechos literais, e a checagem de aprovador, tema e valor passa a considerar o conjunto.

**R2. A ordem do caminho muda a data limite (alto).**
- O cálculo está certo nas 3 execuções. A diferença é de modelagem: uma execução pôs o levantamento antes da assinatura do aditivo, as outras depois.
- As duas leituras são defensáveis, e a skill não orienta.
- **Correção:** a skill passa a definir a ordem (etapas que dependem de licença só depois dela). O motor pode checar isso pelo `kind` da fase: implantação exige licença antes no caminho.

**R3. Um TR formal não tem cobertura item a item obrigatória (alto).**
- No caso 08, os itens 7.2 e 3.3 não aparecem na matriz. O 7.2 é justamente o dos prazos de SLA.
- **Correção:** num processo formal, todo item numerado do TR vira linha da matriz ou é descartado com motivo. Isso é checável no código a partir do insumo.

**R4. Falso positivo na checagem de datas (médio).**
- "itens 5.2/9.1" foi lido como a data 02/09 e custou uma tentativa do autor.
- **Correção:** ignorar números precedidos de ponto decimal.

**R5. Escopo do SLA institucional × suporte contratado (decisão da POPULOS).**
- No caso 08 (exec-1), o autor notou que a tabela da POPULOS tem os mesmos números do TR, mas cobre "falhas dos serviços executados" e diz que "não é sustentação nem suporte gerenciado".
- O TR pede esses prazos para o suporte de 12 meses. O autor bloqueou por isso; as outras duas execuções trataram como compatível.
- A ambiguidade está no padrão institucional, não no autor. **A POPULOS precisa dizer se a tabela cobre o suporte contratado.**

**R6. Cosméticos (baixo).**
- O valor aprovado citado literalmente pode começar em minúscula no quadro "Modelo de fornecimento".
- O diagrama usa a sigla "AAP" em vez do nome comercial.

## 5. Conteúdo do pacote

| Pasta | Conteúdo |
|---|---|
| `1-propostas-emitidas/` | As 11 propostas emitidas: DOCX, PDF (LibreOffice) e relatório de cobertura |
| `2-execucoes/` | As 18 execuções (tentativas, `attempts.json` com códigos, notas, pedido) e o mapa de workspaces |
| `3-codigo/` | Diff v8.4 → v8.5, commits, schema, `institutional-standards.json`, `feasibility.py` e brief |
| `4-isolamento/` | Varredura do histórico de ferramentas |

A conferência visual no Word, combinada com a auditoria, fica com o operador (ambiente Windows).
