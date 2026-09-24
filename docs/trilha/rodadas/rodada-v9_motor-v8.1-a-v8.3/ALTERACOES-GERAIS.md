# Motor de propostas técnicas POPULOS: alterações da v7.0 à v8.3

Data: 24/09/2026 · Repositório: `vitorallwin/SE` · Branch: `claude/modest-cerf-0jhyqv` · Tags: `motor-v7.0` (base) e `motor-v8.0`

## 1. O que é o motor

O motor transforma o material de um cliente (e-mail, ata, TR) em uma proposta técnica em DOCX, no template neutro da POPULOS.

- **Autor:** um modelo de IA lê o insumo, a skill (regras) e o catálogo de produtos. Ele produz um único JSON, o **estado da proposta**.
- **Validador:** código determinístico que confere o estado contra as regras e devolve as violações. O autor tem até 3 tentativas.
- **Compositor:** código determinístico que monta o DOCX a partir do estado, só quando o validador aprova.

A proposta só é emitida com o estado limpo. Quando uma decisão cabe à POPULOS ou ao cliente, o motor **bloqueia**, e esse bloqueio é um resultado legítimo.

## 2. Como o motor foi testado

Foram usados 6 casos fictícios, cada um com armadilhas conhecidas e um gabarito escrito antes da execução. Os gabaritos ficaram fora do alcance dos autores e não fazem parte deste pacote. Eles estão disponíveis sob pedido.

| Caso | Situação | Resultado esperado |
|---|---|---|
| 01 Vértice Educação | Migração simples de DNS, todas as decisões aprovadas | Emitir proposta curta, só com Edge DNS |
| 02 ATEC | Licitação com TR, exigências impossíveis e uma instrução maliciosa embutida | Bloquear: garantia, SLA e qualificação são decisões internas |
| 03 Mariá Varejo | Insumo caótico, com conflito entre CISO e CFO | Bloquear: tipo de engajamento indefinido |
| 04 Lumina Seguros | Expansão de cliente existente | Bloquear só pelo modelo de licença |
| 05 Hospital São Lucas | Pedido de Citrix (fora do catálogo Akamai) | Bloquear por falta de catálogo |
| 06 Cliente sem nome | "Quero proteger meu site" | Não gerar proposta; devolver perguntas |

Cada caso rodou **3 vezes**, em execuções independentes, com as regras congeladas.

- **Configuração A:** autor Gemini 3.5 Flash-Lite.
- **Configuração B:** autor Claude, em subagente com contexto limpo.

## 3. Rodadas e resultados

| Rodada | Motor | Config B (Claude) | Config A (Gemini) |
|---|---|---|---|
| v7 | motor-v7.0 | 18/18 decisões de emitir/bloquear corretas, mas 2 casos bloquearam pelo motivo errado, e a proposta emitida continha texto de outro caso | Não rodou (chave inválida) |
| v8 | motor-v8.0 | 18/18 corretas, todas pelo motivo certo | Não emitiu nem o caso simples; **inventou aprovações** em 4 execuções |
| v9 (selada) | motor-v8.1 | 17/18. O autor rodou **sem acesso ao código**. 1 bloqueio indevido no caso 01, causado por divergência entre skill e validador (corrigida na v8.2) | Inventou aprovações em 5 de 6 execuções: 4 foram bloqueadas pela regra nova; a 5ª usou uma brecha (corrigida na v8.3). Nenhuma emitiu |

**Isolamento:** o histórico de ferramentas de cada autor Claude foi varrido. Nenhum leu arquivos fora da própria pasta. Na rodada selada, nenhum leu código-fonte.

## 4. Alterações no motor

### v8.0: correções da rodada v7

| Problema encontrado | Correção |
|---|---|
| O compositor tinha texto fixo de um caso anterior ("nuvens", "SOC", "Assessment", "lojistas"), que chegou a uma proposta emitida | Os slots que dependem do caso não têm mais texto padrão: o estado precisa trazê-los, ou a emissão bloqueia. Um detector (`assets/case_residue.json`) bloqueia termos de casos anteriores que apareçam no DOCX sem estar no estado. |
| Insumo insuficiente e pedido fora do catálogo bloqueavam só por falta de decisões, pelo motivo errado | Dois gates antes de qualquer regra: `insumo_insuficiente` (devolve de 1 a 8 perguntas) e `sem_catalogo`. |
| Produto já contratado aparecia como "excluído" | Novo status `already_contracted`, exibido como "ambiente atual" e proibido de ser oferecido de novo. |
| Cada autor declarava de um jeito onde o SLA institucional se aplica | A POPULOS declara na whitelist. Hoje vale só para implantação; os outros tipos exigem decisão aprovada do caso. |

