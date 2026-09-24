# Relatório de cobertura — Solaris Energia (SOLARIS-PORTAL-2026)

- Regras: v11
- Modo dos dados: test
- Engajamento: phased

## Decisões

| Decisão | Valor | Aprovado por | Data | Modo |
|---|---|---|---|---|
| engagement_type | phased | Vitor | 2026-09-24 | test |
| warranty | 90 dias corridos após o aceite de cada fase | Vitor | 2026-09-24 | test |
| license_supply | revenda autorizada | Vitor | 2026-09-24 | test |
| sla | Tabela institucional de SLA POPULOS (ALTA: resposta até 1 hora, solução até 4 horas; MÉDIA: resposta até 2 horas, solução até 8 horas; BAIXA: resposta até 16 horas, solução até 24 horas) | None | None | None |
| sla_applicability | ['phased'] | Vitor | 2026-09-24 | test |
| fase1_estimate | 3 a 4 semanas | Ana Ribeiro | 2026-09-24 | test |
| fase2_estimate | 6 a 8 semanas | Ana Ribeiro | 2026-09-24 | test |

## Cobertura do insumo

| Referência | Trecho | Status | Destino |
|---|---|---|---|
| Ata 22/09/2026, Beatriz (perfil) | Distribuidora de energia em 3 estados, com 4,2 milhões de unidades consumidoras | coberto | sumário, dimensionamento |
| Ata 22/09/2026, Beatriz (portal) | O portal concentra segunda via de conta, pedido de religação e consulta de débitos; o app usa as mesmas APIs | coberto | REQ-01, escopo |
| Ata 22/09/2026, Henrique (ataques) | Portal fora do ar por cerca de 3 horas em junho e em agosto por DDoS de aplicação na consulta de débitos | coberto | REQ-01, sumário |
| Ata 22/09/2026, Henrique (rede) | Não houve ataque volumétrico de rede | coberto | exclusões |
| Ata 22/09/2026, Henrique (robôs) | Robôs testam CPFs na consulta de débitos e a página devolve nome e endereço | coberto | REQ-02, premissas |
| Ata 22/09/2026, Henrique (DPO) | A exposição de dado pessoal já está sendo tratada com o DPO | coberto | exclusões, premissas |
| Ata 22/09/2026, Beatriz (origens) | Datacenter próprio principal e nuvem pública acionada manualmente; desejo de failover automático | coberto | REQ-03, dimensionamento |
| Ata 22/09/2026, Beatriz (campanha) | Campanha estadual de renegociação de dívidas a partir de 01/03/2027; na última campanha o tráfego triplicou | coberto | REQ-04, sumário, dimensionamento |
| Ata 22/09/2026, Henrique (mudanças) | Sem congelamento formal de mudanças; mudanças em produção às terças, das 22h às 2h | coberto | REQ-06, premissas |
| Ata 22/09/2026, Beatriz e Ana (fases) | Assessment e desenho primeiro; implantação como opção após o aceite do desenho | coberto | REQ-05, engajamento |
| Ata 22/09/2026, Henrique (DNS) | O DNS dos domínios fica no provedor atual, funciona bem e não é o foco | coberto | exclusões, premissas |
| E-mail Vitor 24/09/2026 09:14 | Engajamento em fases, revenda das licenças e garantia de 90 dias aprovados | coberto | engajamento |
| E-mail Vitor 24/09/2026 09:20 | Tabela de SLA aplicável somente à Fase 2 | coberto | engajamento |
| E-mail Ana Ribeiro 24/09/2026 10:02 | Fase 1 de 3 a 4 semanas; Fase 2 de 6 a 8 semanas | coberto | engajamento |
| E-mail Vitor 24/09/2026 11:30 | Provisionamento das licenças em até 2 semanas após a assinatura do pedido | coberto | engajamento, premissas |

## Requisitos

| REQ | Requisito | Origem | Evidência no insumo | Falantes |
|---|---|---|---|---|
| REQ-01 | Proteger o portal do cliente e as APIs usadas pelo app contra DDoS na camada de aplicação, com foco na página de consulta de débitos | Ata de 22/09/2026, Henrique Sato | Em junho e em agosto o portal ficou fora do ar por cerca de 3 horas em cada episódio, por ataque de negação de serviço na camada de aplicação com milhões de requisições na consulta de débitos | client |
| REQ-02 | Detectar e conter robôs que testam números de CPF na consulta de débitos | Ata de 22/09/2026, Henrique Sato | Robôs testam números de CPF; quando o CPF existe, a página devolve nome e endereço | client |
| REQ-03 | Direcionar o tráfego automaticamente para a nuvem pública quando o datacenter próprio ficar indisponível | Ata de 22/09/2026, Beatriz Nogueira | Hoje a nuvem pública só recebe tráfego manualmente quando o datacenter cai; o cliente quer que isso seja automático | client |
| REQ-04 | Estar protegido e com failover automático antes do início da campanha estadual de renegociação de dívidas em 01/03/2027 | Ata de 22/09/2026, Beatriz Nogueira | Na última campanha o tráfego do portal triplicou | client |
| REQ-05 | Realizar levantamento e desenho antes de contratar a implantação | Ata de 22/09/2026, Beatriz Nogueira | Queremos primeiro um assessment e desenho, e depois a implantação | client |
| REQ-06 | Executar mudanças em produção somente às terças-feiras, das 22h às 2h | Ata de 22/09/2026, Henrique Sato | As mudanças em produção só acontecem às terças, das 22h às 2h | client |

## Números do cliente

- Ata 22/09/2026, Beatriz: 3 estados → descartado_com_motivo
- Ata 22/09/2026, Beatriz: 4,2 milhões de unidades consumidoras → dimensionamento
- Ata 22/09/2026, Henrique: cerca de 3 horas em cada episódio → contexto_de_dor
- Ata 22/09/2026, Henrique: Em junho e em agosto → contexto_de_dor
- Ata 22/09/2026, Henrique: milhões de requisições na página de consulta de débitos → contexto_de_dor
- Ata 22/09/2026, Beatriz: dois ambientes de origem → dimensionamento
- Ata 22/09/2026, Beatriz: 01/03/2027 → meta
- Ata 22/09/2026, Beatriz: o tráfego do portal triplicou → contexto_de_dor
- Ata 22/09/2026, Henrique: às terças, das 22h às 2h → descartado_com_motivo

## Perguntas abertas

- Qual é o volume de requisições do portal e das APIs em dia normal e no pico da última campanha de renegociação?
- Quais hostnames e APIs publicados compõem o portal do cliente e o app?
- O provedor de DNS atual permite delegar, por CNAME, os nomes do portal para o Global Traffic Management?
- A nuvem pública mantém dados e aplicação atualizados para assumir o tráfego automaticamente, sem intervenção manual?
- Em quanto tempo a Solaris prevê aprovar o desenho e contratar a Fase 2 após a entrega da Fase 1?
