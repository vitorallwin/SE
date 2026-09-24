# Relatório de cobertura — Vértice Educação (POPULOS-VERTICE-EDGEDNS-2026)

- Regras: v11
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
| E-mail de 22/09/2026, parágrafo 2 | Rede de faculdades particulares com 14 unidades. | coberto | sumário |
| E-mail de 22/09/2026, parágrafo 2 | O DNS fica no painel do registrador e houve dois episódios neste ano em que o painel ficou fora do ar e não foi possível alterar registros. | coberto | REQ-01, sumário |
| E-mail de 22/09/2026, parágrafo 2 | Migrar o DNS autoritativo para a Akamai (Edge DNS), com DNSSEC. | coberto | REQ-01, REQ-02, escopo |
| E-mail de 22/09/2026, parágrafo 3 | São 4 zonas, somando cerca de 380 registros. | coberto | dimensionamento, REQ-01 |
| E-mail de 22/09/2026, parágrafo 3 | Tipos de registro usados: A, AAAA, CNAME, MX, TXT e alguns SRV do e-mail; nenhum recurso exótico. | coberto | REQ-01, escopo, premissas |
| E-mail de 22/09/2026, parágrafo 4 | O período de matrículas começa em 11/01/2027 e a migração precisa estar concluída e estável antes disso. | coberto | REQ-03 |
| E-mail de 22/09/2026, parágrafo 4 | Não pode haver indisponibilidade no portal do aluno. | coberto | REQ-04 |
| E-mail de 22/09/2026, parágrafo 5 | O site principal e o portal do aluno rodam num único servidor em um provedor de hospedagem. | coberto | premissas |
| E-mail de 22/09/2026, parágrafo 5 | Melhoria da segurança do site pode ser considerada no futuro, mas não é o momento e não há orçamento. | coberto | exclusões |
| E-mail de 22/09/2026, parágrafo 6 | Precisamos de uma proposta de implantação. | coberto | engajamento |

## Requisitos

| REQ | Requisito | Origem | Evidência no insumo | Falantes |
|---|---|---|---|---|
| REQ-01 | Migrar o DNS autoritativo das zonas vertice.edu.br, vertice.com.br, portalaluno.vertice.edu.br e vestibularvertice.com.br (cerca de 380 registros dos tipos A, AAAA, CNAME, MX, TXT e SRV) do painel do registrador para o Edge DNS. | E-mail de 22/09/2026, parágrafos 2 e 3 | Dois episódios neste ano de indisponibilidade do painel do registrador impediram a alteração de registros; o cliente pede o Edge DNS. | client |
| REQ-02 | Assinar as 4 zonas com DNSSEC. | E-mail de 22/09/2026, parágrafo 2 | Pedido explícito do cliente: "com DNSSEC". | client |
| REQ-03 | Concluir e estabilizar a migração antes do início do período de matrículas, em 11/01/2027. | E-mail de 22/09/2026, parágrafo 4 | Prazo informado pelo cliente. | client |
| REQ-04 | Não interromper a resolução de nomes do portal do aluno durante a migração. | E-mail de 22/09/2026, parágrafo 4 | "Não podemos ter indisponibilidade no portal do aluno." | client |

## Números do cliente

- E-mail de 22/09/2026, parágrafo 2: 14 unidades → contexto_de_dor
- E-mail de 22/09/2026, parágrafo 2: dois episódios este ano → contexto_de_dor
- E-mail de 22/09/2026, parágrafo 3: 4 zonas → dimensionamento
- E-mail de 22/09/2026, parágrafo 3: cerca de 380 registros → dimensionamento
- E-mail de 22/09/2026, parágrafo 4: 11/01/2027 → meta

## Perguntas abertas

- Existe congelamento de mudanças no ambiente da Vértice Educação antes do período de matrículas? Se sim, a partir de qual data?
- Qual o prazo previsto para a Vértice Educação concluir a aquisição das licenças do Edge DNS junto à Akamai?
- Quem na Vértice Educação tem acesso ao registrador de cada um dos 4 domínios para alterar a delegação e publicar os registros DS?
- Alguma das 4 zonas já usa DNSSEC hoje no registrador?
