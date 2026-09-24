# Relatório de cobertura — Prefeitura Municipal de Rio Claro do Sul (POPULOS-RCS-PE112-2026)

- Regras: v11
- Modo dos dados: test
- Engajamento: implementation

## Decisões

| Decisão | Valor | Aprovado por | Data | Modo |
|---|---|---|---|---|
| engagement_type | implementation | Vitor | 2026-09-24 | test |
| license_supply | licenças Akamai serão fornecidas pela POPULOS por meio de revenda autorizada | Vitor | 2026-09-24 | test |
| warranty | a POPULOS corrigirá defeitos diretamente atribuíveis aos serviços executados por 12 meses após o Termo de Aceite Definitivo | Vitor | 2026-09-24 | test |
| support | suporte técnico 8x5 durante a vigência de 12 meses | Vitor | 2026-09-24 | test |
| qualification | 3 profissionais com certificação técnica Akamai vigente | Vitor | 2026-09-24 | test |
| effort_estimate | 5 a 6 semanas de implantação | Ana Ribeiro | 2026-09-24 | test |
| sla | Tabela institucional de SLA POPULOS | None | None | None |

## Cobertura do insumo

| Referência | Trecho | Status | Destino |
|---|---|---|---|
| TR 1.1 | Objeto: DNS autoritativo e proteção de aplicações web, 12 meses, implantação, repasse e suporte | coberto | sumário, escopo, REQ-09 |
| TR 2.1 | Quatro indisponibilidades em 2026 atribuídas a ataques na camada de aplicação | coberto | sumário, REQ-04 |
| TR 2.2 | DNS em servidor próprio sem redundância geográfica | coberto | sumário, REQ-01 |
| TR 3.1 | 3 zonas DNS com cerca de 150 registros | coberto | REQ-01, dimensionamento |
| TR 3.2 | Proteção para as 5 aplicações do Anexo I | coberto | REQ-03, dimensionamento |
| TR 3.3 | 6 milhões de requisições por dia, picos de 400 req/s | coberto | dimensionamento |
| TR 4.1 | DNS distribuído com DNSSEC | coberto | REQ-02 |
| TR 4.2 | WAF OWASP Top 10 com atualização automática | coberto | REQ-03 |
| TR 4.3 | Mitigação DDoS camada 7 | coberto | REQ-04 |
| TR 4.4 | Controle de taxa por aplicação | coberto | REQ-05 |
| TR 4.5 | Painel de eventos de segurança | coberto | REQ-06 |
| TR 4.6 | Exportação syslog | coberto | REQ-07 |
| TR 5.1 | Migração das zonas e onboarding das aplicações | coberto | REQ-08, escopo |
| TR 5.2 | Prazo de 45 dias corridos | coberto | REQ-08 |
| TR 5.3 | Mudanças em janelas acordadas | coberto | REQ-08, premissas |
| TR 6.1 | 2 profissionais certificados pelo fabricante | coberto | REQ-12 |
| TR 7.1 | Suporte 8x5 por 12 meses | coberto | REQ-10 |
| TR 7.2 | Severidade alta: 1h/4h | coberto | REQ-10 |
| TR 7.3 | Severidade média: 2h/8h | coberto | REQ-10 |
| TR 8.1 | Garantia de 12 meses após o TAD | coberto | REQ-11 |
| TR 9.1 | TAP e TAD | coberto | REQ-14 |
| TR 10.1 | Licenças fornecidas pela contratada por 12 meses | coberto | REQ-13 |
| TR 11.1 | Resposta item a item, marca e nome comercial | coberto | sumário, escopo |
| Anexo I | Cinco aplicações, uma com API | coberto | REQ-03, dimensionamento |

## Requisitos

| REQ | Requisito | Origem | Evidência no insumo | Falantes |
|---|---|---|---|---|
| REQ-01 | DNS autoritativo distribuído para 3 zonas (cerca de 150 registros), com redundância geográfica | TR itens 2.2 e 3.1 | TR 3.1 e 2.2 | input_document |
| REQ-02 | Suporte a DNSSEC nas zonas publicadas | TR item 4.1 | TR 4.1 | input_document |
| REQ-03 | WAF com proteção contra as categorias OWASP Top 10 e atualização automática de regras para as 5 aplicações do Anexo I | TR itens 3.2 e 4.2; Anexo I | TR 3.2, 4.2 e Anexo I | input_document |
| REQ-04 | Mitigação de ataques de negação de serviço na camada 7 | TR itens 2.1 e 4.3 | TR 2.1 e 4.3 | input_document |
| REQ-05 | Controle de taxa de requisições configurável por aplicação | TR item 4.4 | TR 4.4 | input_document |
| REQ-06 | Painel de eventos de segurança acessível pela equipe da SMTI | TR item 4.5 | TR 4.5 | input_document |
| REQ-07 | Exportação de eventos de segurança em formato compatível com syslog | TR item 4.6 | TR 4.6 | input_document |
| REQ-08 | Migração das 3 zonas e onboarding das 5 aplicações em até 45 dias corridos, com mudanças em janelas acordadas | TR itens 5.1, 5.2 e 5.3 | TR 5.1, 5.2 e 5.3 | input_document |
| REQ-09 | Repasse de conhecimento à equipe da SMTI | TR item 1.1 | TR 1.1 | input_document |
| REQ-10 | Suporte técnico 8x5 por 12 meses com tempos de resposta e solução por severidade | TR itens 7.1 a 7.3 | TR 7.1, 7.2 e 7.3 | input_document |
| REQ-11 | Garantia dos serviços de implantação por 12 meses após o TAD | TR item 8.1 | TR 8.1 | input_document |
| REQ-12 | Comprovação de ao menos 2 profissionais certificados pelo fabricante | TR item 6.1 | TR 6.1 | input_document |
| REQ-13 | Licenças por 12 meses fornecidas pela contratada | TR item 10.1 | TR 10.1 | input_document |
| REQ-14 | Aceite em duas etapas: TAP após a implantação e TAD 10 dias após o TAP sem pendências | TR item 9.1 | TR 9.1 | input_document |

## Números do cliente

- TR 2.1: 4 (quatro) indisponibilidades → contexto_de_dor
- TR 3.1: 3 (três) zonas → dimensionamento
- TR 3.1: cerca de 150 registros → dimensionamento
- TR 3.2: 5 (cinco) aplicações → dimensionamento
- TR 3.3: 6 milhões de requisições por dia → dimensionamento
- TR 3.3: 400 requisições por segundo → dimensionamento
- TR 5.2: 45 (quarenta e cinco) dias corridos → meta
- TR 6.1: 2 (dois) profissionais → meta
- TR 7.1: 8x5 → meta
- TR 7.1, 8.1, 10.1: 12 meses → meta
- TR 7.2: resposta em até 1 hora e resolução em até 4 horas → meta
- TR 7.3: resposta em até 2 horas e resolução em até 8 horas → meta
- TR 9.1: 10 dias após o TAP → meta
- Cabeçalho do TR: 28/10/2026 → descartado_com_motivo
- Cabeçalho do TR: Pregão Eletrônico nº 112/2026 → descartado_com_motivo

## Perguntas abertas

- nenhuma
