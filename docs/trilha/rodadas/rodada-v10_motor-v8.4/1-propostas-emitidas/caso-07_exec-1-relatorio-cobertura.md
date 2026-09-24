# Relatório de cobertura — Solaris Energia (POPULOS-SOLARIS-PORTAL-2026)

- Regras: v10
- Modo dos dados: test
- Engajamento: phased

## Decisões

| Decisão | Valor | Aprovado por | Data | Modo |
|---|---|---|---|---|
| engagement_type | phased | Vitor (Executivo de Contas, POPULOS) | 2026-09-24 | test |
| license_supply | revenda autorizada | Vitor (Executivo de Contas, POPULOS) | 2026-09-24 | test |
| warranty | 90 dias corridos após o aceite de cada fase | Vitor (Executivo de Contas, POPULOS) | 2026-09-24 | test |
| sla | Tabela institucional de SLA do template POPULOS | None | None | None |
| sla_applicability | ['phased'] | Vitor (Executivo de Contas, POPULOS) | 2026-09-24 | test |
| phase1_estimate | 3 a 4 semanas | Ana Ribeiro (Arquiteta, POPULOS) | 2026-09-24 | test |
| phase2_estimate | 6 a 8 semanas | Ana Ribeiro (Arquiteta, POPULOS) | 2026-09-24 | test |

## Cobertura do insumo

| Referência | Trecho | Status | Destino |
|---|---|---|---|
| ata de 22/09/2026, fala 1 de Beatriz | Distribuidora em 3 estados, 4,2 milhões de unidades consumidoras; portal com segunda via, religação e consulta de débitos; app usa as mesmas APIs | coberto | REQ-01, dimensionamento |
| ata de 22/09/2026, fala 1 de Henrique | Portal fora do ar por cerca de 3 horas em junho e em agosto por DDoS de aplicação na consulta de débitos; sem ataque volumétrico de rede | coberto | REQ-01, sumário, exclusões |
| ata de 22/09/2026, fala 2 de Henrique | Robôs testam CPFs na consulta de débitos; página devolve nome e endereço; tratado com o DPO | coberto | REQ-02, exclusões, premissas |
| ata de 22/09/2026, fala 2 de Beatriz | Datacenter próprio principal e nuvem pública acionada manualmente; desejo de failover automático | coberto | REQ-03, dimensionamento |
| ata de 22/09/2026, fala 3 de Beatriz | Campanha estadual de renegociação a partir de 01/03/2027; tráfego triplicou na última campanha | coberto | REQ-04, sumário, dimensionamento |
| ata de 22/09/2026, fala 3 de Henrique | Sem congelamento formal; mudanças em produção só às terças, das 22h às 2h | coberto | REQ-06, premissas |
| ata de 22/09/2026, fala 4 de Beatriz | Assessment e desenho primeiro, implantação depois | coberto | REQ-05, engajamento |
| ata de 22/09/2026, fala de Ana (POPULOS) | Proposta em duas fases, Fase 2 opcional após aceite do desenho | coberto | engajamento |
| ata de 22/09/2026, fala 4 de Henrique | DNS dos domínios permanece no provedor atual e não é o foco | coberto | exclusões, premissas |
| e-mail de Vitor, 24/09/2026 09:14 | Engajamento em fases, revenda das licenças e garantia de 90 dias após o aceite de cada fase | coberto | engajamento, escopo |
| e-mail de Vitor, 24/09/2026 09:20 | Tabela institucional de SLA aplicável somente à Fase 2 | coberto | engajamento |
| e-mail de Ana Ribeiro, 24/09/2026 10:02 | Fase 1 de 3 a 4 semanas; Fase 2 de 6 a 8 semanas | coberto | engajamento, sumário |
| e-mail de Vitor, 24/09/2026 11:30 | Provisionamento das licenças em até 2 semanas após a assinatura do pedido | coberto | sumário, premissas |

## Requisitos

| REQ | Requisito | Origem | Evidência no insumo | Falantes |
|---|---|---|---|---|
| REQ-01 | Proteger o portal do cliente e as APIs usadas pelo app contra ataques de negação de serviço na camada de aplicação | ata de 22/09/2026, falas de Henrique (indisponibilidades) e de Beatriz (portal e APIs) | Indisponibilidade de cerca de 3 horas em junho e em agosto por milhões de requisições na página de consulta de débitos; o app usa as mesmas APIs do portal | client |
| REQ-02 | Detectar e conter robôs que testam números de CPF na consulta de débitos | ata de 22/09/2026, fala de Henrique sobre robôs e CPF | Robôs testam CPFs; quando o CPF existe, a página devolve nome e endereço; tema já tratado com o DPO | client |
| REQ-03 | Direcionar o tráfego automaticamente para a nuvem pública quando o datacenter próprio ficar indisponível | ata de 22/09/2026, fala de Beatriz sobre os dois ambientes de origem | Duas origens (datacenter principal e nuvem pública); hoje o desvio é manual | client |
| REQ-04 | Ter proteção e failover automático em operação antes de 01/03/2027, considerando que o tráfego do portal triplicou na última campanha | ata de 22/09/2026, fala de Beatriz sobre a campanha | Campanha estadual de renegociação de dívidas a partir de 01/03/2027 | client |
| REQ-05 | Realizar assessment e desenho antes de contratar a implantação | ata de 22/09/2026, fala de Beatriz sobre assessment e desenho | Cliente não quer contratar a implantação às cegas | client |
| REQ-06 | Executar mudanças em produção somente às terças, das 22h às 2h | ata de 22/09/2026, fala de Henrique sobre mudanças | Não há congelamento formal de mudanças; mudanças apenas às terças, das 22h às 2h | client |

## Números do cliente

- ata de 22/09/2026, fala 1 de Beatriz: 3 estados → dimensionamento
- ata de 22/09/2026, fala 1 de Beatriz: 4,2 milhões de unidades consumidoras → dimensionamento
- ata de 22/09/2026, fala 1 de Henrique: cerca de 3 horas em cada episódio → contexto_de_dor
- ata de 22/09/2026, fala 1 de Henrique: milhões de requisições → contexto_de_dor
- ata de 22/09/2026, fala 2 de Beatriz: dois ambientes de origem → dimensionamento
- ata de 22/09/2026, fala 3 de Beatriz: 01/03/2027 → meta
- ata de 22/09/2026, fala 3 de Beatriz: o tráfego do portal triplicou → dimensionamento
- ata de 22/09/2026, fala 3 de Henrique: às terças, das 22h às 2h → descartado_com_motivo

## Perguntas abertas

- Qual é o volume atual de requisições por segundo do portal e das APIs em dia comum e no pico da última campanha?
- Quais hostnames e APIs publicados compõem o portal do cliente e o app?
- O provedor de DNS atual permite delegar por CNAME os hostnames do portal para o Global Traffic Management?
