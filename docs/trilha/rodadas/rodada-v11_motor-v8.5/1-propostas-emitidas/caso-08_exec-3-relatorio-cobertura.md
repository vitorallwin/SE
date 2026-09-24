# Relatório de cobertura — Prefeitura Municipal de Rio Claro do Sul (POPULOS-RCS-PE112-2026)

- Regras: v11
- Modo dos dados: test
- Engajamento: implementation

## Decisões

| Decisão | Valor | Aprovado por | Data | Modo |
|---|---|---|---|---|
| engagement_type | implementation | Vitor | 2026-09-24 | test |
| license_supply | fornecidas pela POPULOS por meio de revenda autorizada | Vitor | 2026-09-24 | test |
| warranty | corrigirá defeitos diretamente atribuíveis aos serviços executados por 12 meses após o Termo de Aceite Definitivo | Vitor | 2026-09-24 | test |
| support | suporte técnico 8x5 durante a vigência de 12 meses | Vitor | 2026-09-24 | test |
| qualification | 3 profissionais com certificação técnica Akamai vigente | Vitor | 2026-09-24 | test |
| implementation_estimate | 5 a 6 semanas de implantação | Ana Ribeiro | 2026-09-24 | test |
| sla | Tabela institucional de níveis de serviço POPULOS (ALTA 1h/4h, MÉDIA 2h/8h, BAIXA 16h/24h) | None | None | None |

## Cobertura do insumo

| Referência | Trecho | Status | Destino |
|---|---|---|---|
| TR item 1.1 | Objeto: DNS autoritativo e proteção de aplicações web, licenças 12 meses, implantação, repasse e suporte | coberto | sumário, escopo, engajamento |
| TR item 2.1 | 4 indisponibilidades em 2026 atribuídas a ataques na camada de aplicação | coberto | sumário, REQ-04 |
| TR item 2.2 | DNS em servidor próprio sem redundância geográfica | coberto | sumário, REQ-01 |
| TR item 3.1 | 3 zonas DNS com cerca de 150 registros | coberto | REQ-01, dimensionamento |
| TR item 3.2 | Proteção das 5 aplicações do Anexo I | coberto | REQ-03, dimensionamento |
| TR item 3.3 | 6 milhões de requisições por dia, picos de 400 requisições por segundo | coberto | dimensionamento |
| TR item 4.1 | DNS autoritativo distribuído com DNSSEC | coberto | REQ-01, REQ-02 |
| TR item 4.2 | WAF OWASP Top 10 com atualização automática | coberto | REQ-03 |
| TR item 4.3 | Mitigação DDoS camada 7 | coberto | REQ-04 |
| TR item 4.4 | Rate limiting por aplicação | coberto | REQ-05 |
| TR item 4.5 | Painel de eventos de segurança | coberto | REQ-06 |
| TR item 4.6 | Exportação syslog | coberto | REQ-07 |
| TR itens 5.1 a 5.3 | Migração, onboarding, prazo de 45 dias e janelas acordadas | coberto | REQ-08, escopo |
| TR item 6.1 | 2 profissionais certificados pelo fabricante | coberto | REQ-09 |
| TR itens 7.1 a 7.3 | Suporte 8x5 por 12 meses e tempos por severidade | coberto | REQ-10 |
| TR item 8.1 | Garantia de 12 meses após o TAD | coberto | REQ-11 |
| TR item 9.1 | TAP e TAD 10 dias após o TAP | coberto | REQ-12 |
| TR item 10.1 | Licenças fornecidas pela contratada por 12 meses | coberto | REQ-13 |
| TR item 11.1 | Resposta item a item com marca e nome comercial | coberto | REQ-14 |
| TR cabeçalho | Sessão pública em 28/10/2026 | descartado | Data do rito licitatório; não altera escopo nem cronograma de implantação, que conta a partir da Ordem de Serviço. |

## Requisitos

