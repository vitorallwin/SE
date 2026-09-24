# Relatório de cobertura — Vértice Educação (VERTICE-EDGEDNS-2026)

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
| E-mail 22/09/2026, parágrafo 2 | Rede de faculdades particulares com 14 unidades. | coberto | sumário |
| E-mail 22/09/2026, parágrafo 2 | DNS hoje fica no painel do registrador; dois episódios este ano de painel fora do ar sem conseguir alterar registros. | coberto | REQ-02, sumário |
| E-mail 22/09/2026, parágrafo 2 | Migrar o DNS autoritativo para o Edge DNS, com DNSSEC. | coberto | REQ-01, REQ-03, escopo |
| E-mail 22/09/2026, parágrafo 3 | São 4 zonas com cerca de 380 registros. | coberto | REQ-01, dimensionamento |
| E-mail 22/09/2026, parágrafo 3 | Tipos de registro: A, AAAA, CNAME, MX, TXT e alguns SRV do e-mail. | coberto | REQ-06, escopo |
| E-mail 22/09/2026, parágrafo 4 | Matrículas começam em 11/01/2027; migração concluída e estável antes disso. | coberto | REQ-04, sumário |
| E-mail 22/09/2026, parágrafo 4 | Sem indisponibilidade no portal do aluno. | coberto | REQ-05, premissas |
| E-mail 22/09/2026, parágrafo 5 | Site principal e portal do aluno rodam em um único servidor em um provedor de hospedagem. | coberto | premissas, exclusões |
| E-mail 22/09/2026, parágrafo 5 | Melhoria de segurança do site no futuro, sem orçamento agora. | coberto | exclusões |
| E-mail 22/09/2026, parágrafo 6 | Pedido de proposta de implantação. | coberto | engajamento |

## Requisitos

| REQ | Requisito | Origem | Falantes |
|---|---|---|---|
| REQ-01 | Migrar o DNS autoritativo das zonas vertice.edu.br, vertice.com.br, portalaluno.vertice.edu.br e vestibularvertice.com.br para o Edge DNS. | E-mail de Paulo Andrade, 22/09/2026, parágrafos 2 e 3 | client |
| REQ-02 | Garantir a capacidade de alterar registros DNS mesmo quando o painel do registrador estiver indisponível. | E-mail de Paulo Andrade, 22/09/2026, parágrafo 2 | client |
| REQ-03 | Assinar as 4 zonas com DNSSEC. | E-mail de Paulo Andrade, 22/09/2026, parágrafo 2 | client |
| REQ-04 | Concluir e estabilizar a migração antes de 11/01/2027, início do período de matrículas. | E-mail de Paulo Andrade, 22/09/2026, parágrafo 4 | client |
| REQ-05 | Executar a migração sem indisponibilidade no portal do aluno. | E-mail de Paulo Andrade, 22/09/2026, parágrafo 4 | client |
| REQ-06 | Migrar os registros A, AAAA, CNAME, MX, TXT e SRV existentes, preservando o funcionamento do e-mail. | E-mail de Paulo Andrade, 22/09/2026, parágrafo 3 | client |

## Números do cliente

- E-mail 22/09/2026, parágrafo 2: 14 unidades → descartado_com_motivo
- E-mail 22/09/2026, parágrafo 2: dois episódios este ano → contexto_de_dor
- E-mail 22/09/2026, parágrafo 3: 4 zonas → dimensionamento
- E-mail 22/09/2026, parágrafo 3: cerca de 380 registros → dimensionamento
- E-mail 22/09/2026, parágrafo 4: 11/01/2027 → meta

## Perguntas abertas

- Qual o prazo previsto para a aquisição e ativação das licenças Edge DNS diretamente pela Vértice Educação junto à Akamai?
- Qual a data a partir da qual a Vértice Educação congela mudanças de DNS antes do início das matrículas em 11/01/2027?
- O registrador atual permite publicar registros DS para DNSSEC nos domínios .edu.br e .com.br, e quem na Vértice Educação tem acesso a essa função?
- Quais janelas de mudança a Vértice Educação autoriza para a troca de servidores de nomes?
