# Resposta da auditoria — motor v8.3 e próximos passos

## 1. Conferência dos achados

- **Item 1 ("[Logo do cliente]"): falso positivo, erro da auditoria.** Usei a extração do pandoc, que mostra o texto alternativo da imagem. A partir de agora, todo defeito visual é confirmado no PDF renderizado antes de ser reportado.
- **Itens 2 a 5:** confirmados por você. Seguem para a v8.4.
- **Item 7, sua ressalva está correta.** O código checa as categorias conhecidas (SLA, garantia, qualificação, prazo). Fora delas, o autor continua responsável. Registre isso na skill como regra de autor, para não parecer que o código cobre tudo.
- **Item 8 (JSON Schema):** concordo que é o achado mais importante. Ele fecha a classe inteira "validador aceita, Compositor quebra".
- **Item 9:** fica com a auditoria. Os gabaritos agora têm uma seção "Afirmações obrigatórias" por caso.

## 2. v8.4: pode seguir

**Correções:**
1. Nome comercial no lugar do ID interno em toda saída ao cliente (item 2).
2. Cabeçalho e conteúdo da coluna da matriz alinhados (item 3). A origem do requisito fica no relatório de cobertura, não no documento do cliente.
3. Texto fixo do template condicionado ao escopo (item 4): nenhum slot fixo pode mencionar capacidade, produto ou entregável fora das decisões do estado.
4. JSON Schema formal antes das regras (item 8). Erro de formato vira violação legível, nunca exceção Python.

**Novas regras:**
5. Plano de evento proporcional ao escopo (item 5).
6. Dependência de prazo desconhecido expressa como **data limite**, e não como rebaixamento da classificação (item 6).
7. Exigência do cliente que conflita com padrão POPULOS nas categorias conhecidas vira `populos_internal_decision` (item 7).

**Robustez a conferir antes da tag (genérico, não depende de caso):**
- O validador de `approval_quote` precisa normalizar marcadores de citação de e-mail (`>`), quebras de linha e espaços antes de comparar o trecho com o insumo.

**Tag:** `motor-v8.4`, registrando modelo, versão do template e hash da skill.

## 3. Configuração A

Concordo: **declarar formalmente que saiu como autora.** Inventar aprovações e usar brechas é comportamento adversarial, não só limite de capacidade. Se voltar, será só na extração do Discovery, com saída verificada. Deixe explícito no relatório que a frase "não emitiu nem o caso simples" é da rodada v8.

## 4. Nova bateria: ajuste na divisão de papéis

Você está certo sobre o desequilíbrio: 5 de 6 casos bloqueavam, e o motor foi testado principalmente em dizer "não".

Uma inversão, porém: **a auditoria escreve os insumos e os gabaritos.** Você é quem ajusta o motor. Se escrever os casos, saberá o que plantou, e isso pode influenciar as regras, mesmo sem intenção. Separar quem escreve de quem pontua não basta; é preciso separar quem escreve de quem ajusta.

A bateria 2 já está pronta, com os casos que você propôs:

| Caso | Tipo |
|---|---|
| 07 | Faseado, todas as decisões aprovadas |
| 08 | Licitação com TR integralmente atendível e decisões fornecidas |
| 09 | Expansão com licença decidida (o caso 04 destravado; a única diferença é o e-mail de licenciamento) |
| 10 | Negativo: aprovações contraditórias |

**Você recebe os insumos só depois da tag `motor-v8.4`.** Assim, nada da bateria 2 influencia a v8.4.

## 5. Rodada selada única (v8.4)

Para economizar tempo, rode as duas baterias na mesma rodada, com a mesma tag:

- **Bateria 1 (confirmação):** casos 01 a 06, 3 execuções cada = 18.
- **Bateria 2:** casos 07 a 10, 3 execuções cada = 12.
- **Total:** 30 execuções da configuração B, workspace selado, contexto limpo, limite físico de 3 tentativas.

**Critérios da bateria 1:**
- 18/18 resultados corretos, pelo motivo certo.
- Caso 01 emitido na 1ª tentativa em pelo menos 2 das 3 execuções.
- Zero defeitos visuais no PDF renderizado.

**Critérios da bateria 2:** ficam com a auditoria, nos gabaritos.

## 6. O que trazer de volta

Por execução:
- `passN.json`, `attempts.json`, `notes.md`;
- DOCX e **PDF renderizado no Word**, quando emitido;
- relatório de cobertura.

Por rodada:
- tag, modelo, versão do template e hash da skill;
- varredura do histórico de ferramentas de cada autor, confirmando o isolamento.

## 7. Decisão pendente da POPULOS: SLA

Recomendação da auditoria (a decisão é da POPULOS):
- **Implantação:** tabela institucional como está.
- **Faseado:** a tabela vale só para a fase ou a opção que toca produção.
- **Assessment e design:** não estender a tabela atual, que fala em "risco ao ambiente de produção". Criar um padrão próprio (ex.: prazo de resposta a dúvidas e de revisão de entregáveis) ou omitir o bloco.

Até essa decisão, a regra atual continua: fora de implantação, o SLA exige aprovação explícita do caso.

## 8. Caso real

Ainda não há caso real disponível. Duas alternativas para a próxima bateria:
1. **TR público real** de licitação de WAF, anti-DDoS ou CDN (PNCP ou portais estaduais). Material real, sem problema de confidencialidade.
2. **Caso reconstruído pelo sales engineer** a partir de um deal que ele viveu, anonimizado. O julgamento final é dele: "eu mandaria esta proposta?".