| REQ | Requisito | Origem | Evidência no insumo | Falantes |
|---|---|---|---|---|
| REQ-01 | DNS autoritativo distribuído para as 3 zonas municipais, com cerca de 150 registros | TR itens 3.1 e 4.1 | Itens 2.2, 3.1 e 4.1 do TR | input_document |
| REQ-02 | Suporte a DNSSEC | TR item 4.1 | Item 4.1 do TR | input_document |
| REQ-03 | WAF com proteção contra as categorias OWASP Top 10 e atualização automática de regras | TR item 4.2 | Item 4.2 do TR | input_document |
| REQ-04 | Mitigação de DDoS na camada de aplicação (camada 7) | TR item 4.3 | Itens 2.1 e 4.3 do TR | input_document |
| REQ-05 | Controle de taxa de requisições configurável por aplicação | TR item 4.4 | Item 4.4 do TR | input_document |
| REQ-06 | Painel de eventos de segurança acessível pela equipe da SMTI | TR item 4.5 | Item 4.5 do TR | input_document |
| REQ-07 | Exportação de eventos de segurança em formato compatível com syslog | TR item 4.6 | Item 4.6 do TR | input_document |
| REQ-08 | Migração das 3 zonas e onboarding das 5 aplicações em até 45 dias corridos, com mudanças em janelas acordadas | TR itens 5.1 a 5.3 | Itens 5.1, 5.2 e 5.3 do TR | input_document |
| REQ-09 | Ao menos 2 profissionais com certificação técnica do fabricante | TR item 6.1 | Item 6.1 do TR | input_document |
| REQ-10 | Suporte técnico 8x5 por 12 meses, com resposta e resolução por severidade | TR itens 7.1 a 7.3 | Itens 7.1 a 7.3 do TR | input_document |
| REQ-11 | Garantia dos serviços de implantação por 12 meses após o TAD | TR item 8.1 | Item 8.1 do TR | input_document |
| REQ-12 | Termo de Aceite Provisório após a implantação e Termo de Aceite Definitivo 10 dias após o TAP sem pendências | TR item 9.1 | Item 9.1 do TR | input_document |
| REQ-13 | Licenças fornecidas pela contratada com vigência de 12 meses a partir da ativação | TR item 10.1 | Item 10.1 do TR | input_document |
| REQ-14 | Resposta a cada item do TR, com marca e nome comercial dos serviços ofertados | TR item 11.1 | Item 11.1 do TR | input_document |

## Números do cliente

- TR cabeçalho: Pregão Eletrônico nº 112/2026 → descartado_com_motivo
- TR cabeçalho: Sessão pública: 28/10/2026 → descartado_com_motivo
- TR item 1.1: licenciamento por 12 (doze) meses → meta
- TR item 2.1: 4 (quatro) indisponibilidades em 2026 → contexto_de_dor
- TR item 3.1: 3 (três) zonas → dimensionamento
- TR item 3.1: cerca de 150 registros → dimensionamento
- TR item 3.2: 5 (cinco) aplicações → dimensionamento
- TR item 3.3: 6 milhões de requisições por dia → dimensionamento
- TR item 3.3: 400 requisições por segundo → dimensionamento
- TR item 4.2: OWASP Top 10 → descartado_com_motivo
- TR item 4.3: camada 7 → descartado_com_motivo
- TR item 5.2: 45 (quarenta e cinco) dias corridos → meta
- TR item 6.1: 2 (dois) profissionais → meta
- TR item 7.1: 8x5 → meta
- TR item 7.1: vigência de 12 meses → meta
- TR item 7.2: resposta em até 1 hora e resolução em até 4 horas → meta
- TR item 7.3: resposta em até 2 horas e resolução em até 8 horas → meta
- TR item 8.1: 12 (doze) meses após o Termo de Aceite Definitivo → meta
- TR item 9.1: 10 dias após o TAP → meta
- TR item 10.1: vigência de 12 meses a partir da ativação → meta

## Perguntas abertas

- A SMTI pode confirmar os responsáveis e o calendário das janelas de mudança em produção previstas no item 5.3?
- Qual servidor ou coletor syslog da SMTI receberá a exportação de eventos de segurança, e quais campos devem ser encaminhados?
