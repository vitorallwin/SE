# Relatório de cobertura — Vértice Educação (VERTICE-EDGEDNS-2026)

- Regras: v10
- Modo dos dados: test
- Engajamento: implementation

## Decisões

| Decisão | Valor | Aprovado por | Data | Modo |
|---|---|---|---|---|
| engagement_type | implementation | Vitor (dono comercial) | 2026-09-24 | test |
| warranty | A POPULOS corrigirá defeitos diretamente atribuíveis aos serviços executados por 30 dias corridos após o aceite final. | Vitor (dono comercial) | 2026-09-24 | test |
| license_supply | As licenças Akamai serão adquiridas diretamente pela Vértice Educação junto à Akamai. | Vitor (dono comercial) | 2026-09-24 | test |
| sla | Tabela institucional do template POPULOS | None | None | None |
| effort_estimate | 3 a 4 semanas | Ana (arquiteta responsável) | 2026-09-24 | test |

## Cobertura do insumo

| Referência | Trecho | Status | Destino |
|---|---|---|---|
| e-mail de 22/09/2026, parágrafo 2 | Rede de faculdades particulares com 14 unidades. | coberto | sumário |
| e-mail de 22/09/2026, parágrafo 2 | O DNS dos domínios fica no painel do registrador, que ficou fora do ar em dois episódios este ano, impedindo alterações de registros. | coberto | REQ-01, sumário |
| e-mail de 22/09/2026, parágrafo 2 | Migrar o DNS autoritativo para o Edge DNS, com DNSSEC. | coberto | REQ-01, REQ-02, escopo |
| e-mail de 22/09/2026, parágrafo 3 | São 4 zonas: vertice.edu.br, vertice.com.br, portalaluno.vertice.edu.br e vestibularvertice.com.br. | coberto | REQ-01, dimensionamento |
| e-mail de 22/09/2026, parágrafo 3 | Cerca de 380 registros, apenas A, AAAA, CNAME, MX, TXT e alguns SRV do e-mail. | coberto | REQ-05, dimensionamento |
| e-mail de 22/09/2026, parágrafo 4 | Matrículas começam em 11/01/2027; a migração precisa estar concluída e estável antes disso. | coberto | REQ-03, sumário |
| e-mail de 22/09/2026, parágrafo 4 | Não pode haver indisponibilidade no portal do aluno. | coberto | REQ-04 |
| e-mail de 22/09/2026, parágrafo 5 | Site principal e portal do aluno rodam em um único servidor em um provedor de hospedagem. | coberto | premissas |
| e-mail de 22/09/2026, parágrafo 5 | Melhoria de segurança do site talvez no futuro, sem orçamento no momento. | coberto | exclusões |
| e-mail de 22/09/2026, parágrafo 6 | Pedido de proposta de implantação. | coberto | engajamento |

## Requisitos

| REQ | Requisito | Origem | Evidência no insumo | Falantes |
|---|---|---|---|---|
| REQ-01 | Migrar o DNS autoritativo das zonas vertice.edu.br, vertice.com.br, portalaluno.vertice.edu.br e vestibularvertice.com.br do painel do registrador para o Edge DNS, com gestão de registros independente do registrador. | e-mail de 22/09/2026, parágrafos 2 e 3 | Dois episódios em 2026 em que o painel do registrador ficou fora do ar e não foi possível alterar registros. | client |
| REQ-02 | Assinar as 4 zonas com DNSSEC e publicar a cadeia de confiança junto ao registro de cada domínio. | e-mail de 22/09/2026, parágrafo 2 | Pedido explícito de migração "com DNSSEC". | client |
| REQ-03 | Concluir a migração e estabilizá-la antes do início do período de matrículas, em 11/01/2027. | e-mail de 22/09/2026, parágrafo 4 | "O período de matrículas começa em 11/01/2027, e a migração precisa estar concluída e estável antes disso." | client |
| REQ-04 | Não causar indisponibilidade de resolução de nomes do portal do aluno durante a migração. | e-mail de 22/09/2026, parágrafo 4 | "Não podemos ter indisponibilidade no portal do aluno." | client |
| REQ-05 | Migrar integralmente os cerca de 380 registros dos tipos A, AAAA, CNAME, MX, TXT e SRV, preservando o funcionamento do e-mail. | e-mail de 22/09/2026, parágrafo 3 | "Juntas, somam cerca de 380 registros. [...] só A, AAAA, CNAME, MX, TXT e alguns SRV do e-mail." | client |

## Números do cliente

- e-mail de 22/09/2026, parágrafo 2: 14 unidades → contexto_de_dor
- e-mail de 22/09/2026, parágrafo 2: dois episódios este ano → contexto_de_dor
- e-mail de 22/09/2026, parágrafo 3: 4 zonas → dimensionamento
- e-mail de 22/09/2026, parágrafo 3: cerca de 380 registros → dimensionamento
- e-mail de 22/09/2026, parágrafo 4: 11/01/2027 → meta

## Perguntas abertas

- Qual é o prazo da Akamai para ativar as licenças do Edge DNS adquiridas diretamente pela Vértice Educação? As licenças precisam estar ativas até 14/12/2026.
- Existe congelamento de mudanças previsto pela Vértice Educação antes de 11/01/2027? Em caso positivo, qual a data de início?
- Quem na Vértice Educação tem acesso ao registrador de cada domínio para alterar os servidores de nomes e publicar os registros DS?
- O registrador atual permite exportar as zonas em arquivo (formato de zona) e qual é o TTL atual dos registros?
