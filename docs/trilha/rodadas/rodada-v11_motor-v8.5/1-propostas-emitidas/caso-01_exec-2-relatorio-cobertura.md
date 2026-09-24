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
| e-mail 22/09/2026, parágrafo 2 | Rede de faculdades particulares com 14 unidades | coberto | sumário |
| e-mail 22/09/2026, parágrafo 2 | DNS hoje no painel do registrador, com dois episódios de indisponibilidade do painel | coberto | REQ-02, sumário |
| e-mail 22/09/2026, parágrafo 2 | Migrar o DNS autoritativo para o Edge DNS, com DNSSEC | coberto | REQ-01, REQ-03 |
| e-mail 22/09/2026, parágrafo 3 | Quatro zonas: vertice.edu.br, vertice.com.br, portalaluno.vertice.edu.br e vestibularvertice.com.br | coberto | dimensionamento, escopo |
| e-mail 22/09/2026, parágrafo 3 | Cerca de 380 registros A, AAAA, CNAME, MX, TXT e SRV | coberto | REQ-04, dimensionamento |
| e-mail 22/09/2026, parágrafo 4 | Matrículas começam em 11/01/2027; migração concluída e estável antes | coberto | REQ-05 |
| e-mail 22/09/2026, parágrafo 4 | Sem indisponibilidade no portal do aluno | coberto | REQ-06 |
| e-mail 22/09/2026, parágrafo 5 | Site principal e portal do aluno em um único servidor de hospedagem | coberto | premissas, exclusões |
| e-mail 22/09/2026, parágrafo 5 | Melhoria de segurança do site no futuro, sem orçamento agora | coberto | exclusões |
| e-mail 22/09/2026, parágrafo 6 | Pedido de proposta de implantação | coberto | engajamento |

## Requisitos

| REQ | Requisito | Origem | Evidência no insumo | Falantes |
|---|---|---|---|---|
| REQ-01 | Migrar o DNS autoritativo das quatro zonas para a Akamai | e-mail 22/09/2026, parágrafo 2 | "Queremos migrar o DNS autoritativo para a Akamai (Edge DNS)" | client |
| REQ-02 | Garantir a capacidade de alterar registros mesmo quando o painel do registrador estiver indisponível | e-mail 22/09/2026, parágrafo 2 | "já tivemos dois episódios este ano em que o painel ficou fora do ar e não conseguimos alterar registros" | client |
| REQ-03 | Assinar as zonas com DNSSEC | e-mail 22/09/2026, parágrafo 2 | "com DNSSEC" | client |
| REQ-04 | Migrar cerca de 380 registros dos tipos A, AAAA, CNAME, MX, TXT e SRV | e-mail 22/09/2026, parágrafo 3 | "somam cerca de 380 registros" e "só A, AAAA, CNAME, MX, TXT e alguns SRV do e-mail" | client |
| REQ-05 | Concluir e estabilizar a migração antes do início das matrículas em 11/01/2027 | e-mail 22/09/2026, parágrafo 4 | "O período de matrículas começa em 11/01/2027, e a migração precisa estar concluída e estável antes disso." | client |
| REQ-06 | Evitar indisponibilidade do portal do aluno durante a migração | e-mail 22/09/2026, parágrafo 4 | "Não podemos ter indisponibilidade no portal do aluno." | client |

## Números do cliente

- e-mail 22/09/2026, parágrafo 2: 14 unidades → descartado_com_motivo
- e-mail 22/09/2026, parágrafo 2: dois episódios este ano → contexto_de_dor
- e-mail 22/09/2026, parágrafo 3: 4 zonas → dimensionamento
- e-mail 22/09/2026, parágrafo 3: cerca de 380 registros → dimensionamento
- e-mail 22/09/2026, parágrafo 4: 11/01/2027 → meta

## Perguntas abertas

- Qual é o prazo previsto pela Vértice Educação para a aquisição das licenças do Edge DNS junto à Akamai?
- Existe janela de congelamento de mudanças antes do início das matrículas? Se sim, a partir de qual data?
- Os registros do registrador permitem publicar o registro DS para as quatro zonas, e quem na Vértice Educação tem acesso a essa operação?
