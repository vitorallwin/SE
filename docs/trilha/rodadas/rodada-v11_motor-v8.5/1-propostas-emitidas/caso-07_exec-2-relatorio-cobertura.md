# Relatório de cobertura — Solaris Energia (SOLARIS-AKAMAI-2026-09)

- Regras: v11
- Modo dos dados: test
- Engajamento: phased

## Decisões

| Decisão | Valor | Aprovado por | Data | Modo |
|---|---|---|---|---|
| engagement_type | phased | Vitor (Executivo de Contas, POPULOS) | 2026-09-24 | test |
| warranty | A POPULOS corrigirá defeitos diretamente atribuíveis aos serviços executados por 90 dias corridos após o aceite de cada fase. | Vitor (Executivo de Contas, POPULOS) | 2026-09-24 | test |
| license_supply | As licenças Akamai serão fornecidas pela POPULOS por meio de revenda autorizada. | Vitor (Executivo de Contas, POPULOS) | 2026-09-24 | test |
| sla | Tabela institucional de SLA POPULOS (ALTA, MÉDIA, BAIXA) | None | None | None |
| sla_applicability | ['implementation'] | Vitor (Executivo de Contas, POPULOS) | 2026-09-24 | test |
| phase1_estimate | 3 a 4 semanas | Ana Ribeiro (Arquiteta, POPULOS) | 2026-09-24 | test |
| phase2_estimate | 6 a 8 semanas | Ana Ribeiro (Arquiteta, POPULOS) | 2026-09-24 | test |

## Cobertura do insumo

| Referência | Trecho | Status | Destino |
|---|---|---|---|
| Ata 22/09/2026 — Beatriz: perfil da Solaris | Distribuidora de energia em 3 estados, com 4,2 milhões de unidades consumidoras. | coberto | sumário |
| Ata 22/09/2026 — Beatriz: portal e app | O portal concentra segunda via, religação e consulta de débitos; o app usa as mesmas APIs. | coberto | REQ-01, escopo |
| Ata 22/09/2026 — Henrique: ataques L7 | Portal fora do ar por cerca de 3 horas em junho e em agosto por DDoS de aplicação na consulta de débitos; sem ataque volumétrico de rede. | coberto | REQ-01, sumário, exclusões |
| Ata 22/09/2026 — Henrique: robôs de CPF | Robôs testam CPFs na consulta de débitos, que devolve nome e endereço; tratado com o DPO. | coberto | REQ-02, REQ-06 |
| Ata 22/09/2026 — Beatriz: origens | Datacenter próprio principal e nuvem pública acionada manualmente; desejo de failover automático. | coberto | REQ-03, dimensionamento |
| Ata 22/09/2026 — Beatriz: campanha | Campanha de renegociação em 01/03/2027; tráfego triplicou na última campanha. | coberto | REQ-04, dimensionamento |
| Ata 22/09/2026 — Henrique: janela de mudanças | Sem congelamento formal; mudanças em produção só às terças, das 22h às 2h. | coberto | premissas |
| Ata 22/09/2026 — Beatriz e Ana: fases | Assessment e desenho primeiro; implantação como opção após aceite do desenho. | coberto | REQ-05, engajamento |
| Ata 22/09/2026 — Henrique: DNS | O DNS dos domínios fica no provedor atual e não é o foco. | coberto | exclusões, premissas |

## Requisitos

| REQ | Requisito | Origem | Evidência no insumo | Falantes |
|---|---|---|---|---|
| REQ-01 | Proteger o portal do cliente e as APIs usadas pelo app contra negação de serviço na camada de aplicação, em especial na consulta de débitos. | Ata de 22/09/2026 — Henrique (ataques de junho e agosto) | Duas indisponibilidades de cerca de 3 horas (junho e agosto) causadas por milhões de requisições na consulta de débitos. | client |
| REQ-02 | Detectar e conter robôs que testam números de CPF na consulta de débitos. | Ata de 22/09/2026 — Henrique (robôs testando CPF) | Robôs testando CPFs; quando o CPF existe, a página devolve nome e endereço. | client |
| REQ-03 | Tornar automático o failover do portal e das APIs entre o datacenter próprio (principal) e a nuvem pública. | Ata de 22/09/2026 — Beatriz (dois ambientes de origem) | Hoje a nuvem pública só recebe tráfego manualmente quando o datacenter cai. | client |
| REQ-04 | Estar protegido e com failover automático antes do início da campanha estadual de renegociação de dívidas em 01/03/2027, com tráfego que pode triplicar. | Ata de 22/09/2026 — Beatriz (campanha de 01/03/2027) | Na última campanha o tráfego do portal triplicou. | client |
| REQ-05 | Realizar assessment e desenho antes de contratar a implantação. | Ata de 22/09/2026 — Beatriz (assessment e desenho primeiro) | Cliente não quer contratar a implantação às cegas. | client |
| REQ-06 | Não ampliar a exposição de dados pessoais (CPF, nome e endereço) em registros e relatórios gerados pelo projeto. | Ata de 22/09/2026 — Henrique (exposição de dado pessoal e DPO) | Exposição de dado pessoal já em tratamento com o DPO. | client |

## Números do cliente

- Ata 22/09/2026 — Beatriz: 3 estados → contexto_de_dor
- Ata 22/09/2026 — Beatriz: 4,2 milhões de unidades consumidoras → contexto_de_dor
- Ata 22/09/2026 — Henrique: cerca de 3 horas em cada episódio → contexto_de_dor
- Ata 22/09/2026 — Henrique: milhões de requisições na página de consulta de débitos → contexto_de_dor
- Ata 22/09/2026 — Beatriz: dois ambientes de origem → dimensionamento
- Ata 22/09/2026 — Beatriz: Em 01/03/2027 começa a campanha estadual de renegociação de dívidas → meta
- Ata 22/09/2026 — Beatriz: o tráfego do portal triplicou → dimensionamento
- Ata 22/09/2026 — Henrique: às terças, das 22h às 2h → descartado_com_motivo

## Perguntas abertas

- Qual é o volume habitual de requisições do portal e das APIs (média e pico), para dimensionar o pico de até três vezes na campanha?
- O provedor atual de DNS permite apontar (CNAME) os nomes do portal e das APIs para o Global Traffic Management?
- A nuvem pública mantém dados e aplicação sincronizados com o datacenter para assumir o tráfego sem intervenção manual?
- A Solaris deseja definir um período de congelamento de mudanças antes de 01/03/2027?
- Quais nomes de host e APIs compõem o portal e o app a serem protegidos?
