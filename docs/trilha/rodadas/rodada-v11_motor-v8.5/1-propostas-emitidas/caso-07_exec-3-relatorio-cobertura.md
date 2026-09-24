# Relatório de cobertura — Solaris Energia (PROP-SOLARIS-2026-001)

- Regras: v11
- Modo dos dados: test
- Engajamento: phased

## Decisões

| Decisão | Valor | Aprovado por | Data | Modo |
|---|---|---|---|---|
| engagement_type | phased | Vitor | 2026-09-24 | test |
| license_supply | revenda autorizada | Vitor | 2026-09-24 | test |
| warranty | 90 dias corridos após o aceite de cada fase | Vitor | 2026-09-24 | test |
| sla | Tabela institucional de SLA da POPULOS | None | None | None |
| sla_applicability | ['implementation'] | Vitor | 2026-09-24 | test |
| fase1_estimate | 3 a 4 semanas | Ana Ribeiro | 2026-09-24 | test |
| fase2_estimate | 6 a 8 semanas | Ana Ribeiro | 2026-09-24 | test |

## Cobertura do insumo

| Referência | Trecho | Status | Destino |
|---|---|---|---|
| Ata 22/09/2026, Beatriz (1ª) | Distribuidora em 3 estados, 4,2 milhões de unidades consumidoras; portal com segunda via, religação e consulta de débitos; app usa as mesmas APIs | coberto | REQ-01, sumário, dimensionamento |
| Ata 22/09/2026, Henrique (1ª) | Portal fora do ar cerca de 3 horas em junho e em agosto por DDoS de aplicação na consulta de débitos; sem ataque volumétrico | coberto | REQ-01, sumário |
| Ata 22/09/2026, Henrique (2ª) | Robôs testando CPFs na consulta de débitos, com exposição de nome e endereço; tratado com o DPO | coberto | REQ-02, exclusões |
| Ata 22/09/2026, Beatriz (2ª) | Duas origens (datacenter principal e nuvem pública) com failover manual; desejo de failover automático | coberto | REQ-03, dimensionamento |
| Ata 22/09/2026, Beatriz (3ª) | Campanha de renegociação a partir de 01/03/2027; tráfego triplicou na última campanha | coberto | REQ-04, dimensionamento |
| Ata 22/09/2026, Henrique (3ª) | Sem congelamento formal de mudanças; mudanças em produção somente às terças, das 22h às 2h | coberto | premissas |
| Ata 22/09/2026, Beatriz (4ª) | Assessment e desenho antes da implantação | coberto | REQ-05, engajamento |
| Ata 22/09/2026, Ana (POPULOS) | Proposta em duas fases, Fase 2 opcional após aceite do desenho | coberto | REQ-05, engajamento |
| Ata 22/09/2026, Henrique (4ª) | DNS dos domínios permanece no provedor atual e não é foco | coberto | exclusões, premissas |
| E-mail de Vitor (Executivo de Contas, POPULOS) de 24/09/2026 09:14 | Engajamento em fases, revenda de licenças e garantia de 90 dias | coberto | engajamento, escopo |
| E-mail de Vitor (Executivo de Contas, POPULOS) de 24/09/2026 09:20 | SLA institucional somente na Fase 2 | coberto | engajamento |
| E-mail de Ana Ribeiro (Arquiteta, POPULOS) de 24/09/2026 10:02 | Estimativas de esforço das fases | coberto | engajamento |
| E-mail de Vitor (Executivo de Contas, POPULOS) de 24/09/2026 11:30 | Provisionamento das licenças em até 2 semanas após a assinatura do pedido | coberto | premissas |

## Requisitos

| REQ | Requisito | Origem | Evidência no insumo | Falantes |
|---|---|---|---|---|
| REQ-01 | Proteger o portal do cliente e as APIs usadas pelo app contra DDoS na camada de aplicação, em especial na consulta de débitos | Ata de 22/09/2026, falas de Beatriz (1ª) e Henrique (1ª) | Indisponibilidade de cerca de 3 horas em junho e em agosto por milhões de requisições na consulta de débitos; o app usa as mesmas APIs do portal | client |
| REQ-02 | Detectar e bloquear robôs que testam números de CPF na consulta de débitos | Ata de 22/09/2026, fala de Henrique (2ª) | Robôs testando CPFs; a página devolve nome e endereço quando o CPF existe | client |
| REQ-03 | Tornar automático o failover do portal e das APIs entre o datacenter próprio e a nuvem pública | Ata de 22/09/2026, fala de Beatriz (2ª) | Hoje a nuvem pública só recebe tráfego manualmente quando o datacenter cai | client |
| REQ-04 | Estar protegido e com failover automático antes de 01/03/2027, início da campanha estadual de renegociação de dívidas | Ata de 22/09/2026, fala de Beatriz (3ª) | Na última campanha o tráfego do portal triplicou | client |
| REQ-05 | Realizar assessment e desenho antes de contratar a implantação | Ata de 22/09/2026, fala de Beatriz (4ª) | A Solaris não quer contratar a implantação às cegas | client, vendor |

## Números do cliente

- Ata 22/09/2026, Beatriz (1ª): 3 estados → contexto_de_dor
- Ata 22/09/2026, Beatriz (1ª): 4,2 milhões de unidades consumidoras → dimensionamento
- Ata 22/09/2026, Henrique (1ª): cerca de 3 horas em cada episódio → contexto_de_dor
- Ata 22/09/2026, Henrique (1ª): milhões de requisições → contexto_de_dor
- Ata 22/09/2026, Beatriz (2ª): dois ambientes de origem → dimensionamento
- Ata 22/09/2026, Beatriz (3ª): 01/03/2027 → meta
- Ata 22/09/2026, Beatriz (3ª): o tráfego do portal triplicou → dimensionamento
- Ata 22/09/2026, Henrique (3ª): das 22h às 2h → descartado_com_motivo

## Perguntas abertas

- Qual é o volume habitual de requisições do portal e das APIs, para dimensionar o pico da campanha (o triplo do habitual)?
- A Solaris pretende definir um período de congelamento de mudanças antes da campanha de 01/03/2027? Se sim, a partir de qual data?
- Quem na Solaris cria, no provedor de DNS atual, os registros que apontam os nomes do portal e das APIs para o Global Traffic Management?
