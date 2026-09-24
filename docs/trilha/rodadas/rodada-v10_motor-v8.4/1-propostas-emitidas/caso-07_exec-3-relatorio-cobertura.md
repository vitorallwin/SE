# Relatório de cobertura — Solaris Energia (POP-SOLARIS-2026-09)

- Regras: v10
- Modo dos dados: test
- Engajamento: phased

## Decisões

| Decisão | Valor | Aprovado por | Data | Modo |
|---|---|---|---|---|
| engagement_type | phased | Vitor (Executivo de Contas, POPULOS) | 2026-09-24 | test |
| warranty | 90 dias corridos após o aceite de cada fase | Vitor (Executivo de Contas, POPULOS) | 2026-09-24 | test |
| license_supply | revenda autorizada | Vitor (Executivo de Contas, POPULOS) | 2026-09-24 | test |
| sla | Tabela institucional de SLA do template aprovado | None | None | None |
| sla_applicability | ['phased'] | Vitor (Executivo de Contas, POPULOS) | 2026-09-24 | test |
| phase1_estimate | 3 a 4 semanas | Ana Ribeiro (Arquiteta, POPULOS) | 2026-09-24 | test |
| phase2_estimate | 6 a 8 semanas | Ana Ribeiro (Arquiteta, POPULOS) | 2026-09-24 | test |

## Cobertura do insumo

| Referência | Trecho | Status | Destino |
|---|---|---|---|
| Ata 22/09/2026, Beatriz, parágrafo 1 | Distribuidora em 3 estados, 4,2 milhões de unidades consumidoras; portal com segunda via, religação e consulta de débitos; app usa as mesmas APIs | coberto | sumário, REQ-01 |
| Ata 22/09/2026, Henrique, parágrafo 2 | Portal fora do ar por cerca de 3 horas em junho e agosto por DDoS de aplicação; sem ataque volumétrico de rede | coberto | REQ-01, sumário |
| Ata 22/09/2026, Henrique, parágrafo 3 | Robôs testando CPFs na consulta de débitos, com exposição de nome e endereço; tratamento com o DPO | coberto | REQ-02, exclusões |
| Ata 22/09/2026, Beatriz, parágrafo 4 | Datacenter próprio principal e nuvem pública com failover manual; desejo de failover automático | coberto | REQ-03, dimensionamento |
| Ata 22/09/2026, Beatriz, parágrafo 5 | Campanha de renegociação em 01/03/2027; tráfego triplicou na última campanha | coberto | REQ-04, dimensionamento, sumário |
| Ata 22/09/2026, Henrique, parágrafo 6 | Sem congelamento formal; mudanças só às terças, 22h às 2h | coberto | REQ-06, premissas |
| Ata 22/09/2026, Beatriz e Ana, parágrafos 7 e 8 | Assessment e desenho primeiro; implantação como opção após aceite | coberto | REQ-05, engajamento, escopo |
| Ata 22/09/2026, Henrique, parágrafo 9 | DNS dos domínios permanece no provedor atual e não é o foco | coberto | exclusões, premissas |
| E-mails POPULOS de 24/09/2026 | Aprovações de engajamento, licenças, garantia, SLA, estimativas e prazo de licenciamento | coberto | engajamento, escopo, sumário |

## Requisitos

| REQ | Requisito | Origem | Evidência no insumo | Falantes |
|---|---|---|---|---|
| REQ-01 | Proteger o portal do cliente e as APIs usadas pelo app contra negação de serviço na camada de aplicação | Ata de 22/09/2026, Henrique, parágrafo 2 | Portal fora do ar por cerca de 3 horas em junho e em agosto, com milhões de requisições na consulta de débitos | client |
| REQ-02 | Conter robôs que testam números de CPF na consulta de débitos | Ata de 22/09/2026, Henrique, parágrafo 3 | Robôs testando CPFs; a página devolve nome e endereço quando o CPF existe | client |
| REQ-03 | Tornar automático o failover entre o datacenter próprio (principal) e a nuvem pública | Ata de 22/09/2026, Beatriz, parágrafo 4 | Hoje a nuvem só recebe tráfego manualmente quando o datacenter cai | client |
| REQ-04 | Estar protegido e com failover automático antes de 01/03/2027 | Ata de 22/09/2026, Beatriz, parágrafo 5 | Campanha estadual de renegociação começa em 01/03/2027; na última, o tráfego triplicou | client |
| REQ-05 | Realizar assessment e desenho antes de contratar a implantação | Ata de 22/09/2026, Beatriz, parágrafo 7 | Não queremos contratar a implantação às cegas | client |
| REQ-06 | Executar mudanças em produção somente às terças, das 22h às 2h | Ata de 22/09/2026, Henrique, parágrafo 6 | Mudanças em produção só acontecem às terças, das 22h às 2h | client |

## Números do cliente

- Ata 22/09/2026, Beatriz, parágrafo 1: distribuidora de energia em 3 estados → descartado_com_motivo
- Ata 22/09/2026, Beatriz, parágrafo 1: 4,2 milhões de unidades consumidoras → contexto_de_dor
- Ata 22/09/2026, Henrique, parágrafo 2: fora do ar por cerca de 3 horas em cada episódio → contexto_de_dor
- Ata 22/09/2026, Henrique, parágrafo 2: milhões de requisições na página de consulta de débitos → contexto_de_dor
- Ata 22/09/2026, Beatriz, parágrafo 4: dois ambientes de origem → dimensionamento
- Ata 22/09/2026, Beatriz, parágrafo 5: Em 01/03/2027 começa a campanha estadual de renegociação de dívidas → meta
- Ata 22/09/2026, Beatriz, parágrafo 5: o tráfego do portal triplicou → dimensionamento
- Ata 22/09/2026, Henrique, parágrafo 6: às terças, das 22h às 2h → descartado_com_motivo

## Perguntas abertas

- Qual é o volume base de requisições do portal e das APIs, para dimensionar o pico da campanha (referência: tráfego triplicado na última)?
- Quais hostnames e APIs publicadas compõem o portal e o app?
- Qual o tempo máximo aceitável de troca para a nuvem pública e quais critérios de saúde definem a queda do datacenter?
- A nuvem pública tem capacidade para receber sozinha o tráfego de pico da campanha?
