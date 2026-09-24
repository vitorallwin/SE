# NexusPay V5 — relatório de cobertura insumo → proposta

- Código: `PT-2609-NXP5`
- Regras: v5
- Resultado das regras de estado: aprovado, 0 violações

## Decisões do caso (escopo: somente NexusPay)

| Decisão | Valor | Origem |
|---|---|---|
| engagement_type | phased | decisão de teste do caso NexusPay (24/09/2026): Fase 1 assessment e desenho contratada; Fase 2 implantação opcional. Confirmar com o dono comercial. |
| phase1_estimate | 4 a 6 semanas (Assessment 2 a 3; Desenho 2 a 3) | decisão de teste do caso NexusPay (24/09/2026). Confirmar com o arquiteto responsável. |
| warranty | A POPULOS corrigirá defeitos diretamente atribuíveis aos serviços executados por 90 dias corridos após o aceite final. | decisão do caso NexusPay informada pelo responsável (teste) |
| license_supply | As licenças e subscrições Akamai da Fase 2 serão fornecidas pela POPULOS por meio de revenda autorizada e deverão estar ativas antes da configuração. | decisão do caso NexusPay informada pelo responsável (teste) |
| sla | tabela institucional do template POPULOS | populos_standard |

## Cobertura do insumo

| Referência | Trecho | Status | Destino |
|---|---|---|---|
| transcrição [00:00:42] | Estabilidade em Black Friday e Pix Day | coberto | REQ-07 |
| transcrição [00:00:42] | Gargalos no gateway e quedas parciais de API por tráfego malicioso e credential stuffing | coberto | REQ-02, REQ-03, sumário |
| transcrição [00:01:10] | Regulação do Banco Central exige auditoria rigorosa | coberto | REQ-10 |
| transcrição [00:01:10] | Baixa latência; atraso acima de dois segundos causa abandono | coberto | REQ-04, sumário |
| transcrição [00:01:10] | Bots raspadores de tabelas de taxas e de dados de lojistas no cadastro | coberto | REQ-02 |
| transcrição [00:02:05] | Duas nuvens públicas e um datacenter próprio | coberto | dimensionamento |
| transcrição [00:02:05] | DNS tradicional com failover manual | coberto | REQ-01, sumário |
| transcrição [00:02:05] | Automatizar a resiliência sem impactar o SLA | coberto | REQ-01, escopo |
| transcrição [00:02:35] | Dados de cartão e PII não podem ficar expostos em logs | coberto | REQ-08 |
| transcrição [00:02:35] | Dados sensíveis não podem ser interceptados no trânsito | coberto | REQ-09 |
| transcrição [00:02:35] | Conformidade com LGPD e PCI DSS | coberto | REQ-05 |
| transcrição [00:03:10] | Aceleração de APIs transacionais | coberto | REQ-04 |
| requisitos originais 1 a 6 | Seis requisitos registrados | coberto | REQ-01, REQ-02, REQ-03, REQ-04, REQ-05, REQ-06 |
| escopo informado — incluso | Rede e DNS; ameaças web e API; roteamento global; dados sensíveis em trânsito; cenários de pico | coberto | escopo |
| escopo informado — excluído | Código do gateway; implementação nesta fase; homologação jurídica | coberto | exclusões, engajamento |
| premissas originais 1 a 3 | Acesso administrativo; sessões de desenho; documentação atualizada | coberto | premissas |
| transcrição [00:00:15] | Crescimento acelerado e planos de expansão | descartado | Contexto sem requisito verificável; será confirmado no Assessment se alterar a volumetria. |

## Números ditos pelo cliente

| Referência | Número | Destino |
|---|---|---|
| transcrição [00:01:10] | atraso superior a dois segundos no checkout resulta em abandono de carrinho | contexto_de_dor |
| transcrição [00:02:05] | failover manual custa preciosos minutos | contexto_de_dor |
| transcrição [00:00:42] | gargalos no gateway e quedas parciais de API no ano passado | contexto_de_dor |
| transcrição [00:02:05] | dois provedores de nuvem pública e um datacenter próprio | dimensionamento |

## Requisitos e origem

| REQ | Requisito | Origem |
|---|---|---|
| REQ-01 | Failover automatizado entre as três origens, sem impacto ao SLA | requisito original 1; transcrição [00:02:05] |
| REQ-02 | Proteção de APIs de pagamento e cadastro contra bots e fraude automatizada | requisito original 2; transcrição [00:00:42] e [00:01:10] |
| REQ-03 | Mitigação de DDoS volumétrico e de aplicação | requisito original 3; transcrição [00:03:10] |
| REQ-04 | Redução da latência do checkout | requisito original 4; transcrição [00:01:10] |
| REQ-05 | Conformidade com LGPD e PCI DSS | requisito original 5; transcrição [00:02:35] |
| REQ-06 | Visibilidade em tempo real do tráfego legítimo e malicioso para o SOC | requisito original 6 |
| REQ-07 | Estabilidade nos picos de Black Friday e Pix Day | transcrição [00:00:42]; escopo informado (dimensionamento de cenários de pico) |
| REQ-08 | Dados de cartão e PII fora dos logs | transcrição [00:02:35] |
| REQ-09 | Proteção de dados sensíveis em trânsito | transcrição [00:02:35]; escopo informado (inspeção de conformidade em trânsito) |
| REQ-10 | Trilha de auditoria exigida pela regulação do Banco Central | transcrição [00:01:10] |

## Estimativas

- Duração da Fase 1: 4 a 6 semanas — responsável: Arquiteto responsável POPULOS (decisão de teste do caso)