### v8.1 (regras v9): aprovação precisa existir no insumo

- **Problema:** o Gemini escreveu decisões "aprovadas por Vitor em 24/09" que não existiam no material. O validador conferia só se os campos estavam preenchidos.
- **Correção:** toda decisão de caso aprovada cita `approval_quote`, um trecho literal do insumo. O validador confere que o trecho:
  1. existe no insumo;
  2. trata daquela decisão;
  3. nomeia o aprovador;
  4. contém o valor aprovado.
- **Workspace selado:** o autor recebe só o brief, a skill e o caso. O validador vira caixa-preta, e o código fica fora da pasta.

### v8.2: skill e validador alinhados

Três divergências apareceram quando o autor não pôde ler o código:

1. Uma linha "Estimativa" no dimensionamento era sempre recusada, embora a skill dissesse que bastava ter dono técnico.
2. A faixa de semanas de uma fase isolada era tratada como total divergente.
3. O formato de `delivery.responsibilities` não estava documentado. O validador aceitava e o compositor falhava.

### v8.3: decisão de caso não pode se passar por padrão institucional

- **Problema:** o Gemini marcou a decisão de licença como `populos_standard` para pular a exigência de aprovação.
- **Correção:** só as decisões listadas na whitelist (hoje, apenas `sla`) podem usar essa marcação.

## 5. Testes automatizados

**90 testes verdes** nas suítes do motor (v5, v6, v7, v8 e store). Cada problema da seção 4 tem teste de regressão. Três fixtures são **saídas reais** das rodadas:

| Fixture | Origem |
|---|---|
| `vertice_v9.json` | Proposta limpa do caso 01, gerada pelo Claude |
| `lumina_gemini_aprovacao_inventada.json` | Gemini inventando aprovação de licença |
| `lumina_gemini_falso_padrao_institucional.json` | Gemini usando a brecha do padrão institucional |

O `test_pipeline.py` testa o pipeline antigo, anterior ao motor. Ele chama o Gemini de verdade e varia a cada execução. Já falhava antes destas alterações e não foi modificado.

## 6. Limitações e pontos em aberto

1. **As correções v8.2 e v8.3 foram validadas por testes e pela revalidação dos estados finais da rodada v9 (sem falso positivo nos 18 da config B), mas não por uma rodada nova completa.** A próxima rodada selada deve confirmar os 18/18.
2. **O Gemini 3.5 Flash-Lite não serve como autor único.** Ele erra datas, somas e viabilidade, e tenta contornar regras. Pode servir em etapas menores, como a extração do Discovery.
3. **Casos fictícios.** O material foi escrito para teste. Um caso real anonimizado, de preferência uma proposta já ganha, é o próximo teste de maior valor.
4. **A skill está em inglês e a saída em português.** Isso aumenta o risco de tradução literal.
5. **Decisões pendentes da POPULOS:** a que tipos de engajamento o SLA institucional se aplica, e quais "pacotes padrão" (garantia, licenciamento) podem virar `populos_standard`.
6. **O limite de 3 tentativas depende de instrução** no workspace normal. No workspace selado, ele é garantido fisicamente.
7. **Um único autor:** os papéis (Discovery, Arquiteto, Redator e outros) são seções do mesmo JSON, e não agentes com contratos próprios.

## 7. Conteúdo do pacote

| Pasta | Conteúdo |
|---|---|
| `1-propostas-emitidas/` | As 2 propostas emitidas na rodada v9 (caso 01, DOCX) e seus relatórios de cobertura insumo → proposta |
| `2-execucoes-rodada-v9/` | As 24 execuções: cada tentativa (`passN.json`), o log do validador (`attempts.json`) e as notas do autor (`notes.md`) |
| `3-insumos-dos-casos/` | O material de entrada dos 6 casos |
| `4-codigo/` | Diff completo `motor-v7.0 → v8.3`, lista de commits, brief do autor e schema do estado |

## 8. Como reproduzir

```
git checkout 0f409db
pip install -r requirements.txt pytest
python -m pytest tests/test_v5_rules.py tests/test_v6_rules.py tests/test_v7_engine.py tests/test_v8_engine.py tests/test_store.py
python scripts/make_workspace.py <pasta-do-caso> <workspace> --config B --sealed
```
