# Relatório de cobertura — Vértice Educação (POPULOS-VERTICE-EDGEDNS-2026-09)

- Regras: v9
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
| E-mail de 22/09/2026, parágrafo 1 | Rede de faculdades particulares com 14 unidades | descartado | Contexto institucional; o número de unidades não altera o dimensionamento das zonas DNS. |
| E-mail de 22/09/2026, parágrafo 1 | DNS hoje fica no painel do registrador, com dois episódios de indisponibilidade do painel no ano | coberto | REQ-01, REQ-04, sumário |
| E-mail de 22/09/2026, parágrafo 1 | Migrar o DNS autoritativo para Edge DNS com DNSSEC | coberto | REQ-01, REQ-02, escopo |
| E-mail de 22/09/2026, parágrafo 2 | 4 zonas com cerca de 380 registros A, AAAA, CNAME, MX, TXT e SRV | coberto | REQ-03, dimensionamento |
| E-mail de 22/09/2026, parágrafo 3 | Migração concluída e estável antes do início das matrículas em 11/01/2027 | coberto | REQ-05, sumário |
| E-mail de 22/09/2026, parágrafo 3 | Não pode haver indisponibilidade no portal do aluno | coberto | REQ-06, premissas |
| E-mail de 22/09/2026, parágrafo 4 | Site principal e portal do aluno em um único servidor de um provedor de hospedagem | coberto | premissas, exclusões |
| E-mail de 22/09/2026, parágrafo 4 | Melhoria de segurança do site talvez no futuro, sem orçamento agora | coberto | exclusões |
| E-mail de 22/09/2026, parágrafo 5 | Pedido de proposta de implantação | coberto | engajamento |

## Requisitos

| REQ | Requisito | Origem | Falantes |
|---|---|---|---|
| REQ-01 | Migrar o DNS autoritativo das zonas da Vértice Educação para o Edge DNS | E-mail de 22/09/2026, parágrafo 1 | client |
| REQ-02 | Habilitar DNSSEC nas zonas migradas | E-mail de 22/09/2026, parágrafo 1 | client |
| REQ-03 | Migrar 4 zonas (vertice.edu.br, vertice.com.br, portalaluno.vertice.edu.br, vestibularvertice.com.br) com cerca de 380 registros dos tipos A, AAAA, CNAME, MX, TXT e SRV | E-mail de 22/09/2026, parágrafo 2 | client |
| REQ-04 | Permitir alteração de registros sem depender do painel do registrador | E-mail de 22/09/2026, parágrafo 1 | client |
| REQ-05 | Concluir e estabilizar a migração antes de 11/01/2027 | E-mail de 22/09/2026, parágrafo 3 | client |
| REQ-06 | Migrar sem indisponibilidade de resolução DNS para o portal do aluno | E-mail de 22/09/2026, parágrafo 3 | client |

## Números do cliente

- E-mail de 22/09/2026, parágrafo 1: 14 unidades → descartado_com_motivo
- E-mail de 22/09/2026, parágrafo 1: dois episódios este ano → contexto_de_dor
- E-mail de 22/09/2026, parágrafo 2: 4 zonas → dimensionamento
- E-mail de 22/09/2026, parágrafo 2: cerca de 380 registros → dimensionamento
- E-mail de 22/09/2026, parágrafo 3: 11/01/2027 → meta

## Perguntas abertas

- Qual é o prazo previsto pela Vértice Educação para a aquisição das licenças Edge DNS diretamente junto à Akamai?
- Qual data a Vértice Educação define para o congelamento de mudanças no DNS antes do início das matrículas em 11/01/2027?
- Quem detém o acesso administrativo ao registrador de cada domínio para a troca de servidores de nomes e a publicação do registro DS?
- A zona portalaluno.vertice.edu.br é hoje delegada a partir de vertice.edu.br ou está hospedada na mesma zona?
