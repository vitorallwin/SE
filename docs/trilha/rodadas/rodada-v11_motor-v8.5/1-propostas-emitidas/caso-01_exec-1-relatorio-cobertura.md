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
| E-mail de 22/09/2026, parágrafo 1 | Rede de faculdades particulares com 14 unidades. | coberto | sumário |
| E-mail de 22/09/2026, parágrafo 2 | DNS hoje no painel do registrador, com dois episódios de indisponibilidade do painel este ano. | coberto | REQ-01, sumário |
| E-mail de 22/09/2026, parágrafo 2 | Migrar o DNS autoritativo para Edge DNS com DNSSEC. | coberto | REQ-01, REQ-03, escopo |
| E-mail de 22/09/2026, parágrafo 3 | 4 zonas com cerca de 380 registros. | coberto | REQ-02, dimensionamento |
| E-mail de 22/09/2026, parágrafo 3 | Somente registros A, AAAA, CNAME, MX, TXT e SRV do e-mail. | coberto | REQ-02, premissas |
| E-mail de 22/09/2026, parágrafo 4 | Matrículas começam em 11/01/2027; migração concluída e estável antes. | coberto | REQ-04 |
| E-mail de 22/09/2026, parágrafo 4 | Sem indisponibilidade no portal do aluno. | coberto | REQ-05 |
| E-mail de 22/09/2026, parágrafo 5 | Site principal e portal do aluno em um único servidor num provedor de hospedagem. | coberto | premissas, exclusões |
| E-mail de 22/09/2026, parágrafo 5 | Melhoria de segurança do site não é o momento e não há orçamento. | coberto | exclusões |
| E-mail de 22/09/2026, parágrafo 6 | Pedido de proposta de implantação. | coberto | engajamento |

## Requisitos

| REQ | Requisito | Origem | Evidência no insumo | Falantes |
|---|---|---|---|---|
| REQ-01 | Ter DNS autoritativo resiliente, com gestão de registros independente do painel do registrador. | E-mail de 22/09/2026, parágrafo 2 | "já tivemos dois episódios este ano em que o painel ficou fora do ar e não conseguimos alterar registros" | client |
| REQ-02 | Migrar as 4 zonas (vertice.edu.br, vertice.com.br, portalaluno.vertice.edu.br e vestibularvertice.com.br), com cerca de 380 registros dos tipos A, AAAA, CNAME, MX, TXT e SRV. | E-mail de 22/09/2026, parágrafo 3 | "São 4 zonas [...] Juntas, somam cerca de 380 registros." | client |
| REQ-03 | Assinar as zonas com DNSSEC. | E-mail de 22/09/2026, parágrafo 2 | "Queremos migrar o DNS autoritativo para a Akamai (Edge DNS), com DNSSEC." | client |
| REQ-04 | Concluir e estabilizar a migração antes do início das matrículas em 11/01/2027. | E-mail de 22/09/2026, parágrafo 4 | "O período de matrículas começa em 11/01/2027, e a migração precisa estar concluída e estável antes disso." | client |
| REQ-05 | Não causar indisponibilidade no portal do aluno durante a migração. | E-mail de 22/09/2026, parágrafo 4 | "Não podemos ter indisponibilidade no portal do aluno." | client |

## Números do cliente

- E-mail de 22/09/2026, parágrafo 1: 14 unidades → descartado_com_motivo
- E-mail de 22/09/2026, parágrafo 2: dois episódios este ano → contexto_de_dor
- E-mail de 22/09/2026, parágrafo 3: 4 zonas → dimensionamento
- E-mail de 22/09/2026, parágrafo 3: cerca de 380 registros → dimensionamento
- E-mail de 22/09/2026, parágrafo 4: 11/01/2027 → meta
- Cabeçalho do e-mail: 22/09/2026 → descartado_com_motivo

## Perguntas abertas

- Existe congelamento de mudanças antes do início das matrículas em 11/01/2027? Se sim, a partir de qual data?
- Qual o prazo previsto pela Vértice Educação para concluir a aquisição das licenças Edge DNS diretamente com a Akamai?
- Quem na Vértice Educação terá acesso ao registrador para alterar a delegação (NS) e publicar os registros DS do DNSSEC nas 4 zonas?
- Há período mínimo de estabilização que a Vértice Educação deseja entre a conclusão da migração e o início das matrículas?
