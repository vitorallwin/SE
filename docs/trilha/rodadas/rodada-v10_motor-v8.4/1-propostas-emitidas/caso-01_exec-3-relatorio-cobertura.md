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
| E-mail de 22/09/2026, parágrafo 2 | Rede de faculdades particulares com 14 unidades. | descartado | Contexto institucional; o número de unidades não altera o dimensionamento das zonas DNS. |
| E-mail de 22/09/2026, parágrafo 2 | O DNS dos domínios fica no painel do registrador, que ficou fora do ar em dois episódios este ano. | coberto | REQ-03, sumário |
| E-mail de 22/09/2026, parágrafo 2 | Migrar o DNS autoritativo para o Edge DNS, com DNSSEC. | coberto | REQ-01, REQ-02, escopo |
| E-mail de 22/09/2026, parágrafo 3 | São 4 zonas com cerca de 380 registros no total. | coberto | REQ-01, dimensionamento |
| E-mail de 22/09/2026, parágrafo 3 | Tipos de registro utilizados: A, AAAA, CNAME, MX, TXT e alguns SRV do e-mail. | coberto | REQ-01, escopo |
| E-mail de 22/09/2026, parágrafo 4 | A migração precisa estar concluída e estável antes de 11/01/2027, início das matrículas. | coberto | REQ-04, sumário |
| E-mail de 22/09/2026, parágrafo 4 | Não pode haver indisponibilidade no portal do aluno. | coberto | REQ-05, premissas |
| E-mail de 22/09/2026, parágrafo 5 | Site principal e portal do aluno rodam num único servidor em um provedor de hospedagem. | coberto | premissas, exclusões |
| E-mail de 22/09/2026, parágrafo 5 | Melhoria de segurança do site talvez no futuro, sem orçamento no momento. | coberto | exclusões |
| E-mail de 22/09/2026, parágrafo 6 | Pedido de proposta de implantação. | coberto | engajamento |

## Requisitos

| REQ | Requisito | Origem | Evidência no insumo | Falantes |
|---|---|---|---|---|
| REQ-01 | Migrar o DNS autoritativo das zonas vertice.edu.br, vertice.com.br, portalaluno.vertice.edu.br e vestibularvertice.com.br para o Edge DNS, com registros A, AAAA, CNAME, MX, TXT e SRV. | E-mail de 22/09/2026, parágrafos 2 e 3 | "Queremos migrar o DNS autoritativo para a Akamai (Edge DNS), com DNSSEC." e "São 4 zonas: vertice.edu.br, vertice.com.br, portalaluno.vertice.edu.br e vestibularvertice.com.br." | client |
| REQ-02 | Assinar as 4 zonas com DNSSEC. | E-mail de 22/09/2026, parágrafo 2 | "Queremos migrar o DNS autoritativo para a Akamai (Edge DNS), com DNSSEC." | client |
| REQ-03 | Permitir a alteração de registros DNS sem depender da disponibilidade do painel do registrador. | E-mail de 22/09/2026, parágrafo 2 | "já tivemos dois episódios este ano em que o painel ficou fora do ar e não conseguimos alterar registros" | client |
| REQ-04 | Concluir e estabilizar a migração antes do início do período de matrículas, em 11/01/2027. | E-mail de 22/09/2026, parágrafo 4 | "O período de matrículas começa em 11/01/2027, e a migração precisa estar concluída e estável antes disso." | client |
| REQ-05 | Migrar sem indisponibilidade do portal do aluno. | E-mail de 22/09/2026, parágrafo 4 | "Não podemos ter indisponibilidade no portal do aluno." | client |

## Números do cliente

- E-mail de 22/09/2026, parágrafo 2: 14 unidades → descartado_com_motivo
- E-mail de 22/09/2026, parágrafo 2: dois episódios este ano → contexto_de_dor
- E-mail de 22/09/2026, parágrafo 3: 4 zonas → dimensionamento
- E-mail de 22/09/2026, parágrafo 3: cerca de 380 registros → dimensionamento
- E-mail de 22/09/2026, parágrafo 4: 11/01/2027 → meta

## Perguntas abertas

- Qual é o prazo de ativação das licenças do Edge DNS na aquisição direta da Vértice junto à Akamai?
- Quem na Vértice tem acesso ao registrador para alterar os servidores de nomes e publicar o registro DS das 4 zonas, e o registrador aceita registros DS para esses domínios?
- A zona portalaluno.vertice.edu.br é hoje delegada separadamente ou seus registros estão dentro da zona vertice.edu.br?
- Há alguma janela de congelamento de mudanças da Vértice antes de 11/01/2027 que restrinja a data da troca de delegação?
