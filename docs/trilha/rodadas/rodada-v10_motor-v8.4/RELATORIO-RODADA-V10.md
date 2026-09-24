# Rodada selada motor-v8.4: relatório para a auditoria

Data: 24/09/2026 · Tag: `motor-v8.4` (commit `569bfe4`) · Regras v10 · Template `2026.09.24-1`
Skill SHA-256: `b5f3ae9148ae594624fdeb2c874a89ff46cd608c7d71951eff8360a71c8260f2`
Autor: configuração B, Claude (claude-opus-5-5), subagente com contexto limpo, **workspace selado** (sem código do motor), limite físico de 3 tentativas. A configuração A (Gemini) foi retirada como autora.

## 1. Cadeia de custódia da bateria 2

- O zip da bateria 2 foi lacrado sem abrir, com SHA-256 `67b2e8eebfdf780c41669e64244570263ebfbbfcc1834479373d0cde5e1b277e`.
- Ele só foi aberto depois da criação da tag `motor-v8.4`, e o hash conferiu.
- Os insumos da bateria 2 não foram lidos por quem ajusta o motor. Os resultados abaixo vêm dos autores e do validador.

## 2. Resultados

A pontuação contra os gabaritos é da auditoria. Abaixo está o que o motor fez.

| Caso | Resultado nas 3 execuções | Tentativas | Motivo |
|---|---|---|---|
| 01 Vértice | **3/3 emitidas** | **1ª tentativa nas 3** | Todas as decisões aprovadas no insumo |
| 02 ATEC | 3/3 bloqueadas | 1 a 2 | Garantia, SLA do TR e qualificação (+ prazo em 1 execução) |
| 03 Mariá | 3/3 bloqueadas | 1 a 2 | Engajamento, garantia, licença e aplicabilidade do SLA |
| 04 Lumina | 3/3 bloqueadas | 1 a 2 | Só o modelo de licença |
| 05 São Lucas | 3/3 no gate `sem_catalogo` | 2 | Pedido Citrix fora do catálogo |
| 06 Sem nome | 3/3 no gate `insumo_insuficiente` | 1 | 7 a 8 perguntas de qualificação |
| 07 Faseado | 3/3 emitidas | **3ª tentativa nas 3** | Ver achado A2 |
| 08 Licitação | 3/3 bloqueadas | 2 a 3 | Prazos de SLA por severidade (TR 7.2/7.3). Ver achado A1 |
| 09 Expansão | 3/3 emitidas | 2 | Licença decidida |
| 10 Aprovações contraditórias | 3/3 bloqueadas | 2 | Garantia: 90 dias (Vitor) × 60 dias (Renata) × 12 meses (cliente) |

**Critérios da bateria 1 (auditoria, item 5):**

| Critério | Resultado |
|---|---|
| Resultados corretos pelo motivo certo | Pela leitura do operador, 18/18. A confirmação é da auditoria. |
| Caso 01 emitido na 1ª tentativa em ≥ 2 de 3 | **Atingido: 3 de 3** |
| Zero defeitos visuais no PDF | **Não atingido.** Ver achado V1. |

## 3. Incidente de isolamento (resolvido)

- **O que aconteceu:** o sistema oferece aos subagentes uma pasta de rascunho compartilhada. Dois autores do caso 08 (exec-2 e exec-3) gravaram o mesmo `gen.py` nela. A exec-2 editou e rodou o script da exec-3, e sobrescreveu o `estado.json` dela. A exec-3 submeteu esse estado como tentativa final.
- **Alcance:**
  - Só as duas execuções do caso 08 ficaram contaminadas.
  - Dois outros autores (caso 02 exec-1, caso 03 exec-2) usaram a pasta apenas para o próprio script, sem interferência.
  - Um autor listou os nomes dos arquivos da pasta, sem ler o conteúdo. Os gabaritos estão criptografados.
- **Correção:**
  1. O material em texto claro saiu da pasta compartilhada.
  2. Os autores passaram a ser instruídos a não usá-la.
  3. As duas execuções foram refeitas: pastas `caso-08_exec-2-rerun` e `caso-08_exec-3-rerun`.
- **Resultado das execuções refeitas:** o mesmo bloqueio. As originais continuam no pacote, marcadas como contaminadas.
- **Varredura final (32 execuções):** nenhuma leu código do motor, nenhuma acessou outro workspace, e nenhuma leu fora da própria pasta, além do incidente acima.

## 4. Achados para a v8.5 (não aplicados; o motor ficou congelado durante a rodada)

**A1. O autor não enxerga a tabela de SLA institucional (caso 08, alto).**
- O TR pede 1h/4h (alta) e 2h/8h (média), os mesmos valores da tabela do template.
- Como os valores não estão na skill, os autores não conseguiram declarar "compatível" e bloquearam.
- Se o gabarito esperar emissão, este é um bloqueio indevido do motor, não do autor.
- **Correção:** publicar os valores da tabela institucional na skill (versionados com o template).

**A2. Não há SLA por fase (caso 07, alto).**
- A aprovação do Vitor limita o SLA à Fase 2.
- O motor só aceita a aplicabilidade por tipo de engajamento. Para emitir, os 3 autores marcaram "faseado" inteiro, o que diz mais do que o aprovado. Todos avisaram nas notas.
- **Correção:** aplicabilidade por fase ou opção (`applies_to_phases`), e o compositor restringe o texto do bloco.
- Isso também implementa a recomendação da auditoria para projetos faseados.

**A3. A regra de semanas apaga a faixa de uma fase opcional (caso 07, médio).**
- A Fase 2 aprovada tinha 6 a 8 semanas. O autor precisou escrever "no máximo 8 semanas" para passar.
- **Correção:** aceitar também a faixa de fases e ondas opcionais declaradas.

**A4. Prazo de licença conhecido fica fora da janela (caso 09, médio).**
- A licença leva até 10 dias úteis, mas as datas de término contam a partir da data da proposta.
- **Correção:** somar o lead time conhecido à janela.

**A5. Contradição na skill (médio).**
- O `global-rules.md` ainda diz que prazo desconhecido impede `fits`. O schema v10 manda usar a data limite.
- Os autores notaram e seguiram a v10.
- **Correção:** alinhar o texto.

**V1. Diagrama com rótulos longos (visual, alto).**
- O texto encolhe até ficar ilegível e vaza da caixa.
- Ocorreu no caso 01 (exec-1 e exec-2) e no caso 07. O ajuste da v8.4 cobriu só os textos curtos.
- **Correção:** quebrar em até 2 linhas e limitar o tamanho no schema.

**V2. Paginação (visual, baixo, LibreOffice).**
- Títulos isolados no pé da página, linha de tabela isolada e colunas estreitas na tabela de dimensionamento (caso 09).
- É preciso conferir no Word, que é o motor de referência do cliente.

## 5. Conteúdo do pacote

| Pasta | Conteúdo |
|---|---|
| `1-propostas-emitidas/` | As 9 propostas emitidas: DOCX, PDF renderizado (LibreOffice) e relatório de cobertura |
| `2-execucoes/` | As 32 execuções (`passN.json`, `attempts.json`, `notes.md`, `request.json`) e o mapa de workspaces |
| `3-codigo/` | Diff v8.3 → v8.4, commits, JSON Schema, schema em texto e brief |
| `4-isolamento/` | Relatório da varredura do histórico de ferramentas |

O PDF renderizado no Word, pedido no item 6, não pôde ser gerado: o ambiente é Linux, sem Word. Os PDFs são do LibreOffice e servem como teste de portabilidade.
