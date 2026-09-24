# Relatório de cobertura — Solaris Energia (SOLARIS-2026-AAP-GTM)

- Regras: v10
- Modo dos dados: test
- Engajamento: phased

## Decisões

| Decisão | Valor | Aprovado por | Data | Modo |
|---|---|---|---|---|
| engagement_type | phased | Vitor (Executivo de Contas, POPULOS) | 2026-09-24 | test |
| license_supply | revenda autorizada | Vitor (Executivo de Contas, POPULOS) | 2026-09-24 | test |
| warranty | 90 dias corridos após o aceite de cada fase | Vitor (Executivo de Contas, POPULOS) | 2026-09-24 | test |
| sla | Tabela institucional de SLA da POPULOS | None | None | None |
| sla_applicability | ['phased'] | Vitor (Executivo de Contas, POPULOS) | 2026-09-24 | test |
| phase1_estimate | 3 a 4 semanas | Ana Ribeiro (Arquiteta, POPULOS) | 2026-09-24 | test |
| phase2_estimate | 6 a 8 semanas | Ana Ribeiro (Arquiteta, POPULOS) | 2026-09-24 | test |

## Cobertura do insumo

| Referência | Trecho | Status | Destino |
|---|---|---|---|
| ata 22/09/2026, Beatriz | Distribuidora de energia em 3 estados, com 4,2 milhões de unidades consumidoras | coberto | sumário |
| ata 22/09/2026, Beatriz | Portal concentra segunda via de conta, religação e consulta de débitos; o app usa as mesmas APIs | coberto | REQ-01, escopo |
| ata 22/09/2026, Henrique | Portal fora do ar por cerca de 3 horas em junho e agosto por DoS de camada de aplicação | coberto | REQ-01, sumário |
| ata 22/09/2026, Henrique | Não houve ataque volumétrico de rede | coberto | exclusões |
| ata 22/09/2026, Henrique | Robôs testando CPFs na consulta de débitos; exposição de nome e endereço; tratado com o DPO | coberto | REQ-02, premissas |
| ata 22/09/2026, Beatriz | Dois ambientes de origem com failover manual; desejo de failover automático | coberto | REQ-03, dimensionamento |
| ata 22/09/2026, Beatriz | Campanha de renegociação em 01/03/2027; tráfego triplicou na última campanha | coberto | REQ-04, dimensionamento, sumário |
| ata 22/09/2026, Henrique | Sem congelamento formal; mudanças às terças, das 22h às 2h | coberto | REQ-06, premissas |
| ata 22/09/2026, Beatriz e Ana | Assessment e desenho primeiro; implantação depois como opção | coberto | REQ-05, engajamento |
| ata 22/09/2026, Henrique | DNS dos domínios permanece no provedor atual | coberto | exclusões |
| e-mails POPULOS 24/09/2026 | Aprovações de engajamento, licenças, garantia, SLA, estimativas e prazo de licenças | coberto | engajamento, escopo |

## Requisitos

| REQ | Requisito | Origem | Evidência no insumo | Falantes |
|---|---|---|---|---|
| REQ-01 | Proteger o portal do cliente e as APIs usadas pelo app contra negação de serviço na camada de aplicação | ata de 22/09/2026, fala de Henrique Sato | Portal fora do ar por cerca de 3 horas em junho e em agosto por ataque de negação de serviço na camada de aplicação na consulta de débitos | client |
| REQ-02 | Conter robôs que testam números de CPF na consulta de débitos e expõem nome e endereço | ata de 22/09/2026, fala de Henrique Sato | Robôs testando números de CPF; a página devolve nome e endereço quando o CPF existe | client |
| REQ-03 | Tornar automático o failover entre o datacenter próprio (principal) e a nuvem pública | ata de 22/09/2026, fala de Beatriz Nogueira | Nuvem pública hoje só recebe tráfego manualmente quando o datacenter cai; cliente quer failover automático | client |
| REQ-04 | Estar protegido e com failover automático antes de 01/03/2027, início da campanha estadual de renegociação de dívidas | ata de 22/09/2026, fala de Beatriz Nogueira | Campanha começa em 01/03/2027; na última campanha o tráfego do portal triplicou | client |
| REQ-05 | Contratar primeiro o Assessment e o desenho e somente depois a implantação | ata de 22/09/2026, fala de Beatriz Nogueira | Cliente não quer contratar a implantação às cegas | client |
| REQ-06 | Executar mudanças em produção somente às terças, das 22h às 2h | ata de 22/09/2026, fala de Henrique Sato | Sem congelamento formal; mudanças em produção só às terças, das 22h às 2h | client |

## Números do cliente

- ata de 22/09/2026: 3 estados → contexto_de_dor
- ata de 22/09/2026: 4,2 milhões de unidades consumidoras → contexto_de_dor
- ata de 22/09/2026: cerca de 3 horas em cada episódio → contexto_de_dor
- ata de 22/09/2026: milhões de requisições → contexto_de_dor
- ata de 22/09/2026: dois ambientes de origem → dimensionamento
- ata de 22/09/2026: 01/03/2027 → meta
- ata de 22/09/2026: o tráfego do portal triplicou → dimensionamento
- ata de 22/09/2026: às terças, das 22h às 2h → dimensionamento

## Perguntas abertas

- Quais hostnames e APIs do portal e do app entram no escopo?
- Qual é o volume de tráfego habitual e de pico do portal, para dimensionar a campanha em que o tráfego triplicou?
- Qual subdomínio do provedor DNS atual poderá ser delegado ao Global Traffic Management?
